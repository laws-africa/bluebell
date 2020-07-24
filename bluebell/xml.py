import re
from itertools import groupby

from cobalt import FrbrUri
from cobalt.akn import get_maker, StructuredDocument
import lxml.etree as etree


class IdGenerator:
    """ Support class for generating ID elements when building an XML document.
    """
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
    """ Turns a parse tree into XML.

    For example::

        gen = XmlGenerator('/akn/act/za/2020/1', 'chp_1__')
        xml = gen.to_xml(tree)
    """

    akn_version = '3.0'
    """ AKN version to use, relying on Cobalt's versions and namespaces.
    """

    def __init__(self, frbr_uri=None, eid_prefix='', maker=None):
        """ Setup a new generator for an FRBR URI (optional).
        """
        self.ids = IdGenerator()
        self.frbr_uri = frbr_uri
        self.maker = maker or get_maker(self.akn_version)
        self.eid_prefix = eid_prefix

    def to_xml(self, tree):
        """ Transform an entire parse tree to XML, including post-processing.
        """
        self.tree = tree.to_dict()
        return self.xml_from_dict(self.tree, getattr(tree, 'is_root', False))

    def xml_from_dict(self, tree, is_root=False):
        """ Transform an intermediate dict representation into XML, including post-processing.
        """
        xml = self.xml_from_tree(tree)
        if is_root:
            xml = self.add_meta(self.wrap_akn(xml))
        return self.post_process(xml)

    def xml_from_tree(self, tree):
        """ Transform an entire parse tree to XML.
        """
        return etree.fromstring(etree.tostring(self.item_to_xml(tree, self.eid_prefix)))

    def item_to_xml(self, item, prefix=''):
        m = self.maker

        if item['type'] == 'hier':
            eid = self.ids.make(prefix, item)
            pre = []

            if all(k['type'] != 'hier' for k in item['children']):
                # no hierarchy children (ie. all block/content), wrap children in <content>
                kids = self.kids_to_xml(item, prefix=eid)
                kids = [m.content(*kids)]
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
                    group = (self.item_to_xml(k, eid) for k in group)

                    if is_hier:
                        # add hier elemnts as-is
                        seen_hier = True
                        kids.extend(group)
                    elif seen_hier:
                        # content after a hier element
                        if i == len(groups) - 1:
                            # it's the last group, use a wrapUp
                            kids.append(m.wrapUp(*group))
                        else:
                            # more groups to come, use a container
                            kids.append(m.container(*group, name="container", eId=self.ids.make(eid, {'name': 'container'})))
                    else:
                        # before hier
                        kids.append(m.intro(*group))

            if item.get('num'):
                pre.append(m.num(item['num']))

            if item.get('heading'):
                pre.append(m.heading(*(self.item_to_xml(k, eid) for k in item['heading'])))

            if item.get('subheading'):
                pre.append(m.subheading(*(self.item_to_xml(k, eid) for k in item['subheading'])))

            kids = pre + kids
            return m(item['name'], *kids, eId=eid, **item.get('attribs', {}))

        if item['type'] == 'block':
            # TODO: can have num, heading, subheading
            # TODO: make this generic? what else can have num?
            eid = self.ids.make(prefix, item)
            kids = self.kids_to_xml(item, prefix=eid)
            if not kids:
                # block elements must have at least one content child
                kids = [m.p()]

            if 'num' in item:
                kids.insert(0, m('num', item['num']))
            return m(item['name'], eId=eid, *kids)

        if item['type'] == 'content':
            return m(item['name'], *self.kids_to_xml(item, prefix=prefix))

        if item['type'] == 'inline':
            # TODO: should these have ids?
            return m(item['name'], *self.kids_to_xml(item, prefix=prefix), **item.get('attribs', {}))

        if item['type'] == 'marker':
            # TODO: should these have ids?
            return m(item['name'], **item.get('attribs', {}))

        if item['type'] == 'text':
            return item['value']

        if item['type'] == 'element' and item['name'] == 'attachment':
            eid = self.ids.make(prefix, item)

            pre = []
            if item.get('heading'):
                pre.append(m.heading(*(self.item_to_xml(k, eid) for k in item['heading'])))

            if item.get('subheading'):
                pre.append(m.subheading(*(self.item_to_xml(k, eid) for k in item['subheading'])))

            return m('attachment',
                     *pre,
                     m('doc',
                       self.make_meta(self.attachment_frbr_uri(item)),
                       m('mainBody', *self.kids_to_xml(item, prefix=eid)),
                       **item.get('attribs', {})),
                     eId=eid)

        if item['type'] == 'element':
            attrs = item.get('attribs', {})
            eid = self.ids.make(prefix, item)
            if eid and not self.ids.is_unnecessary(prefix, item):
                attrs['eId'] = eid
            return m(item['name'], *self.kids_to_xml(item, prefix=eid), **attrs)

    def kids_to_xml(self, parent=None, kids=None, prefix=None):
        if kids is None:
            kids = parent.get('children', [])
        return [self.item_to_xml(k, prefix) for k in kids]

    def post_process(self, xml):
        return self.resolve_displaced_content(xml)

    def resolve_displaced_content(self, xml):
        """ Resolve displaced content (ie. footnotes).
        """
        ns = xml.nsmap[None]

        def get_displaced_content(start, name, marker):
            for parent in start.iterancestors():
                for child in parent.iter(f'{{{ns}}}displaced'):
                    if child.get('marker') == marker and child.get('name') == name:
                        return child
                # TODO: when to stop

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

    def attachment_frbr_uri(self, item):
        """ Build an FrbrUri instance for the attachment in the given item.
        """
        name = item.get('attribs', {}).get('name', 'attachment')
        num = self.ids.incr('__attachments', name)

        frbr_uri = self.frbr_uri.clone()
        frbr_uri.work_component = f'{name}_{num}'

        return frbr_uri

    def wrap_akn(self, xml):
        """ Wrap in an akomaNtoso element.
        """
        ns = xml.nsmap[None]
        akn = etree.Element(f'{{{ns}}}akomaNtoso', nsmap=xml.nsmap)
        akn.append(xml)
        return akn

    def add_meta(self, xml):
        """ Insert empty meta element as first child of document element.
        """
        if not self.frbr_uri:
            raise ValueError("An frbr_uri must be provided when generating top-level documents.")

        meta = etree.fromstring(etree.tostring(self.make_meta(self.frbr_uri)))
        list(xml)[0].insert(0, meta)
        return xml

    def make_meta(self, frbr_uri):
        """ Create a meta element appropriate for this generator's FRBR URI.
        """
        if not isinstance(frbr_uri, FrbrUri):
            frbr_uri = FrbrUri.parse(frbr_uri)
        cls = StructuredDocument.for_document_type(frbr_uri.doctype)
        return cls.empty_meta(frbr_uri, maker=self.maker)
