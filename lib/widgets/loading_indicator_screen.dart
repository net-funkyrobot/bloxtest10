import 'package:flutter/material.dart';

class LoadingIndicatorScreen extends StatelessWidget {
  final Widget child;
  final bool isLoading;

  const LoadingIndicatorScreen({
    Key? key,
    required this.child,
    required this.isLoading,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        child,
        if (isLoading)
          const Align(
            alignment: Alignment.topCenter,
            child: LinearProgressIndicator(),
          ),
      ],
    );
  }
}
