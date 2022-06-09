import 'package:cloud_firestore/cloud_firestore.dart';

class DocumentNotFoundError extends Error {}

Map<String, dynamic> convertFromDoc(Map<String, dynamic> docData) {
  final Map<String, dynamic> newMap = {};

  for (MapEntry e in docData.entries) {
    if (e.value is Timestamp) {
      newMap[e.key] = (e.value as Timestamp).toDate();
    } else {
      newMap[e.key] = e.value;
    }
  }

  return newMap;
}

Map<String, dynamic> convertToDoc(Map<String, dynamic> docData) {
  final Map<String, dynamic> newMap = {};

  for (MapEntry e in docData.entries) {
    if (e.value is DateTime) {
      newMap[e.key] = Timestamp.fromDate(e.value as DateTime);
    } else {
      newMap[e.key] = e.value;
    }
  }

  return newMap;
}
