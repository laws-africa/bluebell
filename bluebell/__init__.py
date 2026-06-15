__version__ = "4.0.0"


def parse_to_xml(text, root, frbr_uri, eid_prefix=''):
    from .parser import parse_to_xml as _parse_to_xml

    return _parse_to_xml(text, root, frbr_uri, eid_prefix)
