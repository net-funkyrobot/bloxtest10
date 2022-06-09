import 'dart:io';

import 'package:flutter/material.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

import 'package:bloxtest10/blocs/auth.dart';
import 'package:bloxtest10/constants.dart';
import 'package:bloxtest10/l10n/s.dart';
import 'package:bloxtest10/models/models.dart';
import 'package:bloxtest10/widgets/app_wordmark.dart';
import 'package:bloxtest10/widgets/email_password_form.dart';

class EmailPasswordLoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final authBloc = context.read<AuthBloc>();
    final strings = S.of(context);
    const pagePadding = kstPaddingUnit * 3;

    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, authState) {
        return Scaffold(
          appBar: AppBar(title: AppWordmark()),
          body: SafeArea(
            child: Center(
              child: SingleChildScrollView(
                child: Stack(
                  children: [
                    Column(
                      mainAxisSize: MainAxisSize.max,
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: pagePadding,
                          ),
                          child: EmailPasswordForm(
                            errors: authState.authErrors,
                            submitCallback: (email, password) => authBloc.add(
                              AuthEventEmailLogin(
                                email: email,
                                password: password,
                              ),
                            ),
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: pagePadding,
                          ),
                          child: SizedBox(
                            width: double.infinity,
                            child: OutlinedButton(
                              onPressed: () {
                                Navigator.pushNamed(
                                  context,
                                  kstEmailPasswordSignUpScreen,
                                );
                                authBloc.add(AuthEventClearErrors());
                              },
                              child: Text(strings.signUpWithEmailButtonLabel),
                            ),
                          ),
                        ),
                        if (Platform.isIOS)
                          Container(
                            padding: const EdgeInsets.fromLTRB(
                              pagePadding,
                              pagePadding,
                              pagePadding,
                              0,
                            ),
                            child: SizedBox(
                              width: double.infinity,
                              child: OutlinedButton(
                                onPressed: () {
                                  authBloc.add(AuthEventSignInWithApple());
                                },
                                child: Text(strings.signInWithAppleButtonLabel),
                              ),
                            ),
                          ),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: pagePadding,
                          ),
                          child: SizedBox(
                            width: double.infinity,
                            child: OutlinedButton(
                              onPressed: () {
                                authBloc.add(AuthEventSignInWithGoogle());
                              },
                              child: Text(strings.signInWithGoogleButtonLabel),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
