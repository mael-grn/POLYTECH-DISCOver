import '../core/provider.dart';

class Healthservice {
  Future<bool> checkServerHealth() async {
    await Provider.sendRequest(route: '/health', method: HttpMethod.GET);
    return true;
  }
}