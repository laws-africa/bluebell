use std::collections::{BTreeMap, HashMap, HashSet};
#[cfg(not(target_arch = "wasm32"))]
use std::time::{SystemTime, UNIX_EPOCH};

use crate::eid::IdGenerator;
use crate::frbr::{FrbrUri, InvalidFrbrUri};
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

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MetadataSource {
    pub show_as: String,
    pub eid: String,
    pub href: String,
}

impl MetadataSource {
    pub fn new(
        show_as: impl Into<String>,
        eid: impl Into<String>,
        href: impl Into<String>,
    ) -> Self {
        Self {
            show_as: show_as.into(),
            eid: eid.into(),
            href: href.into(),
        }
    }

    fn source_ref(&self) -> String {
        format!("#{}", self.eid)
    }
}

impl Default for MetadataSource {
    fn default() -> Self {
        Self::new("cobalt", "cobalt", "https://github.com/laws-africa/cobalt")
    }
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
    #[error(transparent)]
    FrbrUri(#[from] InvalidFrbrUri),
}

pub fn parse_to_xml(text: &str, root: DocumentRoot) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_xml(&preprocessed, root)
}

pub fn parse_to_xml_with_eid_prefix(
    text: &str,
    root: DocumentRoot,
    eid_prefix: &str,
) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_xml_with_eid_prefix(&preprocessed, root, eid_prefix)
}

pub fn parse_to_xml_document_or_fragment(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_xml_document_or_fragment(&preprocessed, root, frbr_uri)
}

pub fn parse_to_xml_document_or_fragment_with_eid_prefix(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
) -> Result<String, XmlError> {
    parse_to_xml_document_or_fragment_with_eid_prefix_and_source(
        text,
        root,
        frbr_uri,
        eid_prefix,
        &MetadataSource::default(),
    )
}

pub fn parse_to_xml_document_or_fragment_with_eid_prefix_and_source(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
    source: &MetadataSource,
) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_xml_document_or_fragment_with_eid_prefix_and_source(
        &preprocessed,
        root,
        frbr_uri,
        eid_prefix,
        source,
    )
}

pub fn parse_to_akn_xml(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_akn_xml(&preprocessed, root, frbr_uri)
}

pub fn parse_to_akn_xml_with_eid_prefix(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
) -> Result<String, XmlError> {
    parse_to_akn_xml_with_eid_prefix_and_source(
        text,
        root,
        frbr_uri,
        eid_prefix,
        &MetadataSource::default(),
    )
}

pub fn parse_to_akn_xml_with_eid_prefix_and_source(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
    source: &MetadataSource,
) -> Result<String, XmlError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed_to_akn_xml_with_eid_prefix_and_source(
        &preprocessed,
        root,
        frbr_uri,
        eid_prefix,
        source,
    )
}

pub fn parse_preprocessed_to_akn_xml(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
) -> Result<String, XmlError> {
    parse_preprocessed_to_akn_xml_with_eid_prefix(text, root, frbr_uri, "")
}

pub fn parse_preprocessed_to_akn_xml_with_eid_prefix(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
) -> Result<String, XmlError> {
    parse_preprocessed_to_akn_xml_with_eid_prefix_and_source(
        text,
        root,
        frbr_uri,
        eid_prefix,
        &MetadataSource::default(),
    )
}

pub fn parse_preprocessed_to_akn_xml_with_eid_prefix_and_source(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
    source: &MetadataSource,
) -> Result<String, XmlError> {
    if !root.is_document() {
        return parse_preprocessed_to_xml_fragment_with_eid_prefix_and_source(
            text, root, frbr_uri, eid_prefix, source,
        );
    }

    let frbr_uri = FrbrUri::parse(frbr_uri)?;
    let pairs = parse_pairs_preprocessed(text, root)?;
    let mut doc_el = document_to_xml(root, pairs);
    doc_el.attrs.remove("xmlns");
    resolve_displaced_content(&mut doc_el);
    normalise_empty_elements(&mut doc_el);
    add_attachment_doc_meta(&mut doc_el, &frbr_uri, source);
    doc_el
        .children
        .insert(0, XmlNode::Element(make_meta(&frbr_uri, source)));
    let mut akn = XmlElement::new("akomaNtoso").attr("xmlns", AKN_NS);
    akn.children.push(XmlNode::Element(doc_el));
    rewrite_all_eids(&mut akn, eid_prefix);
    Ok(akn.to_xml_string())
}

pub fn parse_preprocessed_to_xml_document_or_fragment(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
) -> Result<String, XmlError> {
    parse_preprocessed_to_xml_document_or_fragment_with_eid_prefix(text, root, frbr_uri, "")
}

pub fn parse_preprocessed_to_xml_document_or_fragment_with_eid_prefix(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
) -> Result<String, XmlError> {
    parse_preprocessed_to_xml_document_or_fragment_with_eid_prefix_and_source(
        text,
        root,
        frbr_uri,
        eid_prefix,
        &MetadataSource::default(),
    )
}

pub fn parse_preprocessed_to_xml_document_or_fragment_with_eid_prefix_and_source(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
    source: &MetadataSource,
) -> Result<String, XmlError> {
    if root.is_document() {
        parse_preprocessed_to_akn_xml_with_eid_prefix_and_source(
            text, root, frbr_uri, eid_prefix, source,
        )
    } else {
        parse_preprocessed_to_xml_fragment_with_eid_prefix_and_source(
            text, root, frbr_uri, eid_prefix, source,
        )
    }
}

