use std::collections::{BTreeMap, HashMap, HashSet};

use crate::eid::IdGenerator;
use crate::parser::{parse_pairs_preprocessed, DocumentRoot, ParseError, Rule};
use crate::preprocess::pre_parse;

const AKN_NS: &str = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0";

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum XmlNode {
    Element(XmlElement),
    Text(String),
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct XmlElement {
    pub name: String,
    pub attrs: BTreeMap<String, String>,
    pub children: Vec<XmlNode>,
}

impl XmlElement {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            attrs: BTreeMap::new(),
            children: Vec::new(),
        }
    }

    pub fn attr(mut self, name: impl Into<String>, value: impl Into<String>) -> Self {
        self.attrs.insert(name.into(), value.into());
        self
    }

    pub fn child(mut self, child: impl Into<XmlNode>) -> Self {
        self.children.push(child.into());
        self
    }

    pub fn text(mut self, text: impl Into<String>) -> Self {
        self.children.push(XmlNode::Text(text.into()));
        self
    }
}

impl From<XmlElement> for XmlNode {
    fn from(value: XmlElement) -> Self {
        XmlNode::Element(value)
    }
}

impl From<String> for XmlNode {
    fn from(value: String) -> Self {
        XmlNode::Text(value)
    }
}

impl From<&str> for XmlNode {
    fn from(value: &str) -> Self {
        XmlNode::Text(value.to_string())
    }
}

#[derive(Debug, thiserror::Error)]
pub enum XmlError {
    #[error(transparent)]
    Parse(#[from] ParseError),
}

pub fn parse_to_xml(text: &str, root: DocumentRoot) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_xml(&preprocessed, root)
}

pub fn parse_preprocessed_to_xml(text: &str, root: DocumentRoot) -> Result<String, XmlError> {
    let pairs = parse_pairs_preprocessed(text, root)?;
    let mut root_el = build_document(root);
    let mut blocks = Vec::new();
    for pair in pairs {
        collect_blocks(pair, &mut blocks);
    }
    insert_blocks(&mut root_el, root, blocks);
    rewrite_all_eids(&mut root_el, "");
    root_el
        .attrs
        .insert("xmlns".to_string(), AKN_NS.to_string());
    Ok(root_el.to_xml_string())
}

fn build_document(root: DocumentRoot) -> XmlElement {
    match root {
        DocumentRoot::Act => XmlElement::new("act").attr("name", "act").child(
            XmlElement::new("body").child(
                XmlElement::new("hcontainer")
                    .attr("name", "hcontainer")
                    .child(XmlElement::new("content").child(XmlElement::new("p"))),
            ),
        ),
        DocumentRoot::Bill => XmlElement::new("bill").attr("name", "bill").child(
            XmlElement::new("body").child(
                XmlElement::new("hcontainer")
                    .attr("name", "hcontainer")
                    .child(XmlElement::new("content").child(XmlElement::new("p"))),
            ),
        ),
        DocumentRoot::Judgment => XmlElement::new("judgment")
            .attr("name", "judgment")
            .child(XmlElement::new("header"))
            .child(
                XmlElement::new("judgmentBody")
                    .child(XmlElement::new("introduction").child(XmlElement::new("p"))),
            ),
        DocumentRoot::Debate => XmlElement::new("debate").attr("name", "debate").child(
            XmlElement::new("debateBody").child(
                XmlElement::new("debateSection")
                    .attr("name", "debateSection")
                    .child(XmlElement::new("p")),
            ),
        ),
        DocumentRoot::DebateReport => open_doc("debateReport"),
        DocumentRoot::Doc => open_doc("doc"),
        DocumentRoot::Statement => open_doc("statement"),
    }
}

fn open_doc(name: &str) -> XmlElement {
    XmlElement::new(name)
        .attr("name", name)
        .child(XmlElement::new("mainBody").child(XmlElement::new("p")))
}

