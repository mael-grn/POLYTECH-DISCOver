import 'package:discover/controllers/ExploreController.dart';
import 'package:discover/widgets/ui/TextInputWidget.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/Song.dart';

class ExploreView extends StatefulWidget {
  ExploreView({super.key});

  @override
  State<ExploreView> createState() => _ExploreView();
}

class _ExploreView extends State<ExploreView> {
  @override
  void initState() {
    super.initState();
    final controller = Provider.of<ExploreController>(context, listen: false);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      controller.initData();
    });
  }

  @override
  Widget build(BuildContext context) {
    print("🟢 ExploreView BUILD");
    final controller = context.watch<ExploreController>();

    return Scaffold(
      appBar: AppBar(
        title: const Text("Explore"),
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Theme(
              data: Theme.of(context).copyWith(
                textSelectionTheme: const TextSelectionThemeData(
                  selectionColor: Colors.yellow,        // couleur du texte sélectionné
                  selectionHandleColor: Colors.orange,  // couleur des "poignées" de sélection
                  cursorColor: Colors.white,            // curseur
                ),
              ),
              child: TextInputWidget(
                controller: controller.searchQueryController,
                hint: "Artists, songs, ...",
                icon: Icons.search,
                big: true,
                onSubmitted: (_) => controller.searchSongs(),
                onIconClick: () => controller.searchSongs(),
              ),
            ),
            const SizedBox(height: 20),

            // ⚡️ Indicateur de chargement
            if (controller.isLoading)
              const Center(child: CircularProgressIndicator()),

            // ⚡️ Si pas de résultats et pas en train de charger
            if (!controller.isLoading && controller.searchResults.isEmpty)
              Expanded(
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Image.asset(
                        "images/team/nahel-search.png",
                        height: 200,
                      ),
                      const SizedBox(height: 10),
                      const Text(
                        "Aucune chanson trouvée",
                        style: TextStyle(fontSize: 18),
                      ),
                    ],
                  ),
                ),
              ),

            // ⚡️ Liste des résultats
            if (controller.searchResults.isNotEmpty)
              Expanded(
                child: ListView.builder(
                  itemCount: controller.searchResults.length,
                  itemBuilder: (context, index) {
                    final Song song = controller.searchResults[index];
                    return Container(
                      margin: const EdgeInsets.symmetric(vertical: 6),
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      decoration: BoxDecoration(
                        color: Colors.grey[850], // 🔹 fond du rectangle contrasté avec le noir
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: ListTile(
                        title: Text(
                          song.name,
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                        subtitle: Text(
                          "${song.artist} • ${song.album}",
                          style: TextStyle(color: Colors.grey[300]),
                        ),
                        trailing: Icon(Icons.play_arrow, color: Colors.lightGreenAccent),
                        onTap: () {
                          // Optionnel : jouer la chanson ou afficher les détails
                        },
                      ),
                    );
                  },
                ),
              ),
          ],
        ),
      ),
    );
  }
}
