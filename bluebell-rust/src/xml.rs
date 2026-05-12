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

pub fn parse_to_akn_xml(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_akn_xml(&preprocessed, root, frbr_uri)
}

pub fn parse_preprocessed_to_akn_xml(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
) -> Result<String, XmlError> {
    let pairs = parse_pairs_preprocessed(text, root)?;
    let mut doc_el = document_to_xml(root, pairs);
    doc_el.attrs.remove("xmlns");
    add_attachment_doc_meta(&mut doc_el, frbr_uri);
    resolve_displaced_content(&mut doc_el);
    doc_el
        .children
        .insert(0, XmlNode::Element(make_meta(frbr_uri, root_name(root))));
    let mut akn = XmlElement::new("akomaNtoso").attr("xmlns", AKN_NS);
    akn.children.push(XmlNode::Element(doc_el));
    rewrite_all_eids(&mut akn, "");
    Ok(akn.to_xml_string())
}

fn add_attachment_doc_meta(element: &mut XmlElement, frbr_uri: &str) {
    if element.name == "doc"
        && !element
            .children
            .iter()
            .any(|child| matches!(child, XmlNode::Element(el) if el.name == "meta"))
    {
        element
            .children
            .insert(0, XmlNode::Element(make_attachment_meta(frbr_uri)));
    }
    for child in &mut element.children {
        if let XmlNode::Element(el) = child {
            add_attachment_doc_meta(el, frbr_uri);
        }
    }
}

pub fn parse_preprocessed_to_xml(text: &str, root: DocumentRoot) -> Result<String, XmlError> {
    let pairs = parse_pairs_preprocessed(text, root)?;
    let mut root_el = document_to_xml(root, pairs);
    resolve_displaced_content(&mut root_el);
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

fn document_to_xml(root: DocumentRoot, pairs: pest::iterators::Pairs<'_, Rule>) -> XmlElement {
    let mut parts = Vec::new();
    for pair in pairs {
        collect_document_parts(pair, &mut parts);
    }
    if parts.is_empty() {
        return build_document(root);
    }

    let mut root_el = XmlElement::new(root_name(root)).attr("name", root_name(root));
    match root {
        DocumentRoot::Act | DocumentRoot::Bill => {
            push_part(&mut root_el, &parts, "preface");
            push_part(&mut root_el, &parts, "preamble");
            push_required_part(&mut root_el, &parts, "body", default_body());
            push_part(&mut root_el, &parts, "conclusions");
            push_part(&mut root_el, &parts, "attachments");
        }
        DocumentRoot::Statement | DocumentRoot::Doc | DocumentRoot::DebateReport => {
            push_part(&mut root_el, &parts, "preface");
            push_part(&mut root_el, &parts, "preamble");
            push_required_part(
                &mut root_el,
                &parts,
                "mainBody",
                XmlElement::new("mainBody").child(XmlElement::new("p")),
            );
            push_part(&mut root_el, &parts, "conclusions");
            push_part(&mut root_el, &parts, "attachments");
        }
        DocumentRoot::Judgment => {
            root_el
                .children
                .push(XmlNode::Element(XmlElement::new("header")));
            let mut judgment_body = XmlElement::new("judgmentBody");
            for name in [
                "introduction",
                "background",
                "arguments",
                "remedies",
                "motivation",
                "decision",
            ] {
                push_part(&mut judgment_body, &parts, name);
            }
            if judgment_body.children.is_empty() {
                judgment_body.children.push(XmlNode::Element(
                    XmlElement::new("introduction").child(XmlElement::new("p")),
                ));
            }
            root_el.children.push(XmlNode::Element(judgment_body));
            push_part(&mut root_el, &parts, "conclusions");
            push_part(&mut root_el, &parts, "attachments");
        }
        DocumentRoot::Debate => {
            push_part(&mut root_el, &parts, "preface");
            push_required_part(
                &mut root_el,
                &parts,
                "debateBody",
                XmlElement::new("debateBody").child(
                    XmlElement::new("debateSection")
                        .attr("name", "debateSection")
                        .child(XmlElement::new("p")),
                ),
            );
            push_part(&mut root_el, &parts, "conclusions");
            push_part(&mut root_el, &parts, "attachments");
        }
    }
    root_el
}

fn root_name(root: DocumentRoot) -> &'static str {
    match root {
        DocumentRoot::Act => "act",
        DocumentRoot::Bill => "bill",
        DocumentRoot::Debate => "debate",
        DocumentRoot::DebateReport => "debateReport",
        DocumentRoot::Doc => "doc",
        DocumentRoot::Judgment => "judgment",
        DocumentRoot::Statement => "statement",
    }
}

