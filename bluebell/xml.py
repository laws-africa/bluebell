import re

from lxml.builder import ElementMaker

E = ElementMaker(nsmap={None: 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'})


class IdGenerator:
    counters = {}
    num_strip_re = re.compile('[ .()[\]]')
    num_exempt = ['body', 'preface']

    aliases = {
        'alinea': 'al',
        'amendmentBody': 'body',
        'article': 'art',
        'attachment': 'att',
        'blockList': 'list',
        'chapter': 'chp',
        'citation': 'cit',
        'citations': 'cits',
        'clause': 'cl',
        'component': 'cmp',
        'components': 'cmpnts',
        'componentRef': 'cref',
        'debateBody': 'body',
        'debateSection': 'dbsect',
        'division': 'dvs',
        'documentRef': 'dref',
        'eventRef': 'eref',
        'judgmentBody': 'body',
        'intro': 'intro',
        'list': 'list',
        'listIntroduction': 'intro',
        'listWrapUp': 'wrap',
        'mainBody': 'body',
        'paragraph': 'para',
        'quotedStructure': 'qstr',
        'quotedText': 'qtext',
        'recital': 'rec',
        'recitals': 'recs',
        'section': 'sec',
        'subchapter': 'subchp',
        'subclause': 'subcl',
        'subdivision': 'subdvs',
        'subparagraph': 'subpara',
        'subsection': 'subsec',
        'temporalGroup': 'tmpg',
        'wrapUp': 'wrapup',
    }

    def incr(self, prefix, name):
        sub = self.counters.setdefault(prefix, {})
        sub[name] = sub.get(name, 0) + 1
        return sub[name]

    def make(self, prefix, item=None, name=None):
        # TODO: should some tags (like body, etc.) have ids?
        item = item or {}
        if prefix:
            eid = prefix + '__'
        else:
            eid = ''

        name = name or item['name']
        eid = eid + self.aliases.get(name, name)

        if self.needs_num(name):
            if item.get('num'):
                num = self.clean_num(item.get('num'))
            else:
                num = self.incr(prefix, name)

            if num:
                eid = f'{eid}_{num}'

        return eid

    def clear(self):
        self.counters.clear()

    def needs_num(self, name):
        return name not in self.num_exempt

    def clean_num(self, num):
        return self.num_strip_re.sub('', num)


ids = IdGenerator()

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


def kids_to_xml(parent=None, kids=None, prefix=None):
    if kids is None:
        kids = parent.get('children', [])
    return [to_xml(k, prefix) for k in kids]


def to_xml(item, prefix=''):
    if item['type'] == 'preface':
        # preface is already a block, so hoist in any block children
        kids = hoist_blocks(item.get('children', []))
        eid = ids.make(prefix, name='preface')
        return E('preface', eId=eid, *kids_to_xml(kids=kids, prefix=eid))

    if item['type'] == 'hier':
        eid = ids.make(prefix, item)
        kids = kids_to_xml(item, prefix=eid)
        pre = []

        # by default, if all children are hier elements, we add them as-is
        # if no hierarchy children (ie. all block/content), wrap children in <content>
        if all(k['type'] != 'hier' for k in item['children']):
            kids = [E.content(*kids)]

        if item.get('num'):
            pre.append(E.num(item['num']))

        if item.get('heading'):
            pre.append(E.heading(*(to_xml(k, eid) for k in item['heading'])))

        if item.get('subheading'):
            pre.append(E.subheading(*(to_xml(k, eid) for k in item['subheading'])))

        kids = pre + kids

        return E(item['name'], *kids, eId=eid, **item.get('attribs', {}))

        # if block/content at start and end, use intro and wrapup
        # TODO

        # otherwise, panic
        # TODO

    if item['type'] == 'block':
        # TODO: can have num, heading, subheading
        # TODO: make this generic? what else can have num?
        eid = ids.make(prefix, item)
        kids = kids_to_xml(item, prefix=eid)
        if 'num' in item:
            kids.insert(0, E('num', item['num']))
        return E(item['name'], eId=eid, *kids)

    if item['type'] == 'content':
        return E(item['name'], *kids_to_xml(item, prefix=prefix))

    if item['type'] == 'inline':
        # TODO: should these have ids?
        return E(item['name'], *kids_to_xml(item, prefix=prefix), **item.get('attribs', {}))

    if item['type'] == 'marker':
        # TODO: should these have ids?
        return E(item['name'], **item.get('attribs', {}))

    if item['type'] == 'text':
        return item['value']

    if item['type'] == 'element':
        eid = ids.make(prefix, item)
        return E(item['name'], eId=eid, *kids_to_xml(item, prefix=eid))


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