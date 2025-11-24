import 'package:flutter/material.dart';
  import 'package:flutter/services.dart';

  import '../../core/theme/app_theme.dart';

  class TextFieldWidget extends StatelessWidget {
    final TextEditingController? controller;
    final String? labelText;
    final String? hintText;
    final String? errorText;
    final IconData? prefixIcon;
    final IconButton? suffixIcon;
    final bool obscureText;
    final TextInputType? keyboardType;
    final TextInputAction? textInputAction;
    final TextCapitalization textCapitalization;
    final TextStyle? style;
    final TextStyle? labelStyle;
    final TextStyle? hintStyle;
    final TextStyle? errorStyle;
    final EdgeInsetsGeometry? contentPadding;
    final int? maxLength;
    final List<TextInputFormatter>? inputFormatters;
    final ValueChanged<String>? onChanged;
    final FormFieldValidator<String>? validator;
    final GestureTapCallback? onTap;
    final ValueChanged<String>? onSubmitted;
    final FocusNode? focusNode;
    final bool readOnly;
    final bool autocorrect;
    final bool enableSuggestions;
    final int? maxLines;
    final int? minLines;
    final TextAlign textAlign;
    final TextAlignVertical? textAlignVertical;
    final bool expands;
    final Brightness? keyboardAppearance;
    final String? obscuringCharacter;
    final bool? enableInteractiveSelection;
    final InputBorder? focusedBorder;
    final InputBorder? enabledBorder;
    final InputBorder? errorBorder;
    final InputBorder? disabledBorder;

    const TextFieldWidget({
      super.key,
      this.controller,
      this.labelText,
      this.hintText,
      this.errorText,
      this.prefixIcon,
      this.suffixIcon,
      this.obscureText = false,
      this.keyboardType,
      this.textInputAction,
      this.textCapitalization = TextCapitalization.none,
      this.style,
      this.labelStyle,
      this.hintStyle,
      this.errorStyle,
      this.contentPadding = const EdgeInsets.all(16.0),
      this.maxLength,
      this.inputFormatters,
      this.onChanged,
      this.validator,
      this.onTap,
      this.onSubmitted,
      this.focusNode,
      this.readOnly = false,
      this.autocorrect = true,
      this.enableSuggestions = true,
      this.maxLines = 1,
      this.minLines,
      this.textAlign = TextAlign.start,
      this.textAlignVertical,
      this.expands = false,
      this.keyboardAppearance,
      this.obscuringCharacter = '•',
      this.enableInteractiveSelection,
      this.focusedBorder,
      this.enabledBorder,
      this.errorBorder,
      this.disabledBorder,
    });

    @override
    Widget build(BuildContext context) {

      return TextFormField(
        controller: controller,
        decoration: InputDecoration(
          labelText: labelText,
          hintText: hintText,
          errorText: errorText,
          prefixIcon: prefixIcon != null ? Icon(prefixIcon, color: foregroundVariantColor) : null,
          suffixIcon: suffixIcon,
          labelStyle: labelStyle ?? TextStyle(color: foregroundColor.withOpacity(0.7)),
          hintStyle: hintStyle ?? TextStyle(color: foregroundVariantColor.withOpacity(0.6)),
          errorStyle: errorStyle ?? TextStyle(color: Colors.redAccent),
          errorMaxLines: 3, // <-- Ajouté pour permettre le retour à la ligne du message d'erreur
          contentPadding: contentPadding,
          border: enabledBorder ?? OutlineInputBorder(
            borderRadius: BorderRadius.circular(8.0),
            borderSide: BorderSide(color: backgroundVariantColor),
          ),
          focusedBorder: focusedBorder ?? OutlineInputBorder(
            borderRadius: BorderRadius.circular(8.0),
            borderSide: BorderSide(color: primaryColor, width: 2.0),
          ),
          errorBorder: errorBorder ?? OutlineInputBorder(
            borderRadius: BorderRadius.circular(8.0),
            borderSide: const BorderSide(color: Colors.redAccent),
          ),
          disabledBorder: disabledBorder ?? OutlineInputBorder(
            borderRadius: BorderRadius.circular(8.0),
            borderSide: BorderSide(color: backgroundVariantColor.withOpacity(0.5)),
          ),
          enabledBorder: enabledBorder ?? OutlineInputBorder(
            borderRadius: BorderRadius.circular(8.0),
            borderSide: BorderSide(color: backgroundVariantColor),
          ),
          filled: true,
          fillColor: backgroundColor,
        ),
        obscureText: obscureText,
        keyboardType: keyboardType,
        textInputAction: textInputAction,
        textCapitalization: textCapitalization,
        style: style ?? TextStyle(color: foregroundColor),
        maxLength: maxLength,
        inputFormatters: inputFormatters,
        onChanged: onChanged,
        validator: validator,
        onTap: onTap,
        focusNode: focusNode,
        readOnly: readOnly,
        autocorrect: autocorrect,
        enableSuggestions: enableSuggestions,
        maxLines: maxLines,
        minLines: minLines,
        textAlign: textAlign,
        textAlignVertical: textAlignVertical,
        expands: expands,
        keyboardAppearance: keyboardAppearance,
        obscuringCharacter: obscuringCharacter ?? "",
        enableInteractiveSelection: enableInteractiveSelection,
      );
    }
  }