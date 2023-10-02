class FormField(object):
    name: str = None
    label: str = None
    value = ""
    inputType: str = None
    defaultValue = None
    dataType: str = None
    required: bool = False
    placeholder = None
    errorText: str = None
    isErrorTextOn: bool = True
    isError: bool = False
    helpText: str = None
    isWrapper: bool = True
    isLabel: bool = True
    allAttributes: dict = None

    # Select Input
    isMultiSelect: bool = False
    selectOptions: dict = None

    # Radio & Check
    radioItem: dict = None
    checked: str = "True"
    unchecked: str = "False"

    def add_attribute(self, name, value):
        if not self.allAttributes:
            self.allAttributes = {}
        if name not in self.allAttributes:
            self.allAttributes[name] = value
        elif name in self.allAttributes:
            self.allAttributes[name] = f"{self.allAttributes[name]} {value}"
