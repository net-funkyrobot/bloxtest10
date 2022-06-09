import 'package:flutter/material.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

import 'package:bloxtest10/blocs/auth.dart';
import 'package:bloxtest10/constants.dart';
import 'package:bloxtest10/l10n/s.dart';
import 'package:bloxtest10/models/models.dart';
import 'package:bloxtest10/widgets/loading_indicator_screen.dart';
import 'package:bloxtest10/widgets/email_password_form.dart';

class EmailPasswordSignUpScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final authBloc = context.read<AuthBloc>();
    final theme = Theme.of(context);
    final mediaQuery = MediaQuery.of(context);
    final strings = S.of(context);
    const pagePadding = kstPaddingUnit * 3;

    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, authState) {
        return Stack(
          children: [
            Scaffold(
              appBar: AppBar(title: Text(strings.signUpButtonLabel)),
              body: LoadingIndicatorScreen(
                isLoading: authState.isLoading,
                child: Center(
                  child: SingleChildScrollView(
                    child: Column(
                      mainAxisSize: MainAxisSize.max,
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: pagePadding,
                          ),
                          child: EmailPasswordForm(
                            signUp: true,
                            errors: authState.authErrors,
                            submitCallback: (email, password) => authBloc.add(
                              AuthEventEmailSignUp(
                                email: email,
                                password: password,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            if (authState.isLoading)
              Opacity(
                opacity: 0.95,
                child: Container(
                  color: theme.highlightColor,
                  height: mediaQuery.size.height,
                  width: mediaQuery.size.width,
                ),
              ),
          ],
        );
      },
    );
  }
}
