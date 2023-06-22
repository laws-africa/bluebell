import re
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


def empty_hcontainer():
    return {
        'type': 'element',
        'name': 'hcontainer',
        'attribs': {'name': 'hcontainer'},
        'children': [{
            'type': 'element',
            'name': 'content',
            'children': [empty_p()],
        }]
    }


ESCAPE_RE = re.compile(r'\\(.)')


def unescape(s):
    return ESCAPE_RE.sub('\\1', s)

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


class NestedAltBlockElement(NestedBlockElement):
    pass


class Preface(BlockIndentElement):
    name = 'preface'


class Preamble(BlockIndentElement):
    name = 'preamble'


class Conclusions(BlockIndentElement):
    name = 'conclusions'


class Longtitle:
    def to_dict(self):
        if self.body.text:
            kids = [{
                'type': 'content',
                'name': 'p',
                'children': InlineText.many_to_dict(k for k in self.body.content),
            }]
        else:
            # longtitles may be empty
            kids = []

        return {
            'type': 'element',
            'name': 'longTitle',
            'children': kids,
        }


class Crossheading:
    def to_dict(self):
        # crossheadings may be empty
        if self.body.text:
            kids = InlineText.many_to_dict(k for k in self.body.content)
        else:
            kids = []

        return {
            'type': 'element',
            'name': 'crossHeading',
            'children': kids
        }


class MainContentElement:
    """ Top-level main content container. Named to match the maincontenttype in the AKN schema.

    Used here for <body>, <mainBody>, and <mainBody>'s equivalents such as <background>.
    """
    name = None
    content_element = 'hier_block_indent'

    def empty(self):
        return empty_p()

    def classify(self, item):
        # only crossheadings are special for mainBody and friends
        if item['name'] == 'crossHeading':
            return 'crossHeading'

    def wrap_children(self, kids):
        """ Adjust kids, taking into account that crossHeading must be wrapped at the top level.
        """
        children = []
        for class_, group in groupby(kids, self.classify):
            if class_ == 'crossHeading':
                # crossHeading can't be a direct child of mainBody (even though it can be a peer of hier elements later)
                # so we wrap it in an hcontainer here
                children.append({
                    'type': 'element',
                    'name': 'hcontainer',
                    'attribs': {'name': 'hcontainer'},
                    'children': list(group),
                })

            elif class_ == 'content':
                # wrap top-level content in hcontainer
                children.append({
                    'type': 'element',
                    'name': 'hcontainer',
                    'attribs': {'name': 'hcontainer'},
                    'children': [{
                        'type': 'element',
                        'name': 'content',
                        'children': list(group),
                    }]
                })

            else:
                # don't change it
                children.extend(list(group))

        return children

    def to_dict(self):
        kids = many_to_dict(getattr(c, self.content_element) for c in self.content)
        kids = self.wrap_children(kids)
        return {
            'type': 'element',
            'name': self.name,
            'children': kids or [self.empty()]
        }


class Body(MainContentElement):
    name = 'body'

    def empty(self):
        return empty_hcontainer()

    def classify(self, item):
        # for body, crossHeading and content must both be wrapped
        if item['type'] == 'hier':
            return 'hier'
        if item['name'] == 'crossHeading':
            return 'crossHeading'
        return 'content'


class HierElement:
    type = 'hier'
    name_element = 'hier_element_name'
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
        name = getattr(self, self.name_element).text.lower()
        name = self.synonyms.get(name, name)
        if self.body.text:
            kids = many_to_dict(self.body.content)
        else:
            kids = []

        info = {
            'type': self.type,
            'name': name,
            'children': kids,
        }

        if self.heading.text:
            self.heading.update_dict(info)

        if self.body.text and self.body.subheading.text:
            info['subheading'] = self.body.subheading.to_dict()

        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


class HierElementHeading:
    def update_dict(self, info):
        if self.text:
            if hasattr(self.num, 'content'):
                num = unescape(self.num.content.text)
                if num:
                    info['num'] = num

            heading = self.heading_to_dict()
            if heading:
                info['heading'] = heading

    def heading_to_dict(self):
        if hasattr(self.heading, 'heading_content') and self.heading.heading_content.text:
            return InlineText.many_to_dict(x for x in self.heading.heading_content.content)


class SpeechContainer(HierElement):
    type = 'speechhier'
    name_element = 'speech_container_name'
    synonyms = {
        'administrationofoath': 'administrationOfOath',
        'debatesection': 'debateSection',
        'declarationofvote': 'declarationOfVote',
        'ministerialstatements': 'ministerialStatements',
        'noticesofmotion': 'noticesOfMotion',
        'oralstatements': 'oralStatements',
        'personalstatements': 'personalStatements',
        'pointoforder': 'pointOfOrder',
        'proceduralmotions': 'proceduralMotions',
        'rollcall': 'rollCall',
        'writtenstatements': 'writtenStatements',
    }

    def to_dict(self):
        info = super().to_dict()
        if info['name'] == 'debateSection':
            if 'name' not in info.get('attribs', {}):
                info.setdefault('attribs', {})['name'] = 'debateSection'
        return info