fn make_meta(frbr_uri: &str, root_name: &str) -> XmlElement {
    let info = FrbrInfo::parse(frbr_uri, root_name);
    XmlElement::new("meta")
        .child(
            XmlElement::new("identification")
                .attr("source", "#cobalt")
                .child(
                    XmlElement::new("FRBRWork")
                        .child(XmlElement::new("FRBRthis").attr("value", info.work_uri.clone()))
                        .child(XmlElement::new("FRBRuri").attr("value", info.work_uri.clone()))
                        .child(
                            XmlElement::new("FRBRalias")
                                .attr("value", "Untitled")
                                .attr("name", "title"),
                        )
                        .child(
                            XmlElement::new("FRBRdate")
                                .attr("date", info.work_date())
                                .attr("name", "Generation"),
                        )
                        .child(XmlElement::new("FRBRauthor").attr("href", ""))
                        .child(XmlElement::new("FRBRcountry").attr("value", info.country.clone()))
                        .child(XmlElement::new("FRBRnumber").attr("value", info.number.clone())),
                )
                .child(
                    XmlElement::new("FRBRExpression")
                        .child(XmlElement::new("FRBRthis").attr("value", info.expr_uri.clone()))
                        .child(XmlElement::new("FRBRuri").attr("value", info.expr_uri.clone()))
                        .child(
                            XmlElement::new("FRBRdate")
                                .attr("date", "2026-05-12")
                                .attr("name", "Generation"),
                        )
                        .child(XmlElement::new("FRBRauthor").attr("href", ""))
                        .child(XmlElement::new("FRBRlanguage").attr("language", "eng")),
                )
                .child(
                    XmlElement::new("FRBRManifestation")
                        .child(XmlElement::new("FRBRthis").attr("value", info.expr_uri.clone()))
                        .child(XmlElement::new("FRBRuri").attr("value", info.expr_uri))
                        .child(
                            XmlElement::new("FRBRdate")
                                .attr("date", "2026-05-12")
                                .attr("name", "Generation"),
                        )
                        .child(XmlElement::new("FRBRauthor").attr("href", "")),
                ),
        )
        .child(
            XmlElement::new("references")
                .attr("source", "#cobalt")
                .child(
                    XmlElement::new("TLCOrganization")
                        .attr("eId", "cobalt")
                        .attr("href", "https://github.com/laws-africa/cobalt")
                        .attr("showAs", "cobalt"),
                ),
        )
}

fn make_attachment_meta(frbr_uri: &str) -> XmlElement {
    let info = FrbrInfo::parse(frbr_uri, "doc");
    XmlElement::new("meta").child(
        XmlElement::new("identification")
            .attr("source", "#cobalt")
            .child(
                XmlElement::new("FRBRWork")
                    .child(
                        XmlElement::new("FRBRthis")
                            .attr("value", format!("{}/!attachment_1", info.work_uri)),
                    )
                    .child(XmlElement::new("FRBRuri").attr("value", info.work_uri.clone()))
                    .child(
                        XmlElement::new("FRBRalias")
                            .attr("value", "Untitled")
                            .attr("name", "title"),
                    )
                    .child(
                        XmlElement::new("FRBRdate")
                            .attr("date", info.work_date())
                            .attr("name", "Generation"),
                    )
                    .child(XmlElement::new("FRBRauthor").attr("href", ""))
                    .child(XmlElement::new("FRBRcountry").attr("value", info.country.clone()))
                    .child(XmlElement::new("FRBRnumber").attr("value", info.number.clone())),
            )
            .child(
                XmlElement::new("FRBRExpression")
                    .child(
                        XmlElement::new("FRBRthis")
                            .attr("value", format!("{}/!attachment_1", info.expr_uri)),
                    )
                    .child(XmlElement::new("FRBRuri").attr("value", info.expr_uri.clone()))
                    .child(
                        XmlElement::new("FRBRdate")
                            .attr("date", "2026-05-12")
                            .attr("name", "Generation"),
                    )
                    .child(XmlElement::new("FRBRauthor").attr("href", ""))
                    .child(XmlElement::new("FRBRlanguage").attr("language", "eng")),
            )
            .child(
                XmlElement::new("FRBRManifestation")
                    .child(
                        XmlElement::new("FRBRthis")
                            .attr("value", format!("{}/!attachment_1", info.expr_uri)),
                    )
                    .child(XmlElement::new("FRBRuri").attr("value", info.expr_uri))
                    .child(
                        XmlElement::new("FRBRdate")
                            .attr("date", "2026-05-12")
                            .attr("name", "Generation"),
                    )
                    .child(XmlElement::new("FRBRauthor").attr("href", "")),
            ),
    )
}

