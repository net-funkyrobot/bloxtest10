part of 'models.dart';

abstract class UserProfileEvent {}

class UserProfileEventInitialize extends UserProfileEvent {}

@freezed
class UserProfileEventUpdateDisplayName extends UserProfileEvent
    with _$UserProfileEventUpdateDisplayName {
  factory UserProfileEventUpdateDisplayName({
    required String displayName,
  }) = _UserProfileEventUpdateDisplayName;
}

@freezed
class UserProfileState with _$UserProfileState {
  const UserProfileState._();
  const factory UserProfileState({
    @Default(true) @JsonKey(ignore: true) bool isLoading,
    @Default(false) bool hasUserSetDisplayName,
    String? displayName,
    String? email,
    String? photoUrl,
    DateTime? created,
  }) = _UserProfileState;

  factory UserProfileState.fromJson(Map<String, dynamic> json) =>
      _$UserProfileStateFromJson(json);

  String getUserIdentifyingString() {
    return displayName ?? email ?? "Unknown user";
  }
}
