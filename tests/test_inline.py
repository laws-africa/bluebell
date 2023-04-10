from unittest import TestCase

from tests.support import ParserSupport


class InlineTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_remark(self):
        tree = self.parse("""
{{*[a remark]}}
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <remark status="editorial">[a remark]</remark>
</p>
""", xml)

    def test_double_bold(self):
        """ double inlines are not supported """
        tree = self.parse("""
****Notice**s**
""", 'line')

        self.assertDictEqual({
            'type': 'content',
            'name': 'p',
            'children': [
                {
                    'type': 'text',
                    'value': '*',
                },
                {
                    'type': 'inline',
                    'name': 'b',
                    'children': [
                        {
                            'type': 'text',
                            'value': '*',
                        },
                        {
                            'type': 'text',
                            'value': 'Notice',
                        },
                    ],
                },
                {
                    'type': 'text',
                    'value': 's',
                },
                {
                    'type': 'text',
                    'value': '*',
                },
                {
                    'type': 'text',
                    'value': '*',
                },
            ],
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">*<b>*Notice</b>s**</p>
""", xml)

    def test_multiline_remark(self):
        tree = self.parse("""
{{*[a remark

that covers
multiple lines]}}
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
                    'value': '[a remark',
                }, {
                    'type': 'element',
                    'name': 'br'
                }, {
                    'type': 'element',
                    'name': 'br'
                }, {
                    'type': 'text',
                    'value': 'that covers',
                }, {
                    'type': 'element',
                    'name': 'br'
                }, {
                    'type': 'text',
                    'value': 'multiple lines]',
                }]
            }],
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <remark status="editorial">[a remark<br/><br/>that covers<br/>multiple lines]</remark>
</p>
""", xml)

    def test_multiline_remark_with_indents(self):
        # this is not allowed and is effectively ignored
        tree = self.parse("""
PARA
    {{*[a remark

        that covers
    multiple lines]}}
""", 'hier_element')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<paragraph xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="para_nn_1">
  <content>
    <p eId="para_nn_1__p_1">{{*[a remark</p>
    <p eId="para_nn_1__p_2">that covers</p>
    <p eId="para_nn_1__p_3">multiple lines]}}</p>
  </content>
</paragraph>
""", xml)

    def test_multiline_remark_with_dedents(self):
        # this is not allowed and is effectively ignored
        tree = self.parse("""
SEC
  PARA
    {{*[a remark

  that covers
    multiple lines]}}
""", 'hier_element')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="sec_nn_1">
  <paragraph eId="sec_nn_1__para_nn_1">
    <content>
      <p eId="sec_nn_1__para_nn_1__p_1">{{*[a remark</p>
    </content>
  </paragraph>
  <wrapUp>
    <p eId="sec_nn_1__wrapup__p_1">that covers</p>
    <p eId="sec_nn_1__wrapup__p_2">multiple lines]}}</p>
  </wrapUp>