fn parse_preprocessed_to_xml_fragment_with_eid_prefix_and_source(
    text: &str,
    root: DocumentRoot,
    frbr_uri: &str,
    eid_prefix: &str,
    source: &MetadataSource,
) -> Result<String, XmlError> {
    let frbr_uri = FrbrUri::parse(frbr_uri)?;
    let pairs = parse_pairs_preprocessed(text, root)?;
    let mut root_el = fragment_to_xml(pairs);
    resolve_displaced_content(&mut root_el);
    normalise_empty_elements(&mut root_el);
    add_attachment_doc_meta(&mut root_el, &frbr_uri, source);
    rewrite_all_eids(&mut root_el, eid_prefix);
    root_el
        .attrs
        .insert("xmlns".to_string(), AKN_NS.to_string());
    Ok(root_el.to_xml_string())
}

fn add_attachment_doc_meta(element: &mut XmlElement, frbr_uri: &FrbrUri, source: &MetadataSource) {
    if element.name == "attachment" {
        if let Some((doc_name, title)) = attachment_doc_name_and_title(element) {
            let component = format!("{doc_name}_1");
            insert_attachment_meta(element, frbr_uri, &component, &title, source);
            for child in &mut element.children {
                if let XmlNode::Element(el) = child {
                    add_attachment_doc_meta_scoped(el, frbr_uri, &component, source);
                }
            }
            return;
        }
    }
    add_attachment_doc_meta_scoped(element, frbr_uri, "", source);
}

fn add_attachment_doc_meta_scoped(
    element: &mut XmlElement,
    frbr_uri: &FrbrUri,
    parent: &str,
    source: &MetadataSource,
) {
    if element.name == "attachments" {
        let mut counts: HashMap<String, usize> = HashMap::new();
        for child in &mut element.children {
            let XmlNode::Element(attachment) = child else {
                continue;
            };
            if attachment.name != "attachment" {
                continue;
            }
            let Some((doc_name, title)) = attachment_doc_name_and_title(attachment) else {
                continue;
            };
            let count = counts.entry(doc_name.clone()).or_insert(0);
            *count += 1;
            let local = format!("{doc_name}_{count}");
            let component = if parent.is_empty() {
                local
            } else {
                format!("{parent}/{local}")
            };
            insert_attachment_meta(attachment, frbr_uri, &component, &title, source);
            add_attachment_doc_meta_scoped(attachment, frbr_uri, &component, source);
        }
        return;
    }
    for child in &mut element.children {
        if let XmlNode::Element(el) = child {
            add_attachment_doc_meta_scoped(el, frbr_uri, parent, source);
        }
    }
}

fn attachment_doc_name_and_title(attachment: &XmlElement) -> Option<(String, String)> {
    let doc_name = attachment.children.iter().find_map(|child| match child {
        XmlNode::Element(doc) if doc.name == "doc" => Some(
            doc.attrs
                .get("name")
                .cloned()
                .unwrap_or_else(|| "attachment".to_string()),
        ),
        _ => None,
    })?;
    let title = attachment
        .children
        .iter()
        .find_map(|child| match child {
            XmlNode::Element(el) if el.name == "heading" => Some(el.text_content()),
            _ => None,
        })
        .unwrap_or_else(|| "Untitled".to_string());
    Some((doc_name, title))
}

fn insert_attachment_meta(
    attachment: &mut XmlElement,
    frbr_uri: &FrbrUri,
    component: &str,
    title: &str,
    source: &MetadataSource,
) {
    for child in &mut attachment.children {
        if let XmlNode::Element(doc) = child {
            if doc.name == "doc"
                && !doc
                    .children
                    .iter()
                    .any(|child| matches!(child, XmlNode::Element(el) if el.name == "meta"))
            {
                doc.children.insert(
                    0,
                    XmlNode::Element(make_attachment_meta(frbr_uri, component, title, source)),
                );
            }
        }
    }
}

pub fn parse_preprocessed_to_xml(text: &str, root: DocumentRoot) -> Result<String, XmlError> {
    parse_preprocessed_to_xml_with_eid_prefix(text, root, "")
}

pub fn parse_preprocessed_to_xml_with_eid_prefix(
    text: &str,
    root: DocumentRoot,
    eid_prefix: &str,
) -> Result<String, XmlError> {
    let pairs = parse_pairs_preprocessed(text, root)?;
    let mut root_el = if root.is_document() {
        document_to_xml(root, pairs)
    } else {
        fragment_to_xml(pairs)
    };
    resolve_displaced_content(&mut root_el);
    normalise_empty_elements(&mut root_el);
    rewrite_all_eids(&mut root_el, eid_prefix);
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
        _ => unreachable!("build_document only supports document roots"),
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
        _ => unreachable!("document_to_xml only supports document roots"),
    }
    root_el
}

fn fragment_to_xml(pairs: pest::iterators::Pairs<'_, Rule>) -> XmlElement {
    pairs
        .into_iter()
        .find_map(fragment_pair_to_xml)
        .expect("fragment parser returned no XML-producing pair")
}

