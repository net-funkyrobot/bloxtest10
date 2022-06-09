part of 'models.dart';

abstract class AuthEvent {}

class AuthEventInitialize extends AuthEvent {}

class AuthEventClearErrors extends AuthEvent {}

@freezed
class AuthEventUserChanged extends AuthEvent with _$AuthEventUserChanged {
  factory AuthEventUserChanged({
    required User? newUser,
  }) = _AuthEventUserChanged;
}

@freezed
class AuthEventEmailLogin extends AuthEvent with _$AuthEventEmailLogin {
  @JsonSerializable()
  factory AuthEventEmailLogin({
    required String email,
    required String password,
  }) = _AuthEventEmailLogin;
}

@freezed
class AuthEventEmailSignUp extends AuthEvent with _$AuthEventEmailSignUp {
  @JsonSerializable()
  factory AuthEventEmailSignUp({
    required String email,
    required String password,
  }) = _AuthEventEmailSignUp;
}

class AuthEventEmailStartVerification extends AuthEvent {}

class AuthEventEmailVerificationCheck extends AuthEvent {}

enum AuthErrors {
  weakPassword,
  emailInUse,
  userNotFound,
  wrongPassword,
  userDisabled,
  invalidCredential,
  unknown,
}

@freezed
class AuthEventSignInWithOAuthCredential extends AuthEvent
    with _$AuthEventSignInWithOAuthCredential {
  factory AuthEventSignInWithOAuthCredential({
    required OAuthCredential credential,
  }) = _AuthEventSignInWithOAuthCredential;
}

class AuthEventSignInWithApple extends AuthEvent {}

class AuthEventSignInWithGoogle extends AuthEvent {}

class AuthEventSignOut extends AuthEvent {}

@freezed
class AuthState with _$AuthState {
  const AuthState._();

  const factory AuthState({
    @JsonKey(ignore: true) User? firebaseUser,
    @Default(true) bool isLoading,
    @Default(false) bool isEmailVerificationInProgress,
    @Default([]) List<AuthErrors> authErrors,
  }) = _AuthState;

  factory AuthState.fromJson(Map<String, dynamic> json) =>
      _$AuthStateFromJson(json);

  bool get isAuthenticated => firebaseUser != null;

  bool get isAnonymous => firebaseUser?.isAnonymous ?? false;

  bool get isEmailVerified => firebaseUser?.emailVerified ?? false;
}
