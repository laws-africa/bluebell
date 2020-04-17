from lxml.builder import ElementMaker

E = ElementMaker(nsmap={None: 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'})

# TODO: block lists
# TODO: nested block lists
# TODO: arbitrary indents
# TODO: schedules and annexures - how to "push" to end?
# TODO: tables


def hoist_blocks(children):
    """ Block elements can use this to pull grandchildren of anonymous block
        elements into their child list.

        So this:
            block -> block -> block
        becomes:
            block -> block
    """
    kids = []

    for kid in children:
        if kid['type'] == 'block' and kid['name'] == 'block':
            kids.extend(c for c in kid.get('children', []))
        else:
            kids.append(kid)

    return kids


def kids_to_xml(parent=None, kids=None):
    if kids is None:
        kids = parent.get('children', [])
    return [to_xml(k) for k in kids]


def to_xml(item):
    if item['type'] == 'preface':
        # preface is already a block, so hoist in any block children
        kids = hoist_blocks(item.get('children', []))
        return E('preface', *kids_to_xml(kids=kids))

    if item['type'] == 'hier':
        pre = []
        kids = kids_to_xml(item)

        # by default, if all children are hier elements, we add them as-is
        # if no hierarchy children (ie. all block/content), wrap children in <content>
        if all(k['type'] != 'hier' for k in item['children']):
            kids = [E.content(*kids)]

        if item.get('num'):
            pre.append(E.num(item['num']))

        if item.get('heading'):
            pre.append(E.heading(*(to_xml(k) for k in item['heading'])))

        if item.get('subheading'):
            pre.append(E.subheading(*(to_xml(k) for k in item['subheading'])))

        kids = pre + kids

        return E(item['name'], *kids, **item.get('attribs', {}))

        # if block/content at start and end, use intro and wrapup
        # TODO

        # otherwise, panic
        # TODO

    if item['type'] == 'block':
        # TODO: can have num, heading, subheading
        # TODO: make this generic? what else can have num?
        kids = kids_to_xml(item)
        if 'num' in item:
            kids.insert(0, E('num', item['num']))
        return E(item['name'], *kids)

    if item['type'] == 'content':
        return E(item['name'], *kids_to_xml(item))

    if item['type'] == 'inline':
        return E(item['name'], *kids_to_xml(item), **item.get('attribs', {}))

    if item['type'] == 'marker':
        return E(item['name'], **item.get('attribs', {}))

    if item['type'] == 'text':
        return item['value']

    if item['type'] == 'element':
        return E(item['name'], *kids_to_xml(item))


class Judgment:
    def to_xml(self, tree):
        return E.akomaNtoso(
            E.judgment(
                E.meta(),
                *to_xml(tree),
            ),
        )


class Act:
    def to_xml(self, tree):
        items = []
        if 'preface' in tree:
            items.append(to_xml(tree['preface']))
        items.append(to_xml(tree['body']))

        return E.akomaNtoso(
            E.act(
                E.meta(),
                *items,
            ),
        )
