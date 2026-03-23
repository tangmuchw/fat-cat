main() async {
  var halogens = {'fluorine', 'chlorine', 'bromine', 'iodine', 'astatine'};

  var elements = <String>{};
  elements.add('fluorine');
  // elements.addAll(halogens);
  assert(elements.length == 5);
  print(elements);
}
