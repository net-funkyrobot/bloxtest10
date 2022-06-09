import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:loggy/loggy.dart';
import 'package:provider/provider.dart';

import 'package:bloxtest10/blocs/user_profile.dart';
import 'package:bloxtest10/developer/developer.dart';
import 'package:bloxtest10/l10n/s.dart';
import 'package:bloxtest10/screens/home.dart';
import 'package:bloxtest10/screens/info.dart';
import 'package:bloxtest10/theme.dart';
import 'package:bloxtest10/blocs/auth.dart';
import 'package:bloxtest10/models/models.dart';
import 'package:bloxtest10/constants.dart';
import 'package:bloxtest10/screens/email_password_sign_up.dart';
import 'package:bloxtest10/screens/settings_screen.dart';
import 'package:bloxtest10/screens/email_password_login.dart';
import 'package:bloxtest10/screens/email_password_verification.dart';
import 'package:bloxtest10/screens/loading.dart';

class App extends StatelessWidget {
  final FirebaseApp firebaseApp;

  const App({Key? key, required this.firebaseApp}) : super(key: key);

  // This widget is the root the application.
  @override
  Widget build(BuildContext context) {
    // This global key is used to keep the SignInApp's NavigatorState alive when
    // SignInApp is no longer in the tree
    final navigatorKey = GlobalKey<NavigatorState>();

    return MultiProvider(
      providers: [
        // SignInApp's NavigatorState key, added to top-level provider so it can
        // be accessed inside SignInApp
        // Get's overridden by HomeApp's key by home app's provider
        Provider<GlobalKey<NavigatorState>>(
          create: (_) => navigatorKey,
        ),
        Provider<FirebaseApp>(
          create: (_) => firebaseApp,
        ),
        Provider<AuthBloc>(
          create: (_) => AuthBloc(firebaseApp)..add(AuthEventInitialize()),
          dispose: (_, authBloc) => authBloc.close(),
          lazy: false,
        ),
      ],
      child: _RootApp(navigatorKey: navigatorKey),
    );
  }
}

class _RootApp extends StatelessWidget with UiLoggy {
  final GlobalKey<NavigatorState> navigatorKey;

  const _RootApp({Key? key, required this.navigatorKey}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, authState) {
        // Only display one "XApp" (containing a MaterialApp) at one time
        // depending on auth status
        if (authState.isLoading ||
            !authState.isAuthenticated ||
            authState.isAnonymous ||
            !authState.isEmailVerified) {
          // When not authenticated as a real user OR email verification
          // required
          return _SignInApp(navigatorKey: navigatorKey);
        } else {
          // Only when authenticated as a real user
          return _HomeApp();
        }
      },
    );
  }
}

class _SignInRootScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocListener<AuthBloc, AuthState>(
      // Only trigger listen callback once, when the logged in state changes
      listenWhen: (prevState, state) {
        return prevState.firebaseUser?.uid != state.firebaseUser?.uid;
      },
      listener: (context, authState) {
        // Pop if/when the user changes
        Navigator.popUntil(
          context,
          ModalRoute.withName(kstSignInHomeScreen),
        );
      },
      child: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, authState) {
          if (authState.isLoading || !authState.isAuthenticated) {
            // Display loading
            return LoadingScreen();
          } else if (authState.isAnonymous) {
            // Display login/signup for anonymous user
            return EmailPasswordLoginScreen();
          } else if (!authState.isEmailVerified) {
            // Display email verification
            return EmailPasswordVerificationScreen();
          } else {
            // Display loading
            return LoadingScreen();
          }
        },
      ),
    );
  }
}

class _SignInApp extends StatelessWidget {
  final GlobalKey<NavigatorState> navigatorKey;

  const _SignInApp({Key? key, required this.navigatorKey}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      key: const ValueKey("sign-in-app"),
      title: "BloxTest10",
      localizationsDelegates: S.localizationsDelegates,
      supportedLocales: S.supportedLocales,
      theme: blocksLightTheme,
      darkTheme: blocksDarkTheme,
      routes: <String, WidgetBuilder>{
        kstSignInHomeScreen: (_) => _SignInRootScreen(),
        kstEmailPasswordSignUpScreen: (_) => EmailPasswordSignUpScreen(),
      },
      // Assign a single global key and put it in top level provider
      navigatorKey: navigatorKey,
      initialRoute: kstSignInHomeScreen,
    );
  }
}

class _HomeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final firebaseApp = context.read<FirebaseApp>();
    final navigatorKey = GlobalKey<NavigatorState>();
    final homeScreenKey = GlobalKey<HomeScreenState>();

    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, authState) {
        // HomeApp has it's own provider for injecting blocs and services that
        // only make sense once you have a single, authenticated user
        return MultiProvider(
          providers: [
            Provider<GlobalKey<HomeScreenState>>(
              create: (_) => homeScreenKey,
            ),
            Provider<UserProfileBloc>(
              create: (_) => UserProfileBloc(
                app: firebaseApp,
                user: authState.firebaseUser!,
              )..add(UserProfileEventInitialize()),
              lazy: false,
            ),
          ],
          child: MaterialApp(
            key: const ValueKey("home-app"),
            title: "BloxTest10",
            theme: blocksLightTheme,
            localizationsDelegates: S.localizationsDelegates,
            supportedLocales: S.supportedLocales,
            darkTheme: blocksDarkTheme,
            routes: <String, WidgetBuilder>{
              kstHomeScreen: (_) => HomeScreen(key: homeScreenKey),
              kstSettingsScreen: (_) => SettingsScreen(),
              kstInfoScreen: (_) => InfoScreen(),
              // Developer screen
              if (kDebugMode)
                kstDeveloperMenuScreen: (_) => DeveloperMenuScreen(),
            },
            initialRoute: kstHomeScreen,
            navigatorKey: navigatorKey,
          ),
        );
      },
    );
  }
}
