// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$_AuthEventEmailLogin _$$_AuthEventEmailLoginFromJson(
        Map<String, dynamic> json) =>
    _$_AuthEventEmailLogin(
      email: json['email'] as String,
      password: json['password'] as String,
    );

Map<String, dynamic> _$$_AuthEventEmailLoginToJson(
        _$_AuthEventEmailLogin instance) =>
    <String, dynamic>{
      'email': instance.email,
      'password': instance.password,
    };

_$_AuthEventEmailSignUp _$$_AuthEventEmailSignUpFromJson(
        Map<String, dynamic> json) =>
    _$_AuthEventEmailSignUp(
      email: json['email'] as String,
      password: json['password'] as String,
    );

Map<String, dynamic> _$$_AuthEventEmailSignUpToJson(
        _$_AuthEventEmailSignUp instance) =>
    <String, dynamic>{
      'email': instance.email,
      'password': instance.password,
    };

_$_AuthState _$$_AuthStateFromJson(Map<String, dynamic> json) => _$_AuthState(
      isLoading: json['isLoading'] as bool? ?? true,
      isEmailVerificationInProgress:
          json['isEmailVerificationInProgress'] as bool? ?? false,
      authErrors: (json['authErrors'] as List<dynamic>?)
              ?.map((e) => $enumDecode(_$AuthErrorsEnumMap, e))
              .toList() ??
          const [],
    );

Map<String, dynamic> _$$_AuthStateToJson(_$_AuthState instance) =>
    <String, dynamic>{
      'isLoading': instance.isLoading,
      'isEmailVerificationInProgress': instance.isEmailVerificationInProgress,
      'authErrors':
          instance.authErrors.map((e) => _$AuthErrorsEnumMap[e]).toList(),
    };

const _$AuthErrorsEnumMap = {
  AuthErrors.weakPassword: 'weakPassword',
  AuthErrors.emailInUse: 'emailInUse',
  AuthErrors.userNotFound: 'userNotFound',
  AuthErrors.wrongPassword: 'wrongPassword',
  AuthErrors.userDisabled: 'userDisabled',
  AuthErrors.invalidCredential: 'invalidCredential',
  AuthErrors.unknown: 'unknown',
};

_$_UserProfileState _$$_UserProfileStateFromJson(Map<String, dynamic> json) =>
    _$_UserProfileState(
      hasUserSetDisplayName: json['hasUserSetDisplayName'] as bool? ?? false,
      displayName: json['displayName'] as String?,
      email: json['email'] as String?,
      photoUrl: json['photoUrl'] as String?,
      created: json['created'] == null
          ? null
          : DateTime.parse(json['created'] as String),
    );

Map<String, dynamic> _$$_UserProfileStateToJson(_$_UserProfileState instance) =>
    <String, dynamic>{
      'hasUserSetDisplayName': instance.hasUserSetDisplayName,
      'displayName': instance.displayName,
      'email': instance.email,
      'photoUrl': instance.photoUrl,
      'created': instance.created?.toIso8601String(),
    };