class SpeechGroup(SpeechContainer):
    name_element = 'speech_group_name'
    non_letters_re = re.compile(r'[\W]', re.UNICODE)

    def to_dict(self):
        info = super().to_dict()
        info['from'] = self.body.speech_from.to_dict()
        if 'by' not in info.get('attribs', {}):
            info.setdefault('attribs', {})['by'] = self.make_by()

        return info

    def make_by(self):
        return '#' + self.non_letters_re.sub('', self.body.speech_from.text)


class Attachments:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'attachments',
            'children': [c.to_dict() for c in self]
        }


class Attachment(MainContentElement):
    def to_dict(self):
        if hasattr(self.indented, 'content'):
            kids = many_to_dict(c.hier_block_element for c in self.indented.content)
        else:
            kids = []

        kids.extend(many_to_dict(c.hier_block_indent for c in self.content))
        kids = self.wrap_children(kids)

        # nested attachments
        attachments = None
        if hasattr(self.indented, 'attachments') and self.indented.attachments.text:
            attachments = self.indented.attachments.to_dict()

        info = {
            'type': 'element',
            'name': 'attachment',
            'attribs': {
                'name': self.attachment_marker.text.lower(),
            },
            'children': [{
                'type': 'element',
                'name': 'mainBody',
                'children': kids or [self.empty()]
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


class MainBody(MainContentElement):
    name = 'mainBody'


class Introduction(MainContentElement):
    name = 'introduction'


class Background(MainContentElement):
    name = 'background'


class Arguments(MainContentElement):
    name = 'arguments'


class Remedies(MainContentElement):
    name = 'remedies'


class Motivation(MainContentElement):
    name = 'motivation'


class Decision(MainContentElement):
    name = 'decision'


class DebateBody(MainContentElement):
    name = 'debateBody'
    content_element = 'speech_container_indent'


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
            for kid in self.content.siblings:
                if hasattr(kid, 'to_dict'):
                    kids.append(kid.to_dict())
                else:
                    kids.extend(kid.to_children())

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


class Subheading:
    def to_dict(self):
        if self.body.text:
            return InlineText.many_to_dict(k for k in self.body.content)
        else:
            return []


class From:
    def to_dict(self):
        return InlineText.many_to_dict(k for k in self.content)


class SpeechBlock:
    def to_dict(self):
        info = {
            'type': 'element',
            'name': self.speech_block_name.text.lower(),
            'children': InlineText.many_to_dict(self.content.elements),
        }

        if self.attrs.text:
            info['attribs'] = self.attrs.to_dict()

        return info


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

    def make_empty(self, tag):
        return {
            'type': 'element',
            'name': tag,
        }

    def add_empty_required(self, kids, tag):
        maker = getattr(self, f'make_empty_{tag}', self.make_empty)
        kids.append(maker(tag))
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
    required_children = {'body'}
    name = 'hierarchicalStructure'

    def make_empty_body(self, tag):
        return {
            'type': 'element',
            'name': tag,
            'children': [empty_hcontainer()],
        }


class Act(HierarchicalStructure):
    name = 'act'


class Bill(HierarchicalStructure):
    name = 'bill'


class Judgment(DocumentRoot):
    children = ['header', 'judgmentBody', 'conclusions', 'attachments']
    required_children = {'header', 'judgmentBody'}
    name = 'judgment'

    def make_empty_judgmentBody(self, tag):
        return {
            'type': 'element',
            'name': tag,
            'children': [{
                'type': 'element',
                'name': 'introduction',
                'children': [empty_p()],
            }]
        }


class OpenStructure(DocumentRoot):
    children = ['preface', 'preamble', 'mainBody', 'conclusions', 'attachments']
    name = 'openStructure'
    required_children = {'mainBody'}

    def make_empty_mainBody(self, tag):
        return {
            'type': 'element',
            'name': tag,
            'children': [empty_p()],
        }


class Statement(OpenStructure):
    name = 'statement'


class Doc(OpenStructure):
    name = 'doc'


class DebateReport(OpenStructure):
    name = 'debateReport'


class DebateStructure(DocumentRoot):
    children = ['preface', 'debateBody', 'conclusions', 'attachments']
    name = 'debateStructure'
    required_children = {'debateBody'}

    def make_empty_debateBody(self, tag):
        return {
            'type': 'element',
            'name': tag,
            'children': [{
                'type': 'element',
                'name': 'debateSection',
                'attribs': {'name': 'debateSection'},
                'children': [empty_p()]
            }]
        }


class Debate(DebateStructure):
    name = 'debate'