fn fragment_pair_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> Option<XmlElement> {
    match pair.as_rule() {
        Rule::preface => Some(container_to_xml("preface", pair, false)),
        Rule::preamble => Some(container_to_xml("preamble", pair, false)),
        Rule::body => Some(body_container_to_xml("body", pair)),
        Rule::mainBody => Some(body_container_to_xml("mainBody", pair)),
        Rule::debateBody => Some(body_container_to_xml("debateBody", pair)),
        Rule::conclusions => Some(container_to_xml("conclusions", pair, false)),
        Rule::introduction => Some(container_to_xml("introduction", pair, true)),
        Rule::background => Some(container_to_xml("background", pair, true)),
        Rule::arguments if !pair.as_str().trim().is_empty() => {
            Some(container_to_xml("arguments", pair, true))
        }
        Rule::remedies => Some(container_to_xml("remedies", pair, true)),
        Rule::motivation => Some(container_to_xml("motivation", pair, true)),
        Rule::decision => Some(container_to_xml("decision", pair, true)),
        Rule::hier_element_block => Some(hier_to_xml(pair)),
        Rule::p | Rule::line => Some(p_to_xml(pair)),
        Rule::longtitle => Some(line_element_to_xml(pair, "longTitle")),
        Rule::crossheading => Some(line_element_to_xml(pair, "crossHeading")),
        Rule::blocks => Some(blocks_to_xml(pair)),
        Rule::block_quote => Some(block_quote_to_xml(pair)),
        Rule::block_list => Some(block_list_to_xml(pair)),
        Rule::block_list_item => Some(block_list_item_to_xml(pair)),
        Rule::bullet_list => Some(bullet_list_to_xml(pair)),
        Rule::bullet_list_item => Some(bullet_list_item_to_xml(pair)),
        Rule::table => Some(table_to_xml(pair)),
        Rule::table_row => Some(table_row_to_xml(pair)),
        Rule::table_cell => Some(table_cell_to_xml(pair)),
        Rule::attachment => Some(attachment_to_xml(pair)),
        Rule::attachments => Some(attachments_to_xml(pair)),
        Rule::speech_block => Some(speech_block_to_xml(pair)),
        Rule::speech_container => Some(speech_container_to_xml(pair)),
        Rule::speech_group => Some(speech_group_to_xml(pair)),
        _ => pair.into_inner().find_map(fragment_pair_to_xml),
    }
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
        _ => unreachable!("root_name only supports document roots"),
    }
}

fn make_meta(frbr_uri: &FrbrUri, source: &MetadataSource) -> XmlElement {
    identification_meta(frbr_uri, "Untitled", source).child(
        XmlElement::new("references")
            .attr("source", source.source_ref())
            .child(
                XmlElement::new("TLCOrganization")
                    .attr("eId", source.eid.clone())
                    .attr("href", source.href.clone())
                    .attr("showAs", source.show_as.clone()),
            ),
    )
}

fn make_attachment_meta(
    frbr_uri: &FrbrUri,
    component: &str,
    title: &str,
    source: &MetadataSource,
) -> XmlElement {
    let mut frbr_uri = frbr_uri.clone();
    frbr_uri.work_component = Some(component.to_string());
    identification_meta(&frbr_uri, title, source)
}

fn identification_meta(frbr_uri: &FrbrUri, title: &str, source: &MetadataSource) -> XmlElement {
    let today = today_iso_date();
    XmlElement::new("meta").child(
        XmlElement::new("identification")
            .attr("source", source.source_ref())
            .child(
                XmlElement::new("FRBRWork")
                    .child(XmlElement::new("FRBRthis").attr("value", frbr_uri.work_uri(true)))
                    .child(XmlElement::new("FRBRuri").attr("value", frbr_uri.work_uri(false)))
                    .child(
                        XmlElement::new("FRBRalias")
                            .attr("value", title)
                            .attr("name", "title"),
                    )
                    .child(
                        XmlElement::new("FRBRdate")
                            .attr("date", frbr_uri.date.clone())
                            .attr("name", "Generation"),
                    )
                    .child(XmlElement::new("FRBRauthor").attr("href", ""))
                    .child(XmlElement::new("FRBRcountry").attr("value", frbr_uri.place()))
                    .child(XmlElement::new("FRBRnumber").attr("value", frbr_uri.number.clone())),
            )
            .child(
                XmlElement::new("FRBRExpression")
                    .child(XmlElement::new("FRBRthis").attr("value", frbr_uri.expression_uri(true)))
                    .child(XmlElement::new("FRBRuri").attr("value", frbr_uri.expression_uri(false)))
                    .child(
                        XmlElement::new("FRBRdate")
                            .attr("date", today.clone())
                            .attr("name", "Generation"),
                    )
                    .child(XmlElement::new("FRBRauthor").attr("href", ""))
                    .child(
                        XmlElement::new("FRBRlanguage").attr("language", frbr_uri.language.clone()),
                    ),
            )
            .child(
                XmlElement::new("FRBRManifestation")
                    .child(
                        XmlElement::new("FRBRthis").attr("value", frbr_uri.manifestation_uri(true)),
                    )
                    .child(
                        XmlElement::new("FRBRuri").attr("value", frbr_uri.manifestation_uri(false)),
                    )
                    .child(
                        XmlElement::new("FRBRdate")
                            .attr("date", today)
                            .attr("name", "Generation"),
                    )
                    .child(XmlElement::new("FRBRauthor").attr("href", "")),
            ),
    )
}

