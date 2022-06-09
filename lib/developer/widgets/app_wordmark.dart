part of '../developer.dart';

final appWordmarkExample = _WidgetDisplayData(
  title: 'App wordmark',
  widgets: [
    _WidgetFrameData(
      title: "App bar wordmark",
      description: "Displayed under app bar background (primaryColor).",
      builder: (context) {
        final theme = Theme.of(context);
        return SizedBox(
          width: double.infinity,
          height: AppBar().preferredSize.height,
          child: Stack(
            children: [
              Container(color: theme.primaryColor),
              Center(child: AppWordmark()),
            ],
          ),
        );
      },
    ),
  ],
);
