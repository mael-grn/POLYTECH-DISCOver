import 'dart:ffi';

class Analyze {
  final Float probViralite;

  const Analyze(this.probViralite);

  factory Analyze.fromJson(Map<String, dynamic> json) {
    return Analyze(
      json['probViralite'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'probViralite': probViralite,
    };
  }
}