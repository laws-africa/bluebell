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
    return (
        char == "_"
        or "A" <= char <= "Z"
        or "a" <= char <= "z"
        or 0xC0 <= codepoint <= 0xD6
        or 0xD8 <= codepoint <= 0xF6
        or 0xF8 <= codepoint <= 0x2FF
        or 0x370 <= codepoint <= 0x37D
        or 0x37F <= codepoint <= 0x1FFF
        or 0x200C <= codepoint <= 0x200D
        or 0x2070 <= codepoint <= 0x218F
        or 0x2C00 <= codepoint <= 0x2FEF
        or 0x3001 <= codepoint <= 0xD7FF
        or 0xF900 <= codepoint <= 0xFDCF
        or 0xFDF0 <= codepoint <= 0xFFFD
        or 0x10000 <= codepoint <= 0xEFFFF
    )


def _is_name_char(char):
    codepoint = ord(char)
    return (
        _is_name_start_char(char)
        or char in "-."
        or "0" <= char <= "9"
        or codepoint == 0xB7
        or 0x0300 <= codepoint <= 0x036F
        or 0x203F <= codepoint <= 0x2040
    )
