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
            num = self.heading.num.text.strip()
            if num:
                info['num'] = num

            heading = self.heading.heading_to_dict()
            if heading:
                info['heading'] = heading

        if self.subheading.text:
            info['subheading'] = self.subheading.to_dict()

        return info


class HierElementHeading:
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
        if self.indented.text:
            kids = many_to_dict(self.indented.content)
        else:
            kids = []

        kids.extend(many_to_dict(c.hier_block_indent for c in self.content))

        info = {
            'type': 'element',
            'name': 'attachment',
            'attribs': {
                'contains': 'originalVersion',
                'name': self.attachment_marker.text.lower(),
            },
            'children': kids,
        }

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
        return {
            'type': 'block',
            'name': 'blockList',
            'children': [c.to_dict() for c in self],
        }


class BlockItem:
    def to_dict(self):
        kids = []

        # preamble content on the same line as the number
        if self.preamble.text and hasattr(self.preamble, 'block_elements'):
            kids.append(self.preamble.block_elements.to_dict())

        # nested blocks
        if self.children.text:
            kids.extend(many_to_dict(self.children.content))

        return {
            'type': 'block',
            'name': 'item',
            'num': self.num.text,
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
            kids = [{
                'type': 'content',
                'name': 'p',
                'children': [],
            }]

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

        if self.first.text:
            attrs.update(self.first.to_dict())

        for el in self.rest:
            if el.attr.text:
                attrs.update(el.attr.to_dict())

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


class EmbeddedStructure:
    def to_dict(self):
        info = {
            'type': 'element',
            'name': 'embeddedStructure',
            'children': many_to_dict(self.content),
        }
        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


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

    def to_dict(self):
        return {
            'type': 'inline',
            'name': self.name,
            'children': InlineText.many_to_dict(x.inline_nested for x in self.content),
        }


class SymmetricInline:
    name = None

    def to_dict(self):
        return {
            'type': 'inline',
            'name': self.name,
            'children': InlineText.many_to_dict(x.inline for x in self.content),
        }


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

    def to_dict(self):
        d = super().to_dict()
        d['attribs'] = {'status': 'editorial'}

        # add [
        if d['children'] and d['children'][0]['type'] == 'text':
            d['children'][0]['value'] = '[' + d['children'][0]['value']
        else:
            d['children'].insert(0, {'type': 'text', 'value': '['})

        # add ]
        if d['children'][-1]['type'] == 'text':
            d['children'][-1]['value'] = d['children'][-1]['value'] + ']'
        else:
            d['children'].append({'type': 'text', 'value': ']'})

        return d


class Ref:
    def to_dict(self):
        return {
            'type': 'inline',
            'name': 'ref',
            'attribs': {
                'href': self.href.text,
            },
            'children': InlineText.many_to_dict(x.inline_nested for x in self.content),
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


# ------------------------------------------------------------------------------
# Top-level documents
# ------------------------------------------------------------------------------


class DocumentRoot:
    name = None
    is_root = True
    children = []

    def to_dict(self):
        kids = []
        for tag in self.children:
            node = getattr(self, tag, None)
            if node and node.text:
                kids.append(node.to_dict())

        return {
            'type': 'element',
            'name': self.name,
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
    name = 'judgment'


class OpenStructure(DocumentRoot):
    children = ['preface', 'preamble', 'main_body', 'conclusions', 'attachments']
    name = 'openStructure'


class Statement(OpenStructure):
    name = 'statement'


class Doc(OpenStructure):
    name = 'doc'


class DebateReport(OpenStructure):
    name = 'debateReport'