fn insert_blocks(root_el: &mut XmlElement, root: DocumentRoot, blocks: Vec<XmlElement>) {
    if blocks.is_empty() {
        return;
    }
    match root {
        DocumentRoot::Act | DocumentRoot::Bill => {
            let body = if blocks.iter().all(|block| is_hier_name(&block.name)) {
                XmlElement::new("body").children(blocks)
            } else {
                XmlElement::new("body").child(
                    XmlElement::new("hcontainer")
                        .attr("name", "hcontainer")
                        .child(XmlElement::new("content").children(blocks)),
                )
            };
            root_el.children = vec![XmlNode::Element(body)];
        }
        DocumentRoot::Statement | DocumentRoot::Doc | DocumentRoot::DebateReport => {
            root_el.children = vec![XmlNode::Element(
                XmlElement::new("mainBody").children(blocks),
            )];
        }
        DocumentRoot::Judgment => {
            root_el.children = vec![
                XmlNode::Element(XmlElement::new("header")),
                XmlNode::Element(
                    XmlElement::new("judgmentBody")
                        .child(XmlElement::new("introduction").children(blocks)),
                ),
            ];
        }
        DocumentRoot::Debate => {
            root_el.children = vec![XmlNode::Element(
                XmlElement::new("debateBody").child(
                    XmlElement::new("debateSection")
                        .attr("name", "debateSection")
                        .children(blocks),
                ),
            )];
        }
    }
}

trait Children {
    fn children(self, children: Vec<XmlElement>) -> Self;
    fn children_nodes(self, children: Vec<XmlNode>) -> Self;
}

impl Children for XmlElement {
    fn children(mut self, children: Vec<XmlElement>) -> Self {
        self.children = children.into_iter().map(XmlNode::Element).collect();
        self
    }

    fn children_nodes(mut self, children: Vec<XmlNode>) -> Self {
        self.children = children;
        self
    }
}

fn collect_blocks(pair: pest::iterators::Pair<'_, Rule>, blocks: &mut Vec<XmlElement>) {
    match pair.as_rule() {
        Rule::line | Rule::p => blocks.push(p_to_xml(pair)),
        Rule::hier_element_block => {
            blocks.push(hier_to_xml(pair));
        }
        Rule::block_list => blocks.push(block_list_to_xml(pair)),
        Rule::bullet_list => blocks.push(bullet_list_to_xml(pair)),
        Rule::table => blocks.push(table_to_xml(pair)),
        _ => {
            for child in pair.into_inner() {
                collect_blocks(child, blocks);
            }
        }
    }
}

fn block_list_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut list = XmlElement::new("blockList");
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => list.attrs.extend(block_attrs_to_map(child)),
            Rule::block_list_intro => list.children.push(XmlNode::Element(line_like_to_named_xml(
                child,
                "listIntroduction",
            ))),
            Rule::block_list_wrapup => list.children.push(XmlNode::Element(
                line_like_to_named_xml(child, "listWrapUp"),
            )),
            Rule::block_list_item => list
                .children
                .push(XmlNode::Element(block_list_item_to_xml(child))),
            _ => {}
        }
    }
    list
}

fn line_like_to_named_xml(pair: pest::iterators::Pair<'_, Rule>, name: &str) -> XmlElement {
    let mut el = XmlElement::new(name);
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::line | Rule::p => el.children.extend(p_to_xml(child).children),
            Rule::footnote => {}
            _ => {}
        }
    }
    el
}

fn block_list_item_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut item = XmlElement::new("item");
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::hier_element_heading => {
                let (num, heading) = parse_heading(child);
                if let Some(num) = num.filter(|num| !num.is_empty()) {
                    item.children
                        .push(XmlNode::Element(XmlElement::new("num").text(num)));
                }
                if let Some(heading) = heading.filter(|heading| !heading.is_empty()) {
                    item.children
                        .push(XmlNode::Element(XmlElement::new("heading").text(heading)));
                }
            }
            Rule::block_element => collect_blocks(child, &mut blocks),
            Rule::subheading => {}
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    if blocks.is_empty() {
        blocks.push(XmlElement::new("p"));
    }
    item.children
        .extend(blocks.into_iter().map(XmlNode::Element));
    item
}

