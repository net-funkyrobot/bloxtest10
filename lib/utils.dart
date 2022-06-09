import 'dart:convert';

String? createFoldableForObject(Object o, {String? objectDescription}) {
  String? objectJson;
  String? foldableString;
  const encoder = JsonEncoder.withIndent("  ");

  try {
    objectJson = encoder.convert(o);
  } on Error {
    objectJson = null;
  }

  if (objectJson != null) {
    foldableString = createFoldable(
      objectJson,
      description: objectDescription,
    );
  }

  return foldableString;
}

String createFoldable(String str, {String? description}) {
  final lines = str.split("\n");
  List<String> newLines = ["╔ ${description ?? ""}"];

  for (int i = 0; i < lines.length; i++) {
    newLines.add("║  ${lines[i]}");
  }

  newLines.addAll(["╚"]);

  return newLines.join("\n");
}