struct FrbrInfo {
    work_uri: String,
    expr_uri: String,
    country: String,
    year: String,
    number: String,
}

impl FrbrInfo {
    fn parse(frbr_uri: &str, root_name: &str) -> Self {
        let parts: Vec<_> = frbr_uri.trim_matches('/').split('/').collect();
        let country = parts.get(1).copied().unwrap_or("za").to_string();
        let year = parts.get(3).copied().unwrap_or("2026").to_string();
        let number = parts.get(4).copied().unwrap_or("1").to_string();
        let work_uri = if frbr_uri.starts_with("/akn/") {
            frbr_uri.to_string()
        } else {
            format!("/akn/{country}/{root_name}/{year}/{number}")
        };
        let expr_uri = format!("{work_uri}/eng");
        Self {
            work_uri,
            expr_uri,
            country,
            year,
            number,
        }
    }

    fn work_date(&self) -> String {
        if self.year.len() == 4 && self.year.chars().all(|c| c.is_ascii_digit()) {
            format!("{}-01-01", self.year)
        } else {
            self.year.clone()
        }
    }
}

fn push_part(root: &mut XmlElement, parts: &[XmlElement], name: &str) {
    if let Some(part) = parts
        .iter()
        .find(|part| part.name == name && !part.children.is_empty())
    {
        root.children.push(XmlNode::Element(part.clone()));
    }
}

fn push_required_part(
    root: &mut XmlElement,
    parts: &[XmlElement],
    name: &str,
    default: XmlElement,
) {
    if let Some(part) = parts.iter().find(|part| part.name == name) {
        root.children.push(XmlNode::Element(part.clone()));
    } else {
        root.children.push(XmlNode::Element(default));
    }
}

fn collect_document_parts(pair: pest::iterators::Pair<'_, Rule>, parts: &mut Vec<XmlElement>) {
    match pair.as_rule() {
        Rule::preface => parts.push(container_to_xml("preface", pair, false)),
        Rule::preamble => parts.push(container_to_xml("preamble", pair, false)),
        Rule::conclusions => parts.push(container_to_xml("conclusions", pair, false)),
        Rule::introduction => parts.push(container_to_xml("introduction", pair, true)),
        Rule::background => parts.push(container_to_xml("background", pair, true)),
        Rule::arguments => parts.push(container_to_xml("arguments", pair, true)),
        Rule::remedies => parts.push(container_to_xml("remedies", pair, true)),
        Rule::motivation => parts.push(container_to_xml("motivation", pair, true)),
        Rule::decision => parts.push(container_to_xml("decision", pair, true)),
        Rule::body => parts.push(body_container_to_xml("body", pair)),
        Rule::mainBody => parts.push(body_container_to_xml("mainBody", pair)),
        Rule::debateBody => parts.push(body_container_to_xml("debateBody", pair)),
        Rule::attachments => parts.push(attachments_to_xml(pair)),
        _ => {
            for child in pair.into_inner() {
                collect_document_parts(child, parts);
            }
        }
    }
}

fn container_to_xml(
    name: &str,
    pair: pest::iterators::Pair<'_, Rule>,
    allow_hier: bool,
) -> XmlElement {
    let mut blocks = Vec::new();
    collect_container_blocks(pair, &mut blocks, allow_hier);
    XmlElement::new(name).children(wrap_top_level_crossheadings(blocks))
}

fn wrap_top_level_crossheadings(blocks: Vec<XmlElement>) -> Vec<XmlElement> {
    let mut out = Vec::new();
    let mut pending = Vec::new();
    for block in blocks {
        if block.name == "crossHeading" {
            pending.push(block);
        } else {
            if !pending.is_empty() {
                out.push(
                    XmlElement::new("hcontainer")
                        .attr("name", "hcontainer")
                        .children(std::mem::take(&mut pending)),
                );
            }
            out.push(block);
        }
    }
    if !pending.is_empty() {
        out.push(
            XmlElement::new("hcontainer")
                .attr("name", "hcontainer")
                .children(pending),
        );
    }
    out
}

