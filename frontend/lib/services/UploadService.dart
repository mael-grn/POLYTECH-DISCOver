
import 'package:discover/models/Song.dart';

import '../core/provider.dart';

class Uploadservice {


  Future<Song?> getLastUploadedSongByUser() async {
    return null;
  }

  Future<void> uploadSong(String filepath, String filename, bool private) async {
    await Provider.sendMultipartRequest(
      route: '/upload/file',
      filePath: filepath,
      fields: {
        'private': private ? 'true' : 'false',
        'name': filename,
      },
    );
  }

}