fn bullet_list_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut ul = XmlElement::new("ul");
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => ul.attrs.extend(block_attrs_to_map(child)),
            Rule::bullet_list_item => ul
                .children
                .push(XmlNode::Element(bullet_list_item_to_xml(child))),
            _ => {}
        }
    }
    ul
}

fn bullet_list_item_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_elements | Rule::block_element => collect_blocks(child, &mut blocks),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    if blocks.is_empty() {
        blocks.push(XmlElement::new("p"));
    }
    XmlElement::new("li").children(blocks)
}

fn table_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut table = XmlElement::new("table");
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => table.attrs.extend(block_attrs_to_map(child)),
            Rule::table_row => table
                .children
                .push(XmlNode::Element(table_row_to_xml(child))),
            _ => {}
        }
    }
    table
}

fn table_row_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut row = XmlElement::new("tr");
    for child in pair.into_inner() {
        if child.as_rule() == Rule::table_cell {
            row.children
                .push(XmlNode::Element(table_cell_to_xml(child)));
        }
    }
    row
}

fn table_cell_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let name = if pair.as_str().starts_with("TH") {
        "th"
    } else {
        "td"
    };
    let mut cell = XmlElement::new(name);
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => cell.attrs.extend(block_attrs_to_map(child)),
            Rule::block_element => collect_blocks(child, &mut blocks),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    if blocks.is_empty() {
        blocks.push(XmlElement::new("p"));
    }
    cell.children
        .extend(blocks.into_iter().map(XmlNode::Element));
    cell
}

fn collect_block_descendants(pair: pest::iterators::Pair<'_, Rule>, blocks: &mut Vec<XmlElement>) {
    match pair.as_rule() {
        Rule::line
        | Rule::p
        | Rule::hier_element_block
        | Rule::block_list
        | Rule::bullet_list
        | Rule::table => collect_blocks(pair, blocks),
        _ => {
            for child in pair.into_inner() {
                collect_block_descendants(child, blocks);
            }
        }
    }
}

fn hier_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut name = "hcontainer".to_string();
    let mut num = None;
    let mut heading = None;
    let mut attrs = BTreeMap::new();
    let mut content = Vec::new();

    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::hier_element_name => name = hier_name(child.as_str()),
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            Rule::hier_element_heading => {
                let (n, h) = parse_heading(child);
                num = n;
                heading = h;
            }
            Rule::line | Rule::p => content.push(p_to_xml(child)),
            Rule::hier_element_block => content.push(hier_to_xml(child)),
            _ => collect_hier_content(child, &mut content),
        }
    }

    let mut el = XmlElement::new(name);
    el.attrs = attrs;
    if let Some(num) = num {
        if !num.is_empty() {
            el.children
                .push(XmlNode::Element(XmlElement::new("num").text(num)));
        }
    }
    if let Some(heading) = heading {
        if !heading.is_empty() {
            el.children
                .push(XmlNode::Element(XmlElement::new("heading").text(heading)));
        }
    }
    if content.is_empty() {
        el.children.push(XmlNode::Element(
            XmlElement::new("content").child(XmlElement::new("p")),
        ));
    } else if content.iter().any(|c| is_hier_name(&c.name)) {
        el.children
            .extend(content.into_iter().map(XmlNode::Element));
    } else {
        el.children.push(XmlNode::Element(
            XmlElement::new("content").children(content),
        ));
    }
    el
}

fn collect_hier_content(pair: pest::iterators::Pair<'_, Rule>, content: &mut Vec<XmlElement>) {
    match pair.as_rule() {
        Rule::line | Rule::p => content.push(p_to_xml(pair)),
        Rule::hier_element_block => content.push(hier_to_xml(pair)),
        _ => {
            for child in pair.into_inner() {
                collect_hier_content(child, content);
            }
        }
    }
}