fn body_container_to_xml(name: &str, pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut blocks = Vec::new();
    collect_container_blocks(pair, &mut blocks, true);
    match name {
        "body" => body_from_blocks(blocks),
        "debateBody" => XmlElement::new(name).children(blocks),
        _ => XmlElement::new(name).children(if blocks.is_empty() {
            vec![XmlElement::new("p")]
        } else {
            blocks
        }),
    }
}

fn collect_container_blocks(
    pair: pest::iterators::Pair<'_, Rule>,
    blocks: &mut Vec<XmlElement>,
    allow_hier: bool,
) {
    match pair.as_rule() {
        Rule::hier_element_block if allow_hier => blocks.push(hier_to_xml(pair)),
        Rule::hier_element_block => {
            blocks.push(XmlElement::new("p").text(pair.as_str().trim().to_string()))
        }
        Rule::line
        | Rule::p
        | Rule::speech_container
        | Rule::speech_group
        | Rule::speech_block
        | Rule::block_list
        | Rule::bullet_list
        | Rule::table
        | Rule::longtitle
        | Rule::crossheading
        | Rule::footnote
        | Rule::block_quote => collect_blocks(pair, blocks),
        _ => {
            for child in pair.into_inner() {
                collect_container_blocks(child, blocks, allow_hier);
            }
        }
    }
}

fn default_body() -> XmlElement {
    body_from_blocks(Vec::new())
}

fn body_from_blocks(blocks: Vec<XmlElement>) -> XmlElement {
    if blocks.is_empty() {
        return XmlElement::new("body").child(
            XmlElement::new("hcontainer")
                .attr("name", "hcontainer")
                .child(XmlElement::new("content").child(XmlElement::new("p"))),
        );
    }
    if blocks
        .iter()
        .any(|block| is_hier_name(&block.name) || block.name == "crossHeading")
    {
        let mut body = XmlElement::new("body");
        body.children = body_mixed_children(blocks);
        body
    } else {
        XmlElement::new("body").child(
            XmlElement::new("hcontainer")
                .attr("name", "hcontainer")
                .child(XmlElement::new("content").children(blocks)),
        )
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
        Rule::speech_container => blocks.push(speech_container_to_xml(pair)),
        Rule::speech_group => blocks.push(speech_group_to_xml(pair)),
        Rule::speech_block => blocks.push(speech_block_to_xml(pair)),
        Rule::longtitle => blocks.push(line_element_to_xml(pair, "longTitle")),
        Rule::crossheading => blocks.push(line_element_to_xml(pair, "crossHeading")),
        Rule::block_quote => blocks.push(block_quote_to_xml(pair)),
        Rule::footnote => blocks.push(footnote_to_xml(pair)),
        _ => {
            for child in pair.into_inner() {
                collect_blocks(child, blocks);
            }
        }
    }
}

fn attachments_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut attachments = XmlElement::new("attachments");
    for child in pair.into_inner() {
        if child.as_rule() == Rule::attachment {
            attachments
                .children
                .push(XmlNode::Element(attachment_to_xml(child)));
        }
    }
    attachments
}

fn attachment_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut marker_name = "attachment".to_string();
    let mut att_attrs = BTreeMap::new();
    let mut heading = None;
    let mut blocks = Vec::new();
    let mut nested = None;

    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::attachment_marker => marker_name = child.as_str().to_ascii_lowercase(),
            Rule::block_attrs => att_attrs.extend(block_attrs_to_map(child)),
            Rule::attachment_heading => {
                let text = collect_inline_text(child).trim().to_string();
                if !text.is_empty() {
                    heading = Some(text);
                }
            }
            Rule::attachments => nested = Some(attachments_to_xml(child)),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }

    let mut attachment = XmlElement::new("attachment");
    attachment.attrs = att_attrs;
    if let Some(heading) = heading {
        attachment
            .children
            .push(XmlNode::Element(XmlElement::new("heading").text(heading)));
    }

    let main_body = XmlElement::new("mainBody").children(if blocks.is_empty() {
        vec![XmlElement::new("p")]
    } else {
        wrap_top_level_crossheadings(blocks)
    });
    let mut doc = XmlElement::new("doc")
        .attr("name", marker_name)
        .child(main_body);
    if let Some(nested) = nested {
        doc.children.push(XmlNode::Element(nested));
    }
    attachment.children.push(XmlNode::Element(doc));
    attachment
}

fn speech_container_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    speech_hier_to_xml(pair, false)
}

fn speech_group_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    speech_hier_to_xml(pair, true)
}

