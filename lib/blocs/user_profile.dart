import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:loggy/loggy.dart';

import 'package:bloxtest10/models/models.dart';
import 'package:bloxtest10/services/firestore_converters.dart';

class UserProfileBloc extends Bloc<UserProfileEvent, UserProfileState>
    with UiLoggy {
  final User user;

  late final DocumentReference<UserProfileState> fsRef;

  UserProfileBloc({
    required this.user,
    required FirebaseApp app,
  }) : super(const UserProfileState()) {
    fsRef = FirebaseFirestore.instanceFor(app: app)
        .doc("users/${user.uid}/")
        .withConverter<UserProfileState>(
      fromFirestore: (snapshot, _) {
        return UserProfileState.fromJson(convertFromDoc(snapshot.data()!));
      },
      toFirestore: (UserProfileState state, _) {
        return convertToDoc(state.toJson());
      },
    );

    on<UserProfileEventInitialize>((event, emit) async {
      /// State is initially blank and loading
      /// Loads from Firestore
      /// If we have a document, we use the data from it
      ///   If any values have changed, we update it
      /// If we don't, we create one using the values from the user

      // Clear state and set loading flag
      emit(const UserProfileState());

      // We definitely have a user, initialise a new Firestore ref
      final snapshot = await fsRef.get();

      // Try getting an existing profile document
      if (snapshot.exists) {
        emit(snapshot.data()!);

        // Update user profile if new values are received from the auth provider
        if ({user.displayName, user.email, user.photoURL}
            .any((value) => value != null)) {
          emit(
            state.copyWith(
              displayName: state.hasUserSetDisplayName
                  ? state.displayName
                  : user.displayName ?? state.displayName,
              email: user.email ?? state.email,
              photoUrl: user.photoURL ?? state.photoUrl,
            ),
          );
          fsRef.set(state);
        }
      } else {
        // Initialise (from new Firebase user) and create a new document if
        // none exists
        final newState = UserProfileState(
          displayName: user.displayName,
          email: user.email,
          photoUrl: user.photoURL,
          created: user.metadata.creationTime,
        );

        emit(newState.copyWith(isLoading: false));
        fsRef.set(newState);
      }
    });

    on<UserProfileEventUpdateDisplayName>((event, emit) {
      emit(state.copyWith(displayName: event.displayName));
      fsRef.set(state);
    });
  }
}