fn p_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut p = XmlElement::new("p");
    let mut nodes = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => p.attrs.extend(block_attrs_to_map(child)),
            _ => collect_inline_nodes_inner(child, &mut nodes),
        }
    }
    p.children = merge_adjacent_text(nodes);
    p
}

fn collect_inline_nodes_inner(pair: pest::iterators::Pair<'_, Rule>, nodes: &mut Vec<XmlNode>) {
    match pair.as_rule() {
        Rule::non_inline_start
        | Rule::inline_nested_start
        | Rule::escape
        | Rule::not_newline
        | Rule::marker
        | Rule::num_content => push_text(nodes, unescaped(pair.as_str())),
        Rule::bold => nodes.push(XmlNode::Element(
            XmlElement::new("b").children_nodes(collect_inline_nodes_from_children(pair)),
        )),
        Rule::italics => nodes.push(XmlNode::Element(
            XmlElement::new("i").children_nodes(collect_inline_nodes_from_children(pair)),
        )),
        Rule::underline => nodes.push(XmlNode::Element(
            XmlElement::new("u").children_nodes(collect_inline_nodes_from_children(pair)),
        )),
        Rule::sup => nodes.push(XmlNode::Element(
            XmlElement::new("sup").children_nodes(collect_inline_nodes_from_children(pair)),
        )),
        Rule::sub => nodes.push(XmlNode::Element(
            XmlElement::new("sub").children_nodes(collect_inline_nodes_from_children(pair)),
        )),
        Rule::remark => nodes.push(XmlNode::Element(
            XmlElement::new("remark")
                .attr("status", "editorial")
                .children_nodes(collect_inline_nodes_from_children(pair)),
        )),
        Rule::block_attrs
        | Rule::block_attr_class
        | Rule::block_attr_pairs
        | Rule::block_attr
        | Rule::class_name
        | Rule::attr_name
        | Rule::attr_value => {}
        _ => {
            for child in pair.into_inner() {
                collect_inline_nodes_inner(child, nodes);
            }
        }
    }
}

fn collect_inline_nodes_from_children(pair: pest::iterators::Pair<'_, Rule>) -> Vec<XmlNode> {
    let mut nodes = Vec::new();
    for child in pair.into_inner() {
        collect_inline_nodes_inner(child, &mut nodes);
    }
    merge_adjacent_text(nodes)
}

fn push_text(nodes: &mut Vec<XmlNode>, text: String) {
    if !text.is_empty() {
        nodes.push(XmlNode::Text(text));
    }
}

fn unescaped(text: &str) -> String {
    text.strip_prefix('\\').unwrap_or(text).to_string()
}

fn merge_adjacent_text(nodes: Vec<XmlNode>) -> Vec<XmlNode> {
    let mut merged = Vec::new();
    for node in nodes {
        match (merged.last_mut(), node) {
            (Some(XmlNode::Text(existing)), XmlNode::Text(text)) => existing.push_str(&text),
            (_, node) => merged.push(node),
        }
    }
    merged
}

fn block_attrs_to_map(pair: pest::iterators::Pair<'_, Rule>) -> BTreeMap<String, String> {
    let mut attrs = BTreeMap::new();
    let mut classes = Vec::new();
    collect_block_attrs(pair, &mut attrs, &mut classes);
    if !classes.is_empty() {
        attrs
            .entry("class".to_string())
            .and_modify(|existing| {
                existing.push(' ');
                existing.push_str(&classes.join(" "));
            })
            .or_insert_with(|| classes.join(" "));
    }
    attrs
}

fn collect_block_attrs(
    pair: pest::iterators::Pair<'_, Rule>,
    attrs: &mut BTreeMap<String, String>,
    classes: &mut Vec<String>,
) {
    match pair.as_rule() {
        Rule::block_attr_class => {
            let text = pair.as_str();
            if text.len() > 1 {
                classes.push(text[1..].to_string());
            }
        }
        Rule::block_attr => {
            let mut name = None;
            let mut value = String::new();
            for child in pair.into_inner() {
                match child.as_rule() {
                    Rule::attr_name => name = Some(child.as_str().to_string()),
                    Rule::attr_value => value = child.as_str().trim().to_string(),
                    _ => {}
                }
            }
            if let Some(name) = name {
                attrs.insert(name, value);
            }
        }
        _ => {
            for child in pair.into_inner() {
                collect_block_attrs(child, attrs, classes);
            }
        }
    }
}