fn speech_hier_to_xml(pair: pest::iterators::Pair<'_, Rule>, group: bool) -> XmlElement {
    let mut name = if group { "speech" } else { "debateSection" }.to_string();
    let mut attrs = BTreeMap::new();
    let mut heading = None;
    let mut from = None;
    let mut blocks = Vec::new();

    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::speech_container_name | Rule::speech_group_name => {
                name = speech_name(child.as_str())
            }
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            Rule::hier_element_heading => {
                let (_num, h) = parse_heading(child);
                heading = h;
            }
            Rule::speech_from => from = Some(collect_inline_text(child).trim().to_string()),
            Rule::speech_container => blocks.push(speech_container_to_xml(child)),
            Rule::speech_group => blocks.push(speech_group_to_xml(child)),
            Rule::speech_block => blocks.push(speech_block_to_xml(child)),
            Rule::line | Rule::p | Rule::block_list | Rule::bullet_list | Rule::table => {
                collect_blocks(child, &mut blocks)
            }
            _ => collect_block_descendants(child, &mut blocks),
        }
    }

    if name == "debateSection" {
        attrs
            .entry("name".to_string())
            .or_insert_with(|| "debateSection".to_string());
    }
    if group && !attrs.contains_key("by") {
        if let Some(from) = &from {
            let by: String = from.chars().filter(|c| c.is_alphanumeric()).collect();
            attrs.insert("by".to_string(), format!("#{by}"));
        }
    }

    let mut el = XmlElement::new(name);
    el.attrs = attrs;
    if let Some(heading) = heading.filter(|heading| !heading.is_empty()) {
        el.children
            .push(XmlNode::Element(XmlElement::new("heading").text(heading)));
    }
    if let Some(from) = from {
        el.children
            .push(XmlNode::Element(XmlElement::new("from").text(from)));
    }
    el.children.extend(blocks.into_iter().map(XmlNode::Element));
    if el.children.is_empty() {
        el.children.push(XmlNode::Element(XmlElement::new("p")));
    }
    el
}

fn speech_block_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut name = "narrative".to_string();
    let mut attrs = BTreeMap::new();
    let mut children = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::speech_block_name => name = child.as_str().to_ascii_lowercase(),
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            _ => collect_inline_nodes_inner(child, &mut children),
        }
    }
    let mut el = XmlElement::new(name);
    el.attrs = attrs;
    el.children = merge_adjacent_text(children);
    el
}

fn speech_name(name: &str) -> String {
    match name.to_ascii_lowercase().as_str() {
        "administrationofoath" => "administrationOfOath".to_string(),
        "debatesection" => "debateSection".to_string(),
        "declarationofvote" => "declarationOfVote".to_string(),
        "ministerialstatements" => "ministerialStatements".to_string(),
        "noticesofmotion" => "noticesOfMotion".to_string(),
        "oralstatements" => "oralStatements".to_string(),
        "personalstatements" => "personalStatements".to_string(),
        "pointoforder" => "pointOfOrder".to_string(),
        "proceduralmotions" => "proceduralMotions".to_string(),
        "rollcall" => "rollCall".to_string(),
        "writtenstatements" => "writtenStatements".to_string(),
        other => other.to_string(),
    }
}

fn line_element_to_xml(pair: pest::iterators::Pair<'_, Rule>, name: &str) -> XmlElement {
    let mut el = XmlElement::new(name);
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => el.attrs.extend(block_attrs_to_map(child)),
            _ => collect_inline_nodes_inner(child, &mut el.children),
        }
    }
    el.children = merge_adjacent_text(std::mem::take(&mut el.children));
    if name == "longTitle" && !el.children.is_empty() {
        let mut p = XmlElement::new("p");
        p.children = std::mem::take(&mut el.children);
        el.children.push(XmlNode::Element(p));
    }
    el
}

fn block_quote_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut quote_attrs = BTreeMap::new();
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => quote_attrs.extend(block_attrs_to_map(child)),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    let mut embedded = XmlElement::new("embeddedStructure").children(blocks);
    embedded.attrs = quote_attrs;
    XmlElement::new("block")
        .attr("name", "quote")
        .child(embedded)
}

