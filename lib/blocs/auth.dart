import 'dart:async';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:loggy/loggy.dart';

import 'package:bloxtest10/models/models.dart';
import 'package:bloxtest10/services/identity_providers.dart'
    as identity_providers;

bool isEmailUser(User user) {
  var isEmailUser = false;
  if (!user.isAnonymous) {
    isEmailUser = user.providerData.any(
      (provider) => provider.providerId == EmailAuthProvider.PROVIDER_ID,
    );
  }
  return isEmailUser;
}

bool isUserVerified(User user) => !isEmailUser(user) || user.emailVerified;

class AuthBloc extends Bloc<AuthEvent, AuthState> with UiLoggy {
  late final FirebaseAuth fbAuthInstance;

  StreamSubscription? userChangesSubscription;

  // todo: use timer to periodically check if user is verified
  Timer? emailVerificationTimer;

  AuthBloc(FirebaseApp app) : super(const AuthState()) {
    fbAuthInstance = FirebaseAuth.instanceFor(app: app);

    // Sign in anonymously or sign in with cached, non-anonymous user
    on<AuthEventInitialize>((event, emit) {
      final fbInstanceUser = fbAuthInstance.currentUser;

      if (fbInstanceUser == null) {
        // Sign in anonymously, returning the user to the sign in screen
        emit(const AuthState(isLoading: true));
        fbAuthInstance.signInAnonymously();
      } else if (!fbInstanceUser.isAnonymous) {
        // Initialize called on a newly initialized bloc and we have a signed in
        // user cached by the FirebaseAuth service
        // Return a fresh state with the cached user
        emit(AuthState(firebaseUser: fbInstanceUser, isLoading: false));

        // Initiate email verification if not yet verified
        if (!isUserVerified(fbInstanceUser)) {
          fbInstanceUser.sendEmailVerification();
          emit(state.copyWith(isEmailVerificationInProgress: true));
        }
      } else {
        // We're already signed into an anonymous user, return a fresh state
        emit(AuthState(firebaseUser: fbInstanceUser, isLoading: false));
      }
    });

    on<AuthEventUserChanged>((event, emit) {
      emit(
        AuthState(
          firebaseUser: event.newUser,
          isLoading: event.newUser == null,
        ),
      );

      if (event.newUser == null) {
        // Sign in with anonymous user if we've logged out
        add(AuthEventInitialize());
      } else if (!isUserVerified(event.newUser!)) {
        // Initiate email verification if not yet verified
        event.newUser!.sendEmailVerification();
        emit(state.copyWith(isEmailVerificationInProgress: true));
      }
    });

    on<AuthEventEmailLogin>((event, emit) async {
      // Reset auth, keeping the user, which indicates loading
      // Loading flag is reset upon success in [AuthEventUserChanged] or failure
      // here
      emit(AuthState(firebaseUser: state.firebaseUser));

      try {
        await fbAuthInstance.signInWithEmailAndPassword(
          email: event.email,
          password: event.password,
        );
      } on FirebaseAuthException catch (e) {
        if (e.code == 'user-not-found') {
          emit(
            state.copyWith(
              authErrors: [AuthErrors.userNotFound],
              isLoading: false,
            ),
          );
        } else if (e.code == 'wrong-password') {
          emit(
            state.copyWith(
              authErrors: [AuthErrors.wrongPassword],
              isLoading: false,
            ),
          );
        } else {
          loggy.error(
            "Unknown error occurred when signing in "
            "with email and password: $e",
          );
          emit(
            state.copyWith(
              authErrors: [AuthErrors.unknown],
              isLoading: false,
            ),
          );
        }
      }
    });

    on<AuthEventEmailSignUp>((event, emit) async {
      // Reset auth, keeping the user, which indicates loading
      // Loading flag is reset upon success in [AuthEventUserChanged] or failure
      // here
      emit(AuthState(firebaseUser: state.firebaseUser));

      try {
        await fbAuthInstance.createUserWithEmailAndPassword(
          email: event.email,
          password: event.password,
        );
      } on FirebaseAuthException catch (e) {
        if (e.code == 'weak-password') {
          emit(
            state.copyWith(
              authErrors: [AuthErrors.weakPassword],
              isLoading: false,
            ),
          );
        } else if (e.code == 'email-already-in-use') {
          emit(
            state.copyWith(
              authErrors: [AuthErrors.emailInUse],
              isLoading: false,
            ),
          );
        } else {
          emit(
            state.copyWith(
              authErrors: [AuthErrors.unknown],
              isLoading: false,
            ),
          );
        }
      }
    });

    on<AuthEventEmailVerificationCheck>((event, emit) async {
      // This is currently manual, we should switch this to poll periodically
      emit(state.copyWith(isLoading: true));
      await state.firebaseUser!.reload();
      emit(state.copyWith(isLoading: false));

      if (state.firebaseUser!.emailVerified) {
        emit(state.copyWith(isEmailVerificationInProgress: false));
      }
    });

    on<AuthEventSignInWithApple>((event, emit) async {
      // Reset auth, keeping the user, which indicates loading
      // Loading flag is reset upon success in [AuthEventUserChanged] or failure
      // here
      emit(AuthState(firebaseUser: state.firebaseUser));

      final credential = await identity_providers.getAppleSignInCredential();

      add(AuthEventSignInWithOAuthCredential(credential: credential));
    });

    on<AuthEventSignInWithGoogle>((event, emit) async {
      // Reset auth, keeping the user, which indicates loading
      // Loading flag is reset upon success in [AuthEventUserChanged] or failure
      // here
      emit(AuthState(firebaseUser: state.firebaseUser));

      final credential = await identity_providers.getGoogleSignInCredential();

      add(AuthEventSignInWithOAuthCredential(credential: credential));
    });

    on<AuthEventSignInWithOAuthCredential>((event, emit) async {
      emit(AuthState(firebaseUser: state.firebaseUser));

      try {
        await fbAuthInstance.signInWithCredential(event.credential);
      } on FirebaseAuthException catch (e) {
        if (e.code == "account-exists-with-different-credential") {
          // todo: link accounts flow
          loggy.error(
            "User account already exists with a different credential. "
            "Link accounts flow not yet implemented.",
          );
        } else if (e.code == "invalid-credential") {
          emit(
            state.copyWith(
              isLoading: false,
              authErrors: [AuthErrors.invalidCredential],
            ),
          );
        } else if (e.code == "user-disabled") {
          emit(
            state.copyWith(
              isLoading: false,
              authErrors: [AuthErrors.userDisabled],
            ),
          );
        } else {
          loggy.error(
            "Unknown error occurred when signing in with a credential: $e",
          );
          emit(
            state.copyWith(
              isLoading: false,
              authErrors: [AuthErrors.unknown],
            ),
          );
        }
      }
    });

    on<AuthEventSignOut>((event, emit) {
      emit(AuthState(firebaseUser: state.firebaseUser));
      fbAuthInstance.signOut();
    });

    on<AuthEventClearErrors>((event, emit) {
      emit(state.copyWith(authErrors: []));
    });

    userChangesSubscription = fbAuthInstance
        .userChanges()
        .listen((User? user) => add(AuthEventUserChanged(newUser: user)));
  }

  @override
  Future<void> close() {
    userChangesSubscription!.cancel();
    return super.close();
  }
}
