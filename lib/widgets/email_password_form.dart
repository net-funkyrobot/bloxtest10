import 'package:flutter/material.dart';

import 'package:bloxtest10/constants.dart';
import 'package:bloxtest10/l10n/s.dart';
import 'package:bloxtest10/models/models.dart';

class EmailPasswordForm extends StatefulWidget {
  final bool signUp;
  final Function(String email, String password) submitCallback;
  final List<AuthErrors> errors;

  const EmailPasswordForm({
    Key? key,
    this.signUp = false,
    required this.submitCallback,
    this.errors = const [],
  }) : super(key: key);

  @override
  State<StatefulWidget> createState() => _EmailPasswordFormState();
}

class _EmailPasswordFormState extends State<EmailPasswordForm> {
  late final TextEditingController email;
  late final TextEditingController password;
  late final TextEditingController signUpPasswordConfirmation;

  @override
  void initState() {
    email = TextEditingController()
      ..addListener(() {
        setState(() {});
      });
    password = TextEditingController()
      ..addListener(() {
        setState(() {});
      });
    signUpPasswordConfirmation = TextEditingController()
      ..addListener(() {
        setState(() {});
      });

    super.initState();
  }

  @override
  void dispose() {
    email.dispose();
    password.dispose();
    signUpPasswordConfirmation.dispose();
    super.dispose();
  }

  bool get _isLoginValid => email.text.isNotEmpty && password.text.isNotEmpty;

  bool get _isSignUpValid =>
      email.text.isNotEmpty &&
      password.text.isNotEmpty &&
      password.text == signUpPasswordConfirmation.text;

  @override
  Widget build(BuildContext context) {
    final strings = S.of(context);
    final errorTexts = <AuthErrors, String>{
      AuthErrors.emailInUse: strings.authErrorEmailAlreadyInUse,
      AuthErrors.unknown: strings.authErrorUnknown,
      AuthErrors.userNotFound: strings.authErrorUserNotFound,
      AuthErrors.weakPassword: strings.authErrorWeakPassword,
      AuthErrors.wrongPassword: strings.authErrorWrongPassword,
      AuthErrors.invalidCredential: strings.authErrorInvalidCredential,
      AuthErrors.userDisabled: strings.authErrorUserAccountDisabled,
    };
    final errorMessage = widget.errors.isNotEmpty
        ? widget.errors.map((errorCode) => errorTexts[errorCode]).join("\n")
        : null;
    final theme = Theme.of(context);

    return Column(
      mainAxisSize: MainAxisSize.max,
      children: [
        if (errorMessage != null)
          SizedBox(
            width: double.infinity,
            child: Container(
              margin: const EdgeInsets.only(bottom: kstPaddingUnit),
              height: 40.0,
              child: Text(
                errorMessage,
                textAlign: TextAlign.center,
                style: theme.textTheme.bodyLarge
                    ?.copyWith(color: theme.errorColor),
              ),
            ),
          ),
        Container(
          padding: const EdgeInsets.only(bottom: kstPaddingUnit),
          child: TextField(
            controller: email,
            decoration: InputDecoration(
              border: const OutlineInputBorder(),
              labelText: strings.authEmailLabel,
            ),
          ),
        ),
        Container(
          padding: const EdgeInsets.only(bottom: kstPaddingUnit),
          child: TextField(
            controller: password,
            obscureText: true,
            decoration: InputDecoration(
              border: const OutlineInputBorder(),
              labelText: strings.authPasswordLabel,
            ),
          ),
        ),
        if (widget.signUp)
          Container(
            padding: const EdgeInsets.only(bottom: kstPaddingUnit),
            child: TextField(
              controller: signUpPasswordConfirmation,
              obscureText: true,
              decoration: InputDecoration(
                border: const OutlineInputBorder(),
                labelText: strings.authConfirmPasswordLabel,
              ),
            ),
          ),
        if (widget.signUp)
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _isSignUpValid
                  ? () {
                      if (_isSignUpValid) {
                        widget.submitCallback(
                          email.value.text,
                          password.value.text,
                        );
                      } else {
                        // todo: show error message
                      }
                    }
                  : null,
              child: Text(strings.authCreateAccountButtonLabel),
            ),
          ),
        if (!widget.signUp)
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _isLoginValid
                  ? () {
                      if (_isLoginValid) {
                        widget.submitCallback(
                          email.value.text,
                          password.value.text,
                        );
                      } else {
                        // todo: show error message
                      }
                    }
                  : null,
              child: Text(strings.authLogInButtonLabel),
            ),
          ),
      ],
    );
  }
}