fn collect_inline_text(pair: pest::iterators::Pair<'_, Rule>) -> String {
    let mut out = String::new();
    collect_inline_text_inner(pair, &mut out);
    out
}

fn collect_inline_text_inner(pair: pest::iterators::Pair<'_, Rule>, out: &mut String) {
    match pair.as_rule() {
        Rule::non_inline_start
        | Rule::inline_nested_start
        | Rule::escape
        | Rule::not_newline
        | Rule::marker
        | Rule::attr_value
        | Rule::num_content => {
            let text = pair.as_str();
            if let Some(stripped) = text.strip_prefix('\\') {
                out.push_str(stripped);
            } else {
                out.push_str(text);
            }
        }
        _ => {
            for child in pair.into_inner() {
                collect_inline_text_inner(child, out);
            }
        }
    }
}

fn parse_heading(pair: pest::iterators::Pair<'_, Rule>) -> (Option<String>, Option<String>) {
    let mut num = None;
    let mut heading = None;
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::hier_element_heading_num => {
                let text = collect_inline_text(child).trim().to_string();
                if !text.is_empty() {
                    num = Some(text);
                }
            }
            Rule::hier_element_heading_heading => {
                let mut text = collect_inline_text(child).trim().to_string();
                if let Some(stripped) = text.strip_prefix('-') {
                    text = stripped.trim_start().to_string();
                }
                if !text.is_empty() {
                    heading = Some(text);
                }
            }
            _ => {}
        }
    }
    (num, heading)
}

fn hier_name(name: &str) -> String {
    match name.to_ascii_lowercase().as_str() {
        "art" => "article".to_string(),
        "chap" => "chapter".to_string(),
        "para" => "paragraph".to_string(),
        "sec" => "section".to_string(),
        "subchap" => "subchapter".to_string(),
        "subpara" => "subparagraph".to_string(),
        "subsec" => "subsection".to_string(),
        other => other.to_string(),
    }
}

fn is_hier_name(name: &str) -> bool {
    matches!(
        name,
        "alinea"
            | "article"
            | "book"
            | "chapter"
            | "clause"
            | "division"
            | "indent"
            | "level"
            | "list"
            | "paragraph"
            | "part"
            | "point"
            | "proviso"
            | "rule"
            | "section"
            | "subchapter"
            | "subclause"
            | "subdivision"
            | "sublist"
            | "subparagraph"
            | "subpart"
            | "subrule"
            | "subsection"
            | "subtitle"
            | "title"
            | "tome"
            | "transitional"
    )
}

fn rewrite_all_eids(element: &mut XmlElement, prefix: &str) {
    let mut rewriter = EidRewriter::default();
    rewriter.rewrite(element, prefix);
}

#[derive(Default)]
struct EidRewriter {
    ids: IdGenerator,
    counters: HashMap<String, HashMap<String, usize>>,
    eid_counter: HashMap<String, usize>,
}

impl EidRewriter {
    fn rewrite(&mut self, element: &mut XmlElement, prefix: &str) {
        if element.name == "meta" {
            return;
        }

        let mut child_prefix = prefix.to_string();
        if !id_exempt().contains(element.name.as_str())
            && !id_exempt_but_pass_to_children().contains(element.name.as_str())
        {
            let num = element
                .children
                .iter()
                .find_map(|child| match child {
                    XmlNode::Element(el) if el.name == "num" => Some(el.text_content()),
                    _ => None,
                })
                .unwrap_or_default();
            let eid = self.get_eid(prefix, &element.name, &num);
            element.attrs.insert("eId".to_string(), eid.clone());
            child_prefix = eid;
        }

        if id_exempt_but_pass_to_children().contains(element.name.as_str()) {
            child_prefix = if child_prefix.is_empty() {
                element.name.to_ascii_lowercase()
            } else {
                format!("{}__{}", child_prefix, element.name.to_ascii_lowercase())
            };
        }

        for child in &mut element.children {
            if let XmlNode::Element(el) = child {
                self.rewrite(el, &child_prefix);
            }
        }
    }

