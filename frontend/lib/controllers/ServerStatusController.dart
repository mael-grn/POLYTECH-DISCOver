
import 'package:discover/dialogs/AlertDialogBuilder.dart';
import 'package:discover/services/HealthService.dart';
import 'package:flutter/cupertino.dart';

import '../exceptions/RequestException.dart';

class ServerStatusController with ChangeNotifier {

  Healthservice healthService;
  ServerStatusController(this.healthService);

  bool serverHealthy = false;

  Future<void> initData() async {
    await checkServerHealth();
  }

  Future<void> checkServerHealth() async {
    DialogBuilder.loading();
    try {
      serverHealthy = await healthService.checkServerHealth();
    } on NetworkException catch (e) {
      serverHealthy = false;
    } finally {

      DialogBuilder.closeCurrentDialog();
      notifyListeners();
    }
  }
}