"""Validation for namespace-free XML attribute names.

Bluebell's attribute syntax has no way to bind XML namespaces.  It therefore
accepts XML ``NCName`` values, rather than qualified names: this is the XML
1.0 (Fifth Edition) ``Name`` production with ``:`` excluded.  The character
ranges below are the W3C ``NameStartChar`` and ``NameChar`` productions.
"""


def is_xml_ncname(value):
    """Return whether *value* is an XML 1.0 namespace-free name.

    Keep this deliberately range-based instead of using a Unicode category or
    an ASCII regular expression: XML defines its own, stable character ranges.
    """
    return bool(value) and _is_name_start_char(value[0]) and all(
        _is_name_char(char) for char in value[1:]
    )


def _is_name_start_char(char):
    codepoint = ord(char)
    return any((
        char == "_",
        "A" <= char <= "Z",
        "a" <= char <= "z",
        0xC0 <= codepoint <= 0xD6,
        0xD8 <= codepoint <= 0xF6,
        0xF8 <= codepoint <= 0x2FF,
        0x370 <= codepoint <= 0x37D,
        0x37F <= codepoint <= 0x1FFF,
        0x200C <= codepoint <= 0x200D,
        0x2070 <= codepoint <= 0x218F,
        0x2C00 <= codepoint <= 0x2FEF,
        0x3001 <= codepoint <= 0xD7FF,
        0xF900 <= codepoint <= 0xFDCF,
        0xFDF0 <= codepoint <= 0xFFFD,
        0x10000 <= codepoint <= 0xEFFFF,
    ))


def _is_name_char(char):
    codepoint = ord(char)
    return any((
        _is_name_start_char(char),
        char in "-.",
        "0" <= char <= "9",
        codepoint == 0xB7,
        0x0300 <= codepoint <= 0x036F,
        0x203F <= codepoint <= 0x2040,
    ))
