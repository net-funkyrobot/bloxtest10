import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:loggy/loggy.dart';

import 'package:bloxtest10/utils.dart';

class DebugBlocObserver extends BlocObserver with UiLoggy {
  @override
  void onEvent(Bloc bloc, Object? event) {
    if (event != null) {
      final foldableString = createFoldableForObject(event);

      if (foldableString != null) {
        loggy.info(
          '${bloc.runtimeType} [EVENT] ${event.runtimeType}\n'
          '$foldableString',
        );
      } else {
        loggy.info('${bloc.runtimeType} [EVENT] ${event.runtimeType}');
      }
    } else {
      loggy.info('${bloc.runtimeType} [EVENT]');
    }

    super.onEvent(bloc, event);
  }

  @override
  void onChange(BlocBase bloc, Change change) {
    final foldableString = createFoldableForObject(
      change.nextState,
      objectDescription: "Next state",
    );

    String className = "";
    try {
      className = change.nextState.runtimeType.toString().split("(")[0];
    } on Error {
      className = change.nextState.runtimeType.toString();
    }

    if (foldableString != null) {
      loggy.info(
        '${bloc.runtimeType} [STATE] $className\n'
        '$foldableString',
      );
    } else {
      loggy.info('${bloc.runtimeType} [STATE] $className');
    }

    super.onChange(bloc, change);
  }
}
