from itertools import groupby


def many_to_dict(items):
    kids = []
    for item in items:
        if hasattr(item, 'to_dict'):
            kids.append(item.to_dict())
        elif hasattr(item, 'to_children'):
            # recurse into children directly
            kids.extend(item.to_children())
        else:
            kids.extend(many_to_dict(c for c in item.content))
    return kids


def empty_p():
    return {
        'name': 'p',
        'type': 'content',
        'children': [],
    }

# ------------------------------------------------------------------------------
# Hier elements and containers
# ------------------------------------------------------------------------------


class JudgmentBody:
    def to_dict(self):
        kids = [getattr(self, c) for c in ['introduction', 'background', 'arguments', 'remedies', 'motivation', 'decision']]

        return {
            'type': 'element',
            'name': 'judgmentBody',
            'children': [c.to_dict() for c in kids if c.text],
        }


class HierBlockIndentElement:
    name = None

    def to_dict(self):
        return {
            'type': 'element',
            'name': self.name,
            'children': many_to_dict(c.hier_block_indent for c in self.content),
        }


class BlockIndentElement:
    name = None

    def to_dict(self):
        return {
            'type': 'element',
            'name': self.name,
            'children': many_to_dict(c.block_element for c in self.content),
        }


class NestedBlockElement:
    # this class wraps nested blocks, just recurse into the children
    def to_children(self):
        return many_to_dict(self.content)


class Preface(BlockIndentElement):
    name = 'preface'


class Preamble(BlockIndentElement):
    name = 'preamble'


class Conclusions(BlockIndentElement):
    name = 'conclusions'


class Longtitle:
    # TODO: this is actually a block element
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'longTitle',
            'children': [{
                'type': 'content',
                'name': 'p',
                'children': InlineText.many_to_dict(k for k in self.content),
            }]
        }


class Crossheading:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'crossHeading',
            'children': InlineText.many_to_dict(k for k in self.content),
        }


class Body:
    def to_dict(self):
        # the body element MUST only contain hier elements at the top level
        # so group non-hier children into hcontainers
        kids = many_to_dict(c.hier_block_indent for c in self.content)
        children = []
        for is_hier, group in groupby(kids, lambda k: k['type'] == 'hier'):
            if is_hier:
                children.extend(group)
            else:
                children.append({
                    'type': 'element',
                    'name': 'hcontainer',
                    'attribs': {'name': 'hcontainer'},
                    'children': list(group),
                })

        return {
            'type': 'element',
            'name': 'body',
            'children': children,
        }


class MainBody(HierBlockIndentElement):
    name = 'mainBody'


class HierElement:
    synonyms = {
        'art': 'article',
        'chap': 'chapter',
        'para': 'paragraph',
        'sec': 'section',
        'subchap': 'subchapter',
        'subpara': 'subparagraph',
        'subsec': 'subsection',
    }

    def to_dict(self):
        name = self.hier_element_name.text.lower()
        name = self.synonyms.get(name, name)

        info = {
            'type': 'hier',
            'name': name,
            'children': many_to_dict(self.content),
        }

        if self.heading.text:
            self.heading.update_dict(info)

        if self.subheading.text:
            info['subheading'] = self.subheading.to_dict()

        return info


class HierElementHeading:
    def update_dict(self, info):
        if self.text:
            num = self.num.text.strip()
            if num:
                info['num'] = num

            heading = self.heading_to_dict()
            if heading:
                info['heading'] = heading

    def heading_to_dict(self):
        if hasattr(self.heading, 'content') and self.heading.content.text.strip():
            return InlineText.many_to_dict(x for x in self.heading.content)


class Attachments:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'attachments',
            'children': [c.to_dict() for c in self]
        }