    fn get_eid(&mut self, prefix: &str, name: &str, num: &str) -> String {
        let mut eid = String::new();
        if !prefix.is_empty() {
            eid.push_str(prefix);
            eid.push_str("__");
        }
        eid.push_str(alias(name));

        let mut nn = false;
        let mut clean_num = self.ids.clean_num(num);
        if clean_num.is_empty() && num_expected().contains(name) {
            clean_num = "nn".to_string();
            nn = true;
        }
        if clean_num.is_empty() {
            clean_num = self.incr(prefix, name).to_string();
        }
        self.ensure_unique(format!("{eid}_{clean_num}"), nn)
    }

    fn incr(&mut self, prefix: &str, name: &str) -> usize {
        let sub = self.counters.entry(prefix.to_string()).or_default();
        let count = sub.entry(name.to_string()).or_default();
        *count += 1;
        *count
    }

    fn ensure_unique(&mut self, eid: String, nn: bool) -> String {
        let count = {
            let count = self.eid_counter.entry(eid.clone()).or_default();
            *count += 1;
            *count
        };
        if count == 1 && !nn {
            return eid;
        }
        self.ensure_unique(format!("{eid}_{count}"), false)
    }
}

impl XmlElement {
    fn text_content(&self) -> String {
        let mut out = String::new();
        for child in &self.children {
            match child {
                XmlNode::Element(el) => out.push_str(&el.text_content()),
                XmlNode::Text(text) => out.push_str(text),
            }
        }
        out
    }

    fn to_xml_string(&self) -> String {
        let mut out = String::new();
        self.write_xml(&mut out);
        out
    }

    fn write_xml(&self, out: &mut String) {
        out.push('<');
        out.push_str(&self.name);
        for (name, value) in &self.attrs {
            out.push(' ');
            out.push_str(name);
            out.push_str("=\"");
            escape_attr(value, out);
            out.push('"');
        }
        if self.children.is_empty() {
            out.push_str("/>");
            return;
        }
        out.push('>');
        for child in &self.children {
            match child {
                XmlNode::Element(el) => el.write_xml(out),
                XmlNode::Text(text) => escape_text(text, out),
            }
        }
        out.push_str("</");
        out.push_str(&self.name);
        out.push('>');
    }
}

fn escape_text(text: &str, out: &mut String) {
    for c in text.chars() {
        match c {
            '&' => out.push_str("&amp;"),
            '<' => out.push_str("&lt;"),
            '>' => out.push_str("&gt;"),
            _ => out.push(c),
        }
    }
}

fn escape_attr(text: &str, out: &mut String) {
    for c in text.chars() {
        match c {
            '&' => out.push_str("&amp;"),
            '<' => out.push_str("&lt;"),
            '"' => out.push_str("&quot;"),
            _ => out.push(c),
        }
    }
}

fn id_exempt() -> HashSet<&'static str> {
    "akomaNtoso act amendment amendmentList bill debate debateReport doc documentCollection judgment officialGazette portion statement amendmentBody attachments body collectionBody components coverPage debateBody judgmentBody mainBody meta portionBody br tr td th num heading subheading content abbr b i u sub sup ins del inline img remark span"
        .split_whitespace()
        .collect()
}

fn id_exempt_but_pass_to_children() -> HashSet<&'static str> {
    "arguments background conclusions decision header intro introduction motivation preamble preface remedies wrapUp"
        .split_whitespace()
        .collect()
}

fn num_expected() -> HashSet<&'static str> {
    "alinea article book chapter clause division indent item level list paragraph part point proviso rule section subchapter subclause subdivision sublist subparagraph subpart subrule subsection subtitle title tome transitional"
        .split_whitespace()
        .collect()
}

