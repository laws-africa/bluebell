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

    id_exempt = set("akomaNtoso act amendment amendmentList bill debate debateReport doc documentCollection judgment"
                    " officialGazette portion statement"
                    " amendmentBody attachments body collectionBody components coverPage debateBody"
                    " judgmentBody mainBody meta portionBody"
                    " br tr td th num heading subheading content"
                    " abbr b i u sub sup ins del inline img remark span".split())
    """ Elements that never have ids, such as top-level documents and self-closing inlines.
        Note that we don't include block in this list, even though eId is optional on block, because we consider it a
        peer of p, blockList and friends, which should have eIds.
    """

    id_exempt_but_pass_to_children = set("arguments background conclusions decision header intro introduction"
                                         " motivation preamble preface remedies wrapUp".split())
    """ Elements for which an id is not required but any descendants get the parent's prefix."""

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

    def rewrite_all_eids(self, element, prefix=''):
        """ Rewrites all eId attributes for this tree.
        :param element: XML tree
        :returns: mappings of old --> new eids
        """
        self.reset()
        self.rewrite_eid(element, prefix)
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

        # don't generate an eId for `act`, `num`, etc
        if tag not in self.id_exempt and tag not in self.id_exempt_but_pass_to_children:
            old_eid = element.get('eId', '')

            num = next((n.text for n in element.iterchildren(f'{{{element.nsmap[None]}}}num')), '')
            new_eid = self.get_eid(prefix, tag, num) or ''

            # update prefix on all descendants if changed
            if old_eid != new_eid:
                element.set('eId', new_eid)
                # update mappings if changed (ignores duplicates and elements with no eIds in original)
                if old_eid:
                    self.mappings.setdefault(old_eid, new_eid)

            # use the new eId as the prefix if there is one, or keep using the same one
            prefix = new_eid or prefix

        # include the current tag in the prefix if needed
        if tag in self.id_exempt_but_pass_to_children:
            prefix = f'{prefix}__{tag.lower()}' if prefix else tag.lower()

        # keep drilling down
        for kid in element.iterchildren():
            self.rewrite_eid(kid, prefix)

    def get_eid(self, prefix, name, num):
        if name in self.id_exempt:
            return None

        eid = f'{prefix}__' if prefix else ''
        eid = eid + self.aliases.get(name, name)

        # some elements are effectively unique and so don't need a differentiating number
        if name not in self.id_exempt_but_pass_to_children:
            num, nn = self.get_num(prefix, name, num)
            eid = self.ensure_unique(f'{eid}_{num}', nn)

        return eid

    def get_num(self, prefix, name, num):
        nn = False

        # e.g. PARA (a)
        if num:
            num = self.clean_num(num)

        # e.g. PARA, or num was cleaned to ''
        if not num and name in self.num_expected:
            num = 'nn'
            nn = True

        # produce e.g. hcontainer_1
        if not num:
            num = self.incr(prefix, name)

        return num, nn

    def reset(self):
        self.counters.clear()
        self.eid_counter.clear()
        self.mappings.clear()

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

    def incr(self, prefix, name):
        sub = self.counters.setdefault(prefix, {})
        sub[name] = sub.get(name, 0) + 1
        return sub[name]

    def ensure_unique(self, eid, nn):
        # update counter with number of elements with this eid, including this one
        count = self.eid_counter[eid] = self.eid_counter.get(eid, 0) + 1

        # eid must be unique, and unnumbered elements must end with _{count} regardless
        if count == 1 and not nn:
            return eid

        # if it's not unique, or the element is unnumbered,
        # include the count for disambiguation and check for uniqueness
        return self.ensure_unique(f'{eid}_{count}', nn=False)


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
        return etree.fromstring(etree.tostring(self.item_to_xml(tree), encoding='utf-8'))

    def item_to_xml(self, item):
        return getattr(self, f'item_to_xml_{item["type"]}')(item)

    def item_to_xml_hier(self, item):
        m = self.maker

        def check_hier(x):
            return x['type'] == 'hier' or x['name'] == 'crossHeading'

        if all(not check_hier(k) for k in item['children']):
            # no hierarchy children (ie. all block/content), wrap children in <content>
            kids = self.kids_to_xml(item)
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
            groups = [(is_hier, list(group)) for is_hier, group in groupby(item['children'], check_hier)]

            kids = []
            seen_hier = False
            for i, (is_hier, group) in enumerate(groups):
                def make_group():
                    return (self.item_to_xml(k) for k in group)

                if is_hier:
                    # add hier elemnts as-is
                    seen_hier = True
                    kids.extend(make_group())
                elif seen_hier:
                    # content after a hier element
                    if i == len(groups) - 1:
                        # it's the last group, use a wrapUp
                        kids.append(m.wrapUp(*make_group()))
                    else:
                        # more groups to come, use a container
                        kids.append(m.hcontainer(m.content(*make_group()), name="hcontainer"))
                else:
                    # before hier
                    kids.append(m.intro(*make_group()))

        pre = []
        self.add_num_heading_subheading(m, item, pre)

        kids = pre + kids
        return m(item['name'], *kids, **item.get('attribs', {}))

    def item_to_xml_block(self, item):
        m = self.maker
        kids = []

        self.add_num_heading_subheading(m, item, kids)

        kids.extend(self.kids_to_xml(item))
        if not kids:
            # block elements must have at least one content child
            kids = [m.p()]

        return m(item['name'], *kids, **item.get('attribs', {}))

    def item_to_xml_speechhier(self, item):
        """ Speech hier is similar to normal hier, but without having to worry about <content>."""
        m = self.maker
        kids = []

        self.add_num_heading_subheading(m, item, kids)

        if 'from' in item:
            kids.append(getattr(m, 'from')(*(self.item_to_xml(k) for k in item['from'])))
        kids.extend(self.kids_to_xml(item))

        return m(item['name'], *kids, **item.get('attribs', {}))

    def item_to_xml_content(self, item):
        return self.maker(item['name'], *self.kids_to_xml(item), **item.get('attribs', {}))

    def item_to_xml_inline(self, item):
        # TODO: should these have ids?
        return self.maker(item['name'], *self.kids_to_xml(item), **item.get('attribs', {}))

    def item_to_xml_marker(self, item):
        # TODO: should these have ids?
        return self.maker(item['name'], **item.get('attribs', {}))

    def item_to_xml_text(self, item):
        return item['value']

    def item_to_xml_element(self, item):
        m = self.maker

        if item['name'] == 'attachment':
            return self.item_to_xml_element_attachment(item)

        attrs = item.get('attribs', {})
        return m(item['name'], *self.kids_to_xml(item), **attrs)

    def item_to_xml_element_attachment(self, item):
        m = self.maker

        attachment_name = self.get_attachment_name(item)

        pre = []
        if item.get('heading'):
            pre.append(m.heading(*(self.item_to_xml(k) for k in item['heading'])))

        if item.get('subheading'):
            pre.append(m.subheading(*(self.item_to_xml(k) for k in item['subheading'])))

        self.attachment_names.append(attachment_name)
        try:
            return m('attachment',
                     *pre,
                     m('doc',
                       self.make_meta(self.attachment_frbr_uri(attachment_name), False),
                       *self.kids_to_xml(kids=item['children']),
                       **item.get('attribs', {})))
        finally:
            self.attachment_names.pop()

    def get_attachment_name(self, item):
        parent = self.attachment_names[-1] if self.attachment_names else None
        name = item.get('attribs', {}).get('name', 'attachment')
        num = self.ids.incr(f'__attachments', f'{parent}__{name}' if parent else name)
        return f'{parent}/{name}_{num}' if parent else f'{name}_{num}'

    def kids_to_xml(self, parent=None, kids=None):
        if kids is None:
            kids = parent.get('children', [])
        return [self.item_to_xml(k) for k in kids]

    def add_num_heading_subheading(self, m, item, kids):
        if item.get('num'):
            kids.append(m.num(item['num']))

        if item.get('heading'):
            kids.append(m.heading(*(self.item_to_xml(k) for k in item['heading'])))

        if item.get('subheading'):
            kids.append(m.subheading(*(self.item_to_xml(k) for k in item['subheading'])))

    def post_process(self, xml):
        """ Post-processing of generated XML to make final changes.
        """
        xml = self.resolve_displaced_content(xml)
        xml = self.normalise(xml)
        xml = self.generate_eids(xml)
        xml = self.set_attachment_titles(xml)
        return xml

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

            content = get_displaced_content(ref, name, ref.get('marker'))
            if content is not None:
                # move children of the displaced element into the ref
                for child in content:
                    ref.append(child)
                content.getparent().remove(content)
            else:
                # we couldn't find the content
                # TODO: stash a warning somewhere?
                p = etree.Element(f'{{{ns}}}p', nsmap=xml.nsmap)
                p.text = "(content missing)"
                ref.append(p)

        # don't lose unused displaced content. Instead, change it to a p tag and pull in its children
        # as siblings
        for displaced in xml.iter(f'{{{ns}}}displaced'):
            p = etree.Element(f'{{{ns}}}p', nsmap=xml.nsmap)
            # eg. FOOTNOTE 99
            p.text = displaced.get('name').upper() + ' ' + displaced.get('marker')

            displaced.addprevious(p)

            for child in displaced:
                displaced.addprevious(child)

            # remove the empty element
            displaced.getparent().remove(displaced)

        return xml

    def set_attachment_titles(self, xml):
        """ Derive attachment aliases from their headings, if available.
        """
        ns = xml.nsmap[None]
        for attachment in xml.xpath('//a:attachment', namespaces={'a': ns}):
            heading = attachment.xpath('./a:heading', namespaces={'a': ns})
            if heading:
                title = ''.join(heading[0].itertext())
                alias = attachment.xpath('./a:doc/a:meta/a:identification/a:FRBRWork/a:FRBRalias[@name="title"]', namespaces={'a': ns})
                if alias:
                    alias[0].attrib['value'] = title

        return xml

    def normalise(self, xml):
        """ Make some basic normalisations. It's easier (and a better separation of concerns) to do these afterwards,
        rather than when translating the intermediate structure into XML.

        1. remove empty crossHeading and longTitle elements which can be produced by the grammar.
        2. remove empty content elements which can be produced for empty hierarchical elements.
        3. remove empty containers that are not valid
        """
        for elem in xml.xpath('//*[self::a:crossHeading or self::a:longTitle or self::a:content or self::a:preface'
                              ' or self::a:preamble or self::a:conclusions][not(node())]',
                              namespaces={'a': xml.nsmap[None]}):
            elem.getparent().remove(elem)
        return xml

    def generate_eids(self, xml):
        """ Add eIds to elements.
        """
        self.ids.reset()
        self.ids.rewrite_all_eids(xml, self.eid_prefix)
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

        meta = etree.fromstring(etree.tostring(self.make_meta(self.frbr_uri, True), encoding='utf-8'))
        list(xml)[0].insert(0, meta)
        return xml

    def make_meta(self, frbr_uri, for_root):
        """ Create a meta element appropriate for this generator's FRBR URI.
        """
        cls = StructuredDocument.for_document_type(frbr_uri.doctype)
        return cls.empty_meta(frbr_uri, maker=self.maker, for_root=for_root)
