# This file was generated from bluebell/akn.peg
# See http://canopy.jcoglan.com/ for documentation.

from collections import defaultdict
import re


class TreeNode(object):
    def __init__(self, text, offset, elements):
        self.text = text
        self.offset = offset
        self.elements = elements

    def __iter__(self):
        for el in self.elements:
            yield el


class TreeNode1(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode1, self).__init__(text, offset, elements)
        self.judgment_body = elements[0]
        self.conclusions = elements[1]
        self.attachments = elements[2]


class TreeNode2(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode2, self).__init__(text, offset, elements)
        self.introduction = elements[0]
        self.background = elements[1]
        self.arguments = elements[2]
        self.remedies = elements[3]
        self.motivation = elements[4]
        self.decision = elements[5]


class TreeNode3(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode3, self).__init__(text, offset, elements)
        self.preface = elements[0]
        self.preamble = elements[1]
        self.body = elements[2]
        self.conclusions = elements[3]
        self.attachments = elements[4]


class TreeNode4(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode4, self).__init__(text, offset, elements)
        self.preface = elements[0]
        self.preamble = elements[1]
        self.main_body = elements[2]
        self.conclusions = elements[3]
        self.attachments = elements[4]


class TreeNode5(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode5, self).__init__(text, offset, elements)
        self.hier_element_name = elements[0]
        self.heading = elements[1]
        self.eol = elements[2]
        self.indent = elements[3]
        self.subheading = elements[4]
        self.content = elements[5]
        self.dedent = elements[6]


class TreeNode6(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode6, self).__init__(text, offset, elements)
        self.space = elements[0]
        self.num = elements[1]
        self.heading = elements[2]


class TreeNode7(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode7, self).__init__(text, offset, elements)
        self.space = elements[1]
        self.content = elements[2]


class TreeNode8(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode8, self).__init__(text, offset, elements)
        self.indent = elements[0]
        self.content = elements[1]
        self.dedent = elements[2]


class TreeNode9(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode9, self).__init__(text, offset, elements)
        self.indent = elements[0]
        self.content = elements[1]
        self.dedent = elements[2]


class TreeNode10(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode10, self).__init__(text, offset, elements)
        self.preface_marker = elements[0]
        self.content = elements[1]


class TreeNode11(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode11, self).__init__(text, offset, elements)
        self.block_element = elements[2]


class TreeNode12(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode12, self).__init__(text, offset, elements)
        self.preamble_marker = elements[0]
        self.content = elements[1]


class TreeNode13(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode13, self).__init__(text, offset, elements)
        self.block_element = elements[1]


