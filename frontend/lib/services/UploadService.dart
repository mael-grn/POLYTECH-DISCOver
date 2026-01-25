
import 'dart:convert';

import 'package:discover/models/Song.dart';
import 'package:discover/models/Upload.dart';
import 'package:discover/models/UploadedResult.dart';

import '../core/provider.dart';

class Uploadservice {


  Future<Song?> getLastUploadedSongByUser() async {
    return null;
  }

  Future<UploadedResult> uploadSong(String filepath, String filename, bool private) async {
    final response = await Provider.sendMultipartRequest(
      route: '/uploads/file',
      filePath: filepath,
      fields: {
        'private': private ? 'true' : 'false',
        'name': filename,
      },
    );
    return UploadedResult.fromJson(jsonDecode(response));
  }

  Future<List<Upload>> getMyUploads() async {
    final response = await Provider.sendRequest(route: '/analyze/me', method: HttpMethod.GET);
    final Map<String, dynamic> data = jsonDecode(response);
    print(response);
    final List<dynamic> listData = data['items'];
    return listData.map((item) => Upload.fromJson(item)).toList();
  }

}