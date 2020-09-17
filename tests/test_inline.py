from unittest import TestCase

from lxml import etree
from tests.support import ParserSupport


class InlineTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_remark(self):
        tree = self.parse("""
[[a remark]]
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [{
                'type': 'inline',
                'name': 'remark',
                'attribs': {'status': 'editorial'},
                'children': [{
                    'type': 'text',
                    'value': '[a remark]',
                }]
            }],
        }, tree.to_dict())

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <remark status="editorial">[a remark]</remark>
</p>
""", xml)

    def test_remark_with_inlines(self):
        tree = self.parse("""
[[{{>https://example.com a link}}]]
""", 'line')

        self.assertEqual({
            'type': 'content',
            'name': 'p',
            'children': [{
                'type': 'inline',
                'name': 'remark',
                'attribs': {'status': 'editorial'},
                'children': [{
                    'type': 'text',
                    'value': '[',
                }, {
                    'type': 'inline',
                    'name': 'ref',
                    'attribs': {'href': 'https://example.com'},
                    'children': [{
                        'type': 'text',
                        'value': 'a link',
                    }]
                }, {
                    'type': 'text',
                    'value': ']',
                }]
            }],
        }, tree.to_dict())

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <remark status="editorial">[<ref href="https://example.com">a link</ref>]</remark>
</p>
""", xml)

    def test_ref(self):
        tree = self.parse("""
{{>https://example.com a link}}
        """, 'line')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref href="https://example.com">a link</ref>
</p>
""", xml)

    def test_ref_nested(self):
        tree = self.parse("""
{{>https://example.com  a link{{^2}} **with stuff**}}
""", 'line')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref href="https://example.com"> a link<sup>2</sup> <b>with stuff</b></ref>
</p>
""", xml)

    def test_ref_no_text(self):
        tree = self.parse("""
{{>https://example.com}}
        """, 'line')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref href="https://example.com"/>
</p>
""", xml)

    def test_ref_no_href(self):
        tree = self.parse("""
{{> link text}}
        """, 'line')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref href="">link text</ref>
</p>
""", xml)

    def test_images(self):
        tree = self.parse("""
{{IMG /foo.png}} {{IMG/foo.png}} {{IMGfoo.png}}
        """, 'line')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1"><img src="/foo.png"/> <img src="/foo.png"/> <img src="foo.png"/></p>
""", xml)

    def test_images_with_alt(self):
        tree = self.parse("""
{{IMG /foo.png  description text }}
        """, 'line')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <img src="/foo.png" alt="description text"/>
</p>
""", xml)

    def test_image_no_src(self):
        tree = self.parse("""
{{IMG }} {{IMG}}
        """, 'line')

        xml = etree.tostring(self.to_xml(tree.to_dict()), encoding='unicode', pretty_print=True)

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">{{IMG }} {{IMG}}</p>
""", xml)
