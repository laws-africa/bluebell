# ------------------------------------------------------------------------------
# Judgement
# ------------------------------------------------------------------------------


class Judgment:
    xml = 'Judgment'

    def to_dict(self):
        kids = [{
            'type': 'element',
            'name': 'judgmentBody',
            'children': [c.to_dict() for c in self.judgment_body if c.text],
        }]

        if self.conclusions.text:
            kids.append(self.conclusions.to_dict())

        return {
            'type': 'element',
            'name': 'judgment',
            'children': kids,
        }


class Introduction:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'introduction',
            'children': many_to_dict(c.hier_block_indent for c in self.content),
        }


class Background:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'background',
            'children': many_to_dict(c.hier_block_indent for c in self.content),
        }


class Arguments:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'arguments',
            'children': many_to_dict(c.hier_block_indent for c in self.content),
        }


class Remedies:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'remedies',
            'children': many_to_dict(c.hier_block_indent for c in self.content),
        }


class Motivation:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'motivation',
            'children': many_to_dict(c.hier_block_indent for c in self.content),
        }


class Decision:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'decision',
            'children': many_to_dict(c.hier_block_indent for c in self.content),
        }


class Conclusions:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'conclusions',
            'children': many_to_dict(self.content),
        }

# ------------------------------------------------------------------------------
# Hierarchical structures (act, bill)
# ------------------------------------------------------------------------------


class Act:
    xml = 'Act'


class HierarchicalStructure:
    def to_dict(self):
        info = {
            'type': 'hierarchicalStructure',
            'body': self.body.to_dict(),
        }

        if self.preface.text:
            info['preface'] = self.preface.to_dict()

        if self.preamble.text:
            info['preamble'] = self.preamble.to_dict()

        if self.conclusions.text:
            info['conclusions'] = self.conclusions.to_dict()

        return info


class Preface:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'preface',
            'children': many_to_dict(c.block_indent for c in self.content),
        }


class Preamble:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'preamble',
            'children': many_to_dict(c.block_indent for c in self.content),
        }


class Longtitle:
    # TODO: this is actually a block element
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'longTitle',
            'children': [{
                'type': 'content',
                'name': 'p',
                'children': Inline.many_to_dict(k for k in self.content),
            }]
        }


class Body:
    def to_dict(self):
        return {
            'type': 'element',
            'name': 'body',
            'children': [c.elements[1].to_dict() for c in self.content]
        }


class HierElement:
    def to_dict(self):
        info = {
            'type': 'hier',
            'name': self.hier_element_name.text.lower(),
            'children': [c.elements[1].to_dict() for c in self.content]
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
            return Inline.many_to_dict(x for x in self.heading.content)


class Heading:
    def to_dict(self):
        return Inline.many_to_dict(k for k in self.content)


class Block:
    def to_dict(self):
        # if we have one child, it's a block element and we're only a wrapper,
        # return it directly
        if len(self.content.elements) == 1:
            return self.content.elements[0].to_dict()

        # TODO: name and attribs for arbitrary indented block
        return {
            'type': 'block',
            # TODO: name? the block is essentially anonymous?
            # what about arbitrary indented text?
            'name': 'block',
            'children': [c.to_dict() for c in self.content]
        }


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
        if self.preamble.text and hasattr(self.preamble, 'block_element'):
            kids.append(self.preamble.block_element)

        # nested blocks
        if self.content.text:
            kids.extend(self.content.content)

        return {
            'type': 'block',
            'name': 'item',
            'num': self.num.text,
            'children': [c.to_dict() for c in kids],
        }


class Table:
    def to_dict(self):
        return {
            'type': 'block',
            'name': 'table',
        }


# TODO: document content and inline types
class Line:
    def to_dict(self):
        return {
            'type': 'content',
            'name': 'p',
            'children': Inline.many_to_dict(self.content.elements),
        }


class Ref:
    def to_dict(self):
        return {
            'type': 'inline',
            'name': 'ref',
            'attribs': {
                'href': self.href.text,
            },
            'children': [{
                'type': 'text',
                'value': self.content.text,
            }],
        }


class Remark:
    def to_dict(self):
        return {
            'type': 'inline',
            'name': 'remark',
            'attribs': {'status': 'editorial'},
            'children': Inline.many_to_dict(x.inline for x in self.content.elements),
        }


class Image:
    def to_dict(self):
        attribs = {'src': self.href.text}
        if self.content.text:
            attribs['alt'] = self.content.text

        return {
            'type': 'marker',
            'name': 'img',
            'attribs': attribs,
        }


class Bold:
    def to_dict(self):
        return {
            'type': 'inline',
            'name': 'b',
            'children': Inline.many_to_dict(x.inline for x in self.content.elements),
        }


class Italics:
    def to_dict(self):
        return {
            'type': 'inline',
            'name': 'i',
            'children': Inline.many_to_dict(x.inline for x in self.content.elements),
        }


class Inline:
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


def many_to_dict(items):
    kids = []
    for item in items:
        if hasattr(item, 'to_dict'):
            kids.append(item.to_dict())
        else:
            kids.extend(c.to_dict() for c in item.content)
    return kids