</section>
""", xml)

    def test_remark_with_inlines(self):
        tree = self.parse("""
{{*[{{>https://example.com a link}}]}}
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

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <remark status="editorial">[<ref eId="p_1__ref_1" href="https://example.com">a link</ref>]</remark>
</p>
""", xml)

    def test_inlines_with_remark(self):
        tree = self.parse("""
**bold {{^super {{*[foo {{>/bar link}} end]}}}} {{*[and another]}}**
""", 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <b>bold <sup>super <remark status="editorial">[foo <ref eId="p_1__ref_1" href="/bar">link</ref> end]</remark></sup> <remark status="editorial">[and another]</remark></b>
</p>
""", xml)

    def test_ref(self):
        tree = self.parse("""
{{>https://example.com a link}}
        """, 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref eId="p_1__ref_1" href="https://example.com">a link</ref>
</p>
""", xml)

    def test_ref_nested(self):
        tree = self.parse("""
{{>https://example.com  a link{{^2}} **with stuff**}}
""", 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref eId="p_1__ref_1" href="https://example.com"> a link<sup>2</sup> <b>with stuff</b></ref>
</p>
""", xml)

    def test_ref_no_text(self):
        tree = self.parse("""
{{>https://example.com}}
        """, 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref eId="p_1__ref_1" href="https://example.com"/>
</p>
""", xml)

    def test_ref_no_href(self):
        tree = self.parse("""
{{> link text}}
        """, 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ref eId="p_1__ref_1" href="">link text</ref>
</p>
""", xml)

    def test_images(self):
        tree = self.parse("""
{{IMG /foo.png}} {{IMG/foo.png}} {{IMGfoo.png}}
        """, 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1"><img src="/foo.png"/> <img src="/foo.png"/> <img src="foo.png"/></p>
""", xml)

    def test_images_with_alt(self):
        tree = self.parse("""
{{IMG /foo.png  description text }}
        """, 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <img alt="description text" src="/foo.png"/>
</p>
""", xml)

    def test_image_no_src(self):
        tree = self.parse("""
{{IMG }} {{IMG}}
        """, 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">{{IMG }} {{IMG}}</p>
""", xml)

    def test_image_broken(self):
        tree = self.parse("""{{IMG
 }}
""", 'statement')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<statement xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" name="statement">
  <mainBody>
    <p eId="p_1">{{IMG</p>
    <p eId="p_2">}}</p>
  </mainBody>
</statement>
""", xml)

    def test_sup(self):
        tree = self.parse("""
        {{^su}per}}
        """, 'line')

        self.assertEqual({
            'name': 'p',
            'type': 'content',
            'children': [{
                'type': 'inline',
                'name': 'sup',
                'children': [
                    {'type': 'text', 'value': 'su'},
                    {'type': 'text', 'value': '}'},
                    {'type': 'text', 'value': 'per'},
                ]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <sup>su}per</sup>
</p>
""", xml)

    def test_sup_nested(self):
        tree = self.parse("""
{{^super {{_s}ub}} **bo*ld**}}
""", 'line')

        self.assertEqual({
            'name': 'p',
            'type': 'content',
            'children': [{
                'type': 'inline',
                'name': 'sup',
                'children': [
                    {'type': 'text', 'value': 'super '},
                    {
                        'type': 'inline',
                        'name': 'sub',
                        'children': [
                            {'type': 'text', 'value': 's'},
                            {'type': 'text', 'value': '}'},
                            {'type': 'text', 'value': 'ub'},
                        ]
                    },
                    {'type': 'text', 'value': ' '},
                    {
                        'type': 'inline',
                        'name': 'b',
                        'children': [
                            {'type': 'text', 'value': 'bo'},
                            {'type': 'text', 'value': '*'},
                            {'type': 'text', 'value': 'ld'},
                        ]
                    }
                ]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <sup>super <sub>s}ub</sub> <b>bo*ld</b></sup>
</p>
""", xml)

    def test_ins(self):
        tree = self.parse("""
        {{+ in}s}} and {{+  one with a space at the start and end }}
        """, 'line')

        self.assertEqual({
            'name': 'p',
            'type': 'content',
            'children': [{
                'type': 'inline',
                'name': 'ins',
                'children': [
                    {'type': 'text', 'value': 'in'},
                    {'type': 'text', 'value': '}'},
                    {'type': 'text', 'value': 's'},
                ]
            }, {
                'type': 'text', 'value': ' and '
            }, {
                'type': 'inline',
                'name': 'ins',
                'children': [
                    {'type': 'text', 'value': ' one with a space at the start and end '},
                ]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1"><ins>in}s</ins> and <ins> one with a space at the start and end </ins></p>
""", xml)

    def test_del(self):
        tree = self.parse("""
        {{- de}l}} and {{-  one with a space at the start and end }}
        """, 'line')

        self.assertEqual({
            'name': 'p',
            'type': 'content',
            'children': [{
                'type': 'inline',
                'name': 'del',
                'children': [
                    {'type': 'text', 'value': 'de'},
                    {'type': 'text', 'value': '}'},
                    {'type': 'text', 'value': 'l'},
                ]
            }, {
                'type': 'text', 'value': ' and '
            }, {
                'type': 'inline',
                'name': 'del',
                'children': [
                    {'type': 'text', 'value': ' one with a space at the start and end '},
                ]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1"><del>de}l</del> and <del> one with a space at the start and end </del></p>
""", xml)

    def test_ins_del_nested(self):
        tree = self.parse("""
{{+ ins {{- de}l}} **bo*ld**}}
""", 'line')

        self.assertEqual({
            'name': 'p',
            'type': 'content',
            'children': [{
                'type': 'inline',
                'name': 'ins',
                'children': [
                    {'type': 'text', 'value': 'ins '},
                    {
                        'type': 'inline',
                        'name': 'del',
                        'children': [
                            {'type': 'text', 'value': 'de'},
                            {'type': 'text', 'value': '}'},
                            {'type': 'text', 'value': 'l'},
                        ]
                    },
                    {'type': 'text', 'value': ' '},
                    {
                        'type': 'inline',
                        'name': 'b',
                        'children': [
                            {'type': 'text', 'value': 'bo'},
                            {'type': 'text', 'value': '*'},
                            {'type': 'text', 'value': 'ld'},
                        ]
                    }
                ]
            }]
        }, tree.to_dict())

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">
  <ins>ins <del>de}l</del> <b>bo*ld</b></ins>
</p>
""", xml)

    def test_term(self):
        tree = self.parse("""
Text with {{term{refersTo #foo} a term}} and {{term{refersTo #bar}  extra space}} and {{term{refersTo #baz}no space}}.
""", 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">Text with <term eId="p_1__term_1" refersTo="#foo">a term</term> and <term eId="p_1__term_2" refersTo="#bar"> extra space</term> and <term eId="p_1__term_3" refersTo="#baz">no space</term>.</p>
""", xml)

    def test_abbr(self):
        tree = self.parse("""
Text with {{abbr{title Laws.Africa} LA}} and {{abbr No Title}}.
""", 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">Text with <abbr title="Laws.Africa">LA</abbr> and <abbr title="">No Title</abbr>.</p>
""", xml)

    def test_em(self):
        """ em is syntactic sugar for inline[@name=em]
        """
        tree = self.parse("""
Text with {{em emphasized text}}.
""", 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">Text with <inline name="em">emphasized text</inline>.</p>
""", xml)

    def test_generic_inline(self):
        tree = self.parse("""
Text with {{inline{name em} some text}} and {{inline no name}}.
""", 'line')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<p xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" eId="p_1">Text with <inline name="em">some text</inline> and <inline name="inline">no name</inline>.</p>
""", xml)

    def test_inline_attrs(self):
        tree = self.parse("""
Text with {{inline.foo.bar{name em} some text}}
Class {{inline.boom but no attrs}}
Class but no text {{term.foo}}
""", 'mainBody')

        xml = self.tostring(self.to_xml(tree.to_dict()))

        self.assertEqual("""<mainBody xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <p eId="p_1">Text with <inline class="foo bar" name="em">some text</inline></p>
  <p eId="p_2">Class <inline class="boom" name="inline">but no attrs</inline></p>
  <p eId="p_3">Class but no text <term class="foo" eId="p_3__term_1" refersTo=""/></p>
</mainBody>
""", xml)
