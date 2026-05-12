#[derive(Debug, thiserror::Error)]
pub enum UnparseError {
    #[error(transparent)]
    Xml(#[from] roxmltree::Error),
}

pub fn unparse(xml: &str) -> Result<String, UnparseError> {
    let doc = roxmltree::Document::parse(xml)?;
    let root = document_root(doc.root_element());
    let mut out = String::new();
    write_children(root, 0, &mut out);
    Ok(out.trim_matches('\n').to_string() + "\n")
}

fn document_root<'a, 'input>(root: roxmltree::Node<'a, 'input>) -> roxmltree::Node<'a, 'input> {
    if tag(root) == "akomaNtoso" {
        root.children()
            .find(|n| n.is_element() && tag(*n) != "meta")
            .unwrap_or(root)
    } else {
        root
    }
}

fn write_children(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    for child in node.children().filter(|n| n.is_element()) {
        write_element(child, indent, out);
    }
}

fn write_element(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    match tag(node) {
        "preface" => write_marker_container("PREFACE", node, indent, out),
        "preamble" => write_marker_container("PREAMBLE", node, indent, out),
        "body" => write_optional_marker_container("BODY", node, indent, out),
        "mainBody" | "judgmentBody" | "debateBody" | "content" => write_children(node, indent, out),
        "conclusions" => write_marker_container("CONCLUSIONS", node, indent, out),
        "introduction" => write_marker_container("INTRODUCTION", node, indent, out),
        "background" => write_marker_container("BACKGROUND", node, indent, out),
        "arguments" => write_marker_container("ARGUMENTS", node, indent, out),
        "remedies" => write_marker_container("REMEDIES", node, indent, out),
        "motivation" => write_marker_container("MOTIVATION", node, indent, out),
        "decision" => write_marker_container("DECISION", node, indent, out),
        "hcontainer" => write_children(node, indent, out),
        "p" => write_line(node, indent, out),
        "longTitle" => write_line_element("LONGTITLE", node, indent, out),
        "crossHeading" => write_line_element("CROSSHEADING", node, indent, out),
        "blockList" => write_block_list(node, indent, out),
        "ul" => write_bullets(node, indent, out),
        "table" => write_table(node, indent, out),
        "block" if node.attribute("name") == Some("quote") => write_quote(node, indent, out),
        name if is_hier(name) => write_hier(node, indent, out),
        name if is_speech_container(name) => write_speech_container(node, indent, out),
        "speech" | "speechGroup" | "question" | "answer" => write_speech_group(node, indent, out),
        "scene" | "narrative" | "summary" => {
            write_line_element(&tag(node).to_ascii_uppercase(), node, indent, out)
        }
        "attachments" => write_children(node, indent, out),
        "attachment" => write_attachment(node, indent, out),
        "doc" | "header" | "meta" => write_children(node, indent, out),
        _ => write_children(node, indent, out),
    }
}

fn write_marker_container(
    marker: &str,
    node: roxmltree::Node<'_, '_>,
    indent: usize,
    out: &mut String,
) {
    write_indent(indent, out);
    out.push_str(marker);
    out.push('\n');
    write_children(node, indent + 1, out);
}

fn write_optional_marker_container(
    marker: &str,
    node: roxmltree::Node<'_, '_>,
    indent: usize,
    out: &mut String,
) {
    write_indent(indent, out);
    out.push_str(marker);
    out.push('\n');
    write_children(node, indent + 1, out);
}

fn write_line_element(
    marker: &str,
    node: roxmltree::Node<'_, '_>,
    indent: usize,
    out: &mut String,
) {
    write_indent(indent, out);
    out.push_str(marker);
    out.push_str(&attrs_text(node, false));
    let text = inline_text(node);
    if !text.is_empty() {
        out.push(' ');
        out.push_str(&text);
    }
    out.push('\n');
}

fn write_line(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    if has_bluebell_attrs(node, false) {
        out.push('P');
        out.push_str(&attrs_text(node, false));
        out.push(' ');
    }
    out.push_str(&inline_text(node));
    out.push('\n');
}

fn write_hier(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str(&tag(node).to_ascii_uppercase());
    out.push_str(&attrs_text(node, false));
    let num = child_text(node, "num");
    let heading = child_text(node, "heading");
    if !num.is_empty() {
        out.push(' ');
        out.push_str(&num);
    }
    if !heading.is_empty() {
        out.push_str(" - ");
        out.push_str(&heading);
    }
    out.push('\n');
    for child in node.children().filter(|n| n.is_element()) {
        if matches!(tag(child), "num" | "heading" | "subheading") {
            continue;
        }
        write_element(child, indent + 1, out);
    }
}

fn write_block_list(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str("ITEMS");
    out.push_str(&attrs_text(node, false));
    out.push('\n');
    for child in node.children().filter(|n| n.is_element()) {
        match tag(child) {
            "item" => {
                write_indent(indent + 1, out);
                out.push_str("ITEM");
                out.push_str(&attrs_text(child, false));
                let num = child_text(child, "num");
                let heading = child_text(child, "heading");
                if !num.is_empty() {
                    out.push(' ');
                    out.push_str(&num);
                }
                if !heading.is_empty() {
                    out.push_str(" - ");
                    out.push_str(&heading);
                }
                out.push('\n');
                for kid in child.children().filter(|n| n.is_element()) {
                    if !matches!(tag(kid), "num" | "heading" | "subheading") {
                        write_element(kid, indent + 2, out);
                    }
                }
            }
            "listIntroduction" | "listWrapUp" => write_line(child, indent + 1, out),
            _ => {}
        }
    }
}

fn write_bullets(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str("BULLETS");
    out.push_str(&attrs_text(node, false));
    out.push('\n');
    for li in node
        .children()
        .filter(|n| n.is_element() && tag(*n) == "li")
    {
        if let Some(p) = li.children().find(|n| n.is_element() && tag(*n) == "p") {
            write_indent(indent + 1, out);
            out.push_str("* ");
            out.push_str(&inline_text(p));
            out.push('\n');
        } else {
            write_children(li, indent + 1, out);
        }
    }
}

fn write_table(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str("TABLE");
    out.push_str(&attrs_text(node, false));
    out.push('\n');
    for tr in node
        .children()
        .filter(|n| n.is_element() && tag(*n) == "tr")
    {
        write_indent(indent + 1, out);
        out.push_str("TR\n");
        for cell in tr.children().filter(|n| n.is_element()) {
            write_indent(indent + 2, out);
            out.push_str(if tag(cell) == "th" { "TH" } else { "TC" });
            out.push_str(&attrs_text(cell, false));
            out.push('\n');
            write_children(cell, indent + 3, out);
        }
    }
}

fn write_quote(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str("QUOTE");
    out.push_str(&attrs_text(node, true));
    out.push('\n');
    write_children(node, indent + 1, out);
}

fn write_speech_container(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str(&tag(node).to_ascii_uppercase());
    out.push_str(&attrs_text(node, true));
    out.push('\n');
    write_children(node, indent + 1, out);
}

fn write_speech_group(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str(&tag(node).to_ascii_uppercase());
    out.push_str(&attrs_text(node, true));
    out.push('\n');
    write_children(node, indent + 1, out);
}

fn write_attachment(node: roxmltree::Node<'_, '_>, indent: usize, out: &mut String) {
    write_indent(indent, out);
    out.push_str("ATTACHMENT");
    out.push_str(&attrs_text(node, true));
    let heading = child_text(node, "heading");
    if !heading.is_empty() {
        out.push(' ');
        out.push_str(&heading);
    }
    out.push('\n');
    write_children(node, indent + 1, out);
}

fn inline_text(node: roxmltree::Node<'_, '_>) -> String {
    let mut out = String::new();
    for child in node.children() {
        if child.is_text() {
            out.push_str(&escape_text(child.text().unwrap_or("")));
        } else if child.is_element() {
            match tag(child) {
                "b" => out.push_str(&format!("**{}**", inline_text(child))),
                "i" => out.push_str(&format!("//{}//", inline_text(child))),
                "u" => out.push_str(&format!("__{}__", inline_text(child))),
                "sup" => out.push_str(&format!("{{{{^{}}}}}", inline_text(child))),
                "sub" => out.push_str(&format!("{{{{_{}}}}}", inline_text(child))),
                "ref" => out.push_str(&format!(
                    "{{{{>{} {}}}}}",
                    escape_text(child.attribute("href").unwrap_or("")),
                    inline_text(child)
                )),
                "img" => out.push_str(&format!(
                    "{{{{IMG {} {}}}}}",
                    escape_text(child.attribute("src").unwrap_or("")),
                    escape_text(child.attribute("alt").unwrap_or(""))
                )),
                "authorialNote" => out.push_str(&format!(
                    "{{{{FOOTNOTE {}}}}}",
                    child.attribute("marker").unwrap_or("")
                )),
                "term" => out.push_str(&format!("{{{{term {}}}}}", inline_text(child))),
                "ins" => out.push_str(&format!("{{{{+{}}}}}", inline_text(child))),
                "del" => out.push_str(&format!("{{{{-{}}}}}", inline_text(child))),
                _ => out.push_str(&inline_text(child)),
            }
        }
    }
    out
}

fn child_text(node: roxmltree::Node<'_, '_>, name: &str) -> String {
    node.children()
        .find(|n| n.is_element() && tag(*n) == name)
        .map(inline_text)
        .unwrap_or_default()
}

fn attrs_text(node: roxmltree::Node<'_, '_>, skip_name: bool) -> String {
    let mut classes = Vec::new();
    let mut attrs = Vec::new();
    for attr in node.attributes() {
        match attr.name() {
            "eId" | "wId" | "GUID" | "xmlns" => {}
            "name" if skip_name => {}
            "class" => classes.extend(attr.value().split_whitespace().map(str::to_string)),
            name => attrs.push((name.to_string(), attr.value().to_string())),
        }
    }

    let mut out = String::new();
    for class in classes {
        out.push('.');
        out.push_str(&class);
    }
    if !attrs.is_empty() {
        out.push('{');
        for (idx, (name, value)) in attrs.iter().enumerate() {
            if idx > 0 {
                out.push('|');
            }
            out.push_str(name);
            if !value.is_empty() {
                out.push(' ');
                out.push_str(value);
            }
        }
        out.push('}');
    }
    out
}

fn has_bluebell_attrs(node: roxmltree::Node<'_, '_>, skip_name: bool) -> bool {
    node.attributes().any(|attr| {
        !matches!(attr.name(), "eId" | "wId" | "GUID" | "xmlns")
            && !(skip_name && attr.name() == "name")
    })
}

fn tag<'a, 'input>(node: roxmltree::Node<'a, 'input>) -> &'input str {
    node.tag_name().name()
}

