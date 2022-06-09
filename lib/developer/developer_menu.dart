part of 'developer.dart';

final _devMenuItems = <String, WidgetBuilder>{
  "Widget catalog": (_) => _WidgetCatalogScreen(),
};

class DeveloperMenuScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final menuEntries = _devMenuItems.entries.toList();

    return Scaffold(
      appBar: AppBar(title: const Text("Developer menu")),
      body: ListView.separated(
        itemCount: _devMenuItems.length,
        separatorBuilder: (_, __) => const Divider(),
        itemBuilder: (context, i) => ListTile(
          title: Text(menuEntries[i].key),
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: menuEntries[i].value)
          )
        ),
      ),
    );
  }
}