class Attachment:
    def to_dict(self):
        if hasattr(self.indented, 'content'):
            kids = many_to_dict(c.hier_block_element for c in self.indented.content)
        else:
            kids = []

        kids.extend(many_to_dict(c.hier_block_indent for c in self.content))

        # nested attachments
        attachments = None
        if hasattr(self.indented, 'attachments') and self.indented.attachments.text:
            attachments = self.indented.attachments.to_dict()

        info = {
            'type': 'element',
            'name': 'attachment',
            'attribs': {
                'contains': 'originalVersion',
                'name': self.attachment_marker.text.lower(),
            },
            'children': [{
                'type': 'element',
                'name': 'mainBody',
                'children': kids or [empty_p()],
            }],
        }
        if attachments:
            info['children'].append(attachments)

        if self.heading.text:
            heading = self.heading.heading_to_dict()
            if heading:
                info['heading'] = heading

        if self.indented.text and self.indented.subheading.text:
            info['subheading'] = self.indented.subheading.to_dict()

        return info


class AttachmentHeading:
    def heading_to_dict(self):
        if self.content.text:
            return InlineText.many_to_dict(x for x in self.content)


class Introduction(HierBlockIndentElement):
    name = 'introduction'


class Background(HierBlockIndentElement):
    name = 'background'


class Arguments(HierBlockIndentElement):
    name = 'arguments'


class Remedies(HierBlockIndentElement):
    name = 'remedies'


class Motivation(HierBlockIndentElement):
    name = 'motivation'


class Decision(HierBlockIndentElement):
    name = 'decision'


# ------------------------------------------------------------------------------
# Block elements
# ------------------------------------------------------------------------------


class BlockList:
    def to_dict(self):
        kids = []

        if self.intro.text:
            kids.append(self.intro.to_dict())

        kids.extend(c.to_dict() for c in self.items)

        if self.wrapup.text:
            kids.append(self.wrapup.to_dict())

        info = {
            'type': 'block',
            'name': 'blockList',
            'children': kids,
        }

        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


class BlockListIntro:
    name = 'listIntroduction'

    def to_dict(self):
        info = self.line.to_dict()
        info['name'] = self.name

        if self.footnotes.elements:
            info['children'].extend(f.to_dict() for f in self.footnotes)

        return info


class BlockListWrapUp(BlockListIntro):
    name = 'listWrapUp'


class BlockListItem:
    def to_dict(self):
        kids = []

        # nested blocks
        if self.content.text and self.content.children.text:
            kids.extend(many_to_dict(self.content.children))
        else:
            kids.append(empty_p())

        info = {
            'type': 'block',
            'name': 'item',
            'children': kids,
        }

        if self.heading.text:
            self.heading.update_dict(info)

        if self.content.text and self.content.subheading.text:
            info['subheading'] = self.content.subheading.to_dict()

        return info


class BulletList:
    def to_dict(self):
        kids = [c.to_dict() for c in self.items]
        info = {
            'type': 'block',
            'name': 'ul',
            'children': kids,
        }

        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


class BulletListItem:
    def to_dict(self):
        kids = []

        if hasattr(self.initial, 'to_dict'):
            kids.append(self.initial.to_dict())

        # force an empty line if we have content, but no initial
        if not kids:
            kids.append(empty_p())

        if self.content.text:
            kids.extend(k.to_dict() for k in self.content.siblings)

        return {
            'type': 'element',
            'name': 'li',
            'children': kids,
        }


class Table:
    def to_dict(self):
        info = {
            'type': 'element',
            'name': 'table',
            'children': [r.to_dict() for r in self.rows],
        }
        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


class TableRow:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'tr',
            'children': [c.to_dict() for c in self.cells],
        }


class TableCell:
    names = {
        'TH': 'th',
        'TC': 'td',
    }

    def to_dict(self):
        if self.content.text:
            kids = many_to_dict(self.content.content)
        else:
            kids = [empty_p()]

        info = {
            'type': 'element',
            'name': self.names[self.name.text],
            'children': kids,
        }
        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