fn footnote_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut marker = String::new();
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::marker => marker = child.as_str().trim().to_string(),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    let mut displaced = XmlElement::new("displaced")
        .attr("marker", marker)
        .attr("name", "footnote");
    displaced.children = blocks.into_iter().map(XmlNode::Element).collect();
    displaced
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
        | Rule::speech_container
        | Rule::speech_group
        | Rule::speech_block
        | Rule::block_list
        | Rule::bullet_list
        | Rule::table
        | Rule::longtitle
        | Rule::crossheading
        | Rule::footnote
        | Rule::block_quote => collect_blocks(pair, blocks),
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
    } else if content
        .iter()
        .any(|c| is_hier_name(&c.name) || c.name == "crossHeading")
    {
        el.children.extend(mixed_hier_children(content));
    } else {
        el.children.push(XmlNode::Element(
            XmlElement::new("content").children(content),
        ));
    }
    el
}

fn mixed_hier_children(content: Vec<XmlElement>) -> Vec<XmlNode> {
    let mut children = Vec::new();
    let mut pending = Vec::new();
    let mut seen_hier = false;

    for child in content {
        let is_hier = is_hier_name(&child.name) || child.name == "crossHeading";
        if is_hier {
            if !pending.is_empty() {
                let wrapper = if seen_hier { "hcontainer" } else { "intro" };
                children.push(XmlNode::Element(wrap_content_group(
                    wrapper,
                    std::mem::take(&mut pending),
                )));
            }
            seen_hier = true;
            children.push(XmlNode::Element(child));
        } else {
            pending.push(child);
        }
    }

    if !pending.is_empty() {
        let wrapper = if seen_hier { "wrapUp" } else { "intro" };
        children.push(XmlNode::Element(wrap_content_group(wrapper, pending)));
    }

    children
}

fn body_mixed_children(content: Vec<XmlElement>) -> Vec<XmlNode> {
    let mut children = Vec::new();
    let mut pending_cross = Vec::new();
    let mut pending_blocks = Vec::new();

    for child in content {
        if child.name == "crossHeading" {
            if !pending_blocks.is_empty() {
                children.push(XmlNode::Element(
                    XmlElement::new("hcontainer")
                        .attr("name", "hcontainer")
                        .child(
                            XmlElement::new("content")
                                .children(std::mem::take(&mut pending_blocks)),
                        ),
                ));
            }
            pending_cross.push(child);
        } else if is_hier_name(&child.name) {
            if !pending_cross.is_empty() {
                children.push(XmlNode::Element(
                    XmlElement::new("hcontainer")
                        .attr("name", "hcontainer")
                        .children(std::mem::take(&mut pending_cross)),
                ));
            }
            if !pending_blocks.is_empty() {
                children.push(XmlNode::Element(
                    XmlElement::new("hcontainer")
                        .attr("name", "hcontainer")
                        .child(
                            XmlElement::new("content")
                                .children(std::mem::take(&mut pending_blocks)),
                        ),
                ));
            }
            children.push(XmlNode::Element(child));
        } else {
            if !pending_cross.is_empty() {
                children.push(XmlNode::Element(
                    XmlElement::new("hcontainer")
                        .attr("name", "hcontainer")
                        .children(std::mem::take(&mut pending_cross)),
                ));
            }
            pending_blocks.push(child);
        }
    }

    if !pending_cross.is_empty() {
        children.push(XmlNode::Element(
            XmlElement::new("hcontainer")
                .attr("name", "hcontainer")
                .children(pending_cross),
        ));
    }
    if !pending_blocks.is_empty() {
        children.push(XmlNode::Element(
            XmlElement::new("hcontainer")
                .attr("name", "hcontainer")
                .child(XmlElement::new("content").children(pending_blocks)),
        ));
    }
    children
}

