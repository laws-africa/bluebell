import re
from itertools import groupby, chain

from cobalt.akn import get_maker, StructuredDocument
import lxml.etree as etree


class IdGenerator:
    """ Support class for generating ID elements when building an XML document.
    """
    # leading whitespace and punctuation
    leading_punct_re = re.compile(r'^[\s\u2000-\u206f\u2e00-\u2e7f!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~]+')
    # trailing whitespace and punctuation
    trailing_punct_re = re.compile(r'[\s\u2000-\u206f\u2e00-\u2e7f!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~]+$')
    # whitespace
    whitespace_re = re.compile(r'\s')
    # general punctuation
    punct_re = re.compile(r'[\u2000-\u206f\u2e00-\u2e7f!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~]+')

    id_exempt = set("act amendment amendmentList bill debate debateReport doc documentCollection judgment"
                    " officialGazette portion statement body mainBody judgmentBody attachments"
                    " br tr td th num heading content".split())
    """ Elements that never have ids, such as top-level documents and self-closing inlines."""

    id_unnecessary = set("arguments background conclusions decision header introduction motivation preamble preface"
                         " remedies".split())
    """ Elements for which an id is optional. """

    id_unnecessary_but_pass_to_children = ['intro', 'wrapUp']
    """ Elements for which an id is optional but any descendants get the parent's prefix."""

    num_expected = set("alinea article book chapter clause division indent item level list"
                       " paragraph part point proviso rule section subchapter subclause"
                       " subdivision sublist subparagraph subpart subrule subsection subtitle"
                       " title tome transitional".split())
    """ Elements for which a num is expected. """

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
        'listWrapUp': 'wrapup',
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
        self.eid_counter = {}
        self.mappings = {}

    def incr(self, prefix, name):
        sub = self.counters.setdefault(prefix, {})
        sub[name] = sub.get(name, 0) + 1
        return sub[name]

    def is_unnecessary(self, prefix, item):
        """ Certain top-level elements only need ids if they're embedded and therefore have a prefix.
        """
        return item['name'] in self.id_unnecessary and not prefix

    def make(self, prefix, item):
        if item['name'] in self.id_exempt:
            return None

        eid = f'{prefix}__' if prefix else ''
        name = item['name']
        eid = eid + self.aliases.get(name, name)

        if self.needs_num(name):
            num, nn = self.get_num(item, prefix, name)
            eid = self.ensure_unique(f'{eid}_{num}', nn)

        return eid

    def get_num(self, item, prefix, name):
        num = None
        nn = False

        # e.g. PARA (a)
        if item.get('num'):
            num = self.clean_num(item.get('num'))

        # e.g. PARA, or num was cleaned to ''
        if not num and self.needs_nn(name):
            num = 'nn'
            nn = True

        # produce e.g. hcontainer_1
        if not num:
            num = self.incr(prefix, name)

        return num, nn

    def ensure_unique(self, eid, nn):
        # update counter with number of elements with this eid, including this one
        count = self.eid_counter[eid] = self.eid_counter.get(eid, 0) + 1

        # eid must be unique, and unnumbered elements must end with _{count} regardless
        if count == 1 and not nn:
            return eid

        # if it's not unique, or the element is unnumbered,
        # include the count for disambiguation and check for uniqueness
        return self.ensure_unique(f'{eid}_{count}', nn=False)

    def reset(self):
        self.counters.clear()
        self.eid_counter.clear()

    def needs_num(self, name):
        return name not in self.id_unnecessary

    def needs_nn(self, name):
        return name in self.num_expected

    def clean_num(self, num):
        """ Clean a <num> value for use in an eId
        See https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/os/akn-nc-v1.0-os.html*_Toc531692306

        "The number part of the identifiers of such elements corresponds to the
        stripping of all final punctuation, meaningless separations as well as
        redundant characters in the content of the <num> element. The
        representation is case-sensitive."

        Our algorithm is:
        1. strip all leading and trailing whitespace and punctuation (using the unicode punctuation blocks)
        2. strip all whitespace
        3. replace all remaining punctuation with a hyphen.

        The General Punctuation block is \u2000-\u206F, and the Supplemental Punctuation block is \u2E00-\u2E7F.

        (i) -> i
        1.2. -> 1-2
        “2.3“ -> 2-3
        3a bis -> 3abis
        """
        num = self.leading_punct_re.sub('', num)
        num = self.trailing_punct_re.sub('', num)
        num = self.whitespace_re.sub('', num)
        num = self.punct_re.sub('-', num)
        return num

    def rewrite_id_prefix(self, root, old_prefix, new_prefix):
        """ Rewrite the eId attributes of elem and its descendants to replace old_prefix with new_prefix.

        The old_prefix and the new_prefix are both without the '__' suffix, to permit exact and substring matches.
        """
        offset = len(old_prefix) + 2 if old_prefix else 0

        # rewrite element and children
        for elem in chain([root], root.xpath('.//a:*[@eId]', namespaces={'a': root.nsmap[None]})):
            old_id = elem.get('eId')

            if old_id == old_prefix:
                elem.set('eId', new_prefix)

            elif old_id.startswith(old_prefix + '__'):
                elem.set('eId', new_prefix + '__' + old_id[offset:])

    def rewrite_all_eids(self, doc_tree):
        """ Rewrites all eId attributes for this tree.
        :param doc_tree: XML tree
        :returns: mappings of old --> new eids
        """
        self.mappings = {}

        for child in doc_tree.iterchildren():
            self.rewrite_eid(child)

        return self.mappings

    def rewrite_eid(self, element, prefix=''):
        """ Rewrites all eIds recursively in `element`, ensuring correctness and uniqueness.
            :param element: XML element
            :param prefix: string of parent eId or other prefix to be used (e.g. "preface"); defaults to empty string
        """
        tag = element.tag.split('}', 1)[-1]
        # skip meta blocks entirely
        if tag == 'meta':
            return

        # don't generate new eId for `act`, `num`, etc
        if tag not in self.id_exempt:
            old_eid = element.get('eId')

            # use preface / preamble as prefix
            parent = element.getparent().tag.split('}', 1)[-1]
            if parent in ['preface', 'preamble']:
                prefix = parent

            # nums = [n.text for n in element.iterchildren(f'{{{element.nsmap[None]}}}num')]
            num = next((n.text for n in element.iterchildren(f'{{{element.nsmap[None]}}}num')), '')
            item = {
                'name': tag,
                # 'num': nums[0] if nums else '',
                'num': num,
            }
            new_eid = self.make(prefix, item) or ''

            # update prefix on all descendants if changed
            if old_eid != new_eid:
                self.rewrite_id_prefix(element, old_eid, new_eid)

                # update mappings if changed (ignores duplicates and elements with no eIds in original)
                if old_eid:
                    self.mappings.setdefault(old_eid, new_eid)

            # use the new eId as the prefix if there is one, or keep using the same one
            prefix = new_eid or prefix

        # include the current tag in the prefix if needed
        if tag in self.id_unnecessary_but_pass_to_children:
            prefix = f'{prefix}__{tag.lower()}' if prefix else tag.lower()

        # keep drilling down
        for kid in element.iterchildren():
            self.rewrite_eid(kid, prefix)


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
        self.attachment_names = []

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
        return etree.fromstring(etree.tostring(self.item_to_xml(tree, self.eid_prefix), encoding='unicode'))

    def item_to_xml(self, item, prefix=''):
        return getattr(self, f'item_to_xml_{item["type"]}')(item, prefix)

    def item_to_xml_hier(self, item, prefix):
        m = self.maker
        eid = self.ids.make(prefix, item)

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
            # hcontainer
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
                def make_group(pre):
                    return (self.item_to_xml(k, pre) for k in group)

                if is_hier:
                    # add hier elemnts as-is
                    seen_hier = True
                    kids.extend(make_group(eid))
                elif seen_hier:
                    # content after a hier element
                    if i == len(groups) - 1:
                        # it's the last group, use a wrapUp
                        kids.append(m.wrapUp(*make_group(eid + '__wrapup')))
                    else:
                        # more groups to come, use a container
                        hcontainer_eid = self.ids.make(eid, {'name': 'hcontainer'})
                        kids.append(m.hcontainer(m.content(*make_group(hcontainer_eid)), name="hcontainer", eId=hcontainer_eid))
                else:
                    # before hier
                    kids.append(m.intro(*make_group(eid + '__intro')))

        pre = []
        self.add_num_heading_subheading(m, item, eid, pre)

        kids = pre + kids
        return m(item['name'], *kids, eId=eid, **item.get('attribs', {}))

    def item_to_xml_block(self, item, prefix):
        m = self.maker
        eid = self.ids.make(prefix, item)
        kids = []

        self.add_num_heading_subheading(m, item, eid, kids)

        kids.extend(self.kids_to_xml(item, prefix=eid))
        if not kids:
            # block elements must have at least one content child
            kids = [m.p()]

        return m(item['name'], eId=eid, *kids, **item.get('attribs', {}))

    def item_to_xml_content(self, item, prefix):
        eid = self.ids.make(prefix, item)
        return self.maker(item['name'], eId=eid, *self.kids_to_xml(item, prefix=eid), **item.get('attribs', {}))

    def item_to_xml_inline(self, item, prefix):
        # TODO: should these have ids?
        return self.maker(item['name'], *self.kids_to_xml(item, prefix=prefix), **item.get('attribs', {}))

    def item_to_xml_marker(self, item, prefix):
        # TODO: should these have ids?
        return self.maker(item['name'], **item.get('attribs', {}))

    def item_to_xml_text(self, item, prefix):
        return item['value']

    def item_to_xml_element(self, item, prefix):
        m = self.maker

        if item['name'] == 'attachment':
            return self.item_to_xml_element_attachment(item, prefix)

        attrs = item.get('attribs', {})
        eid = self.ids.make(prefix, item)
        if eid and not self.ids.is_unnecessary(prefix, item):
            attrs['eId'] = eid
        return m(item['name'], *self.kids_to_xml(item, prefix=(eid or prefix)), **attrs)

    def item_to_xml_element_attachment(self, item, prefix):
        m = self.maker

        eid = self.ids.make(prefix, item)
        attachment_name = self.get_attachment_name(item)

        pre = []
        if item.get('heading'):
            pre.append(m.heading(*(self.item_to_xml(k, eid) for k in item['heading'])))

        if item.get('subheading'):
            pre.append(m.subheading(*(self.item_to_xml(k, eid) for k in item['subheading'])))

        self.attachment_names.append(attachment_name)
        try:
            return m('attachment',
                     *pre,
                     m('doc',
                       self.make_meta(self.attachment_frbr_uri(attachment_name)),
                       *self.kids_to_xml(kids=item['children'], prefix=eid),
                       **item.get('attribs', {})),
                     eId=eid)
        finally:
            self.attachment_names.pop()

    def get_attachment_name(self, item):
        parent = self.attachment_names[-1] if self.attachment_names else None
        name = item.get('attribs', {}).get('name', 'attachment')
        num = self.ids.incr(f'__attachments', f'{parent}__{name}' if parent else name)
        return f'{parent}/{name}_{num}' if parent else f'{name}_{num}'

    def kids_to_xml(self, parent=None, kids=None, prefix=None):
        if kids is None:
            kids = parent.get('children', [])
        return [self.item_to_xml(k, prefix) for k in kids]

    def add_num_heading_subheading(self, m, item, eid, kids):
        if item.get('num'):
            kids.append(m.num(item['num']))

        if item.get('heading'):
            kids.append(m.heading(*(self.item_to_xml(k, eid) for k in item['heading'])))

        if item.get('subheading'):
            kids.append(m.subheading(*(self.item_to_xml(k, eid) for k in item['subheading'])))

    def post_process(self, xml):
        return self.resolve_displaced_content(xml)

    def resolve_displaced_content(self, xml):
        """ Resolve displaced content (ie. footnotes).
        """
        ns = xml.nsmap[None]

        def get_displaced_content(start, name, marker):
            # find the displaced content, by walking through following nodes in the tree
            for parent in start.iterancestors():
                for child in parent.iter(f'{{{ns}}}displaced'):
                    if child.get('marker') == marker and child.get('name') == name:
                        return child
                # TODO: when to stop

        for ref in xml.xpath('//a:*[@displaced]', namespaces={'a': ns}):
            name = ref.attrib.pop('displaced')
            new_prefix = ref.attrib.get('eId')

            content = get_displaced_content(ref, name, ref.get('marker'))
            if content is not None:
                old_prefix = content.get('eId')

                # move children of the displaced element into the ref
                for child in content:
                    self.ids.rewrite_id_prefix(child, old_prefix, new_prefix)
                    ref.append(child)
                content.getparent().remove(content)
            else:
                # we couldn't find the content
                # TODO: stash a warning somewhere?
                p = etree.Element(f'{{{ns}}}p', nsmap=xml.nsmap)
                p.text = "(content missing)"
                p.set('eId', self.ids.make(new_prefix, {'name': 'p'}))
                ref.append(p)

        # don't lose unused displaced content. Instead, change it to a p tag and pull in its children
        # as siblings
        for displaced in xml.iter(f'{{{ns}}}displaced'):
            p = etree.Element(f'{{{ns}}}p', nsmap=xml.nsmap)
            # eg. FOOTNOTE 99
            p.text = displaced.get('name').upper() + ' ' + displaced.get('marker')

            # eg. part_1__displaced_2 -> part_1
            new_prefix = displaced.attrib.get('eId').rsplit('__', 1)[0]
            # eg. part_1__p_1
            p.set('eId', self.ids.make(new_prefix, {'name': 'p'}))

            displaced.addprevious(p)

            for child in displaced:
                name = child.tag.split('}', 1)[1]
                eid = self.ids.make(new_prefix, {'name': name})
                self.ids.rewrite_id_prefix(child, child.get('eId'), eid)
                displaced.addprevious(child)

            # remove the empty element
            displaced.getparent().remove(displaced)

        return xml

    def attachment_frbr_uri(self, attachment_name):
        """ Build an FrbrUri instance for the attachment in the given item.
        """
        frbr_uri = self.frbr_uri.clone()
        frbr_uri.work_component = attachment_name

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
        cls = StructuredDocument.for_document_type(frbr_uri.doctype)
        return cls.empty_meta(frbr_uri, maker=self.maker)