class BlockAttrs:
    def to_dict(self):
        attrs = {}

        if self.pairs.text:
            if self.pairs.first.text:
                attrs.update(self.pairs.first.to_dict())

            for el in self.pairs.rest:
                if el.attr.text:
                    attrs.update(el.attr.to_dict())

        classes = []
        if self.classes.text:
            classes = [
                cls.text[1:]
                for cls in self.classes
                # must have .foo
                if len(cls.text) > 1
            ]

        if classes:
            if 'class' in attrs:
                attrs['class'] = attrs['class'] + ' ' + ' '.join(classes)
            else:
                attrs['class'] = ' '.join(classes)

        return attrs


class BlockAttr:
    def to_dict(self):
        return {self.attr_name.text: self.value.text.strip()}


# ------------------------------------------------------------------------------
# Content elements
# ------------------------------------------------------------------------------


class Heading:
    def to_dict(self):
        return InlineText.many_to_dict(k for k in self.content)


class P:
    def to_dict(self):
        info = {
            'type': 'content',
            'name': 'p',
            'children': InlineText.many_to_dict(self.content.elements),
        }

        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


# TODO: document content and inline types
class Line:
    def to_dict(self):
        return {
            'type': 'content',
            'name': 'p',
            'children': InlineText.many_to_dict(self.content.elements),
        }


# ------------------------------------------------------------------------------
# Subflow elements
# ------------------------------------------------------------------------------


class BlockQuote:
    def to_dict(self):
        info = {
            'type': 'element',
            'name': 'embeddedStructure',
            'children': many_to_dict(self.content),
        }
        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        # embeddedStructure is an inline element, so wrap it in a block
        return {
            'type': 'element',
            'name': 'block',
            'attribs': {'name': 'quote'},
            'children': [info],
        }


class FootnoteRef:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'authorialNote',
            'attribs': {
                'marker': self.marker.text.strip(),
                'placement': 'bottom',
                # TODO: document
                'displaced': 'footnote',
            },
        }


class Footnote:
    """ This returns a non-AKN element, which is pulled into the referencing element
    during post-processing.
    """
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'displaced',
            'attribs': {
                'marker': self.marker.text.strip(),
                'name': 'footnote',
            },
            'children': many_to_dict(self.content),
        }


# ------------------------------------------------------------------------------
# Inline elements
# ------------------------------------------------------------------------------


class InlineText:
    def to_dict(self):
        if hasattr(self, 'inline_marker'):
            return self.inline_marker.to_dict()

        return {
            'type': 'text',
            'value': self.elements[0].text if self.elements else self.text,
        }

    @classmethod
    def many_to_dict(cls, items):
        """ Convert adjacent inline items, merging consecutive single characters.
        """
        merged = []
        text = []

        for item in items:
            if not hasattr(item, 'to_dict'):
                # an char escaped with a backslash is just the char
                if item.text[0] == '\\':
                    text.append(item.text[1:])
                else:
                    text.append(item.text)

            else:
                if text:
                    merged.append({
                        'type': 'text',
                        'value': ''.join(text),
                    })
                    text = []
                merged.append(item.to_dict())

        if text:
            merged.append({
                'type': 'text',
                'value': ''.join(text),
            })

        return merged


class Inline:
    name = None
    default_attribs = {}

    def to_dict(self):
        info = {
            'type': 'inline',
            'name': self.name,
            'children': InlineText.many_to_dict(x.inline_nested for x in self.content),
        }
        attribs = self.get_attribs()
        if attribs:
            info['attribs'] = attribs
        return info

    def get_attribs(self):
        return self.default_attribs


class SymmetricInline(Inline):
    name = None

    def to_dict(self):
        info = {
            'type': 'inline',
            'name': self.name,
            'children': InlineText.many_to_dict(x.inline for x in self.content),
        }
        attribs = self.get_attribs()
        if attribs:
            info['attribs'] = attribs
        return info


class Bold(SymmetricInline):
    name = 'b'


class Italics(SymmetricInline):
    name = 'i'


class Underline(SymmetricInline):
    name = 'u'


class Sup(Inline):
    name = 'sup'


class Sub(Inline):
    name = 'sub'


