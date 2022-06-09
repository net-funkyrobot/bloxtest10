import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

import 'package:bloxtest10/blocs/auth.dart';
import 'package:bloxtest10/constants.dart';
import 'package:bloxtest10/l10n/s.dart';
import 'package:bloxtest10/models/models.dart';
import 'package:bloxtest10/widgets/app_wordmark.dart';

enum HSPopupMenuAction { settings, info, developerMenu, logout }

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => HomeScreenState();
}

class HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 1;
  AuthBloc? _authBloc;

  @override
  void initState() {
    _authBloc = context.read<AuthBloc>();
    super.initState();
  }

  void showScreenAtIndex(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _handlePopupMenuAction(HSPopupMenuAction action) {
    switch (action) {
      case HSPopupMenuAction.settings:
        Navigator.pushNamed(context, kstSettingsScreen);
        break;
      case HSPopupMenuAction.info:
        Navigator.pushNamed(context, kstInfoScreen);
        break;
      case HSPopupMenuAction.developerMenu:
        Navigator.pushNamed(context, kstDeveloperMenuScreen);
        break;
      case HSPopupMenuAction.logout:
        _authBloc?.add(AuthEventSignOut());
        break;
      default:
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    final strings = S.of(context);

    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, authState) {
        return Scaffold(
          appBar: AppBar(
            title: AppWordmark(),
            actions: [
              PopupMenuButton(
                itemBuilder: (BuildContext context) =>
                    <PopupMenuEntry<HSPopupMenuAction>>[
                  PopupMenuItem<HSPopupMenuAction>(
                    child: ListTile(
                      leading: const Icon(Icons.settings),
                      title: Text(strings.settingsScreenLabel),
                    ),
                    value: HSPopupMenuAction.settings,
                  ),
                  PopupMenuItem<HSPopupMenuAction>(
                    child: ListTile(
                      leading: const Icon(Icons.info),
                      title: Text(strings.infoScreenLabel),
                    ),
                    value: HSPopupMenuAction.info,
                  ),
                  if (kDebugMode) ...[
                    const PopupMenuDivider(),
                    PopupMenuItem<HSPopupMenuAction>(
                      child: ListTile(
                        leading: const Icon(Icons.developer_mode),
                        title: Text(strings.developerScreenLabel),
                      ),
                      value: HSPopupMenuAction.developerMenu,
                    ),
                    const PopupMenuDivider(),
                  ],
                  PopupMenuItem<HSPopupMenuAction>(
                    child: ListTile(
                      leading: const Icon(Icons.logout),
                      title: Text(strings.logoutActionLabel),
                    ),
                    value: HSPopupMenuAction.logout,
                  ),
                ],
                onSelected: _handlePopupMenuAction,
              ),
            ],
          ),
          bottomNavigationBar: BottomNavigationBar(
            items: [
              BottomNavigationBarItem(
                icon: const Icon(Icons.add_circle),
                label: strings.leftTabLabel,
              ),
              BottomNavigationBarItem(
                icon: const Icon(Icons.feed),
                label: strings.homeTabLabel,
              ),
              BottomNavigationBarItem(
                icon: const Icon(Icons.add_location),
                label: strings.rightTabLabel,
              ),
            ],
            currentIndex: _selectedIndex,
            landscapeLayout: BottomNavigationBarLandscapeLayout.linear,
            onTap: showScreenAtIndex,
          ),
          body: SafeArea(
            child: Center(
              child: Text(strings.helloWorld),
            ),
          ),
        );
      },
    );
  }
}
