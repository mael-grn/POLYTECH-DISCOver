import 'package:flutter/material.dart';
import 'package:discover/core/theme/app_theme.dart';

class PopupPageWidget extends StatelessWidget {
  final String? title;
  final Widget body;
  final String? closeButtonTag;
  const PopupPageWidget({this.title, required this.body, this.closeButtonTag, super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: backgroundColor,
        elevation: 0,
        scrolledUnderElevation: 0,
        title: Text(
          title ?? "",
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SizedBox(
        width: double.infinity,
        height: double.infinity,
        child: Container(
            color: backgroundColor,
            child: Padding(
              padding: EdgeInsets.fromLTRB(20, 0, 20, 0),
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(height: 15),
                    body,
                    SizedBox(height: 100),
                  ],
                ),
              ),
            ),
        ),
      ),
    );
  }
}