fn write_indent(indent: usize, out: &mut String) {
    out.push_str(&"  ".repeat(indent));
}

fn escape_text(text: &str) -> String {
    text.replace('\\', "\\\\")
        .replace('*', "\\*")
        .replace('_', "\\_")
}

fn is_hier(name: &str) -> bool {
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

fn is_speech_container(name: &str) -> bool {
    matches!(
        name,
        "address"
            | "adjournment"
            | "administrationOfOath"
            | "communication"
            | "debateSection"
            | "declarationOfVote"
            | "ministerialStatements"
            | "nationalInterest"
            | "noticesOfMotion"
            | "oralStatements"
            | "papers"
            | "personalStatements"
            | "petitions"
            | "pointOfOrder"
            | "prayers"
            | "proceduralMotions"
            | "questions"
            | "resolutions"
            | "rollCall"
            | "writtenStatements"
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::xml::parse_to_xml;
    use crate::DocumentRoot;

    #[test]
    fn unparse_basic_rust_xml() {
        let xml = parse_to_xml("P Hello **bold**", DocumentRoot::Statement).unwrap();
        assert_eq!("Hello **bold**\n", unparse(&xml).unwrap());
    }

    #[test]
    fn unparse_hierarchy() {
        let xml = parse_to_xml("SECTION 1 - Heading\n  Text", DocumentRoot::Act).unwrap();
        assert_eq!(
            "BODY\n  SECTION 1 - Heading\n    Text\n",
            unparse(&xml).unwrap()
        );
    }

    #[test]
    fn unparse_list_and_table() {
        let text = "ITEMS\n  ITEM (a)\n    first\nTABLE\n  TR\n    TC\n      cell\n";
        let xml = parse_to_xml(text, DocumentRoot::Statement).unwrap();
        let out = unparse(&xml).unwrap();
        assert!(out.contains("ITEMS\n  ITEM (a)\n    first\n"));
        assert!(out.contains("TABLE\n  TR\n    TC\n      cell\n"));
    }

    #[test]
    fn unparse_full_akn_wrapper() {
        let xml = crate::xml::parse_to_akn_xml(
            "P Hello",
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
        )
        .unwrap();
        assert_eq!("Hello\n", unparse(&xml).unwrap());
    }
}
