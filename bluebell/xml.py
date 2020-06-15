import re
from itertools import groupby

from lxml.builder import ElementMaker
import lxml.etree as ET

AKN3_NAMESPACE = 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'

E = ElementMaker(nsmap={None: AKN3_NAMESPACE})


class IdGenerator:
    num_strip_re = re.compile(r'[ .()[\]]')

    id_exempt = set("act amendment amendmentList bill debate debateReport doc documentCollection judgment"
                    " officialGazette portion statement body mainBody judgmentBody attachments"
                    " tr td th".split())
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

    def __init__(self):
        self.counters = {}

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

    def reset(self):
        self.counters.clear()

    def needs_num(self, name):
        return name not in self.id_unnecessary

    def clean_num(self, num):
        return self.num_strip_re.sub('', num)


class XmlGenerator:
    def __init__(self):
        self.ids = IdGenerator()

    def tree_to_xml(self, tree):
        """ Transform an entire parse tree to XML, including post-processing.
        """
        root = ET.fromstring(ET.tostring(self.to_xml(tree)))
        return self.post_process(root)

    def kids_to_xml(self, parent=None, kids=None, prefix=None):
        if kids is None:
            kids = parent.get('children', [])
        return [self.to_xml(k, prefix) for k in kids]

    def to_xml(self, item, prefix=''):
        if item['type'] == 'hier':
            eid = self.ids.make(prefix, item)
            pre = []

            if all(k['type'] != 'hier' for k in item['children']):
                # no hierarchy children (ie. all block/content), wrap children in <content>
                kids = self.kids_to_xml(item, prefix=eid)
                kids = [E.content(*kids)]
            else:
                # there are potentially mixed hier and block/content children
                # group non-hier children into <intro> and <wrapUp>, with hier children sandwiched in the middle
                #
                # intro
                #   ...
                # hier
                #   ...
                # container
                #   ...
                # hier
                #   ...
                # wrapUp
                #   ...
                #
                groups = [
                    (is_hier, list(group))
                    for is_hier, group in
                    groupby(item['children'], lambda x: x['type'] == 'hier' or x['name'] == 'crossHeading')
                ]

                kids = []
                seen_hier = False
                for i, (is_hier, group) in enumerate(groups):
                    group = (self.to_xml(k, eid) for k in group)

                    if is_hier:
                        # add hier elemnts as-is
                        seen_hier = True
                        kids.extend(group)
                    elif seen_hier:
                        # content after a hier element
                        if i == len(groups) - 1:
                            # it's the last group, use a wrapUp
                            kids.append(E.wrapUp(*group))
                        else:
                            # more groups to come, use a container
                            kids.append(E.container(*group, name="container", eId=self.ids.make(eid, {'name': 'container'})))
                    else:
                        # before hier
                        kids.append(E.intro(*group))

            if item.get('num'):
                pre.append(E.num(item['num']))

            if item.get('heading'):
                pre.append(E.heading(*(self.to_xml(k, eid) for k in item['heading'])))

            if item.get('subheading'):
                pre.append(E.subheading(*(self.to_xml(k, eid) for k in item['subheading'])))

            kids = pre + kids
            return E(item['name'], *kids, eId=eid, **item.get('attribs', {}))

        if item['type'] == 'block':
            # TODO: can have num, heading, subheading
            # TODO: make this generic? what else can have num?
            eid = self.ids.make(prefix, item)
            kids = self.kids_to_xml(item, prefix=eid)
            if not kids:
                # block elements must have at least one content child
                kids = [E.p()]

            if 'num' in item:
                kids.insert(0, E('num', item['num']))
            return E(item['name'], eId=eid, *kids)

        if item['type'] == 'content':
            return E(item['name'], *self.kids_to_xml(item, prefix=prefix))

        if item['type'] == 'inline':
            # TODO: should these have ids?
            return E(item['name'], *self.kids_to_xml(item, prefix=prefix), **item.get('attribs', {}))

        if item['type'] == 'marker':
            # TODO: should these have ids?
            return E(item['name'], **item.get('attribs', {}))

        if item['type'] == 'text':
            return item['value']

        if item['type'] == 'element' and item['name'] == 'attachment':
            eid = self.ids.make(prefix, item)

            pre = []
            if item.get('heading'):
                pre.append(E.heading(*(self.to_xml(k, eid) for k in item['heading'])))

            if item.get('subheading'):
                pre.append(E.subheading(*(self.to_xml(k, eid) for k in item['subheading'])))

            return E('attachment',
                     *pre,
                     E('doc',
                       E('meta'),
                       E('mainBody', *self.kids_to_xml(item, prefix=eid)),
                       **item.get('attribs', {})),
                     eId=eid)

        if item['type'] == 'element':
            attrs = item.get('attribs', {})
            eid = self.ids.make(prefix, item)
            if eid and not self.ids.is_unnecessary(prefix, item):
                attrs['eId'] = eid
            return E(item['name'], *self.kids_to_xml(item, prefix=eid), **attrs)

    def post_process(self, xml):
        ns = xml.nsmap[None]

        def get_displaced_content(start, name, marker):
            for parent in start.iterancestors():
                for child in parent.iter(f'{{{ns}}}displaced'):
                    if child.get('marker') == marker and child.get('name') == name:
                        return child
                # TODO: when to stop

        # resolve displaced content (ie. footnotes)
        for ref in xml.xpath('//a:*[@displaced]', namespaces={'a': ns}):
            name = ref.attrib.pop('displaced')

            # find the displaced content, by walking through following nodes in the tree
            content = get_displaced_content(ref, name, ref.get('marker'))
            for child in content:
                ref.append(child)
            content.getparent().remove(content)

        # clean up unused displaced content
        for displaced in xml.iter(f'{{{ns}}}displaced'):
            displaced.getparent().remove(displaced)

        return xml


def to_xml(item):
    """ Transform an item in a parse tree to XML.
    """
    return XmlGenerator().to_xml(item)


def tree_to_xml(tree):
    """ Transform an entire parse tree to XML.
    """
    return XmlGenerator().tree_to_xml(tree)


class Document:
    def make_xml(self, tree):
        # TODO: empty ARGUMENTS, REMEDIES etc. should be excluded
        return E.akomaNtoso(tree_to_xml(tree))

    def meta(self):
        return ET.fromstring(ET.tostring(E.meta()))

    def to_xml(self, tree):
        tree = ET.fromstring(ET.tostring(self.make_xml(tree)))

        # insert empty meta element as first child of document element
        list(tree)[0].insert(0, self.meta())

        return tree