// `std::time::SystemTime::now()` has no working backend on
// `wasm32-unknown-unknown` (it compiles but panics at runtime with "time not
// implemented on this platform"). When targeting wasm32, use the JS `Date`
// API instead via `js-sys`, which is only pulled in as a dependency for that
// target (see `[target.'cfg(target_arch = "wasm32")'.dependencies]` in
// Cargo.toml) so native builds are unaffected.
#[cfg(not(target_arch = "wasm32"))]
fn today_iso_date() -> String {
    let days = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|duration| (duration.as_secs() / 86_400) as i64)
        .unwrap_or(0);
    let (year, month, day) = civil_from_days(days);
    format!("{year:04}-{month:02}-{day:02}")
}

#[cfg(target_arch = "wasm32")]
fn today_iso_date() -> String {
    let millis = js_sys::Date::now();
    let days = (millis / 86_400_000.0).floor() as i64;
    let (year, month, day) = civil_from_days(days);
    format!("{year:04}-{month:02}-{day:02}")
}

fn civil_from_days(days_since_unix_epoch: i64) -> (i64, i64, i64) {
    let z = days_since_unix_epoch + 719_468;
    let era = if z >= 0 { z } else { z - 146_096 } / 146_097;
    let doe = z - era * 146_097;
    let yoe = (doe - doe / 1_460 + doe / 36_524 - doe / 146_096) / 365;
    let y = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let day = doy - (153 * mp + 2) / 5 + 1;
    let month = mp + if mp < 10 { 3 } else { -9 };
    let year = y + if month <= 2 { 1 } else { 0 };
    (year, month, day)
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
        Rule::arguments if !pair.as_str().trim().is_empty() => {
            parts.push(container_to_xml("arguments", pair, true))
        }
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
    let mut attrs = BTreeMap::new();
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            _ => collect_container_blocks(child, &mut blocks, allow_hier),
        }
    }
    if allow_hier && blocks.is_empty() {
        blocks.push(XmlElement::new("p"));
    }
    let mut el = XmlElement::new(name).children(wrap_top_level_crossheadings(blocks));
    el.attrs = attrs;
    el
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
        "debateBody" => XmlElement::new(name).children(if blocks.is_empty() {
            vec![XmlElement::new("debateSection")
                .attr("name", "debateSection")
                .child(XmlElement::new("p"))]
        } else {
            blocks
        }),
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
        | Rule::blocks
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
        Rule::blocks => blocks.push(blocks_to_xml(pair)),
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
    let mut heading: Option<Vec<XmlNode>> = None;
    let mut subheading: Option<XmlElement> = None;
    let mut blocks = Vec::new();
    let mut nested = None;

    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::attachment_marker => marker_name = child.as_str().to_ascii_lowercase(),
            Rule::block_attrs => att_attrs.extend(block_attrs_to_map(child)),
            Rule::attachment_heading => {
                let nodes = line_inline_nodes(child);
                if !nodes.is_empty() {
                    heading = Some(nodes);
                }
            }
            Rule::subheading => subheading = Some(line_element_to_xml(child, "subheading")),
            Rule::attachments => nested = Some(attachments_to_xml(child)),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }

    let mut attachment = XmlElement::new("attachment");
    attachment.attrs = att_attrs;
    if let Some(heading) = heading {
        attachment.children.push(XmlNode::Element(
            XmlElement::new("heading").children_nodes(heading),
        ));
    }
    if let Some(subheading) = subheading.filter(|subheading| !subheading.children.is_empty()) {
        attachment.children.push(XmlNode::Element(subheading));
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
    let mut num = None;
    let mut heading = None;
    let mut subheading = None;
    let mut from = None;
    let mut by = None;
    let mut blocks = Vec::new();

    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::speech_container_name | Rule::speech_group_name => {
                name = speech_name(child.as_str())
            }
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            Rule::hier_element_heading => {
                let (n, h) = parse_heading(child);
                num = n;
                heading = h;
            }
            Rule::subheading => subheading = Some(line_element_to_xml(child, "subheading")),
            Rule::speech_from => {
                by = Some(
                    child
                        .as_str()
                        .chars()
                        .filter(|c| c.is_alphanumeric())
                        .collect::<String>(),
                );
                from = Some(collect_inline_text(child).trim().to_string());
            }
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
        if let Some(by) = &by {
            attrs.insert("by".to_string(), format!("#{by}"));
        }
    }

    let mut el = XmlElement::new(name);
    el.attrs = attrs;
    if let Some(num) = num.filter(|num| !num.is_empty()) {
        el.children
            .push(XmlNode::Element(XmlElement::new("num").text(num)));
    }
    if let Some(heading) = heading.filter(|heading| !heading.is_empty()) {
        el.children.push(XmlNode::Element(
            XmlElement::new("heading").children_nodes(heading),
        ));
    }
    if let Some(subheading) = subheading.filter(|subheading| !subheading.children.is_empty()) {
        el.children.push(XmlNode::Element(subheading));
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

fn blocks_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut attrs = BTreeMap::new();
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            Rule::block_element => collect_blocks(child, &mut blocks),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    if blocks.is_empty() {
        blocks.push(XmlElement::new("p"));
    }
    let mut el = XmlElement::new("blockContainer").children(blocks);
    el.attrs = attrs;
    el
}

fn footnote_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut marker = String::new();
    let mut attrs = BTreeMap::new();
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::marker => marker = child.as_str().trim().to_string(),
            Rule::block_attrs => attrs.extend(block_attrs_to_map(child)),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    attrs.insert("marker".to_string(), marker);
    attrs.insert("name".to_string(), "footnote".to_string());
    let mut displaced = XmlElement::new("displaced");
    displaced.attrs = attrs;
    displaced.children = blocks.into_iter().map(XmlNode::Element).collect();
    displaced
}