fn alias(name: &str) -> &str {
    match name {
        "alinea" => "al",
        "amendmentBody" => "body",
        "article" => "art",
        "attachment" => "att",
        "blockList" => "list",
        "chapter" => "chp",
        "citation" => "cit",
        "citations" => "cits",
        "clause" => "cl",
        "component" => "cmp",
        "components" => "cmpnts",
        "componentRef" => "cref",
        "debateBody" => "body",
        "debateSection" => "dbsect",
        "division" => "dvs",
        "documentRef" => "dref",
        "eventRef" => "eref",
        "judgmentBody" => "body",
        "listIntroduction" => "intro",
        "listWrapUp" => "wrapup",
        "mainBody" => "body",
        "paragraph" => "para",
        "quotedStructure" => "qstr",
        "quotedText" => "qtext",
        "recital" => "rec",
        "recitals" => "recs",
        "section" => "sec",
        "subchapter" => "subchp",
        "subclause" => "subcl",
        "subdivision" => "subdvs",
        "subparagraph" => "subpara",
        "subsection" => "subsec",
        "temporalGroup" => "tmpg",
        "wrapUp" => "wrapup",
        other => other,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_statement_xml() {
        let xml = parse_to_xml("", DocumentRoot::Statement).unwrap();
        assert!(xml.contains("<statement"));
        assert!(xml.contains("<mainBody><p eId=\"p_1\"/></mainBody>"));
    }

    #[test]
    fn simple_act_xml_contains_hierarchy_and_eids() {
        let xml = parse_to_xml(
            "CHAPTER 1 - Heading\n\n  SECTION 1 - Short title\n\n    Some text.",
            DocumentRoot::Act,
        )
        .unwrap();
        assert!(xml.contains("<chapter eId=\"chp_1\">"));
        assert!(xml.contains("<section eId=\"chp_1__sec_1\">"));
        assert!(xml.contains("<p eId=\"chp_1__sec_1__p_1\">Some text.</p>"));
    }

    #[test]
    fn simple_inline_xml_preserves_elements() {
        let xml =
            parse_to_xml("P Hello **bold** and //italics//", DocumentRoot::Statement).unwrap();
        assert!(xml.contains("Hello <b>bold</b> and <i>italics</i>"));
    }

    #[test]
    fn paragraph_attrs_are_preserved() {
        let xml = parse_to_xml("P.rtl{foo bar} Text", DocumentRoot::Statement).unwrap();
        assert!(xml.contains("<p class=\"rtl\" eId=\"p_1\" foo=\"bar\">Text</p>"));
    }

    #[test]
    fn block_list_xml() {
        let xml = parse_to_xml(
            "ITEMS\n  ITEM (a)\n    first\n\n  ITEM (b) - Heading\n    second",
            DocumentRoot::Statement,
        )
        .unwrap();
        assert!(xml.contains("<blockList eId=\"list_1\">"));
        assert!(xml.contains("<item eId=\"list_1__item_a\">"));
        assert!(xml.contains("<num>(a)</num>"));
        assert!(xml.contains("<heading>Heading</heading>"));
    }

    #[test]
    fn bullet_list_xml() {
        let xml = parse_to_xml("BULLETS\n  * first\n  * second", DocumentRoot::Statement).unwrap();
        assert!(xml.contains("<ul eId=\"ul_1\">"));
        assert!(xml.contains("<li eId=\"ul_1__li_1\"><p eId=\"ul_1__li_1__p_1\">first</p></li>"));
    }

    #[test]
    fn table_xml() {
        let xml = parse_to_xml(
            "TABLE\n  TR\n    TH\n      heading\n    TC{colspan 2}\n      cell",
            DocumentRoot::Statement,
        )
        .unwrap();
        assert!(xml.contains("<table eId=\"table_1\">"));
        assert!(xml.contains("<th><p eId=\"table_1__p_1\">heading</p></th>"));
        assert!(xml.contains("<td colspan=\"2\"><p eId=\"table_1__p_2\">cell</p></td>"));
    }
}