fn wrap_content_group(name: &str, blocks: Vec<XmlElement>) -> XmlElement {
    if name == "hcontainer" {
        XmlElement::new("hcontainer")
            .attr("name", "hcontainer")
            .child(XmlElement::new("content").children(blocks))
    } else {
        XmlElement::new(name).children(blocks)
    }
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
        Rule::image => nodes.push(XmlNode::Element(image_to_xml(pair.as_str()))),
        Rule::ref_ => nodes.push(XmlNode::Element(ref_to_xml(pair.as_str()))),
        Rule::footnote_ref => nodes.push(XmlNode::Element(footnote_ref_to_xml(pair.as_str()))),
        Rule::standard_inline => nodes.push(XmlNode::Element(standard_inline_to_xml(pair))),
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

fn image_to_xml(text: &str) -> XmlElement {
    let body = text
        .strip_prefix("{{IMG")
        .and_then(|s| s.strip_suffix("}}"))
        .unwrap_or("")
        .trim();
    let (src, alt) = split_first_word(body);
    let mut img = XmlElement::new("img").attr("src", src);
    if !alt.is_empty() {
        img.attrs.insert("alt".to_string(), alt.to_string());
    }
    img
}

fn ref_to_xml(text: &str) -> XmlElement {
    let body = text
        .strip_prefix("{{>")
        .and_then(|s| s.strip_suffix("}}"))
        .unwrap_or("");
    let (href, label) = split_first_word(body);
    let mut ref_el = XmlElement::new("ref").attr("href", href);
    if !label.is_empty() {
        ref_el.children.push(XmlNode::Text(label.to_string()));
    }
    ref_el
}

fn footnote_ref_to_xml(text: &str) -> XmlElement {
    let marker = text
        .strip_prefix("{{FOOTNOTE")
        .and_then(|s| s.strip_suffix("}}"))
        .unwrap_or("")
        .trim();
    XmlElement::new("authorialNote")
        .attr("marker", marker)
        .attr("placement", "bottom")
}

fn standard_inline_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut tag = "inline".to_string();
    let mut attrs = BTreeMap::new();
    let mut children = Vec::new();

    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::standard_inline_marker => tag = child.as_str().to_string(),
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            _ => collect_inline_nodes_inner(child, &mut children),
        }
    }

    let mut name = tag.as_str();
    match tag.as_str() {
        "em" => {
            name = "inline";
            attrs
                .entry("name".to_string())
                .or_insert_with(|| "em".to_string());
        }
        "+" => name = "ins",
        "-" => name = "del",
        "abbr" => {
            attrs.entry("title".to_string()).or_insert_with(String::new);
        }
        "term" => {
            attrs
                .entry("refersTo".to_string())
                .or_insert_with(String::new);
        }
        "inline" => {
            attrs
                .entry("name".to_string())
                .or_insert_with(|| "inline".to_string());
        }
        _ => {}
    }

    let mut el = XmlElement::new(name);
    el.attrs = attrs;
    el.children = merge_adjacent_text(children);
    el
}

