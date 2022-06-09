import 'package:flutter/material.dart';

import 'package:bloxtest10/l10n/s.dart';

class InfoScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final strings = S.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(strings.infoScreenLabel)),
      body: Center(child: Text(strings.infoScreenDescription)),
    );
  }
}