fn block_list_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut list = XmlElement::new("blockList");
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => list.attrs.extend(block_attrs_to_map(child)),
            Rule::block_list_intro => list.children.extend(
                line_like_to_named_elements(child, "listIntroduction")
                    .into_iter()
                    .map(XmlNode::Element),
            ),
            Rule::block_list_wrapup => list.children.extend(
                line_like_to_named_elements(child, "listWrapUp")
                    .into_iter()
                    .map(XmlNode::Element),
            ),
            Rule::block_list_item => list
                .children
                .push(XmlNode::Element(block_list_item_to_xml(child))),
            _ => {}
        }
    }
    list
}

fn line_like_to_named_elements(
    pair: pest::iterators::Pair<'_, Rule>,
    name: &str,
) -> Vec<XmlElement> {
    let mut el = XmlElement::new(name);
    let mut siblings = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::line | Rule::p => el.children.extend(p_to_xml(child).children),
            Rule::footnote => siblings.push(footnote_to_xml(child)),
            _ => {}
        }
    }
    let mut elements = vec![el];
    elements.extend(siblings);
    elements
}

fn block_list_item_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let mut item = XmlElement::new("item");
    let mut blocks = Vec::new();
    let mut subheading = None;
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::block_attrs => item.attrs.extend(block_attrs_to_map(child)),
            Rule::hier_element_heading => {
                let (num, heading) = parse_heading(child);
                if let Some(num) = num.filter(|num| !num.is_empty()) {
                    item.children
                        .push(XmlNode::Element(XmlElement::new("num").text(num)));
                }
                if let Some(heading) = heading.filter(|heading| !heading.is_empty()) {
                    item.children.push(XmlNode::Element(
                        XmlElement::new("heading").children_nodes(heading),
                    ));
                }
            }
            Rule::subheading => subheading = Some(line_element_to_xml(child, "subheading")),
            Rule::block_element => collect_blocks(child, &mut blocks),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    if let Some(subheading) = subheading.filter(|subheading| !subheading.children.is_empty()) {
        item.children.push(XmlNode::Element(subheading));
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
    let starts_with_empty_paragraph = starts_with_empty_bullet_paragraph(pair.as_str());
    let mut attrs = BTreeMap::new();
    let mut blocks = Vec::new();
    for child in pair.into_inner() {
        match child.as_rule() {
            Rule::bullet_list_marker => {
                for marker_child in child.into_inner() {
                    if marker_child.as_rule() == Rule::block_attrs {
                        attrs.extend(block_attrs_to_map(marker_child));
                    }
                }
            }
            Rule::block_elements | Rule::block_element => collect_blocks(child, &mut blocks),
            _ => collect_block_descendants(child, &mut blocks),
        }
    }
    if blocks.is_empty() {
        blocks.push(XmlElement::new("p"));
    } else if starts_with_empty_paragraph {
        blocks.insert(0, XmlElement::new("p"));
    }
    let mut li = XmlElement::new("li").children(blocks);
    li.attrs = attrs;
    li
}

fn starts_with_empty_bullet_paragraph(text: &str) -> bool {
    let trimmed = text.trim_start();
    trimmed == "*" || trimmed.starts_with("*\n") || trimmed.starts_with("*\r\n")
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
        match child.as_rule() {
            Rule::block_attrs => row.attrs.extend(block_attrs_to_map(child)),
            Rule::table_cell => row
                .children
                .push(XmlNode::Element(table_cell_to_xml(child))),
            _ => {}
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
        | Rule::blocks
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
    let mut heading: Option<Vec<XmlNode>> = None;
    let mut subheading: Option<XmlElement> = None;
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
            Rule::subheading => subheading = Some(line_element_to_xml(child, "subheading")),
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
    if let Some(heading) = heading.filter(|heading| !heading.is_empty()) {
        el.children.push(XmlNode::Element(
            XmlElement::new("heading").children_nodes(heading),
        ));
    }
    if let Some(subheading) = subheading.filter(|subheading| !subheading.children.is_empty()) {
        el.children.push(XmlNode::Element(subheading));
    }
    if content
        .iter()
        .any(|c| is_hier_name(&c.name) || c.name == "crossHeading")
    {
        el.children.extend(mixed_hier_children(content));
    } else if !content.is_empty() {
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
        Rule::speech_container
        | Rule::speech_group
        | Rule::speech_block
        | Rule::block_list
        | Rule::bullet_list
        | Rule::table
        | Rule::blocks
        | Rule::longtitle
        | Rule::crossheading
        | Rule::footnote
        | Rule::block_quote => collect_blocks(pair, content),
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
        Rule::remark => nodes.push(XmlNode::Element(remark_to_xml(pair))),
        Rule::image => nodes.push(XmlNode::Element(image_to_xml(pair.as_str()))),
        Rule::ref_ => nodes.push(XmlNode::Element(ref_to_xml(pair))),
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

fn remark_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let span = pair.as_span();
    let inner_start = span.start() + "{{*".len();
    let inner_end = span.end().saturating_sub("}}".len());
    let mut cursor = inner_start;
    let mut nodes = Vec::new();

    for child in pair.into_inner() {
        let child_span = child.as_span();
        if child_span.end() <= inner_start || child_span.start() >= inner_end {
            continue;
        }
        push_remark_gap_breaks(&mut nodes, child_span.start().saturating_sub(cursor));
        collect_inline_nodes_inner(child, &mut nodes);
        cursor = child_span.end();
    }
    push_remark_gap_breaks(&mut nodes, inner_end.saturating_sub(cursor));

    XmlElement::new("remark")
        .attr("status", "editorial")
        .children_nodes(merge_adjacent_text(nodes))
}

fn push_remark_gap_breaks(nodes: &mut Vec<XmlNode>, bytes: usize) {
    for _ in 0..bytes {
        nodes.push(XmlNode::Element(XmlElement::new("br")));
    }
}

fn ref_to_xml(pair: pest::iterators::Pair<'_, Rule>) -> XmlElement {
    let body = pair
        .as_str()
        .strip_prefix("{{>")
        .and_then(|s| s.strip_suffix("}}"))
        .unwrap_or("");
    let href = ref_href(body);
    let mut ref_el = XmlElement::new("ref").attr("href", href);
    ref_el.children = collect_inline_nodes_from_children(pair);
    ref_el
}

fn ref_href(body: &str) -> &str {
    if body.starts_with(' ') {
        return "";
    }
    body.split_once([' ', '\n'])
        .map(|(href, _)| href)
        .unwrap_or(body)
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
    match text.strip_prefix('\\') {
        Some(stripped) if !stripped.is_empty() => stripped.to_string(),
        _ => text.to_string(),
    }
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
                // Bluebell attributes are namespace-free. Accept the XML 1.0
                // (Fifth Edition) NCName production, so malformed pairs are
                // discarded without preventing the rest of the block parsing.
                if is_xml_ncname(&name) {
                    attrs.insert(name, value);
                }
            }
        }
        _ => {
            for child in pair.into_inner() {
                collect_block_attrs(child, attrs, classes);
            }
        }
    }
}

