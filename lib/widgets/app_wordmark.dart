import 'package:flutter/material.dart';

import 'package:bloxtest10/l10n/s.dart';

class AppWordmark extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final strings = S.of(context);

    return Text(
      strings.appTitle.toLowerCase(),
      style: const TextStyle(
        fontSize: 40,
        fontFamily: "Baskerville",
        fontWeight: FontWeight.w900,
        fontStyle: FontStyle.italic,
      ),
    );
  }
}
