import 'package:flutter/cupertino.dart';

class TextInfoWidget extends StatelessWidget {
  final String labelText;
  final String valueText;

  const TextInfoWidget(this.labelText, this.valueText, {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(0, 5, 0, 5),
      child: Row(
        children: [
          Text(
            style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
            labelText,
          ),
          SizedBox(width: 5),
          valueText == ""
              ? Text(
            style: TextStyle(fontStyle: FontStyle.italic, fontSize: 17),
            overflow: TextOverflow.ellipsis,
            maxLines: 1,
            "Aucune information",
          )
              : Text(
            style: TextStyle(fontSize: 17),
            overflow: TextOverflow.ellipsis,
            maxLines: 1,
            valueText,
          ),
        ],
      ),
    );
  }
}