/// XML 1.0 (Fifth Edition) `NCName`: `Name` with `:` excluded because
/// Bluebell has no syntax for binding attribute namespaces.
fn is_xml_ncname(name: &str) -> bool {
    let mut chars = name.chars();
    matches!(chars.next(), Some(first) if is_xml_name_start_char(first))
        && chars.all(is_xml_name_char)
}

fn is_xml_name_start_char(character: char) -> bool {
    let codepoint = character as u32;
    character == '_'
        || character.is_ascii_alphabetic()
        || (0xC0..=0xD6).contains(&codepoint)
        || (0xD8..=0xF6).contains(&codepoint)
        || (0xF8..=0x2FF).contains(&codepoint)
        || (0x370..=0x37D).contains(&codepoint)
        || (0x37F..=0x1FFF).contains(&codepoint)
        || (0x200C..=0x200D).contains(&codepoint)
        || (0x2070..=0x218F).contains(&codepoint)
        || (0x2C00..=0x2FEF).contains(&codepoint)
        || (0x3001..=0xD7FF).contains(&codepoint)
        || (0xF900..=0xFDCF).contains(&codepoint)
        || (0xFDF0..=0xFFFD).contains(&codepoint)
        || (0x10000..=0xEFFFF).contains(&codepoint)
}

fn is_xml_name_char(character: char) -> bool {
    let codepoint = character as u32;
    is_xml_name_start_char(character)
        || matches!(character, '-' | '.')
        || character.is_ascii_digit()
        || codepoint == 0xB7
        || (0x0300..=0x036F).contains(&codepoint)
        || (0x203F..=0x2040).contains(&codepoint)
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
            out.push_str(&unescaped(pair.as_str()));
        }
        _ => {
            for child in pair.into_inner() {
                collect_inline_text_inner(child, out);
            }
        }
    }
}

fn parse_heading(pair: pest::iterators::Pair<'_, Rule>) -> (Option<String>, Option<Vec<XmlNode>>) {
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
                let nodes = line_inline_nodes(child);
                if !nodes.is_empty() {
                    heading = Some(nodes);
                }
            }
            _ => {}
        }
    }
    (num, heading)
}

fn line_inline_nodes(pair: pest::iterators::Pair<'_, Rule>) -> Vec<XmlNode> {
    trim_edge_whitespace_text_nodes(collect_inline_nodes_from_children(pair))
}

