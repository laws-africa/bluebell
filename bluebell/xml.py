import re
from itertools import groupby

from lxml.builder import ElementMaker
import lxml.etree as ET

AKN3_NAMESPACE = 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'

E = ElementMaker(nsmap={None: AKN3_NAMESPACE})


class IdGenerator:
    counters = {}
    num_strip_re = re.compile(r'[ .()[\]]')

    id_exempt = set("act amendment amendmentList bill debate debateReport doc documentCollection judgment"
                    " officialGazette portion statement body mainBody".split())
    """ Top-level document types that never have ids. """

    id_unnecessary = set("arguments background conclusions decision header introduction motivation preamble preface"
                         " remedies".split())
    """ Elements for which an id is optional. """

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

    def is_exempt(self, prefix, item):
        """ Is this element completely exempt from having an eId?
        """
        return item['name'] in self.id_exempt

    def is_unnecessary(self, prefix, item):
        """ Certain top-level elements only need ids if they're embedded and therefore have a prefix.
        """
        return item['name'] in self.id_unnecessary and not prefix

    def make(self, prefix, item):
        if self.is_exempt(prefix, item):
            return None

        item = item or {}
        if prefix:
            eid = prefix + '__'
        else:
            eid = ''

        name = item['name']
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
        return name not in self.id_unnecessary

    def clean_num(self, num):
        return self.num_strip_re.sub('', num)


ids = IdGenerator()


def kids_to_xml(parent=None, kids=None, prefix=None):
    if kids is None:
        kids = parent.get('children', [])
    return [to_xml(k, prefix) for k in kids]


def to_xml(item, prefix=''):
    if item['type'] == 'hier':
        eid = ids.make(prefix, item)
        pre = []

        if all(k['type'] != 'hier' for k in item['children']):
            # no hierarchy children (ie. all block/content), wrap children in <content>
            kids = kids_to_xml(item, prefix=eid)
            kids = [E.content(*kids)]
        else:
            # potentially mixed children
            # group non-hier children into <intro> and <wrapUp> with hier children sandwiched
            # in the middle
            kids = []
            seen_hier = False
            for is_hier, group in groupby(item['children'], lambda x: x['type'] == 'hier' or x['name'] == 'crossHeading'):
                group = (to_xml(k, eid) for k in group)
                if is_hier:
                    # TODO: what if this hier element is after a wrapUp?
                    seen_hier = True
                    kids.extend(group)
                elif seen_hier:
                    kids.append(E.wrapUp(*group))
                else:
                    kids.append(E.intro(*group))

        if item.get('num'):
            pre.append(E.num(item['num']))

        if item.get('heading'):
            pre.append(E.heading(*(to_xml(k, eid) for k in item['heading'])))

        if item.get('subheading'):
            pre.append(E.subheading(*(to_xml(k, eid) for k in item['subheading'])))

        kids = pre + kids
        return E(item['name'], *kids, eId=eid, **item.get('attribs', {}))

    if item['type'] == 'block':
        # TODO: can have num, heading, subheading
        # TODO: make this generic? what else can have num?
        eid = ids.make(prefix, item)
        kids = kids_to_xml(item, prefix=eid)
        if not kids:
            # block elements must have at least one content child
            kids = [E.p()]

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
        attrs = {}
        eid = ids.make(prefix, item)
        if eid and not ids.is_unnecessary(prefix, item):
            attrs['eId'] = eid
        return E(item['name'], *kids_to_xml(item, prefix=eid), **attrs)


class Document:
    def make_xml(self, tree):
        # TODO: empty ARGUMENTS, REMEDIES etc. should be excluded
        return E.akomaNtoso(to_xml(tree))

    def meta(self):
        return ET.fromstring(ET.tostring(E.meta()))

    def to_xml(self, tree):
        tree = ET.fromstring(ET.tostring(self.make_xml(tree)))

        # insert empty meta element as first child of document element
        list(tree)[0].insert(0, self.meta())

        return tree
