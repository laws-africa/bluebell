from unittest import TestCase

from .support import ParserSupport


class EscapesTestCase(ParserSupport, TestCase):
    maxDiff = None

    def test_ignore_escaped_blocks(self):
        # Remember, in the strings below a double backslash is actually a
        # single backslash because python requires us to backslash a backslash
        tree = self.parse("""
PART
  \\LONGTITLE
  \\SUBHEADING aoeu
  foo \\bar
  foo \\**bar**
  \\CROSSHEADING foo
  \\TABLE
  \\
  \\\\
  \\SECTION 1
""", 'hier_element_block')

        self.assertEqual({
            'name': 'part',
            'type': 'hier',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'LONGTITLE',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'SUBHEADING aoeu',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo bar',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo *',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': 'bar',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': '*',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'CROSSHEADING foo',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'TABLE',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': '\\'
                }],
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': '\\'
                }],
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'SECTION 1'
                }],
            }]
        }, tree.to_dict())

    def test_ignore_escaped_at_top_level(self):
        tree = self.parse("""
\\h\\e\\l\\lo
""", 'hierarchical_structure')

        self.assertEqual({
            'type': 'element',
            'name': 'hierarchicalStructure',
            'attribs': {'name': 'hierarchicalStructure'},
            'children': [{
                'type': 'element',
                'name': 'body',
                'children': [{
                    'type': 'element',
                    'name': 'hcontainer',
                    'attribs': {'name': 'hcontainer'},
                    'children': [{
                        'type': 'element',
                        'name': 'content',
                        'children': [{
                            'type': 'content',
                            'name': 'p',
                            'children': [{
                                'type': 'text',
                                'value': 'hello'
                            }]
                        }]
                    }]
                }]
            }]
        }, tree.to_dict())

    def test_ignore_escaped_inlines(self):
        # Remember, in the strings below a double backslash is actually a
        # single backslash because python requires us to backslash a backslash
        tree = self.parse("""
PART
  foo \\**bar**
  foo **bar\\**
  some \\{{^non-sup}}
  some {{^sup\\}}}
  a \\{{*remark}}
""", 'hier_element_block')

        self.assertEqual({
            'name': 'part',
            'type': 'hier',
            'children': [{
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo *',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': 'bar',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': '*',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'foo ',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': '*',
                }, {
                    'type': 'text',
                    'value': 'bar*',
                }, {
                    'type': 'text',
                    'value': '*',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some {',
                }, {
                    'type': 'text',
                    'value': '{',
                }, {
                    'type': 'text',
                    'value': '^non-sup}}',
                }]
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'some '
                }, {
                    'type': 'inline',
                    'name': 'sup',
                    'children': [{
                        'type': 'text',
                        'value': 'sup}'
                    }]
                }],
            }, {
                'name': 'p',
                'type': 'content',
                'children': [{
                    'type': 'text',
                    'value': 'a {'
                }, {
                    'type': 'text',
                    'value': '{'
                }, {
                    'type': 'text',
                    'value': '*'
                }, {
                    'type': 'text',
                    'value': 'remark}}'
                }]
            }]
        }, tree.to_dict())

    def test_unescape(self):
        xml = """<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <num>1</num>
  <heading>HEADING ** with stars</heading>
  <content>
    <p><b>bold with * and **</b> and <b>**</b></p>
    <p><i>italics // with //</i> and <i>//foo//</i></p>
    <p><sup>sup with }}</sup>}}</p>
    <p><img src="/foo" /></p>
    <p><ref href="/bar">link</ref></p>
    <p>foo ** <b>**</b> <ref href="#foo">// **</ref> ** //</p>
    <p>   PART 1</p>
    <p>   ITEMS</p>
    <p>It is hereby certified that ________________<u>_ of P.O. Box </u>_______ and ID No. _____<u>_ TSC No.</u>_________ having met</p>
    <p>from <u>_ /</u>_<u>_ /</u> [dd/mm/yyyy].</p>
    <p>*<b>*Notice</b>s**</p>
  </content>
</section>"""
        actual = self.parser.unparse(xml)
        self.assertEqual("""SEC 1 - HEADING \\*\\* with stars

  **bold with * and \\*\\*** and **\\*\\***

  //italics \\/\\/ with \\/\\/// and //\\/\\/foo\\/\\///

  {{^sup with \}\}}}\}\}

  {{IMG /foo}}

  {{>/bar link}}

  foo \\*\\* **\\*\\*** {{>#foo \\/\\/ \\*\\*}} \\*\\* \\/\\/

  \PART 1

  \ITEMS

  It is hereby certified that \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\___\_ of P.O. Box __\_\_\_\_\_\_\_ and ID No. \_\_\_\_\___\_ TSC No.__\_\_\_\_\_\_\_\_\_ having met

  from __\_ /__\___\_ /__ [dd/mm/yyyy].

  \***\*Notice**s\*\*

""", actual)

    def test_unescape2(self):
        xml = """<section xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <num>1</num>
  <heading>HEADING ** with stars</heading>
  <content>
    <p>*<b>odd bold before</b></p>
    <p>***<b>odd bold before</b></p>
    <p>****<b>even bold before</b></p>
    <p><b>odd bold after</b>*</p>
    <p><b>odd bold after</b>***</p>
    <p><b>even bold after</b>****</p>
    <p><b>***odd bold before</b></p>
    <p><b>****even bold before</b></p>
    <p><b>odd bold after***</b></p>
    <p><b>even bold after****</b></p>
    <p>foo<b>*bold*</b>bar</p>
    <p>one<b>*</b>odd middle</p>
  </content>
</section>"""
        actual = self.parser.unparse(xml)
        self.assertEqual("""SEC 1 - HEADING \\*\\* with stars

  \***odd bold before**

  \*\*\***odd bold before**

  \*\*\*\***even bold before**

  **odd bold after**\*

  **odd bold after**\*\*\*

  **even bold after**\*\*\*\*

  **\*\*\*odd bold before**

  **\*\*\*\*even bold before**

  **odd bold after\*\*\***

  **even bold after\*\*\*\***

  foo**\*bold\***bar

  one**\***odd middle

""", actual)
