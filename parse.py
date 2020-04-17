#!/usr/bin/env python
import json
import sys
import argparse

from lxml import etree as ET

from bluebell.parser import pre_parse, parse_with_failure, make_akn
from bluebell.akn import ParseError


def print_with_lines(lines):
    for i, line in enumerate(lines.split('\n')):
        i = i + 1
        print(f'{i:02}: {line}', file=sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse text into Akoma Ntoso.')
    parser.add_argument('root', type=str, help='the type of document to parse (eg. judgment)')
    parser.add_argument('input', type=str, help='file to parse')
    parser.add_argument('--json', dest='json', action='store_true', help='output intermediate json, rather than XML.')
    args = parser.parse_args()

    lines = open(args.input, "r").read()
    lines = pre_parse(lines, indent='{', dedent='}')
    try:
        tree = parse_with_failure(lines, args.root)
    except ParseError as e:
        print_with_lines(lines)
        raise

    tree = tree.to_dict()

    if args.json:
        print(json.dumps(tree))
    else:
        xml = make_akn(tree, args.root)
        print(ET.tostring(xml, pretty_print=True, encoding='unicode'))