fn split_first_word(text: &str) -> (&str, &str) {
    let trimmed = text.trim();
    if let Some((first, rest)) = trimmed.split_once(char::is_whitespace) {
        (first, rest.trim_start())
    } else {
        (trimmed, "")
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

fn resolve_displaced_content(root: &mut XmlElement) {
    let mut footnotes = HashMap::new();
    collect_displaced(root, &mut footnotes);
    apply_displaced(root, &footnotes);
    remove_displaced(root);
}

fn collect_displaced(element: &XmlElement, footnotes: &mut HashMap<String, Vec<XmlNode>>) {
    if element.name == "displaced"
        && element
            .attrs
            .get("name")
            .map(|name| name == "footnote")
            .unwrap_or(false)
    {
        if let Some(marker) = element.attrs.get("marker") {
            footnotes.insert(marker.clone(), element.children.clone());
        }
    }
    for child in &element.children {
        if let XmlNode::Element(el) = child {
            collect_displaced(el, footnotes);
        }
    }
}

fn apply_displaced(element: &mut XmlElement, footnotes: &HashMap<String, Vec<XmlNode>>) {
    if element.name == "authorialNote" {
        let marker = element.attrs.get("marker").cloned().unwrap_or_default();
        element.children = footnotes.get(&marker).cloned().unwrap_or_else(|| {
            vec![XmlNode::Element(
                XmlElement::new("p").text("(content missing)"),
            )]
        });
    }
    for child in &mut element.children {
        if let XmlNode::Element(el) = child {
            apply_displaced(el, footnotes);
        }
    }
}

fn remove_displaced(element: &mut XmlElement) {
    element.children.retain(|child| {
        !matches!(
            child,
            XmlNode::Element(el)
                if el.name == "displaced"
                    && el.attrs.get("name").map(|name| name == "footnote").unwrap_or(false)
        )
    });
    for child in &mut element.children {
        if let XmlNode::Element(el) = child {
            remove_displaced(el);
        }
    }
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

    #[test]
    fn refs_images_and_footnote_refs_xml() {
        let xml = parse_to_xml(
            "P See {{>https://example.com example}} {{IMG /x.png alt text}} {{FOOTNOTE 1}}",
            DocumentRoot::Statement,
        )
        .unwrap();
        assert!(xml.contains("<ref eId=\"p_1__ref_1\" href=\"https://example.com\">example</ref>"));
        assert!(xml.contains("<img alt=\"alt text\" src=\"/x.png\"/>"));
        assert!(xml.contains("<authorialNote eId=\"p_1__authorialNote_1\" marker=\"1\" placement=\"bottom\"><p eId=\"p_1__authorialNote_1__p_1\">(content missing)</p></authorialNote>"));
    }

    #[test]
    fn standard_inline_xml() {
        let xml = parse_to_xml(
            "P Text with {{term{refersTo #x}a term}} and {{+inserted}}",
            DocumentRoot::Statement,
        )
        .unwrap();
        assert!(xml.contains("<term eId=\"p_1__term_1\" refersTo=\"#x\">a term</term>"));
        assert!(xml.contains("<ins>inserted</ins>"));
    }

    #[test]
    fn document_containers_are_preserved() {
        let xml = parse_to_xml(
            "PREFACE\n  preface text\nPREAMBLE\n  preamble text\nBODY\n  body text\nCONCLUSIONS\n  done",
            DocumentRoot::Act,
        )
        .unwrap();
        assert!(xml.contains("<preface><p eId=\"preface__p_1\">preface text</p></preface>"));
        assert!(xml.contains("<preamble><p eId=\"preamble__p_1\">preamble text</p></preamble>"));
        assert!(xml.contains("<body><hcontainer eId=\"hcontainer_1\" name=\"hcontainer\"><content><p eId=\"hcontainer_1__p_1\">body text</p></content></hcontainer></body>"));
        assert!(xml.contains("<conclusions><p eId=\"conclusions__p_1\">done</p></conclusions>"));
    }

    #[test]
    fn quote_and_crossheading_xml() {
        let xml = parse_to_xml(
            "CROSSHEADING Intro\n\nQUOTE\n  quoted text",
            DocumentRoot::Statement,
        )
        .unwrap();
        assert!(xml.contains("<crossHeading eId=\"crossHeading_1\">Intro</crossHeading>"));
        assert!(xml.contains("<block eId=\"block_1\" name=\"quote\"><embeddedStructure eId=\"block_1__embeddedStructure_1\"><p eId=\"block_1__embeddedStructure_1__p_1\">quoted text</p></embeddedStructure></block>"));
    }

    #[test]
    fn footnote_content_is_resolved() {
        let xml = parse_to_xml(
            "P hello {{FOOTNOTE 1}} there\n\nFOOTNOTE 1\n  footnote text",
            DocumentRoot::Statement,
        )
        .unwrap();
        assert!(xml.contains("<authorialNote eId=\"p_1__authorialNote_1\" marker=\"1\" placement=\"bottom\"><p eId=\"p_1__authorialNote_1__p_1\">footnote text</p></authorialNote>"));
        assert!(!xml.contains("displaced"));
    }

    #[test]
    fn attachment_xml() {
        let xml = parse_to_xml(
            "ATTACHMENT Schedule\n  attached text",
            DocumentRoot::Statement,
        )
        .unwrap();
        assert!(xml.contains("<attachments>"));
        assert!(xml.contains("<attachment eId=\"att_1\"><heading>Schedule</heading><doc name=\"attachment\"><mainBody><p eId=\"att_1__p_1\">attached text</p></mainBody></doc></attachment>"));
    }

    #[test]
    fn debate_speech_xml() {
        let xml = parse_to_xml(
            "DEBATESECTION 1 - Debate\n  SPEECH\n    FROM Speaker Name\n    NARRATIVE Hello",
            DocumentRoot::Debate,
        )
        .unwrap();
        assert!(xml.contains("<debateSection eId=\"dbsect_1\" name=\"debateSection\">"));
        assert!(xml.contains("<speech by=\"#SpeakerName\" eId=\"dbsect_1__speech_1\">"));
        assert!(xml.contains("<from eId=\"dbsect_1__speech_1__from_1\">Speaker Name</from>"));
        assert!(
            xml.contains("<narrative eId=\"dbsect_1__speech_1__narrative_1\">Hello</narrative>")
        );
    }

    #[test]
    fn full_akn_xml_wraps_meta() {
        let xml = parse_to_akn_xml(
            "P Hello",
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
        )
        .unwrap();
        assert!(xml.starts_with("<akomaNtoso xmlns=\"http://docs.oasis-open.org/legaldocml/ns/akn/3.0\"><statement name=\"statement\"><meta>"));
        assert!(xml.contains("<FRBRuri value=\"/akn/za/statement/2022/1\"/>"));
        assert!(xml.contains("<mainBody><p eId=\"p_1\">Hello</p></mainBody>"));
    }
}
