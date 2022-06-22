


import 's.dart';

/// The translations for English (`en`).
class SEn extends S {
  SEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'BloxTest10';

  @override
  String get helloWorld => 'Hello World!';

  @override
  String get settingsScreenLabel => 'Settings';

  @override
  String get settingsSignedInAsPrompt => 'Settings screen, you\'re signed in as: ';

  @override
  String get infoScreenLabel => 'Info';

  @override
  String get infoScreenDescription => 'Info screen';

  @override
  String get developerScreenLabel => 'Developer menu';

  @override
  String get logoutActionLabel => 'Logout';

  @override
  String get leftTabLabel => 'Left';

  @override
  String get homeTabLabel => 'Home';

  @override
  String get rightTabLabel => 'Right';

  @override
  String get signUpButtonLabel => 'Sign up';

  @override
  String get signUpWithEmailButtonLabel => 'Sign up with email?';

  @override
  String get signInWithAppleButtonLabel => 'Sign in with Apple';

  @override
  String get signInWithGoogleButtonLabel => 'Sign in with Google';

  @override
  String get authEmailLabel => 'Email';

  @override
  String get authPasswordLabel => 'Password';

  @override
  String get authConfirmPasswordLabel => 'Confirm password';

  @override
  String get authCreateAccountButtonLabel => 'Create account';

  @override
  String get authLogInButtonLabel => 'Log in';

  @override
  String get authErrorEmailAlreadyInUse => 'That email is already registered! Try logging in.';

  @override
  String get authErrorUnknown => 'An unknown error occurred, try again later.';

  @override
  String get authErrorUserNotFound => 'We didn\'t recognise those details, try again.';

  @override
  String get authErrorWeakPassword => 'Password is too weak! Try a longer or more complex one.';

  @override
  String get authErrorWrongPassword => 'We didn\'t recognise those details, try again.';

  @override
  String get authErrorInvalidCredential => 'A problem occurred signing in with the identity provider.';

  @override
  String get authErrorUserAccountDisabled => 'Your user account is disabled';

  @override
  String get emailVerifyPrompt => 'Thanks for signing up! Please click the link in the email to verify your email address.';

  @override
  String get emailCheckVerificationButtonLabel => 'I have verified';
}