fn trim_edge_whitespace_text_nodes(mut nodes: Vec<XmlNode>) -> Vec<XmlNode> {
    while matches!(nodes.first(), Some(XmlNode::Text(text)) if text.trim().is_empty()) {
        nodes.remove(0);
    }
    while matches!(nodes.last(), Some(XmlNode::Text(text)) if text.trim().is_empty()) {
        nodes.pop();
    }
    nodes
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

/// Transient attribute used to give authorialNote elements a stable identity
/// while displaced content is moved around, mirroring lxml element identity in
/// the Python implementation. Never serialized: stripped before returning.
const NOTE_RID_ATTR: &str = "\u{1}rid";

/// Resolve displaced content (ie. footnotes), mirroring Python's
/// XmlGenerator.resolve_displaced_content: process refs in document order,
/// find the matching displaced element by walking ancestors nearest-first and
/// scanning each ancestor's subtree in document order, and move (not copy) the
/// displaced children into the ref. Unused displaced content is converted to
/// a "FOOTNOTE <marker>" paragraph followed by its children, in place.
fn resolve_displaced_content(root: &mut XmlElement) {
    let mut note_count = 0usize;
    tag_note_rids(root, &mut note_count);

    for rid in 0..note_count {
        let rid = rid.to_string();
        let Some(note_path) = find_element_path(root, &mut Vec::new(), &|el, _| {
            el.attrs.get(NOTE_RID_ATTR) == Some(&rid)
        }) else {
            continue;
        };
        let marker = element_at_path(root, &note_path)
            .and_then(|el| el.attrs.get("marker").cloned())
            .unwrap_or_default();

        let mut found = None;
        for depth in (0..note_path.len()).rev() {
            let ancestor_path = &note_path[..depth];
            let Some(ancestor) = element_at_path(root, ancestor_path) else {
                continue;
            };
            if let Some(displaced_path) = find_element_path(
                ancestor,
                &mut ancestor_path.to_vec(),
                &|el: &XmlElement, path: &[usize]| {
                    el.name == "displaced"
                        && el.attrs.get("name").map(String::as_str) == Some("footnote")
                        && el.attrs.get("marker") == Some(&marker)
                        // never match displaced content that contains the note
                        // itself; Python raises on this pathological case
                        && !note_path.starts_with(path)
                },
            ) {
                found = Some(displaced_path);
                break;
            }
        }

        let (children, displaced_attrs) = match &found {
            Some(displaced_path) => element_mut_at_path(root, displaced_path)
                .map(|el| {
                    (
                        std::mem::take(&mut el.children),
                        std::mem::take(&mut el.attrs),
                    )
                })
                .unwrap_or_default(),
            None => (
                vec![XmlNode::Element(
                    XmlElement::new("p").text("(content missing)"),
                )],
                BTreeMap::new(),
            ),
        };
        if let Some(note) = element_mut_at_path(root, &note_path) {
            for (name, value) in displaced_attrs {
                if name != "marker" && name != "name" {
                    note.attrs.insert(name, value);
                }
            }
            note.children.extend(children);
        }
        if let Some(displaced_path) = found {
            remove_element_at_path(root, &displaced_path);
        }
    }

    convert_leftover_displaced(root);
    strip_note_rids(root);
}

fn tag_note_rids(element: &mut XmlElement, next: &mut usize) {
    if element.name == "authorialNote" {
        element
            .attrs
            .insert(NOTE_RID_ATTR.to_string(), next.to_string());
        *next += 1;
    }
    for child in &mut element.children {
        if let XmlNode::Element(el) = child {
            tag_note_rids(el, next);
        }
    }
}

fn strip_note_rids(element: &mut XmlElement) {
    element.attrs.remove(NOTE_RID_ATTR);
    for child in &mut element.children {
        if let XmlNode::Element(el) = child {
            strip_note_rids(el);
        }
    }
}

/// Find the first element (in document order, including `element` itself) that
/// matches `pred`. `path` holds the path to `element` and the predicate is
/// given each candidate's full path.
fn find_element_path(
    element: &XmlElement,
    path: &mut Vec<usize>,
    pred: &impl Fn(&XmlElement, &[usize]) -> bool,
) -> Option<Vec<usize>> {
    if pred(element, path) {
        return Some(path.clone());
    }
    for (idx, child) in element.children.iter().enumerate() {
        if let XmlNode::Element(el) = child {
            path.push(idx);
            if let Some(found) = find_element_path(el, path, pred) {
                return Some(found);
            }
            path.pop();
        }
    }
    None
}

fn remove_element_at_path(root: &mut XmlElement, path: &[usize]) {
    let Some((&idx, parent_path)) = path.split_last() else {
        return;
    };
    if let Some(parent) = element_mut_at_path(root, parent_path) {
        if idx < parent.children.len() {
            parent.children.remove(idx);
        }
    }
}

/// Don't lose unused displaced content: change it to a "FOOTNOTE <marker>" p
/// tag and pull its children in as siblings, like Python.
fn convert_leftover_displaced(root: &mut XmlElement) {
    while let Some(path) =
        find_element_path(root, &mut Vec::new(), &|el: &XmlElement, _: &[usize]| {
            el.name == "displaced"
        })
    {
        let Some((&idx, parent_path)) = path.split_last() else {
            return;
        };
        let Some(parent) = element_mut_at_path(root, parent_path) else {
            return;
        };
        let XmlNode::Element(displaced) = parent.children.remove(idx) else {
            return;
        };
        let name = displaced
            .attrs
            .get("name")
            .cloned()
            .unwrap_or_default()
            .to_uppercase();
        let marker = displaced.attrs.get("marker").cloned().unwrap_or_default();
        let mut replacement = vec![XmlNode::Element(
            XmlElement::new("p").text(format!("{name} {marker}")),
        )];
        replacement.extend(displaced.children);
        parent.children.splice(idx..idx, replacement);
    }
}

fn element_mut_at_path<'a>(
    mut element: &'a mut XmlElement,
    path: &[usize],
) -> Option<&'a mut XmlElement> {
    for idx in path {
        match element.children.get_mut(*idx) {
            Some(XmlNode::Element(child)) => element = child,
            _ => return None,
        }
    }
    Some(element)
}

fn element_at_path<'a>(mut element: &'a XmlElement, path: &[usize]) -> Option<&'a XmlElement> {
    for idx in path {
        match element.children.get(*idx) {
            Some(XmlNode::Element(child)) => element = child,
            _ => return None,
        }
    }
    Some(element)
}

