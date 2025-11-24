import 'package:discover/views/AccountView.dart';
import 'package:discover/views/ExploreView.dart';
import 'package:discover/views/UploadView.dart';
import 'package:discover/widgets/ui/PageWidget.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../core/theme/app_theme.dart';
import 'HomeView.dart';

class GlobalLayout extends StatefulWidget {
  const GlobalLayout({super.key});

  @override
  _GlobalLayoutState createState() => _GlobalLayoutState();
}

class _GlobalLayoutState extends State<GlobalLayout> with TickerProviderStateMixin {
  int currentPageIndex = 0;
  late PageController _pageController;

  // Animation pour le mobile
  late AnimationController _animationController;
  late Animation<double> _animation;

  late final List<Widget> _pages;

  @override
  void initState() {
    super.initState();
    // Contrôleur d'animation (gardé pour la version mobile)
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );
    _animation = Tween<double>(begin: 0, end: 0).animate(_animationController);

    _pageController = PageController(initialPage: currentPageIndex);
    _pages = [
      HomeView(key: PageStorageKey('HomeView')),
      ExploreView(key: PageStorageKey('MoneyView')),
      Uploadview(key: PageStorageKey('FriendsView')),
      AccountView(key: PageStorageKey('MeView')),
    ];
  }

  void _onItemTapped(int index) {
    // Animation uniquement utile pour le style mobile, mais on la lance quand même
    _animation = Tween<double>(
      begin: currentPageIndex.toDouble(),
      end: index.toDouble(),
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));

    _animationController.forward(from: 0);

    HapticFeedback.mediumImpact();
    setState(() {
      currentPageIndex = index;
    });
    _pageController.jumpToPage(index);
  }

  @override
  void dispose() {
    _pageController.dispose();
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Utilisation de LayoutBuilder pour la réactivité
    return LayoutBuilder(
      builder: (context, constraints) {
        // On considère "Desktop" si la largeur dépasse 800px (ajustable)
        bool isDesktop = constraints.maxWidth > 800;

        return Scaffold(
          // Sur PC, l'AppBar contient la navigation. Sur Mobile, juste le titre.
          appBar: isDesktop
              ? _buildDesktopAppBar()
              : _buildMobileAppBar(),

          body: Stack(
            children: [
              // Le corps de la page
              Padding(
                // Moins de padding sur les côtés en version desktop pour profiter de l'espace
                padding: EdgeInsets.fromLTRB(isDesktop ? 0 : 20, 0, isDesktop ? 0 : 20, 0),
                child: PageView(
                  controller: _pageController,
                  physics: const NeverScrollableScrollPhysics(), // Empêche le swipe manuel si désiré
                  children: _pages,
                ),
              ),

              // La barre de navigation flottante (Uniquement visible sur MOBILE)
              if (!isDesktop)
                Positioned(
                  bottom: 0,
                  left: 0,
                  right: 0,
                  child: Center(
                    child: Container(
                      margin: const EdgeInsets.only(bottom: 25.0),
                      height: 70,
                      child: Center(
                        child: Container(
                            width: 280,
                            height: 70,
                            decoration: BoxDecoration(
                              color: backgroundVariantColor,
                              borderRadius: BorderRadius.circular(50),
                            ),
                            child: Stack(
                              alignment: Alignment.center,
                              children: [
                                AnimatedBuilder(
                                  animation: _animation,
                                  builder: (context, child) {
                                    return Positioned(
                                      left: (_animation.value * 70.0 + 10),
                                      child: Container(
                                        width: 50,
                                        height: 50,
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          color: primaryColor,
                                        ),
                                      ),
                                    );
                                  },
                                ),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                  children: [
                                    _buildMobileNavItem('icons/home.svg', 0),
                                    _buildMobileNavItem('icons/search.svg', 1),
                                    _buildMobileNavItem('icons/upload.svg', 2),
                                    _buildMobileNavItem('icons/account.svg', 3),
                                  ],
                                ),
                              ],
                            )
                        ),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        );
      },
    );
  }

  // --- WIDGETS MOBILES ---

  PreferredSizeWidget _buildMobileAppBar() {
    return AppBar(
      backgroundColor: backgroundColor,
      elevation: 0,
      scrolledUnderElevation: 0,
      title: Text(
        "DISCOver",
        style: TextStyle(
          color: foregroundColor,
          fontWeight: FontWeight.w600,
          fontSize: 35,
        ),
      ),
    );
  }

  Widget _buildMobileNavItem(String assetPath, int index) {
    return GestureDetector(
      onTap: () => _onItemTapped(index),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: SvgPicture.asset(
          assetPath,
          width: 30,
          height: 30,
          colorFilter: ColorFilter.mode(
            index == currentPageIndex ? Colors.white : foregroundColor,
            BlendMode.srcIn,
          ),
        ),
      ),
    );
  }

  // --- WIDGETS DESKTOP / TABLETTE ---

  PreferredSizeWidget _buildDesktopAppBar() {
    return AppBar(
      backgroundColor: backgroundColor, // Assure-toi que c'est la couleur bleu foncé
      elevation: 0,
      toolbarHeight: 80, // Un peu plus haut pour le style PC
      title: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20.0),
        child: Row(
          children: [
            // Logo / Titre à gauche
            Container(
              width: 50,
              height: 50,
              decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.grey[400]), // Placeholder pour le cercle du logo si besoin
            ),
            const SizedBox(width: 15),
            Text(
              "DISCOver",
              style: TextStyle(
                color: foregroundColor,
                fontWeight: FontWeight.bold,
                fontSize: 32,
              ),
            ),
            const Spacer(), // Pousse les boutons vers la droite

            // Boutons de navigation
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildDesktopNavItem("HOME", 'icons/home.svg', 0),
                const SizedBox(width: 10),
                _buildDesktopNavItem("SEARCH", 'icons/search.svg', 1),
                const SizedBox(width: 10),
                _buildDesktopNavItem("UPLOAD", 'icons/upload.svg', 2),
                const SizedBox(width: 10),
                _buildDesktopNavItem("ACCOUNT", 'icons/account.svg', 3),
              ],
            )
          ],
        ),
      ),
    );
  }

  Widget _buildDesktopNavItem(String label, String assetPath, int index) {
    bool isSelected = index == currentPageIndex;

    return InkWell(
      onTap: () => _onItemTapped(index),
      borderRadius: BorderRadius.circular(30),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        decoration: BoxDecoration(
          // Couleur de fond "Active" (Rose/Primaire) vs Transparent
          color: isSelected ? primaryColor : Colors.transparent,
          borderRadius: BorderRadius.circular(30),
        ),
        child: Row(
          children: [
            SvgPicture.asset(
              assetPath,
              width: 20,
              height: 20,
              colorFilter: ColorFilter.mode(
                Colors.white, // Toujours blanc sur fond foncé ou rose
                BlendMode.srcIn,
              ),
            ),
            const SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w600,
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }
}