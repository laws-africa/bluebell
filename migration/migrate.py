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
    """ Change eol's in p's to consecutive p's, going backwards.

        <p>foo<eol/>bar<eol/>with a <term>term</term></p>
    becomes
        <p>foo</p>
        <p>bar</p>
        <p>with a <term>term</term></p>
    """
    for eol in reversed(xml.xpath('//a:p/a:eol', namespaces={'a': ns})):
        p = maker.p()

        # trailing text
        p.text = eol.tail or ''
        # following siblings elements
        for sibling in eol.itersiblings():
            p.append(sibling)

        parent = eol.getparent()
        parent.addnext(p)
        parent.remove(eol)


if __name__ == '__main__':
    migrate(sys.argv[1])