class Remark(Inline):
    name = 'remark'
    default_attribs = {'status': 'editorial'}

    def to_dict(self):
        kids = []
        batch = []

        def end_batch():
            kids.extend(InlineText.many_to_dict(batch))

        # The content may have newlines, which we transform into <br>, by effectively grouping
        # the content between each newline.
        content = list(self.content)
        # list.pop() removes from the end, so reverse the list
        content.reverse()
        while content:
            kid = content.pop()
            if kid.text == '\n':
                # end this batch and add a <br>
                end_batch()
                batch = []
                kids.append({
                    'type': 'element',
                    'name': 'br'
                })
            else:
                batch.append(kid.content)

        if batch:
            end_batch()

        info = {
            'type': 'inline',
            'name': self.name,
            'children': kids
        }
        attribs = self.get_attribs()
        if attribs:
            info['attribs'] = attribs
        return info


class Ref(Inline):
    name = 'ref'

    def get_attribs(self):
        return {
            'href': self.href.text,
        }


class Image:
    def to_dict(self):
        attribs = {'src': self.href.text}
        if self.content.text:
            attribs['alt'] = self.content.text.strip()

        return {
            'type': 'marker',
            'name': 'img',
            'attribs': attribs,
        }


class StandardInline(Inline):
    """ Standard inline used for many different types of inlines.
    """
    default_attribs = {
        'abbr': {'title': ''},
        'term': {'refersTo': ''},
        'inline': {'name': 'inline'},
    }

    @property
    def name(self):
        return self.tag.text

    def to_dict(self):
        info = super().to_dict()

        # em is syntactic sugar for <inline name="em">
        if self.name == 'em':
            info['name'] = 'inline'
            info.setdefault('attribs', {})['name'] = 'em'

        # + is syntactic sugar for <ins>
        elif self.name == '+':
            info['name'] = 'ins'

        # - is syntactic sugar for <del>
        elif self.name == '-':
            info['name'] = 'del'

        return info

    def get_attribs(self):
        attribs = self.attrs.to_dict() if self.attrs.text else {}
        # set default attributes for this inline
        for attr, val in self.default_attribs.get(self.name, {}).items():
            attribs.setdefault(attr, val)
        return attribs


# ------------------------------------------------------------------------------
# Top-level documents
# ------------------------------------------------------------------------------


class DocumentRoot:
    name = None
    is_root = True
    children = []
    required_children = set()

    def add_empty_required(self, kids, tag):
        kids.append({
            'type': 'element',
            'name': tag,
        })
        return kids

    def to_dict(self):
        kids = []
        for tag in self.children:
            node = getattr(self, tag, None)
            if node and node.text:
                kids.append(node.to_dict())
            elif tag in self.required_children:
                kids = self.add_empty_required(kids, tag)

        return {
            'type': 'element',
            'name': self.name,
            'attribs': {'name': self.name},
            'children': kids,
        }


class HierarchicalStructure(DocumentRoot):
    children = ['preface', 'preamble', 'body', 'conclusions', 'attachments']
    name = 'hierarchicalStructure'


class Act(HierarchicalStructure):
    name = 'act'


class Bill(HierarchicalStructure):
    name = 'bill'


class Judgment(DocumentRoot):
    children = ['header', 'judgment_body', 'conclusions', 'attachments']
    required_children = ['header']
    name = 'judgment'


class OpenStructure(DocumentRoot):
    children = ['preface', 'preamble', 'main_body', 'conclusions', 'attachments']
    name = 'openStructure'
    required_children = {'main_body'}

    def add_empty_required(self, kids, tag):
        if tag == 'main_body':
            kids.append({
                'type': 'element',
                'name': 'mainBody',
                'children': [empty_p()],
            })
            return kids
        return super().add_empty_required(kids, tag)


class Statement(OpenStructure):
    name = 'statement'


class Doc(OpenStructure):
    name = 'doc'


class DebateReport(OpenStructure):
    name = 'debateReport'
