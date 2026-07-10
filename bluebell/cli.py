import json
import sys
import argparse

from cobalt import FrbrUri
from lxml import etree as ET

from bluebell.parser import AkomaNtosoParser, parse_to_xml
from bluebell.akn import ParseError


def print_with_lines(lines):
    for i, line in enumerate(lines.split('\n')):
        i = i + 1
        print(f'{i:02}: {line}', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Parse text into Akoma Ntoso.')
    parser.add_argument('frbr_uri', type=str, help='frbr_uri for the document to parse')
    parser.add_argument('root', type=str, help='the type of document to parse (eg. judgment)')
    parser.add_argument('input', type=str, help='file to parse')
    parser.add_argument('--json', dest='json', action='store_true', help='output intermediate json, rather than XML')
    parser.add_argument('--pretty', dest='pretty', action='store_true', help='prettify output')
    args = parser.parse_args()

    frbr_uri = FrbrUri.parse(args.frbr_uri)
    text = open(args.input, "r").read()

    if args.json:
        akn_parser = AkomaNtosoParser(frbr_uri)
        try:
            tree = akn_parser.parse(text, args.root)
        except ParseError:
            print_with_lines(text)
            raise

        tree = tree.to_dict()
        print(json.dumps(tree))
    else:
        xml = parse_to_xml(text, args.root, frbr_uri)
        print(ET.tostring(xml, pretty_print=args.pretty, encoding='unicode'))
