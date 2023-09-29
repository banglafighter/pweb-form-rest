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
    isError: bool = False
    helpText: str = None
    isWrapper: bool = True
    isLabel: bool = True
    allAttributes: dict = None

    # Select Input
    isMultiSelect: bool = False
    selectOptions: dict = None