class TreeNode14(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode14, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode15(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode15, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[2]


class TreeNode16(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode16, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode17(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode17, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[2]


class TreeNode18(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode18, self).__init__(text, offset, elements)
        self.conclusions_marker = elements[0]
        self.content = elements[1]


class TreeNode19(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode19, self).__init__(text, offset, elements)
        self.block_element = elements[1]


class TreeNode20(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode20, self).__init__(text, offset, elements)
        self.introduction_marker = elements[0]
        self.content = elements[1]


class TreeNode21(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode21, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[7]


class TreeNode22(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode22, self).__init__(text, offset, elements)
        self.background_marker = elements[0]
        self.content = elements[1]


class TreeNode23(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode23, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[6]


class TreeNode24(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode24, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode25(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode25, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[5]


class TreeNode26(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode26, self).__init__(text, offset, elements)
        self.remedies_marker = elements[0]
        self.content = elements[1]


class TreeNode27(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode27, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[4]


class TreeNode28(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode28, self).__init__(text, offset, elements)
        self.motivation_marker = elements[0]
        self.content = elements[1]


class TreeNode29(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode29, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[3]


class TreeNode30(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode30, self).__init__(text, offset, elements)
        self.decision_marker = elements[0]
        self.content = elements[1]


class TreeNode31(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode31, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[2]


class TreeNode32(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode32, self).__init__(text, offset, elements)
        self.attachment_marker = elements[0]
        self.heading = elements[1]
        self.eol = elements[2]
        self.indented = elements[3]
        self.content = elements[4]


class TreeNode33(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode33, self).__init__(text, offset, elements)
        self.indent = elements[0]
        self.subheading = elements[1]
        self.content = elements[2]
        self.dedent = elements[3]


class TreeNode34(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode34, self).__init__(text, offset, elements)
        self.hier_block_indent = elements[1]


class TreeNode35(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode35, self).__init__(text, offset, elements)
        self.space = elements[0]
        self.content = elements[1]


class TreeNode36(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode36, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode37(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode37, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode38(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode38, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode39(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode39, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode40(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode40, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode41(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode41, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode42(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode42, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode43(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode43, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode44(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode44, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode45(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode45, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode46(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode46, self).__init__(text, offset, elements)
        self.indent = elements[0]
        self.content = elements[1]
        self.dedent = elements[2]


class TreeNode47(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode47, self).__init__(text, offset, elements)
        self.num = elements[0]
        self.preamble = elements[1]
        self.children = elements[2]


class TreeNode48(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode48, self).__init__(text, offset, elements)
        self.space = elements[0]
        self.block_elements = elements[2]


class TreeNode49(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode49, self).__init__(text, offset, elements)
        self.indent = elements[0]
        self.content = elements[1]
        self.dedent = elements[2]


class TreeNode50(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode50, self).__init__(text, offset, elements)
        self.space = elements[1]
        self.content = elements[2]
        self.eol = elements[3]


class TreeNode51(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode51, self).__init__(text, offset, elements)
        self.space = elements[1]
        self.content = elements[2]
        self.eol = elements[3]


class TreeNode52(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode52, self).__init__(text, offset, elements)
        self.space = elements[1]
        self.content = elements[2]
        self.eol = elements[3]


class TreeNode53(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode53, self).__init__(text, offset, elements)
        self.content = elements[1]
        self.eol = elements[2]


class TreeNode54(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode54, self).__init__(text, offset, elements)
        self.attrs = elements[1]
        self.eol = elements[2]
        self.indent = elements[3]
        self.rows = elements[4]
        self.dedent = elements[5]


class TreeNode55(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode55, self).__init__(text, offset, elements)
        self.eol = elements[1]
        self.indent = elements[2]
        self.cells = elements[3]
        self.dedent = elements[4]


class TreeNode56(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode56, self).__init__(text, offset, elements)
        self.name = elements[0]
        self.attrs = elements[1]
        self.eol = elements[2]
        self.content = elements[3]


class TreeNode57(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode57, self).__init__(text, offset, elements)
        self.indent = elements[0]
        self.content = elements[1]
        self.dedent = elements[2]


class TreeNode58(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode58, self).__init__(text, offset, elements)
        self.first = elements[1]
        self.rest = elements[3]


class TreeNode59(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode59, self).__init__(text, offset, elements)
        self.attr = elements[2]


class TreeNode60(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode60, self).__init__(text, offset, elements)
        self.attr_name = elements[0]
        self.value = elements[1]


class TreeNode61(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode61, self).__init__(text, offset, elements)
        self.space = elements[0]
        self.attr_value = elements[1]


class TreeNode62(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode62, self).__init__(text, offset, elements)
        self.attrs = elements[1]
        self.eol = elements[2]
        self.indent = elements[3]
        self.content = elements[4]
        self.dedent = elements[5]


class TreeNode63(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode63, self).__init__(text, offset, elements)
        self.space = elements[1]
        self.marker = elements[2]
        self.eol = elements[4]
        self.indent = elements[5]
        self.content = elements[6]
        self.dedent = elements[7]


class TreeNode64(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode64, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode65(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode65, self).__init__(text, offset, elements)
        self.inline = elements[1]


class TreeNode66(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode66, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode67(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode67, self).__init__(text, offset, elements)
        self.inline = elements[1]


class TreeNode68(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode68, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode69(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode69, self).__init__(text, offset, elements)
        self.inline = elements[1]


class TreeNode70(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode70, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode71(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode71, self).__init__(text, offset, elements)
        self.inline = elements[1]


class TreeNode72(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode72, self).__init__(text, offset, elements)
        self.href = elements[2]
        self.content = elements[3]


class TreeNode73(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode73, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode74(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode74, self).__init__(text, offset, elements)
        self.inline = elements[1]


class TreeNode75(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode75, self).__init__(text, offset, elements)
        self.content = elements[1]


class TreeNode76(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode76, self).__init__(text, offset, elements)
        self.inline = elements[1]


class TreeNode77(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode77, self).__init__(text, offset, elements)
        self.href = elements[1]
        self.content = elements[3]


class TreeNode78(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode78, self).__init__(text, offset, elements)
        self.inline = elements[1]


class TreeNode79(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode79, self).__init__(text, offset, elements)
        self.space = elements[1]
        self.marker = elements[2]


class TreeNode80(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode80, self).__init__(text, offset, elements)
        self.newline = elements[0]


class TreeNode81(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode81, self).__init__(text, offset, elements)
        self.eol = elements[1]


class TreeNode82(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode82, self).__init__(text, offset, elements)
        self.eol = elements[1]


class ParseError(SyntaxError):
    pass


FAILURE = object()


class Grammar(object):
    REGEX_1 = re.compile('^[^\\n-]')
    REGEX_2 = re.compile('^[^)]')
    REGEX_3 = re.compile('^[^ \\n|}]')
    REGEX_4 = re.compile('^[^\\n|}]')
    REGEX_5 = re.compile('^[^ \\n]')
    REGEX_6 = re.compile('^[^\\n]')
    REGEX_7 = re.compile('^[^ \\n]')
    REGEX_8 = re.compile('^[^\\n]')
    REGEX_9 = re.compile('^[^ \\n]')
    REGEX_10 = re.compile('^[^\\n]')

    def _read_root(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['root'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0, max0 = None, self._offset + 4
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'noop':
            address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
            self._offset = self._offset + 4
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'noop\'')
        self._cache['root'][index0] = (address0, self._offset)
        return address0

    def _read_judgment(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['judgment'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_judgment_body()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_conclusions()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                index3 = self._offset
                address3 = self._read_attachments()
                if address3 is FAILURE:
                    address3 = TreeNode(self._input[index3:index3], index3, [])
                    self._offset = index3
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode1(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Judgment', (cls0, self._types.Judgment), {})
        self._cache['judgment'][index0] = (address0, self._offset)
        return address0

    def _read_judgment_body(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['judgment_body'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_introduction()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2, [])
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            address2 = self._read_background()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index3:index3], index3, [])
                self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                index4 = self._offset
                address3 = self._read_arguments()
                if address3 is FAILURE:
                    address3 = TreeNode(self._input[index4:index4], index4, [])
                    self._offset = index4
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index5 = self._offset
                    address4 = self._read_remedies()
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index5:index5], index5, [])
                        self._offset = index5
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index6 = self._offset
                        address5 = self._read_motivation()
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index6:index6], index6, [])
                            self._offset = index6
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index7 = self._offset
                            address6 = self._read_decision()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index7:index7], index7, [])
                                self._offset = index7
                            if address6 is not FAILURE:
                                elements0.append(address6)
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode2(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'JudgmentBody', (cls0, self._types.JudgmentBody), {})
        self._cache['judgment_body'][index0] = (address0, self._offset)
        return address0

    def _read_act(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['act'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_hierarchical_structure()
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Act', (cls0, self._types.Act), {})
        self._cache['act'][index0] = (address0, self._offset)
        return address0

    def _read_bill(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['bill'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_hierarchical_structure()
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Bill', (cls0, self._types.Bill), {})
        self._cache['bill'][index0] = (address0, self._offset)
        return address0

    def _read_hierarchical_structure(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hierarchical_structure'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_preface()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2, [])
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            address2 = self._read_preamble()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index3:index3], index3, [])
                self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_body()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index4 = self._offset
                    address4 = self._read_conclusions()
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index4:index4], index4, [])
                        self._offset = index4
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index5 = self._offset
                        address5 = self._read_attachments()
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index5:index5], index5, [])
                            self._offset = index5
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode3(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'HierarchicalStructure', (cls0, self._types.HierarchicalStructure), {})
        self._cache['hierarchical_structure'][index0] = (address0, self._offset)
        return address0

    def _read_debate_report(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['debate_report'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_open_structure()
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'DebateReport', (cls0, self._types.DebateReport), {})
        self._cache['debate_report'][index0] = (address0, self._offset)
        return address0

    def _read_doc(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['doc'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_open_structure()
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Doc', (cls0, self._types.Doc), {})
        self._cache['doc'][index0] = (address0, self._offset)
        return address0

    def _read_statement(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['statement'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_open_structure()
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Statement', (cls0, self._types.Statement), {})
        self._cache['statement'][index0] = (address0, self._offset)
        return address0

    def _read_open_structure(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['open_structure'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_preface()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2, [])
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            address2 = self._read_preamble()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index3:index3], index3, [])
                self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_main_body()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index4 = self._offset
                    address4 = self._read_conclusions()
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index4:index4], index4, [])
                        self._offset = index4
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index5 = self._offset
                        address5 = self._read_attachments()
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index5:index5], index5, [])
                            self._offset = index5
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode4(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'OpenStructure', (cls0, self._types.OpenStructure), {})
        self._cache['open_structure'][index0] = (address0, self._offset)
        return address0

    def _read_hier_element(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hier_element'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_crossheading()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_hier_element_block()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['hier_element'][index0] = (address0, self._offset)
        return address0

    def _read_hier_element_block(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hier_element_block'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_hier_element_name()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_hier_element_heading()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_eol()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_indent()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index3 = self._offset
                        address5 = self._read_subheading()
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index3:index3], index3, [])
                            self._offset = index3
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            remaining0, index4, elements1, address7 = 0, self._offset, [], True
                            while address7 is not FAILURE:
                                address7 = self._read_hier_block_element()
                                if address7 is not FAILURE:
                                    elements1.append(address7)
                                    remaining0 -= 1
                            if remaining0 <= 0:
                                address6 = TreeNode(self._input[index4:self._offset], index4, elements1)
                                self._offset = self._offset
                            else:
                                address6 = FAILURE
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address8 = FAILURE
                                address8 = self._read_dedent()
                                if address8 is not FAILURE:
                                    elements0.append(address8)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode5(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'HierElement', (cls0, self._types.HierElement), {})
        self._cache['hier_element_block'][index0] = (address0, self._offset)
        return address0

    def _read_hier_element_heading(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hier_element_heading'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_space()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 is not None and Grammar.REGEX_1.search(chunk0):
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('[^\\n-]')
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                index3 = self._offset
                index4, elements2 = self._offset, []
                address5 = FAILURE
                chunk1, max1 = None, self._offset + 1
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == '-':
                    address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address5 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'-\'')
                if address5 is not FAILURE:
                    elements2.append(address5)
                    address6 = FAILURE
                    address6 = self._read_space()
                    if address6 is not FAILURE:
                        elements2.append(address6)
                        address7 = FAILURE
                        remaining1, index5, elements3, address8 = 0, self._offset, [], True
                        while address8 is not FAILURE:
                            address8 = self._read_inline()
                            if address8 is not FAILURE:
                                elements3.append(address8)
                                remaining1 -= 1
                        if remaining1 <= 0:
                            address7 = TreeNode(self._input[index5:self._offset], index5, elements3)
                            self._offset = self._offset
                        else:
                            address7 = FAILURE
                        if address7 is not FAILURE:
                            elements2.append(address7)
                        else:
                            elements2 = None
                            self._offset = index4
                    else:
                        elements2 = None
                        self._offset = index4
                else:
                    elements2 = None
                    self._offset = index4
                if elements2 is None:
                    address4 = FAILURE
                else:
                    address4 = TreeNode7(self._input[index4:self._offset], index4, elements2)
                    self._offset = self._offset
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[index3:index3], index3, [])
                    self._offset = index3
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode6(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'HierElementHeading', (cls0, self._types.HierElementHeading), {})
        self._cache['hier_element_heading'][index0] = (address0, self._offset)
        return address0

    def _read_hier_block_element(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hier_block_element'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_hier_element()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_block_element()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['hier_block_element'][index0] = (address0, self._offset)
        return address0

    def _read_hier_indent(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hier_indent'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_indent()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_hier_element()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                address4 = self._read_dedent()
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode8(self._input[index2:self._offset], index2, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_hier_element()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['hier_indent'][index0] = (address0, self._offset)
        return address0

    def _read_hier_block_indent(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hier_block_indent'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_indent()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_hier_block_element()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                address4 = self._read_dedent()
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode9(self._input[index2:self._offset], index2, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_hier_block_element()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['hier_block_indent'][index0] = (address0, self._offset)
        return address0

    def _read_hier_element_name(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hier_element_name'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0, max0 = None, self._offset + 6
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'ALINEA':
            address0 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
            self._offset = self._offset + 6
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'ALINEA\'')
        if address0 is FAILURE:
            self._offset = index1
            chunk1, max1 = None, self._offset + 7
            if max1 <= self._input_size:
                chunk1 = self._input[self._offset:max1]
            if chunk1 == 'ARTICLE':
                address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                self._offset = self._offset + 7
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('\'ARTICLE\'')
            if address0 is FAILURE:
                self._offset = index1
                chunk2, max2 = None, self._offset + 4
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == 'BOOK':
                    address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                    self._offset = self._offset + 4
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'BOOK\'')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3, max3 = None, self._offset + 7
                    if max3 <= self._input_size:
                        chunk3 = self._input[self._offset:max3]
                    if chunk3 == 'CHAPTER':
                        address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                        self._offset = self._offset + 7
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('\'CHAPTER\'')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4, max4 = None, self._offset + 6
                        if max4 <= self._input_size:
                            chunk4 = self._input[self._offset:max4]
                        if chunk4 == 'CLAUSE':
                            address0 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                            self._offset = self._offset + 6
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('\'CLAUSE\'')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5, max5 = None, self._offset + 8
                            if max5 <= self._input_size:
                                chunk5 = self._input[self._offset:max5]
                            if chunk5 == 'DIVISION':
                                address0 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
                                self._offset = self._offset + 8
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('\'DIVISION\'')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6, max6 = None, self._offset + 6
                                if max6 <= self._input_size:
                                    chunk6 = self._input[self._offset:max6]
                                if chunk6 == 'INDENT':
                                    address0 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                                    self._offset = self._offset + 6
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('\'INDENT\'')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7, max7 = None, self._offset + 5
                                    if max7 <= self._input_size:
                                        chunk7 = self._input[self._offset:max7]
                                    if chunk7 == 'LEVEL':
                                        address0 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                                        self._offset = self._offset + 5
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('\'LEVEL\'')
                                    if address0 is FAILURE:
                                        self._offset = index1
                                        chunk8, max8 = None, self._offset + 4
                                        if max8 <= self._input_size:
                                            chunk8 = self._input[self._offset:max8]
                                        if chunk8 == 'LIST':
                                            address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                                            self._offset = self._offset + 4
                                        else:
                                            address0 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append('\'LIST\'')
                                        if address0 is FAILURE:
                                            self._offset = index1
                                            chunk9, max9 = None, self._offset + 9
                                            if max9 <= self._input_size:
                                                chunk9 = self._input[self._offset:max9]
                                            if chunk9 == 'PARAGRAPH':
                                                address0 = TreeNode(self._input[self._offset:self._offset + 9], self._offset, [])
                                                self._offset = self._offset + 9
                                            else:
                                                address0 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append('\'PARAGRAPH\'')
                                            if address0 is FAILURE:
                                                self._offset = index1
                                                chunk10, max10 = None, self._offset + 4
                                                if max10 <= self._input_size:
                                                    chunk10 = self._input[self._offset:max10]
                                                if chunk10 == 'PART':
                                                    address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                                                    self._offset = self._offset + 4
                                                else:
                                                    address0 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append('\'PART\'')
                                                if address0 is FAILURE:
                                                    self._offset = index1
                                                    chunk11, max11 = None, self._offset + 5
                                                    if max11 <= self._input_size:
                                                        chunk11 = self._input[self._offset:max11]
                                                    if chunk11 == 'POINT':
                                                        address0 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                                                        self._offset = self._offset + 5
                                                    else:
                                                        address0 = FAILURE
                                                        if self._offset > self._failure:
                                                            self._failure = self._offset
                                                            self._expected = []
                                                        if self._offset == self._failure:
                                                            self._expected.append('\'POINT\'')
                                                    if address0 is FAILURE:
                                                        self._offset = index1
                                                        chunk12, max12 = None, self._offset + 7
                                                        if max12 <= self._input_size:
                                                            chunk12 = self._input[self._offset:max12]
                                                        if chunk12 == 'PROVISO':
                                                            address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                            self._offset = self._offset + 7
                                                        else:
                                                            address0 = FAILURE
                                                            if self._offset > self._failure:
                                                                self._failure = self._offset
                                                                self._expected = []
                                                            if self._offset == self._failure:
                                                                self._expected.append('\'PROVISO\'')
                                                        if address0 is FAILURE:
                                                            self._offset = index1
                                                            chunk13, max13 = None, self._offset + 4
                                                            if max13 <= self._input_size:
                                                                chunk13 = self._input[self._offset:max13]
                                                            if chunk13 == 'RULE':
                                                                address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                                                                self._offset = self._offset + 4
                                                            else:
                                                                address0 = FAILURE
                                                                if self._offset > self._failure:
                                                                    self._failure = self._offset
                                                                    self._expected = []
                                                                if self._offset == self._failure:
                                                                    self._expected.append('\'RULE\'')
                                                            if address0 is FAILURE:
                                                                self._offset = index1
                                                                chunk14, max14 = None, self._offset + 7
                                                                if max14 <= self._input_size:
                                                                    chunk14 = self._input[self._offset:max14]
                                                                if chunk14 == 'SECTION':
                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                                    self._offset = self._offset + 7
                                                                else:
                                                                    address0 = FAILURE
                                                                    if self._offset > self._failure:
                                                                        self._failure = self._offset
                                                                        self._expected = []
                                                                    if self._offset == self._failure:
                                                                        self._expected.append('\'SECTION\'')
                                                                if address0 is FAILURE:
                                                                    self._offset = index1
                                                                    chunk15, max15 = None, self._offset + 10
                                                                    if max15 <= self._input_size:
                                                                        chunk15 = self._input[self._offset:max15]
                                                                    if chunk15 == 'SUBCHAPTER':
                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 10], self._offset, [])
                                                                        self._offset = self._offset + 10
                                                                    else:
                                                                        address0 = FAILURE
                                                                        if self._offset > self._failure:
                                                                            self._failure = self._offset
                                                                            self._expected = []
                                                                        if self._offset == self._failure:
                                                                            self._expected.append('\'SUBCHAPTER\'')
                                                                    if address0 is FAILURE:
                                                                        self._offset = index1
                                                                        chunk16, max16 = None, self._offset + 9
                                                                        if max16 <= self._input_size:
                                                                            chunk16 = self._input[self._offset:max16]
                                                                        if chunk16 == 'SUBCLAUSE':
                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 9], self._offset, [])
                                                                            self._offset = self._offset + 9
                                                                        else:
                                                                            address0 = FAILURE
                                                                            if self._offset > self._failure:
                                                                                self._failure = self._offset
                                                                                self._expected = []
                                                                            if self._offset == self._failure:
                                                                                self._expected.append('\'SUBCLAUSE\'')
                                                                        if address0 is FAILURE:
                                                                            self._offset = index1
                                                                            chunk17, max17 = None, self._offset + 11
                                                                            if max17 <= self._input_size:
                                                                                chunk17 = self._input[self._offset:max17]
                                                                            if chunk17 == 'SUBDIVISION':
                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 11], self._offset, [])
                                                                                self._offset = self._offset + 11
                                                                            else:
                                                                                address0 = FAILURE
                                                                                if self._offset > self._failure:
                                                                                    self._failure = self._offset
                                                                                    self._expected = []
                                                                                if self._offset == self._failure:
                                                                                    self._expected.append('\'SUBDIVISION\'')
                                                                            if address0 is FAILURE:
                                                                                self._offset = index1
                                                                                chunk18, max18 = None, self._offset + 7
                                                                                if max18 <= self._input_size:
                                                                                    chunk18 = self._input[self._offset:max18]
                                                                                if chunk18 == 'SUBLIST':
                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                                                    self._offset = self._offset + 7
                                                                                else:
                                                                                    address0 = FAILURE
                                                                                    if self._offset > self._failure:
                                                                                        self._failure = self._offset
                                                                                        self._expected = []
                                                                                    if self._offset == self._failure:
                                                                                        self._expected.append('\'SUBLIST\'')
                                                                                if address0 is FAILURE:
                                                                                    self._offset = index1
                                                                                    chunk19, max19 = None, self._offset + 12
                                                                                    if max19 <= self._input_size:
                                                                                        chunk19 = self._input[self._offset:max19]
                                                                                    if chunk19 == 'SUBPARAGRAPH':
                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 12], self._offset, [])
                                                                                        self._offset = self._offset + 12
                                                                                    else:
                                                                                        address0 = FAILURE
                                                                                        if self._offset > self._failure:
                                                                                            self._failure = self._offset
                                                                                            self._expected = []
                                                                                        if self._offset == self._failure:
                                                                                            self._expected.append('\'SUBPARAGRAPH\'')
                                                                                    if address0 is FAILURE:
                                                                                        self._offset = index1
                                                                                        chunk20, max20 = None, self._offset + 7
                                                                                        if max20 <= self._input_size:
                                                                                            chunk20 = self._input[self._offset:max20]
                                                                                        if chunk20 == 'SUBPART':
                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                                                            self._offset = self._offset + 7
                                                                                        else:
                                                                                            address0 = FAILURE
                                                                                            if self._offset > self._failure:
                                                                                                self._failure = self._offset
                                                                                                self._expected = []
                                                                                            if self._offset == self._failure:
                                                                                                self._expected.append('\'SUBPART\'')
                                                                                        if address0 is FAILURE:
                                                                                            self._offset = index1
                                                                                            chunk21, max21 = None, self._offset + 7
                                                                                            if max21 <= self._input_size:
                                                                                                chunk21 = self._input[self._offset:max21]
                                                                                            if chunk21 == 'SUBRULE':
                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                                                                self._offset = self._offset + 7
                                                                                            else:
                                                                                                address0 = FAILURE
                                                                                                if self._offset > self._failure:
                                                                                                    self._failure = self._offset
                                                                                                    self._expected = []
                                                                                                if self._offset == self._failure:
                                                                                                    self._expected.append('\'SUBRULE\'')
                                                                                            if address0 is FAILURE:
                                                                                                self._offset = index1
                                                                                                chunk22, max22 = None, self._offset + 10
                                                                                                if max22 <= self._input_size:
                                                                                                    chunk22 = self._input[self._offset:max22]
                                                                                                if chunk22 == 'SUBSECTION':
                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 10], self._offset, [])
                                                                                                    self._offset = self._offset + 10
                                                                                                else:
                                                                                                    address0 = FAILURE
                                                                                                    if self._offset > self._failure:
                                                                                                        self._failure = self._offset
                                                                                                        self._expected = []
                                                                                                    if self._offset == self._failure:
                                                                                                        self._expected.append('\'SUBSECTION\'')
                                                                                                if address0 is FAILURE:
                                                                                                    self._offset = index1
                                                                                                    chunk23, max23 = None, self._offset + 8
                                                                                                    if max23 <= self._input_size:
                                                                                                        chunk23 = self._input[self._offset:max23]
                                                                                                    if chunk23 == 'SUBTITLE':
                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
                                                                                                        self._offset = self._offset + 8
                                                                                                    else:
                                                                                                        address0 = FAILURE
                                                                                                        if self._offset > self._failure:
                                                                                                            self._failure = self._offset
                                                                                                            self._expected = []
                                                                                                        if self._offset == self._failure:
                                                                                                            self._expected.append('\'SUBTITLE\'')
                                                                                                    if address0 is FAILURE:
                                                                                                        self._offset = index1
                                                                                                        chunk24, max24 = None, self._offset + 5
                                                                                                        if max24 <= self._input_size:
                                                                                                            chunk24 = self._input[self._offset:max24]
                                                                                                        if chunk24 == 'TITLE':
                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                                                                                                            self._offset = self._offset + 5
                                                                                                        else:
                                                                                                            address0 = FAILURE
                                                                                                            if self._offset > self._failure:
                                                                                                                self._failure = self._offset
                                                                                                                self._expected = []
                                                                                                            if self._offset == self._failure:
                                                                                                                self._expected.append('\'TITLE\'')
                                                                                                        if address0 is FAILURE:
                                                                                                            self._offset = index1
                                                                                                            chunk25, max25 = None, self._offset + 4
                                                                                                            if max25 <= self._input_size:
                                                                                                                chunk25 = self._input[self._offset:max25]
                                                                                                            if chunk25 == 'TOME':
                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                                                                                                                self._offset = self._offset + 4
                                                                                                            else:
                                                                                                                address0 = FAILURE
                                                                                                                if self._offset > self._failure:
                                                                                                                    self._failure = self._offset
                                                                                                                    self._expected = []
                                                                                                                if self._offset == self._failure:
                                                                                                                    self._expected.append('\'TOME\'')
                                                                                                            if address0 is FAILURE:
                                                                                                                self._offset = index1
                                                                                                                chunk26, max26 = None, self._offset + 12
                                                                                                                if max26 <= self._input_size:
                                                                                                                    chunk26 = self._input[self._offset:max26]
                                                                                                                if chunk26 == 'TRANSITIONAL':
                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 12], self._offset, [])
                                                                                                                    self._offset = self._offset + 12
                                                                                                                else:
                                                                                                                    address0 = FAILURE
                                                                                                                    if self._offset > self._failure:
                                                                                                                        self._failure = self._offset
                                                                                                                        self._expected = []
                                                                                                                    if self._offset == self._failure:
                                                                                                                        self._expected.append('\'TRANSITIONAL\'')
                                                                                                                if address0 is FAILURE:
                                                                                                                    self._offset = index1
                                                                                                                    chunk27, max27 = None, self._offset + 3
                                                                                                                    if max27 <= self._input_size:
                                                                                                                        chunk27 = self._input[self._offset:max27]
                                                                                                                    if chunk27 == 'ART':
                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
                                                                                                                        self._offset = self._offset + 3
                                                                                                                    else:
                                                                                                                        address0 = FAILURE
                                                                                                                        if self._offset > self._failure:
                                                                                                                            self._failure = self._offset
                                                                                                                            self._expected = []
                                                                                                                        if self._offset == self._failure:
                                                                                                                            self._expected.append('\'ART\'')
                                                                                                                    if address0 is FAILURE:
                                                                                                                        self._offset = index1
                                                                                                                        chunk28, max28 = None, self._offset + 4
                                                                                                                        if max28 <= self._input_size:
                                                                                                                            chunk28 = self._input[self._offset:max28]
                                                                                                                        if chunk28 == 'CHAP':
                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                                                                                                                            self._offset = self._offset + 4
                                                                                                                        else:
                                                                                                                            address0 = FAILURE
                                                                                                                            if self._offset > self._failure:
                                                                                                                                self._failure = self._offset
                                                                                                                                self._expected = []
                                                                                                                            if self._offset == self._failure:
                                                                                                                                self._expected.append('\'CHAP\'')
                                                                                                                        if address0 is FAILURE:
                                                                                                                            self._offset = index1
                                                                                                                            chunk29, max29 = None, self._offset + 4
                                                                                                                            if max29 <= self._input_size:
                                                                                                                                chunk29 = self._input[self._offset:max29]
                                                                                                                            if chunk29 == 'PARA':
                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                                                                                                                                self._offset = self._offset + 4
                                                                                                                            else:
                                                                                                                                address0 = FAILURE
                                                                                                                                if self._offset > self._failure:
                                                                                                                                    self._failure = self._offset
                                                                                                                                    self._expected = []
                                                                                                                                if self._offset == self._failure:
                                                                                                                                    self._expected.append('\'PARA\'')
                                                                                                                            if address0 is FAILURE:
                                                                                                                                self._offset = index1
                                                                                                                                chunk30, max30 = None, self._offset + 3
                                                                                                                                if max30 <= self._input_size:
                                                                                                                                    chunk30 = self._input[self._offset:max30]
                                                                                                                                if chunk30 == 'SEC':
                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
                                                                                                                                    self._offset = self._offset + 3
                                                                                                                                else:
                                                                                                                                    address0 = FAILURE
                                                                                                                                    if self._offset > self._failure:
                                                                                                                                        self._failure = self._offset
                                                                                                                                        self._expected = []
                                                                                                                                    if self._offset == self._failure:
                                                                                                                                        self._expected.append('\'SEC\'')
                                                                                                                                if address0 is FAILURE:
                                                                                                                                    self._offset = index1
                                                                                                                                    chunk31, max31 = None, self._offset + 7
                                                                                                                                    if max31 <= self._input_size:
                                                                                                                                        chunk31 = self._input[self._offset:max31]
                                                                                                                                    if chunk31 == 'SUBCHAP':
                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                                                                                                        self._offset = self._offset + 7
                                                                                                                                    else:
                                                                                                                                        address0 = FAILURE
                                                                                                                                        if self._offset > self._failure:
                                                                                                                                            self._failure = self._offset
                                                                                                                                            self._expected = []
                                                                                                                                        if self._offset == self._failure:
                                                                                                                                            self._expected.append('\'SUBCHAP\'')
                                                                                                                                    if address0 is FAILURE:
                                                                                                                                        self._offset = index1
                                                                                                                                        chunk32, max32 = None, self._offset + 7
                                                                                                                                        if max32 <= self._input_size:
                                                                                                                                            chunk32 = self._input[self._offset:max32]
                                                                                                                                        if chunk32 == 'SUBPARA':
                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                                                                                                            self._offset = self._offset + 7
                                                                                                                                        else:
                                                                                                                                            address0 = FAILURE
                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                self._failure = self._offset
                                                                                                                                                self._expected = []
                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                self._expected.append('\'SUBPARA\'')
                                                                                                                                        if address0 is FAILURE:
                                                                                                                                            self._offset = index1
                                                                                                                                            chunk33, max33 = None, self._offset + 6
                                                                                                                                            if max33 <= self._input_size:
                                                                                                                                                chunk33 = self._input[self._offset:max33]
                                                                                                                                            if chunk33 == 'SUBSEC':
                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                                                                                                                                                self._offset = self._offset + 6
                                                                                                                                            else:
                                                                                                                                                address0 = FAILURE
                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                    self._failure = self._offset
                                                                                                                                                    self._expected = []
                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                    self._expected.append('\'SUBSEC\'')
                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                self._offset = index1
        self._cache['hier_element_name'][index0] = (address0, self._offset)
        return address0

    def _read_preface(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['preface'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_preface_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_preamble_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index5 = self._offset
                    address5 = self._read_body_marker()
                    self._offset = index5
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        address6 = self._read_block_element()
                        if address6 is not FAILURE:
                            elements2.append(address6)
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode11(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode10(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Preface', (cls0, self._types.Preface), {})
        self._cache['preface'][index0] = (address0, self._offset)
        return address0

    def _read_preamble(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['preamble'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_preamble_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_body_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_block_element()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode13(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode12(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Preamble', (cls0, self._types.Preamble), {})
        self._cache['preamble'][index0] = (address0, self._offset)
        return address0

    def _read_body(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['body'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_body_marker()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2, [])
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index4, elements2 = self._offset, []
                address4 = FAILURE
                index5 = self._offset
                address4 = self._read_conclusions_marker()
                self._offset = index5
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index6 = self._offset
                    address5 = self._read_attachment_marker()
                    self._offset = index6
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        address6 = self._read_hier_block_indent()
                        if address6 is not FAILURE:
                            elements2.append(address6)
                        else:
                            elements2 = None
                            self._offset = index4
                    else:
                        elements2 = None
                        self._offset = index4
                else:
                    elements2 = None
                    self._offset = index4
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode15(self._input[index4:self._offset], index4, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode14(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Body', (cls0, self._types.Body), {})
        self._cache['body'][index0] = (address0, self._offset)
        return address0

    def _read_main_body(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['main_body'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_body_marker()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2, [])
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index4, elements2 = self._offset, []
                address4 = FAILURE
                index5 = self._offset
                address4 = self._read_conclusions_marker()
                self._offset = index5
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index6 = self._offset
                    address5 = self._read_attachment_marker()
                    self._offset = index6
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        address6 = self._read_hier_block_indent()
                        if address6 is not FAILURE:
                            elements2.append(address6)
                        else:
                            elements2 = None
                            self._offset = index4
                    else:
                        elements2 = None
                        self._offset = index4
                else:
                    elements2 = None
                    self._offset = index4
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode17(self._input[index4:self._offset], index4, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode16(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'MainBody', (cls0, self._types.MainBody), {})
        self._cache['main_body'][index0] = (address0, self._offset)
        return address0

    def _read_conclusions(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['conclusions'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_conclusions_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_attachment_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_block_element()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode19(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode18(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Conclusions', (cls0, self._types.Conclusions), {})
        self._cache['conclusions'][index0] = (address0, self._offset)
        return address0

    def _read_introduction(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['introduction'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_introduction_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_background_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index5 = self._offset
                    address5 = self._read_arguments_marker()
                    self._offset = index5
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        index6 = self._offset
                        address6 = self._read_remedies_marker()
                        self._offset = index6
                        if address6 is FAILURE:
                            address6 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            index7 = self._offset
                            address7 = self._read_motivation_marker()
                            self._offset = index7
                            if address7 is FAILURE:
                                address7 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                self._offset = self._offset
                            else:
                                address7 = FAILURE
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                address8 = FAILURE
                                index8 = self._offset
                                address8 = self._read_decision_marker()
                                self._offset = index8
                                if address8 is FAILURE:
                                    address8 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                    self._offset = self._offset
                                else:
                                    address8 = FAILURE
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                    address9 = FAILURE
                                    index9 = self._offset
                                    address9 = self._read_conclusions_marker()
                                    self._offset = index9
                                    if address9 is FAILURE:
                                        address9 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                        self._offset = self._offset
                                    else:
                                        address9 = FAILURE
                                    if address9 is not FAILURE:
                                        elements2.append(address9)
                                        address10 = FAILURE
                                        index10 = self._offset
                                        address10 = self._read_attachment_marker()
                                        self._offset = index10
                                        if address10 is FAILURE:
                                            address10 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                            self._offset = self._offset
                                        else:
                                            address10 = FAILURE
                                        if address10 is not FAILURE:
                                            elements2.append(address10)
                                            address11 = FAILURE
                                            address11 = self._read_hier_block_indent()
                                            if address11 is not FAILURE:
                                                elements2.append(address11)
                                            else:
                                                elements2 = None
                                                self._offset = index3
                                        else:
                                            elements2 = None
                                            self._offset = index3
                                    else:
                                        elements2 = None
                                        self._offset = index3
                                else:
                                    elements2 = None
                                    self._offset = index3
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode21(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode20(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Introduction', (cls0, self._types.Introduction), {})
        self._cache['introduction'][index0] = (address0, self._offset)
        return address0

    def _read_background(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['background'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_background_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_arguments_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index5 = self._offset
                    address5 = self._read_remedies_marker()
                    self._offset = index5
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        index6 = self._offset
                        address6 = self._read_motivation_marker()
                        self._offset = index6
                        if address6 is FAILURE:
                            address6 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            index7 = self._offset
                            address7 = self._read_decision_marker()
                            self._offset = index7
                            if address7 is FAILURE:
                                address7 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                self._offset = self._offset
                            else:
                                address7 = FAILURE
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                address8 = FAILURE
                                index8 = self._offset
                                address8 = self._read_conclusions_marker()
                                self._offset = index8
                                if address8 is FAILURE:
                                    address8 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                    self._offset = self._offset
                                else:
                                    address8 = FAILURE
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                    address9 = FAILURE
                                    index9 = self._offset
                                    address9 = self._read_attachment_marker()
                                    self._offset = index9
                                    if address9 is FAILURE:
                                        address9 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                        self._offset = self._offset
                                    else:
                                        address9 = FAILURE
                                    if address9 is not FAILURE:
                                        elements2.append(address9)
                                        address10 = FAILURE
                                        address10 = self._read_hier_block_indent()
                                        if address10 is not FAILURE:
                                            elements2.append(address10)
                                        else:
                                            elements2 = None
                                            self._offset = index3
                                    else:
                                        elements2 = None
                                        self._offset = index3
                                else:
                                    elements2 = None
                                    self._offset = index3
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode23(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode22(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Background', (cls0, self._types.Background), {})
        self._cache['background'][index0] = (address0, self._offset)
        return address0

    def _read_arguments(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['arguments'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_arguments_marker()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2, [])
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index4, elements2 = self._offset, []
                address4 = FAILURE
                index5 = self._offset
                address4 = self._read_remedies_marker()
                self._offset = index5
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index6 = self._offset
                    address5 = self._read_motivation_marker()
                    self._offset = index6
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        index7 = self._offset
                        address6 = self._read_decision_marker()
                        self._offset = index7
                        if address6 is FAILURE:
                            address6 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            index8 = self._offset
                            address7 = self._read_conclusions_marker()
                            self._offset = index8
                            if address7 is FAILURE:
                                address7 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                self._offset = self._offset
                            else:
                                address7 = FAILURE
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                address8 = FAILURE
                                index9 = self._offset
                                address8 = self._read_attachment_marker()
                                self._offset = index9
                                if address8 is FAILURE:
                                    address8 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                    self._offset = self._offset
                                else:
                                    address8 = FAILURE
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                    address9 = FAILURE
                                    address9 = self._read_hier_block_indent()
                                    if address9 is not FAILURE:
                                        elements2.append(address9)
                                    else:
                                        elements2 = None
                                        self._offset = index4
                                else:
                                    elements2 = None
                                    self._offset = index4
                            else:
                                elements2 = None
                                self._offset = index4
                        else:
                            elements2 = None
                            self._offset = index4
                    else:
                        elements2 = None
                        self._offset = index4
                else:
                    elements2 = None
                    self._offset = index4
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode25(self._input[index4:self._offset], index4, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode24(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Arguments', (cls0, self._types.Arguments), {})
        self._cache['arguments'][index0] = (address0, self._offset)
        return address0

    def _read_remedies(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['remedies'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_remedies_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_motivation_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index5 = self._offset
                    address5 = self._read_decision_marker()
                    self._offset = index5
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        index6 = self._offset
                        address6 = self._read_conclusions_marker()
                        self._offset = index6
                        if address6 is FAILURE:
                            address6 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            index7 = self._offset
                            address7 = self._read_attachment_marker()
                            self._offset = index7
                            if address7 is FAILURE:
                                address7 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                self._offset = self._offset
                            else:
                                address7 = FAILURE
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                address8 = FAILURE
                                address8 = self._read_hier_block_indent()
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                else:
                                    elements2 = None
                                    self._offset = index3
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode27(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode26(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Remedies', (cls0, self._types.Remedies), {})
        self._cache['remedies'][index0] = (address0, self._offset)
        return address0

    def _read_motivation(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['motivation'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_motivation_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_decision_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index5 = self._offset
                    address5 = self._read_conclusions_marker()
                    self._offset = index5
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        index6 = self._offset
                        address6 = self._read_attachment_marker()
                        self._offset = index6
                        if address6 is FAILURE:
                            address6 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            address7 = self._read_hier_block_indent()
                            if address7 is not FAILURE:
                                elements2.append(address7)
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode29(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode28(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Motivation', (cls0, self._types.Motivation), {})
        self._cache['motivation'][index0] = (address0, self._offset)
        return address0

    def _read_decision(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['decision'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_decision_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                address4 = self._read_conclusions_marker()
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    index5 = self._offset
                    address5 = self._read_attachment_marker()
                    self._offset = index5
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        address6 = self._read_hier_block_indent()
                        if address6 is not FAILURE:
                            elements2.append(address6)
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode31(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode30(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Decision', (cls0, self._types.Decision), {})
        self._cache['decision'][index0] = (address0, self._offset)
        return address0

    def _read_attachments(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['attachments'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            address1 = self._read_attachment()
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Attachments', (cls0, self._types.Attachments), {})
        self._cache['attachments'][index0] = (address0, self._offset)
        return address0

    def _read_attachment(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['attachment'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_attachment_marker()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_attachment_heading()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_eol()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index3 = self._offset
                    index4, elements1 = self._offset, []
                    address5 = FAILURE
                    address5 = self._read_indent()
                    if address5 is not FAILURE:
                        elements1.append(address5)
                        address6 = FAILURE
                        index5 = self._offset
                        address6 = self._read_subheading()
                        if address6 is FAILURE:
                            address6 = TreeNode(self._input[index5:index5], index5, [])
                            self._offset = index5
                        if address6 is not FAILURE:
                            elements1.append(address6)
                            address7 = FAILURE
                            remaining0, index6, elements2, address8 = 0, self._offset, [], True
                            while address8 is not FAILURE:
                                address8 = self._read_hier_block_element()
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                    remaining0 -= 1
                            if remaining0 <= 0:
                                address7 = TreeNode(self._input[index6:self._offset], index6, elements2)
                                self._offset = self._offset
                            else:
                                address7 = FAILURE
                            if address7 is not FAILURE:
                                elements1.append(address7)
                                address9 = FAILURE
                                address9 = self._read_dedent()
                                if address9 is not FAILURE:
                                    elements1.append(address9)
                                else:
                                    elements1 = None
                                    self._offset = index4
                            else:
                                elements1 = None
                                self._offset = index4
                        else:
                            elements1 = None
                            self._offset = index4
                    else:
                        elements1 = None
                        self._offset = index4
                    if elements1 is None:
                        address4 = FAILURE
                    else:
                        address4 = TreeNode33(self._input[index4:self._offset], index4, elements1)
                        self._offset = self._offset
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index3:index3], index3, [])
                        self._offset = index3
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address10 = FAILURE
                        remaining1, index7, elements3, address11 = 0, self._offset, [], True
                        while address11 is not FAILURE:
                            index8, elements4 = self._offset, []
                            address12 = FAILURE
                            index9 = self._offset
                            address12 = self._read_attachment_marker()
                            self._offset = index9
                            if address12 is FAILURE:
                                address12 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                self._offset = self._offset
                            else:
                                address12 = FAILURE
                            if address12 is not FAILURE:
                                elements4.append(address12)
                                address13 = FAILURE
                                address13 = self._read_hier_block_indent()
                                if address13 is not FAILURE:
                                    elements4.append(address13)
                                else:
                                    elements4 = None
                                    self._offset = index8
                            else:
                                elements4 = None
                                self._offset = index8
                            if elements4 is None:
                                address11 = FAILURE
                            else:
                                address11 = TreeNode34(self._input[index8:self._offset], index8, elements4)
                                self._offset = self._offset
                            if address11 is not FAILURE:
                                elements3.append(address11)
                                remaining1 -= 1
                        if remaining1 <= 0:
                            address10 = TreeNode(self._input[index7:self._offset], index7, elements3)
                            self._offset = self._offset
                        else:
                            address10 = FAILURE
                        if address10 is not FAILURE:
                            elements0.append(address10)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode32(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Attachment', (cls0, self._types.Attachment), {})
        self._cache['attachment'][index0] = (address0, self._offset)
        return address0

    def _read_attachment_heading(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['attachment_heading'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_space()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_inline()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode35(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'AttachmentHeading', (cls0, self._types.AttachmentHeading), {})
        self._cache['attachment_heading'][index0] = (address0, self._offset)
        return address0

    def _read_body_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['body_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 4
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'BODY':
            address1 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
            self._offset = self._offset + 4
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'BODY\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode36(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['body_marker'][index0] = (address0, self._offset)
        return address0

    def _read_conclusions_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['conclusions_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 11
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'CONCLUSIONS':
            address1 = TreeNode(self._input[self._offset:self._offset + 11], self._offset, [])
            self._offset = self._offset + 11
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'CONCLUSIONS\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode37(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['conclusions_marker'][index0] = (address0, self._offset)
        return address0

    def _read_preamble_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['preamble_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 8
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'PREAMBLE':
            address1 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
            self._offset = self._offset + 8
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'PREAMBLE\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode38(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['preamble_marker'][index0] = (address0, self._offset)
        return address0

    def _read_preface_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['preface_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 7
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'PREFACE':
            address1 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
            self._offset = self._offset + 7
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'PREFACE\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode39(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['preface_marker'][index0] = (address0, self._offset)
        return address0

    def _read_introduction_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['introduction_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 12
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'INTRODUCTION':
            address1 = TreeNode(self._input[self._offset:self._offset + 12], self._offset, [])
            self._offset = self._offset + 12
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'INTRODUCTION\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode40(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['introduction_marker'][index0] = (address0, self._offset)
        return address0

    def _read_background_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['background_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 10
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'BACKGROUND':
            address1 = TreeNode(self._input[self._offset:self._offset + 10], self._offset, [])
            self._offset = self._offset + 10
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'BACKGROUND\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode41(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['background_marker'][index0] = (address0, self._offset)
        return address0

    def _read_arguments_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['arguments_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 9
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'ARGUMENTS':
            address1 = TreeNode(self._input[self._offset:self._offset + 9], self._offset, [])
            self._offset = self._offset + 9
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'ARGUMENTS\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode42(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['arguments_marker'][index0] = (address0, self._offset)
        return address0

    def _read_remedies_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['remedies_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 8
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'REMEDIES':
            address1 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
            self._offset = self._offset + 8
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'REMEDIES\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode43(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['remedies_marker'][index0] = (address0, self._offset)
        return address0

    def _read_motivation_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['motivation_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 10
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'MOTIVATION':
            address1 = TreeNode(self._input[self._offset:self._offset + 10], self._offset, [])
            self._offset = self._offset + 10
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'MOTIVATION\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode44(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['motivation_marker'][index0] = (address0, self._offset)
        return address0

    def _read_decision_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['decision_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 8
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'DECISION':
            address1 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
            self._offset = self._offset + 8
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'DECISION\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode45(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['decision_marker'][index0] = (address0, self._offset)
        return address0

    def _read_attachment_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['attachment_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0, max0 = None, self._offset + 10
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'ATTACHMENT':
            address0 = TreeNode(self._input[self._offset:self._offset + 10], self._offset, [])
            self._offset = self._offset + 10
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'ATTACHMENT\'')
        if address0 is FAILURE:
            self._offset = index1
            chunk1, max1 = None, self._offset + 8
            if max1 <= self._input_size:
                chunk1 = self._input[self._offset:max1]
            if chunk1 == 'APPENDIX':
                address0 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
                self._offset = self._offset + 8
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('\'APPENDIX\'')
            if address0 is FAILURE:
                self._offset = index1
                chunk2, max2 = None, self._offset + 8
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == 'SCHEDULE':
                    address0 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
                    self._offset = self._offset + 8
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'SCHEDULE\'')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3, max3 = None, self._offset + 8
                    if max3 <= self._input_size:
                        chunk3 = self._input[self._offset:max3]
                    if chunk3 == 'ANNEXURE':
                        address0 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
                        self._offset = self._offset + 8
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('\'ANNEXURE\'')
                    if address0 is FAILURE:
                        self._offset = index1
        self._cache['attachment_marker'][index0] = (address0, self._offset)
        return address0

    def _read_block_element(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['block_element'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_nested_block_element()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_block_elements()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['block_element'][index0] = (address0, self._offset)
        return address0

    def _read_nested_block_element(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['nested_block_element'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_indent()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_block_element()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                address4 = self._read_dedent()
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode46(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'NestedBlockElement', (cls0, self._types.NestedBlockElement), {})
        self._cache['nested_block_element'][index0] = (address0, self._offset)
        return address0

    def _read_block_elements(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['block_elements'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_block_list()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_table()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_longtitle()
                if address0 is FAILURE:
                    self._offset = index1
                    address0 = self._read_footnote()
                    if address0 is FAILURE:
                        self._offset = index1
                        address0 = self._read_embedded_structure()
                        if address0 is FAILURE:
                            self._offset = index1
                            address0 = self._read_line()
                            if address0 is FAILURE:
                                self._offset = index1
        self._cache['block_elements'][index0] = (address0, self._offset)
        return address0

    def _read_block_list(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['block_list'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            address1 = self._read_block_item()
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'BlockList', (cls0, self._types.BlockList), {})
        self._cache['block_list'][index0] = (address0, self._offset)
        return address0

    def _read_block_item(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['block_item'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2, elements1 = self._offset, []
        address2 = FAILURE
        chunk0, max0 = None, self._offset + 1
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '(':
            address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
            self._offset = self._offset + 1
        else:
            address2 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'(\'')
        if address2 is not FAILURE:
            elements1.append(address2)
            address3 = FAILURE
            remaining0, index3, elements2, address4 = 1, self._offset, [], True
            while address4 is not FAILURE:
                chunk1, max1 = None, self._offset + 1
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 is not None and Grammar.REGEX_2.search(chunk1):
                    address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('[^)]')
                if address4 is not FAILURE:
                    elements2.append(address4)
                    remaining0 -= 1
            if remaining0 <= 0:
                address3 = TreeNode(self._input[index3:self._offset], index3, elements2)
                self._offset = self._offset
            else:
                address3 = FAILURE
            if address3 is not FAILURE:
                elements1.append(address3)
                address5 = FAILURE
                chunk2, max2 = None, self._offset + 1
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == ')':
                    address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address5 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\')\'')
                if address5 is not FAILURE:
                    elements1.append(address5)
                else:
                    elements1 = None
                    self._offset = index2
            else:
                elements1 = None
                self._offset = index2
        else:
            elements1 = None
            self._offset = index2
        if elements1 is None:
            address1 = FAILURE
        else:
            address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
            self._offset = self._offset
        if address1 is not FAILURE:
            elements0.append(address1)
            address6 = FAILURE
            index4 = self._offset
            address6 = self._read_eol()
            if address6 is FAILURE:
                self._offset = index4
                index5 = self._offset
                index6, elements3 = self._offset, []
                address7 = FAILURE
                address7 = self._read_space()
                if address7 is not FAILURE:
                    elements3.append(address7)
                    address8 = FAILURE
                    index7 = self._offset
                    address8 = self._read_block_item()
                    self._offset = index7
                    if address8 is FAILURE:
                        address8 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address8 = FAILURE
                    if address8 is not FAILURE:
                        elements3.append(address8)
                        address9 = FAILURE
                        address9 = self._read_block_elements()
                        if address9 is not FAILURE:
                            elements3.append(address9)
                        else:
                            elements3 = None
                            self._offset = index6
                    else:
                        elements3 = None
                        self._offset = index6
                else:
                    elements3 = None
                    self._offset = index6
                if elements3 is None:
                    address6 = FAILURE
                else:
                    address6 = TreeNode48(self._input[index6:self._offset], index6, elements3)
                    self._offset = self._offset
                if address6 is FAILURE:
                    address6 = TreeNode(self._input[index5:index5], index5, [])
                    self._offset = index5
                if address6 is FAILURE:
                    self._offset = index4
            if address6 is not FAILURE:
                elements0.append(address6)
                address10 = FAILURE
                index8 = self._offset
                index9, elements4 = self._offset, []
                address11 = FAILURE
                address11 = self._read_indent()
                if address11 is not FAILURE:
                    elements4.append(address11)
                    address12 = FAILURE
                    remaining1, index10, elements5, address13 = 1, self._offset, [], True
                    while address13 is not FAILURE:
                        address13 = self._read_block_element()
                        if address13 is not FAILURE:
                            elements5.append(address13)
                            remaining1 -= 1
                    if remaining1 <= 0:
                        address12 = TreeNode(self._input[index10:self._offset], index10, elements5)
                        self._offset = self._offset
                    else:
                        address12 = FAILURE
                    if address12 is not FAILURE:
                        elements4.append(address12)
                        address14 = FAILURE
                        address14 = self._read_dedent()
                        if address14 is not FAILURE:
                            elements4.append(address14)
                        else:
                            elements4 = None
                            self._offset = index9
                    else:
                        elements4 = None
                        self._offset = index9
                else:
                    elements4 = None
                    self._offset = index9
                if elements4 is None:
                    address10 = FAILURE
                else:
                    address10 = TreeNode49(self._input[index9:self._offset], index9, elements4)
                    self._offset = self._offset
                if address10 is FAILURE:
                    address10 = TreeNode(self._input[index8:index8], index8, [])
                    self._offset = index8
                if address10 is not FAILURE:
                    elements0.append(address10)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode47(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'BlockItem', (cls0, self._types.BlockItem), {})
        self._cache['block_item'][index0] = (address0, self._offset)
        return address0

    def _read_longtitle(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['longtitle'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 9
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'LONGTITLE':
            address1 = TreeNode(self._input[self._offset:self._offset + 9], self._offset, [])
            self._offset = self._offset + 9
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'LONGTITLE\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_space()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                remaining0, index2, elements1, address4 = 1, self._offset, [], True
                while address4 is not FAILURE:
                    address4 = self._read_inline()
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address3 = TreeNode(self._input[index2:self._offset], index2, elements1)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address5 = FAILURE
                    address5 = self._read_eol()
                    if address5 is not FAILURE:
                        elements0.append(address5)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode50(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Longtitle', (cls0, self._types.Longtitle), {})
        self._cache['longtitle'][index0] = (address0, self._offset)
        return address0

    def _read_subheading(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['subheading'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 10
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'SUBHEADING':
            address1 = TreeNode(self._input[self._offset:self._offset + 10], self._offset, [])
            self._offset = self._offset + 10
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'SUBHEADING\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_space()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                remaining0, index2, elements1, address4 = 1, self._offset, [], True
                while address4 is not FAILURE:
                    address4 = self._read_inline()
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address3 = TreeNode(self._input[index2:self._offset], index2, elements1)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address5 = FAILURE
                    address5 = self._read_eol()
                    if address5 is not FAILURE:
                        elements0.append(address5)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode51(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Heading', (cls0, self._types.Heading), {})
        self._cache['subheading'][index0] = (address0, self._offset)
        return address0

    def _read_crossheading(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['crossheading'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 12
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'CROSSHEADING':
            address1 = TreeNode(self._input[self._offset:self._offset + 12], self._offset, [])
            self._offset = self._offset + 12
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'CROSSHEADING\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_space()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                remaining0, index2, elements1, address4 = 1, self._offset, [], True
                while address4 is not FAILURE:
                    address4 = self._read_inline()
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address3 = TreeNode(self._input[index2:self._offset], index2, elements1)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address5 = FAILURE
                    address5 = self._read_eol()
                    if address5 is not FAILURE:
                        elements0.append(address5)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode52(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Crossheading', (cls0, self._types.Crossheading), {})
        self._cache['crossheading'][index0] = (address0, self._offset)
        return address0

    def _read_line(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['line'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_dedent()
        self._offset = index2
        if address1 is FAILURE:
            address1 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
            self._offset = self._offset
        else:
            address1 = FAILURE
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_inline()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                address4 = self._read_eol()
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode53(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Line', (cls0, self._types.Line), {})
        self._cache['line'][index0] = (address0, self._offset)
        return address0

    def _read_table(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['table'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 5
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'TABLE':
            address1 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
            self._offset = self._offset + 5
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'TABLE\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_block_attrs()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_eol()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_indent()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        remaining0, index3, elements1, address6 = 1, self._offset, [], True
                        while address6 is not FAILURE:
                            address6 = self._read_table_row()
                            if address6 is not FAILURE:
                                elements1.append(address6)
                                remaining0 -= 1
                        if remaining0 <= 0:
                            address5 = TreeNode(self._input[index3:self._offset], index3, elements1)
                            self._offset = self._offset
                        else:
                            address5 = FAILURE
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address7 = FAILURE
                            address7 = self._read_dedent()
                            if address7 is not FAILURE:
                                elements0.append(address7)
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode54(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Table', (cls0, self._types.Table), {})
        self._cache['table'][index0] = (address0, self._offset)
        return address0

    def _read_table_row(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['table_row'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 2
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'TR':
            address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
            self._offset = self._offset + 2
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'TR\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_indent()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    remaining0, index2, elements1, address5 = 1, self._offset, [], True
                    while address5 is not FAILURE:
                        address5 = self._read_table_cell()
                        if address5 is not FAILURE:
                            elements1.append(address5)
                            remaining0 -= 1
                    if remaining0 <= 0:
                        address4 = TreeNode(self._input[index2:self._offset], index2, elements1)
                        self._offset = self._offset
                    else:
                        address4 = FAILURE
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address6 = FAILURE
                        address6 = self._read_dedent()
                        if address6 is not FAILURE:
                            elements0.append(address6)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode55(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'TableRow', (cls0, self._types.TableRow), {})
        self._cache['table_row'][index0] = (address0, self._offset)
        return address0

    def _read_table_cell(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['table_cell'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        chunk0, max0 = None, self._offset + 2
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'TH':
            address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
            self._offset = self._offset + 2
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'TH\'')
        if address1 is FAILURE:
            self._offset = index2
            chunk1, max1 = None, self._offset + 2
            if max1 <= self._input_size:
                chunk1 = self._input[self._offset:max1]
            if chunk1 == 'TC':
                address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                self._offset = self._offset + 2
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('\'TC\'')
            if address1 is FAILURE:
                self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            address2 = self._read_block_attrs()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index3:index3], index3, [])
                self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_eol()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index4 = self._offset
                    index5, elements1 = self._offset, []
                    address5 = FAILURE
                    address5 = self._read_indent()
                    if address5 is not FAILURE:
                        elements1.append(address5)
                        address6 = FAILURE
                        remaining0, index6, elements2, address7 = 1, self._offset, [], True
                        while address7 is not FAILURE:
                            address7 = self._read_block_element()
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                remaining0 -= 1
                        if remaining0 <= 0:
                            address6 = TreeNode(self._input[index6:self._offset], index6, elements2)
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements1.append(address6)
                            address8 = FAILURE
                            address8 = self._read_dedent()
                            if address8 is not FAILURE:
                                elements1.append(address8)
                            else:
                                elements1 = None
                                self._offset = index5
                        else:
                            elements1 = None
                            self._offset = index5
                    else:
                        elements1 = None
                        self._offset = index5
                    if elements1 is None:
                        address4 = FAILURE
                    else:
                        address4 = TreeNode57(self._input[index5:self._offset], index5, elements1)
                        self._offset = self._offset
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index4:index4], index4, [])
                        self._offset = index4
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode56(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'TableCell', (cls0, self._types.TableCell), {})
        self._cache['table_cell'][index0] = (address0, self._offset)
        return address0

    def _read_block_attrs(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['block_attrs'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 1
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '{':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'{\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_block_attr()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                index3 = self._offset
                address3 = self._read_space()
                if address3 is FAILURE:
                    address3 = TreeNode(self._input[index3:index3], index3, [])
                    self._offset = index3
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    remaining0, index4, elements1, address5 = 0, self._offset, [], True
                    while address5 is not FAILURE:
                        index5, elements2 = self._offset, []
                        address6 = FAILURE
                        chunk1, max1 = None, self._offset + 1
                        if max1 <= self._input_size:
                            chunk1 = self._input[self._offset:max1]
                        if chunk1 == '|':
                            address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address6 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('\'|\'')
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            index6 = self._offset
                            address7 = self._read_space()
                            if address7 is FAILURE:
                                address7 = TreeNode(self._input[index6:index6], index6, [])
                                self._offset = index6
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                address8 = FAILURE
                                index7 = self._offset
                                address8 = self._read_block_attr()
                                if address8 is FAILURE:
                                    address8 = TreeNode(self._input[index7:index7], index7, [])
                                    self._offset = index7
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                else:
                                    elements2 = None
                                    self._offset = index5
                            else:
                                elements2 = None
                                self._offset = index5
                        else:
                            elements2 = None
                            self._offset = index5
                        if elements2 is None:
                            address5 = FAILURE
                        else:
                            address5 = TreeNode59(self._input[index5:self._offset], index5, elements2)
                            self._offset = self._offset
                        if address5 is not FAILURE:
                            elements1.append(address5)
                            remaining0 -= 1
                    if remaining0 <= 0:
                        address4 = TreeNode(self._input[index4:self._offset], index4, elements1)
                        self._offset = self._offset
                    else:
                        address4 = FAILURE
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address9 = FAILURE
                        chunk2, max2 = None, self._offset + 1
                        if max2 <= self._input_size:
                            chunk2 = self._input[self._offset:max2]
                        if chunk2 == '}':
                            address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address9 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('\'}\'')
                        if address9 is not FAILURE:
                            elements0.append(address9)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode58(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'BlockAttrs', (cls0, self._types.BlockAttrs), {})
        self._cache['block_attrs'][index0] = (address0, self._offset)
        return address0

    def _read_block_attr(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['block_attr'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_attr_name()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            index3, elements1 = self._offset, []
            address3 = FAILURE
            address3 = self._read_space()
            if address3 is not FAILURE:
                elements1.append(address3)
                address4 = FAILURE
                address4 = self._read_attr_value()
                if address4 is not FAILURE:
                    elements1.append(address4)
                else:
                    elements1 = None
                    self._offset = index3
            else:
                elements1 = None
                self._offset = index3
            if elements1 is None:
                address2 = FAILURE
            else:
                address2 = TreeNode61(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode60(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'BlockAttr', (cls0, self._types.BlockAttr), {})
        self._cache['block_attr'][index0] = (address0, self._offset)
        return address0

    def _read_attr_name(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['attr_name'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0, max0 = None, self._offset + 1
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 is not None and Grammar.REGEX_3.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[^ \\n|}]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['attr_name'][index0] = (address0, self._offset)
        return address0

    def _read_attr_value(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['attr_value'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            chunk0, max0 = None, self._offset + 1
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 is not None and Grammar.REGEX_4.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[^\\n|}]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['attr_value'][index0] = (address0, self._offset)
        return address0

    def _read_embedded_structure(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['embedded_structure'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 5
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'QUOTE':
            address1 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
            self._offset = self._offset + 5
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'QUOTE\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_block_attrs()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_eol()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_indent()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        remaining0, index3, elements1, address6 = 1, self._offset, [], True
                        while address6 is not FAILURE:
                            address6 = self._read_hier_block_element()
                            if address6 is not FAILURE:
                                elements1.append(address6)
                                remaining0 -= 1
                        if remaining0 <= 0:
                            address5 = TreeNode(self._input[index3:self._offset], index3, elements1)
                            self._offset = self._offset
                        else:
                            address5 = FAILURE
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address7 = FAILURE
                            address7 = self._read_dedent()
                            if address7 is not FAILURE:
                                elements0.append(address7)
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode62(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'EmbeddedStructure', (cls0, self._types.EmbeddedStructure), {})
        self._cache['embedded_structure'][index0] = (address0, self._offset)
        return address0

    def _read_footnote(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['footnote'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 8
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == 'FOOTNOTE':
            address1 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
            self._offset = self._offset + 8
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'FOOTNOTE\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_space()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                remaining0, index2, elements1, address4 = 1, self._offset, [], True
                while address4 is not FAILURE:
                    chunk1, max1 = None, self._offset + 1
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 is not None and Grammar.REGEX_5.search(chunk1):
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('[^ \\n]')
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address3 = TreeNode(self._input[index2:self._offset], index2, elements1)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address5 = FAILURE
                    index3 = self._offset
                    address5 = self._read_space()
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[index3:index3], index3, [])
                        self._offset = index3
                    if address5 is not FAILURE:
                        elements0.append(address5)
                        address6 = FAILURE
                        address6 = self._read_eol()
                        if address6 is not FAILURE:
                            elements0.append(address6)
                            address7 = FAILURE
                            address7 = self._read_indent()
                            if address7 is not FAILURE:
                                elements0.append(address7)
                                address8 = FAILURE
                                remaining1, index4, elements2, address9 = 1, self._offset, [], True
                                while address9 is not FAILURE:
                                    address9 = self._read_hier_block_element()
                                    if address9 is not FAILURE:
                                        elements2.append(address9)
                                        remaining1 -= 1
                                if remaining1 <= 0:
                                    address8 = TreeNode(self._input[index4:self._offset], index4, elements2)
                                    self._offset = self._offset
                                else:
                                    address8 = FAILURE
                                if address8 is not FAILURE:
                                    elements0.append(address8)
                                    address10 = FAILURE
                                    address10 = self._read_dedent()
                                    if address10 is not FAILURE:
                                        elements0.append(address10)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode63(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Footnote', (cls0, self._types.Footnote), {})
        self._cache['footnote'][index0] = (address0, self._offset)
        return address0

    def _read_inline(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['inline'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_inline_marker()
        if address0 is FAILURE:
            self._offset = index1
            chunk0, max0 = None, self._offset + 1
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 is not None and Grammar.REGEX_6.search(chunk0):
                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                self._offset = self._offset + 1
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[^\\n]')
            if address0 is FAILURE:
                self._offset = index1
        self._cache['inline'][index0] = (address0, self._offset)
        return address0

    def _read_inline_marker(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['inline_marker'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_bold()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_image()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_italics()
                if address0 is FAILURE:
                    self._offset = index1
                    address0 = self._read_underline()
                    if address0 is FAILURE:
                        self._offset = index1
                        address0 = self._read_sup()
                        if address0 is FAILURE:
                            self._offset = index1
                            address0 = self._read_sub()
                            if address0 is FAILURE:
                                self._offset = index1
                                address0 = self._read_remark()
                                if address0 is FAILURE:
                                    self._offset = index1
                                    address0 = self._read_ref()
                                    if address0 is FAILURE:
                                        self._offset = index1
                                        address0 = self._read_footnote_ref()
                                        if address0 is FAILURE:
                                            self._offset = index1
        self._cache['inline_marker'][index0] = (address0, self._offset)
        return address0

    def _read_bold(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['bold'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 2
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '**':
            address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
            self._offset = self._offset + 2
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'**\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1, max1 = None, self._offset + 2
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == '**':
                    address4 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'**\'')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_inline()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode65(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk2, max2 = None, self._offset + 2
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == '**':
                    address6 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'**\'')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode64(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Bold', (cls0, self._types.Bold), {})
        self._cache['bold'][index0] = (address0, self._offset)
        return address0

    def _read_italics(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['italics'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 2
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '//':
            address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
            self._offset = self._offset + 2
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'//\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1, max1 = None, self._offset + 2
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == '//':
                    address4 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'//\'')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_inline()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode67(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk2, max2 = None, self._offset + 2
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == '//':
                    address6 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'//\'')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode66(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Italics', (cls0, self._types.Italics), {})
        self._cache['italics'][index0] = (address0, self._offset)
        return address0

    def _read_underline(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['underline'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 2
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '__':
            address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
            self._offset = self._offset + 2
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'__\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1, max1 = None, self._offset + 2
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == '__':
                    address4 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'__\'')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_inline()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode69(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk2, max2 = None, self._offset + 2
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == '__':
                    address6 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'__\'')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode68(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Underline', (cls0, self._types.Underline), {})
        self._cache['underline'][index0] = (address0, self._offset)
        return address0

    def _read_remark(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['remark'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 2
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '[[':
            address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
            self._offset = self._offset + 2
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'[[\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1, max1 = None, self._offset + 2
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == ']]':
                    address4 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\']]\'')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_inline()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode71(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk2, max2 = None, self._offset + 2
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == ']]':
                    address6 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\']]\'')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode70(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Remark', (cls0, self._types.Remark), {})
        self._cache['remark'][index0] = (address0, self._offset)
        return address0

    def _read_image(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['image'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 5
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '{{IMG':
            address1 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
            self._offset = self._offset + 5
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'{{IMG\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_space()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                remaining0, index3, elements1, address4 = 1, self._offset, [], True
                while address4 is not FAILURE:
                    index4, elements2 = self._offset, []
                    address5 = FAILURE
                    index5 = self._offset
                    chunk1, max1 = None, self._offset + 2
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 == '}}':
                        address5 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                        self._offset = self._offset + 2
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('\'}}\'')
                    self._offset = index5
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        chunk2, max2 = None, self._offset + 1
                        if max2 <= self._input_size:
                            chunk2 = self._input[self._offset:max2]
                        if chunk2 is not None and Grammar.REGEX_7.search(chunk2):
                            address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address6 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('[^ \\n]')
                        if address6 is not FAILURE:
                            elements2.append(address6)
                        else:
                            elements2 = None
                            self._offset = index4
                    else:
                        elements2 = None
                        self._offset = index4
                    if elements2 is None:
                        address4 = FAILURE
                    else:
                        address4 = TreeNode(self._input[index4:self._offset], index4, elements2)
                        self._offset = self._offset
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address3 = TreeNode(self._input[index3:self._offset], index3, elements1)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address7 = FAILURE
                    remaining1, index6, elements3, address8 = 0, self._offset, [], True
                    while address8 is not FAILURE:
                        index7, elements4 = self._offset, []
                        address9 = FAILURE
                        index8 = self._offset
                        chunk3, max3 = None, self._offset + 2
                        if max3 <= self._input_size:
                            chunk3 = self._input[self._offset:max3]
                        if chunk3 == '}}':
                            address9 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                            self._offset = self._offset + 2
                        else:
                            address9 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('\'}}\'')
                        self._offset = index8
                        if address9 is FAILURE:
                            address9 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address9 = FAILURE
                        if address9 is not FAILURE:
                            elements4.append(address9)
                            address10 = FAILURE
                            chunk4, max4 = None, self._offset + 1
                            if max4 <= self._input_size:
                                chunk4 = self._input[self._offset:max4]
                            if chunk4 is not None and Grammar.REGEX_8.search(chunk4):
                                address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address10 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('[^\\n]')
                            if address10 is not FAILURE:
                                elements4.append(address10)
                            else:
                                elements4 = None
                                self._offset = index7
                        else:
                            elements4 = None
                            self._offset = index7
                        if elements4 is None:
                            address8 = FAILURE
                        else:
                            address8 = TreeNode(self._input[index7:self._offset], index7, elements4)
                            self._offset = self._offset
                        if address8 is not FAILURE:
                            elements3.append(address8)
                            remaining1 -= 1
                    if remaining1 <= 0:
                        address7 = TreeNode(self._input[index6:self._offset], index6, elements3)
                        self._offset = self._offset
                    else:
                        address7 = FAILURE
                    if address7 is not FAILURE:
                        elements0.append(address7)
                        address11 = FAILURE
                        chunk5, max5 = None, self._offset + 2
                        if max5 <= self._input_size:
                            chunk5 = self._input[self._offset:max5]
                        if chunk5 == '}}':
                            address11 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                            self._offset = self._offset + 2
                        else:
                            address11 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('\'}}\'')
                        if address11 is not FAILURE:
                            elements0.append(address11)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode72(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Image', (cls0, self._types.Image), {})
        self._cache['image'][index0] = (address0, self._offset)
        return address0

    def _read_sup(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['sup'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 3
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '{{^':
            address1 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
            self._offset = self._offset + 3
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'{{^\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1, max1 = None, self._offset + 2
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == '}}':
                    address4 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'}}\'')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_inline()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode74(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk2, max2 = None, self._offset + 2
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == '}}':
                    address6 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'}}\'')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode73(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Sup', (cls0, self._types.Sup), {})
        self._cache['sup'][index0] = (address0, self._offset)
        return address0

    def _read_sub(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['sub'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 3
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '{{_':
            address1 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
            self._offset = self._offset + 3
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'{{_\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1, max1 = None, self._offset + 2
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == '}}':
                    address4 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'}}\'')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    address5 = self._read_inline()
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode76(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk2, max2 = None, self._offset + 2
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == '}}':
                    address6 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'}}\'')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode75(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Sub', (cls0, self._types.Sub), {})
        self._cache['sub'][index0] = (address0, self._offset)
        return address0

    def _read_ref(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['ref'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 3
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '{{>':
            address1 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
            self._offset = self._offset + 3
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'{{>\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1, max1 = None, self._offset + 2
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == '}}':
                    address4 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                    self._offset = self._offset + 2
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\'}}\'')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    chunk2, max2 = None, self._offset + 1
                    if max2 <= self._input_size:
                        chunk2 = self._input[self._offset:max2]
                    if chunk2 is not None and Grammar.REGEX_9.search(chunk2):
                        address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('[^ \\n]')
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                index5 = self._offset
                chunk3, max3 = None, self._offset + 1
                if max3 <= self._input_size:
                    chunk3 = self._input[self._offset:max3]
                if chunk3 == ' ':
                    address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('\' \'')
                if address6 is FAILURE:
                    address6 = TreeNode(self._input[index5:index5], index5, [])
                    self._offset = index5
                if address6 is not FAILURE:
                    elements0.append(address6)
                    address7 = FAILURE
                    remaining1, index6, elements3, address8 = 0, self._offset, [], True
                    while address8 is not FAILURE:
                        index7, elements4 = self._offset, []
                        address9 = FAILURE
                        index8 = self._offset
                        chunk4, max4 = None, self._offset + 2
                        if max4 <= self._input_size:
                            chunk4 = self._input[self._offset:max4]
                        if chunk4 == '}}':
                            address9 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                            self._offset = self._offset + 2
                        else:
                            address9 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('\'}}\'')
                        self._offset = index8
                        if address9 is FAILURE:
                            address9 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address9 = FAILURE
                        if address9 is not FAILURE:
                            elements4.append(address9)
                            address10 = FAILURE
                            address10 = self._read_inline()
                            if address10 is not FAILURE:
                                elements4.append(address10)
                            else:
                                elements4 = None
                                self._offset = index7
                        else:
                            elements4 = None
                            self._offset = index7
                        if elements4 is None:
                            address8 = FAILURE
                        else:
                            address8 = TreeNode78(self._input[index7:self._offset], index7, elements4)
                            self._offset = self._offset
                        if address8 is not FAILURE:
                            elements3.append(address8)
                            remaining1 -= 1
                    if remaining1 <= 0:
                        address7 = TreeNode(self._input[index6:self._offset], index6, elements3)
                        self._offset = self._offset
                    else:
                        address7 = FAILURE
                    if address7 is not FAILURE:
                        elements0.append(address7)
                        address11 = FAILURE
                        chunk5, max5 = None, self._offset + 2
                        if max5 <= self._input_size:
                            chunk5 = self._input[self._offset:max5]
                        if chunk5 == '}}':
                            address11 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                            self._offset = self._offset + 2
                        else:
                            address11 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('\'}}\'')
                        if address11 is not FAILURE:
                            elements0.append(address11)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode77(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'Ref', (cls0, self._types.Ref), {})
        self._cache['ref'][index0] = (address0, self._offset)
        return address0

    def _read_footnote_ref(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['footnote_ref'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 10
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '{{FOOTNOTE':
            address1 = TreeNode(self._input[self._offset:self._offset + 10], self._offset, [])
            self._offset = self._offset + 10
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'{{FOOTNOTE\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_space()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                remaining0, index2, elements1, address4 = 1, self._offset, [], True
                while address4 is not FAILURE:
                    index3, elements2 = self._offset, []
                    address5 = FAILURE
                    index4 = self._offset
                    chunk1, max1 = None, self._offset + 2
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 == '}}':
                        address5 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                        self._offset = self._offset + 2
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('\'}}\'')
                    self._offset = index4
                    if address5 is FAILURE:
                        address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        chunk2, max2 = None, self._offset + 1
                        if max2 <= self._input_size:
                            chunk2 = self._input[self._offset:max2]
                        if chunk2 is not None and Grammar.REGEX_10.search(chunk2):
                            address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address6 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('[^\\n]')
                        if address6 is not FAILURE:
                            elements2.append(address6)
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                    if elements2 is None:
                        address4 = FAILURE
                    else:
                        address4 = TreeNode(self._input[index3:self._offset], index3, elements2)
                        self._offset = self._offset
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address3 = TreeNode(self._input[index2:self._offset], index2, elements1)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address7 = FAILURE
                    chunk3, max3 = None, self._offset + 2
                    if max3 <= self._input_size:
                        chunk3 = self._input[self._offset:max3]
                    if chunk3 == '}}':
                        address7 = TreeNode(self._input[self._offset:self._offset + 2], self._offset, [])
                        self._offset = self._offset + 2
                    else:
                        address7 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('\'}}\'')
                    if address7 is not FAILURE:
                        elements0.append(address7)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode79(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        if address0 is not FAILURE:
            cls0 = type(address0)
            address0.__class__ = type(cls0.__name__ + 'FootnoteRef', (cls0, self._types.FootnoteRef), {})
        self._cache['footnote_ref'][index0] = (address0, self._offset)
        return address0

    def _read_eol(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['eol'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_newline()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_empty_line()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode80(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['eol'][index0] = (address0, self._offset)
        return address0

    def _read_empty_line(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['empty_line'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_newline()
        self._cache['empty_line'][index0] = (address0, self._offset)
        return address0

    def _read_space(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['space'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0, max0 = None, self._offset + 1
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 == ' ':
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('\' \'')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['space'][index0] = (address0, self._offset)
        return address0

    def _read_newline(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['newline'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0, max0 = None, self._offset + 1
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '\n':
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"\\n"')
        self._cache['newline'][index0] = (address0, self._offset)
        return address0

    def _read_indent(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['indent'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 1
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '{':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'{\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode81(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['indent'][index0] = (address0, self._offset)
        return address0

    def _read_dedent(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['dedent'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0, max0 = None, self._offset + 1
        if max0 <= self._input_size:
            chunk0 = self._input[self._offset:max0]
        if chunk0 == '}':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('\'}\'')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_eol()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode82(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['dedent'][index0] = (address0, self._offset)
        return address0


class Parser(Grammar):
    def __init__(self, input, actions, types):
        self._input = input
        self._input_size = len(input)
        self._actions = actions
        self._types = types
        self._offset = 0
        self._cache = defaultdict(dict)
        self._failure = 0
        self._expected = []

    def parse(self):
        tree = self._read_root()
        if tree is not FAILURE and self._offset == self._input_size:
            return tree
        if not self._expected:
            self._failure = self._offset
            self._expected.append('<EOF>')
        raise ParseError(format_error(self._input, self._failure, self._expected))


def format_error(input, offset, expected):
    lines, line_no, position = input.split('\n'), 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1
    message, line = 'Line ' + str(line_no) + ': expected ' + ', '.join(expected) + '\n', lines[line_no - 1]
    message += line + '\n'
    position -= len(line) + 1
    message += ' ' * (offset - position)
    return message + '^'

def parse(input, actions=None, types=None):
    parser = Parser(input, actions, types)
    return parser.parse()