fn normalise_empty_elements(element: &mut XmlElement) {
    for child in &mut element.children {
        if let XmlNode::Element(el) = child {
            normalise_empty_elements(el);
        }
    }
    element.children.retain(|child| {
        !matches!(
            child,
            XmlNode::Element(el)
                if matches!(
                    el.name.as_str(),
                    "crossHeading" | "longTitle" | "content" | "preface" | "preamble" | "conclusions"
                ) && el.children.is_empty()
        )
    });
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
            // a literal \r would be normalized to \n by XML parsers
            '\r' => out.push_str("&#13;"),
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
            // literal whitespace would be normalized to spaces by XML parsers
            '\t' => out.push_str("&#9;"),
            '\n' => out.push_str("&#10;"),
            '\r' => out.push_str("&#13;"),
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
    fn eid_prefix_is_applied_to_generated_eids() {
        let xml = parse_to_xml_with_eid_prefix(
            "P Intro\n\nSEC 1. - Heading\n  Some text.",
            DocumentRoot::Statement,
            "pref",
        )
        .unwrap();
        assert!(xml.contains("<p eId=\"pref__p_1\">Intro</p>"));
        assert!(xml.contains("<section eId=\"pref__sec_1\">"));
        assert!(xml.contains("<p eId=\"pref__sec_1__p_1\">Some text.</p>"));
    }

    #[test]
    fn akn_xml_eid_prefix_is_applied_after_meta_is_inserted() {
        let xml = parse_to_akn_xml_with_eid_prefix(
            "P Hello",
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
            "pref",
        )
        .unwrap();
        assert!(xml.contains("<FRBRuri value=\"/akn/za/statement/2022/1\"/>"));
        assert!(xml.contains("<p eId=\"pref__p_1\">Hello</p>"));
        assert!(!xml.contains("<FRBRuri eId="));
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
    fn invalid_attribute_names_are_dropped_individually() {
        let xml = parse_to_xml(
            "QUOTE{\" foo|@ bar|1baz qux|foo:bar namespace|boom bang|éclair oui|名 value|á accent|quote \"}\n  line one",
            DocumentRoot::Statement,
        )
        .unwrap();

        for attribute in [
            "boom=\"bang\"",
            "éclair=\"oui\"",
            "名=\"value\"",
            "á=\"accent\"",
            "quote=\"&quot;\"",
        ] {
            assert!(xml.contains(attribute), "missing {attribute} in {xml}");
        }
        for invalid_name in ["foo:bar", "1baz=", "@="] {
            assert!(!xml.contains(invalid_name), "found {invalid_name} in {xml}");
        }
    }

    #[test]
    fn xml_ncname_validation_uses_xml_1_0_unicode_ranges() {
        for name in ["name", "_name", "éclair", "名", "á", "𐀀name"] {
            assert!(is_xml_ncname(name), "expected {name:?} to be valid");
        }
        for name in ["", "1name", "foo:bar", "\"", "@"] {
            assert!(!is_xml_ncname(name), "expected {name:?} to be invalid");
        }
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
    fn proviso_xml() {
        let xml = parse_to_xml(
            "PROVISO 1 - Savings\n\n  This rule applies.",
            DocumentRoot::HierElementBlock,
        )
        .unwrap();

        assert!(
            xml.starts_with(
                "<proviso eId=\"proviso_1\" xmlns=\"http://docs.oasis-open.org/legaldocml/ns/akn/3.0\">"
            ),
            "{xml}"
        );
        assert!(xml.contains("<num>1</num><heading>Savings</heading>"));
        assert!(xml.contains("<content><p eId=\"proviso_1__p_1\">This rule applies.</p></content>"));
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
        assert!(xml.contains("<speech by=\"#FROMSpeakerName\" eId=\"dbsect_1__speech_1\">"));
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

    #[test]
    fn default_akn_metadata_source_is_cobalt() {
        let xml = parse_to_akn_xml(
            "P Hello",
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
        )
        .unwrap();

        assert!(xml.contains(r##"<identification source="#cobalt">"##));
        assert!(xml.contains(r##"<references source="#cobalt">"##));
        assert!(xml.contains(
            r#"<TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>"#
        ));
    }

    #[test]
    fn custom_akn_metadata_source_is_used_for_root_meta() {
        let source =
            MetadataSource::new("Indigo Platform", "Indigo-Platform", "https://example.org");
        let xml = parse_to_akn_xml_with_eid_prefix_and_source(
            "P Hello",
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
            "",
            &source,
        )
        .unwrap();

        assert!(xml.contains(r##"<identification source="#Indigo-Platform">"##));
        assert!(xml.contains(r##"<references source="#Indigo-Platform">"##));
        assert!(xml.contains(
            r#"<TLCOrganization eId="Indigo-Platform" href="https://example.org" showAs="Indigo Platform"/>"#
        ));
    }

    #[test]
    fn custom_akn_metadata_source_is_used_for_attachment_meta() {
        let source =
            MetadataSource::new("Indigo Platform", "Indigo-Platform", "https://example.org");
        let xml = parse_to_xml_document_or_fragment_with_eid_prefix_and_source(
            "SCHEDULE Schedule\n  text",
            DocumentRoot::Attachment,
            "/akn/za/act/2022/1",
            "",
            &source,
        )
        .unwrap();

        assert!(xml.starts_with("<attachment"));
        assert!(xml.contains(r##"<identification source="#Indigo-Platform">"##));
        assert!(xml.contains(r#"<FRBRthis value="/akn/za/act/2022/1/!schedule_1"/>"#));
        assert!(!xml.contains(r##"<references source="#Indigo-Platform">"##));
    }
}
