
import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 's_en.dart';

/// Callers can lookup localized strings with an instance of S returned
/// by `S.of(context)`.
///
/// Applications need to include `S.delegate()` in their app's
/// localizationDelegates list, and the locales they support in the app's
/// supportedLocales list. For example:
///
/// ```
/// import 'l10n/s.dart';
///
/// return MaterialApp(
///   localizationsDelegates: S.localizationsDelegates,
///   supportedLocales: S.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the S.supportedLocales
/// property.
abstract class S {
  S(String locale) : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static S of(BuildContext context) {
    return Localizations.of<S>(context, S)!;
  }

  static const LocalizationsDelegate<S> delegate = _SDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates = <LocalizationsDelegate<dynamic>>[
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
  ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en')
  ];

  /// No description provided for @appTitle.
  ///
  /// In en, this message translates to:
  /// **'BloxTest10'**
  String get appTitle;

  /// No description provided for @helloWorld.
  ///
  /// In en, this message translates to:
  /// **'Hello World!'**
  String get helloWorld;

  /// No description provided for @settingsScreenLabel.
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settingsScreenLabel;

  /// No description provided for @settingsSignedInAsPrompt.
  ///
  /// In en, this message translates to:
  /// **'Settings screen, you\'re signed in as: '**
  String get settingsSignedInAsPrompt;

  /// No description provided for @infoScreenLabel.
  ///
  /// In en, this message translates to:
  /// **'Info'**
  String get infoScreenLabel;

  /// No description provided for @infoScreenDescription.
  ///
  /// In en, this message translates to:
  /// **'Info screen'**
  String get infoScreenDescription;

  /// No description provided for @developerScreenLabel.
  ///
  /// In en, this message translates to:
  /// **'Developer menu'**
  String get developerScreenLabel;

  /// No description provided for @logoutActionLabel.
  ///
  /// In en, this message translates to:
  /// **'Logout'**
  String get logoutActionLabel;

  /// No description provided for @leftTabLabel.
  ///
  /// In en, this message translates to:
  /// **'Left'**
  String get leftTabLabel;

  /// No description provided for @homeTabLabel.
  ///
  /// In en, this message translates to:
  /// **'Home'**
  String get homeTabLabel;

  /// No description provided for @rightTabLabel.
  ///
  /// In en, this message translates to:
  /// **'Right'**
  String get rightTabLabel;

  /// No description provided for @signUpButtonLabel.
  ///
  /// In en, this message translates to:
  /// **'Sign up'**
  String get signUpButtonLabel;

  /// No description provided for @signUpWithEmailButtonLabel.
  ///
  /// In en, this message translates to:
  /// **'Sign up with email?'**
  String get signUpWithEmailButtonLabel;

  /// No description provided for @signInWithAppleButtonLabel.
  ///
  /// In en, this message translates to:
  /// **'Sign in with Apple'**
  String get signInWithAppleButtonLabel;

  /// No description provided for @signInWithGoogleButtonLabel.
  ///
  /// In en, this message translates to:
  /// **'Sign in with Google'**
  String get signInWithGoogleButtonLabel;

  /// No description provided for @authEmailLabel.
  ///
  /// In en, this message translates to:
  /// **'Email'**
  String get authEmailLabel;

  /// No description provided for @authPasswordLabel.
  ///
  /// In en, this message translates to:
  /// **'Password'**
  String get authPasswordLabel;

  /// No description provided for @authConfirmPasswordLabel.
  ///
  /// In en, this message translates to:
  /// **'Confirm password'**
  String get authConfirmPasswordLabel;

  /// No description provided for @authCreateAccountButtonLabel.
  ///
  /// In en, this message translates to:
  /// **'Create account'**
  String get authCreateAccountButtonLabel;

  /// No description provided for @authLogInButtonLabel.
  ///
  /// In en, this message translates to:
  /// **'Log in'**
  String get authLogInButtonLabel;

  /// No description provided for @authErrorEmailAlreadyInUse.
  ///
  /// In en, this message translates to:
  /// **'That email is already registered! Try logging in.'**
  String get authErrorEmailAlreadyInUse;

  /// No description provided for @authErrorUnknown.
  ///
  /// In en, this message translates to:
  /// **'An unknown error occurred, try again later.'**
  String get authErrorUnknown;

  /// No description provided for @authErrorUserNotFound.
  ///
  /// In en, this message translates to:
  /// **'We didn\'t recognise those details, try again.'**
  String get authErrorUserNotFound;

  /// No description provided for @authErrorWeakPassword.
  ///
  /// In en, this message translates to:
  /// **'Password is too weak! Try a longer or more complex one.'**
  String get authErrorWeakPassword;

  /// No description provided for @authErrorWrongPassword.
  ///
  /// In en, this message translates to:
  /// **'We didn\'t recognise those details, try again.'**
  String get authErrorWrongPassword;

  /// No description provided for @authErrorInvalidCredential.
  ///
  /// In en, this message translates to:
  /// **'A problem occurred signing in with the identity provider.'**
  String get authErrorInvalidCredential;

  /// No description provided for @authErrorUserAccountDisabled.
  ///
  /// In en, this message translates to:
  /// **'Your user account is disabled'**
  String get authErrorUserAccountDisabled;

  /// No description provided for @emailVerifyPrompt.
  ///
  /// In en, this message translates to:
  /// **'Thanks for signing up! Please click the link in the email to verify your email address.'**
  String get emailVerifyPrompt;

  /// No description provided for @emailCheckVerificationButtonLabel.
  ///
  /// In en, this message translates to:
  /// **'I have verified'**
  String get emailCheckVerificationButtonLabel;
}

class _SDelegate extends LocalizationsDelegate<S> {
  const _SDelegate();

  @override
  Future<S> load(Locale locale) {
    return SynchronousFuture<S>(lookupS(locale));
  }

  @override
  bool isSupported(Locale locale) => <String>['en'].contains(locale.languageCode);

  @override
  bool shouldReload(_SDelegate old) => false;
}

S lookupS(Locale locale) {


  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en': return SEn();
  }

  throw FlutterError(
    'S.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.'
  );
}
