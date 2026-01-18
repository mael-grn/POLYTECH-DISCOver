import '../enums/NetworkErrorEnum.dart';

class NetworkException implements Exception {
  final NetworkErrorEnum networkError;
  final String? message;
  NetworkException(this.networkError, [this.message]);
}