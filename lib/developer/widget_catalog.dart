part of 'developer.dart';

class _WidgetDisplayData {
  final String title;
  final List<_WidgetFrameData> widgets;

  const _WidgetDisplayData({
    required this.title,
    required this.widgets,
  });
}

class _WidgetFrameData {
  final String title;
  final String? description;
  final WidgetBuilder builder;

  const _WidgetFrameData({
    required this.title,
    required this.description,
    required this.builder,
  });
}

final _widgetCatalogItems = <_WidgetDisplayData>[
  appWordmarkExample,
];

class _WidgetCatalogScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Widget catalog")),
      body: ListView.separated(
        itemCount: _widgetCatalogItems.length,
        separatorBuilder: (_, __) => const Divider(),
        itemBuilder: (context, i) => ListTile(
          title: Text(_widgetCatalogItems[i].title),
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => _WidgetDisplayScreen(
                widgetData: _widgetCatalogItems[i],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _WidgetDisplayScreen extends StatelessWidget {
  final _WidgetDisplayData widgetData;

  const _WidgetDisplayScreen({
    Key? key,
    required this.widgetData,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widgetData.title)),
      body: ListView.separated(
        itemCount: widgetData.widgets.length,
        separatorBuilder: (_, __) => const Divider(),
        itemBuilder: (context, i) => _WidgetFrame(
          title: widgetData.widgets[i].title,
          description: widgetData.widgets[i].description,
          builder: widgetData.widgets[i].builder,
        ),
      ),
    );
  }
}

class _WidgetFrame extends StatelessWidget {
  final String title;
  final String? description;
  final WidgetBuilder builder;

  const _WidgetFrame({
    Key? key,
    required this.title,
    this.description,
    required this.builder,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(kstPaddingUnit),
          margin: const EdgeInsets.symmetric(vertical: kstPaddingUnit),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: theme.textTheme.headline6),
              if (description != null) Padding(
                padding: const EdgeInsets.only(top: kstPaddingUnit),
                child: Text(description!),
              ),
            ],
          ),
        ),
        builder(context),
      ],
    );
  }
}
