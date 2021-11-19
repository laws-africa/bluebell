#!/usr/bin/env python

import sys
import os.path

from lxml import etree
from cobalt.akn import get_maker, AKN_NAMESPACES, DEFAULT_VERSION

ns = AKN_NAMESPACES[DEFAULT_VERSION]
maker = get_maker()


def migrate(fname):
    with open(fname) as f:
        xml = etree.parse(f)

    xml = etree.fromstring(apply_xslt(xml))
    eol_to_p(xml)

    sys.stdout.write(etree.tostring(xml, encoding='unicode'))


def apply_xslt(xml):
    fname = os.path.join(os.path.dirname(__file__), 'slaw-to-bluebell.xslt')
    xslt = etree.XSLT(etree.parse(fname))

    return str(xslt(xml))


def eol_to_p(xml):
    # change eol's in p's to consecutive p's, going backwards
    for eol in reversed(xml.xpath('//a:p/a:eol', namespaces={'a': ns})):
        # TODO: handle other elements
        p = maker.p()
        p.text = eol.tail or ''
        eol.addnext(p)
        eol.getparent().remove(eol)


if __name__ == '__main__':
    migrate(sys.argv[1])
