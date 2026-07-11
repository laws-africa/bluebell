use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use bluebell_core::{
    parse_to_xml_document_or_fragment_with_eid_prefix,
    parse_to_xml_document_or_fragment_with_eid_prefix_and_source, DocumentRoot, MetadataSource,
};

mod support;
use support::{python_path, repo_path, unparse};

struct ParityCase {
    name: String,
    root: DocumentRoot,
    python_root: &'static str,
    frbr_uri: String,
    eid_prefix: String,
    input: CaseInput,
}

enum CaseInput {
    File(PathBuf),
    XmlFixture(PathBuf),
    Text(&'static str),
}

#[test]
fn parsed_bluebell_xml_matches_python() {
    for case in parity_cases() {
        assert_case_matches_python(&case);
    }
}

#[test]
fn custom_metadata_source_matches_python_cobalt_override() {
    let case = text_case(
        "custom-metadata-source",
        DocumentRoot::Act,
        "act",
        "BODY\nSEC 1. - Heading\n  Some text.\nSCHEDULE Schedule\n  text",
    );
    let source = MetadataSource::new("Indigo Platform", "Indigo-Platform", "https://example.org");
    let text = case.input.read(&case.name);
    let rust_xml = parse_to_xml_document_or_fragment_with_eid_prefix_and_source(
        &text,
        case.root,
        &case.frbr_uri,
        &case.eid_prefix,
        &source,
    )
    .unwrap_or_else(|err| panic!("Rust failed to parse {}: {err}", case.name));
    let python_xml = python_parse_to_xml_with_source(&case, &text, &source);

    let rust_c14n = python_canonicalize(&rust_xml, &case.name, "rust");
    let python_c14n = python_canonicalize(&python_xml, &case.name, "python");

    if rust_c14n != python_c14n {
        write_failure_artifacts(&case, &rust_xml, &python_xml);
    }
    assert!(
        python_c14n == rust_c14n,
        "XML parity failed for {}; artifacts written to {}",
        case.name,
        artifact_dir(&case.name).display()
    );
}

#[test]
#[ignore = "large real-document parity check; run explicitly with --ignored"]
fn income_tax_xml_roundtrip_parse_matches_python() {
    let case = xml_fixture_case(
        "income-tax".to_string(),
        DocumentRoot::Act,
        "act",
        "/akn/za/act/1962/58".to_string(),
        PathBuf::from(repo_path(
            "crates/bluebell-core/tests/fixtures/income-tax.xml",
        )),
    );
    assert_case_matches_python(&case);
}

fn assert_case_matches_python(case: &ParityCase) {
    let text = case.input.read(&case.name);
    let rust_xml = parse_to_xml_document_or_fragment_with_eid_prefix(
        &text,
        case.root,
        &case.frbr_uri,
        &case.eid_prefix,
    )
    .unwrap_or_else(|err| panic!("Rust failed to parse {}: {err}", case.name));
    let python_xml = python_parse_to_xml(case, &text);

    let rust_c14n = python_canonicalize(&rust_xml, &case.name, "rust");
    let python_c14n = python_canonicalize(&python_xml, &case.name, "python");

    if rust_c14n != python_c14n {
        write_failure_artifacts(case, &rust_xml, &python_xml);
    }
    assert!(
        python_c14n == rust_c14n,
        "XML parity failed for {}; artifacts written to {}",
        case.name,
        artifact_dir(&case.name).display()
    );
}

fn parity_cases() -> Vec<ParityCase> {
    let mut cases = discovered_roundtrip_text_cases();
    cases.extend(discovered_roundtrip_xml_cases());

    cases.extend(focused_cases());
    cases
}

fn discovered_roundtrip_text_cases() -> Vec<ParityCase> {
    let mut paths = fs::read_dir(repo_path("tests/roundtrip"))
        .expect("failed to read roundtrip fixture directory")
        .map(|entry| {
            entry
                .expect("failed to read roundtrip fixture entry")
                .path()
        })
        .filter(|path| path.extension().is_some_and(|ext| ext == "txt"))
        .collect::<Vec<_>>();
    paths.sort();

    paths
        .into_iter()
        .map(|path| {
            let stem = path
                .file_stem()
                .and_then(|stem| stem.to_str())
                .unwrap_or_else(|| panic!("roundtrip fixture path is not valid UTF-8: {path:?}"));
            let (root, python_root) = roundtrip_fixture_root(stem);
            file_case(
                format!("roundtrip-{stem}"),
                root,
                python_root,
                default_roundtrip_frbr_uri(root),
                path,
            )
        })
        .collect()
}

fn discovered_roundtrip_xml_cases() -> Vec<ParityCase> {
    let mut paths = fs::read_dir(repo_path("tests/roundtrip"))
        .expect("failed to read roundtrip fixture directory")
        .map(|entry| {
            entry
                .expect("failed to read roundtrip fixture entry")
                .path()
        })
        .filter(|path| path.extension().is_some_and(|ext| ext == "xml"))
        .collect::<Vec<_>>();
    paths.sort();

    paths
        .into_iter()
        .map(|path| {
            let stem = path
                .file_stem()
                .and_then(|stem| stem.to_str())
                .unwrap_or_else(|| panic!("roundtrip fixture path is not valid UTF-8: {path:?}"));
            let (root, python_root) = roundtrip_xml_fixture_root(stem);
            xml_fixture_case(
                format!("roundtrip-xml-{stem}"),
                root,
                python_root,
                default_roundtrip_frbr_uri(root),
                path,
            )
        })
        .collect()
}

fn roundtrip_fixture_root(stem: &str) -> (DocumentRoot, &'static str) {
    match stem {
        "act" | "act-empty" | "act-escapes" | "act-footnotes" => (DocumentRoot::Act, "act"),
        "debate-report" => (DocumentRoot::DebateReport, "debateReport"),
        "eids" | "nested_attachments" => (DocumentRoot::Statement, "statement"),
        "hansard" => (DocumentRoot::Debate, "debate"),
        "judgment" | "judgment-attachments" => (DocumentRoot::Judgment, "judgment"),
        _ => panic!("no document root mapping for roundtrip fixture {stem}.txt"),
    }
}

fn roundtrip_xml_fixture_root(stem: &str) -> (DocumentRoot, &'static str) {
    match stem {
        "attribs" | "eids_basic" | "eids_edge" | "escapes" | "nested_attachments" => {
            (DocumentRoot::Act, "act")
        }
        "eids_debatereport" => (DocumentRoot::DebateReport, "debateReport"),
        _ => panic!("no document root mapping for roundtrip XML fixture {stem}.xml"),
    }
}

fn default_roundtrip_frbr_uri(root: DocumentRoot) -> String {
    match root {
        DocumentRoot::Act => "/akn/za/act/2022/1",
        DocumentRoot::Bill => "/akn/za/bill/2022/1",
        DocumentRoot::Debate => "/akn/za/debate/2022/1",
        DocumentRoot::DebateReport => "/akn/za/debateReport/2022/1",
        DocumentRoot::Doc => "/akn/za/doc/2022/1",
        DocumentRoot::Judgment => "/akn/za/judgment/2022/1",
        DocumentRoot::Statement => "/akn/za/statement/2022/1",
        _ => "/akn/za/act/2022/1",
    }
    .to_string()
}

fn focused_cases() -> Vec<ParityCase> {
    vec![
        text_case(
            "inline-standard-elements",
            DocumentRoot::Statement,
            "statement",
            "P Text with {{term{refersTo #foo}a term}} and {{abbr{title Laws.Africa}LA}} and {{em emphasized}} and {{inline{name x}named}}.",
        ),
        prefixed_text_case(
            "eids-with-prefix",
            DocumentRoot::Statement,
            "statement",
            "pref",
            "P intro\n\nSEC 1. - Heading\n  text with {{FOOTNOTE 1}}\n\nFOOTNOTE 1\n  note",
        ),
        text_case(
            "fragment-hier-element",
            DocumentRoot::HierElement,
            "hier_element",
            "CROSSHEADING Intro",
        ),
        text_case(
            "fragment-hier-element-block",
            DocumentRoot::HierElementBlock,
            "hier_element_block",
            "SEC 1. - Heading\n  text",
        ),
        text_case(
            "proviso-hier-element-block",
            DocumentRoot::HierElementBlock,
            "hier_element_block",
            "PROVISO 1 - Savings\n  This rule applies.",
        ),
        text_case(
            "fragment-hier-block-element",
            DocumentRoot::HierBlockElement,
            "hier_block_element",
            "SEC 1. - Heading\n  text",
        ),
        text_case(
            "fragment-hier-indent",
            DocumentRoot::HierIndent,
            "hier_indent",
            "SEC 1. - Heading\n  text",
        ),
        text_case(
            "fragment-hier-block-indent",
            DocumentRoot::HierBlockIndent,
            "hier_block_indent",
            "SEC 1. - Heading\n  text",
        ),
        text_case(
            "fragment-attachment",
            DocumentRoot::Attachment,
            "attachment",
            "SCHEDULE Schedule\n  text",
        ),
        text_case(
            "fragment-attachments",
            DocumentRoot::Attachments,
            "attachments",
            "SCHEDULE One\n  one\nSCHEDULE Two\n  two",
        ),
        text_case(
            "fragment-block-element",
            DocumentRoot::BlockElement,
            "block_element",
            "ITEMS\n  ITEM (a)\n    text",
        ),
        text_case(
            "fragment-block-elements",
            DocumentRoot::BlockElements,
            "block_elements",
            "ITEMS\n  ITEM (a)\n    text",
        ),
        text_case(
            "fragment-block-list",
            DocumentRoot::BlockList,
            "block_list",
            "ITEMS\n  ITEM (a)\n    text",
        ),
        text_case(
            "fragment-block-list-item",
            DocumentRoot::BlockListItem,
            "block_list_item",
            "ITEM (a)\n  text",
        ),
        text_case(
            "fragment-bullet-list",
            DocumentRoot::BulletList,
            "bullet_list",
            "BULLETS\n  * text",
        ),
        text_case(
            "fragment-bullet-list-item",
            DocumentRoot::BulletListItem,
            "bullet_list_item",
            "* text",
        ),
        text_case(
            "fragment-table",
            DocumentRoot::Table,
            "table",
            "TABLE\n  TR\n    TC\n      text",
        ),
        text_case(
            "fragment-table-row",
            DocumentRoot::TableRow,
            "table_row",
            "TR\n  TC\n    text",
        ),
        text_case("fragment-table-cell", DocumentRoot::TableCell, "table_cell", "TC\n  text"),
        text_case(
            "fragment-speech-container",
            DocumentRoot::SpeechContainer,
            "speech_container",
            "DEBATESECTION 1 - Debate\n  SPEECH\n    FROM Speaker\n    NARRATIVE Hello",
        ),
        text_case(
            "fragment-speech-container-indent",
            DocumentRoot::SpeechContainerIndent,
            "speech_container_indent",
            "DEBATESECTION 1 - Debate\n  SPEECH\n    FROM Speaker\n    NARRATIVE Hello",
        ),
        text_case(
            "fragment-speech-group",
            DocumentRoot::SpeechGroup,
            "speech_group",
            "SPEECH\n  FROM Speaker\n  NARRATIVE Hello",
        ),
        text_case(
            "fragment-speech-hier-block-element",
            DocumentRoot::SpeechHierBlockElement,
            "speech_hier_block_element",
            "SPEECH\n  FROM Speaker\n  NARRATIVE Hello",
        ),
        text_case(
            "fragment-speech-block",
            DocumentRoot::SpeechBlock,
            "speech_block",
            "NARRATIVE Hello",
        ),
        text_case("fragment-p", DocumentRoot::P, "p", "P Hello"),
        text_case("fragment-line", DocumentRoot::Line, "line", "Hello"),
        text_case(
            "fragment-longtitle",
            DocumentRoot::Longtitle,
            "longtitle",
            "LONGTITLE Long title",
        ),
        text_case(
            "fragment-crossheading",
            DocumentRoot::Crossheading,
            "crossheading",
            "CROSSHEADING Cross",
        ),
        text_case("fragment-blocks", DocumentRoot::Blocks, "blocks", "BLOCKS\n  text"),
        text_case(
            "fragment-block-quote",
            DocumentRoot::BlockQuote,
            "block_quote",
            "QUOTE\n  text",
        ),
        text_case("fragment-preface", DocumentRoot::Preface, "preface", "PREFACE\nhello"),
        text_case(
            "fragment-preamble",
            DocumentRoot::Preamble,
            "preamble",
            "PREAMBLE\nhello",
        ),
        text_case(
            "fragment-body",
            DocumentRoot::Body,
            "body",
            "BODY\nSEC 1. - Heading\n  text",
        ),
        text_case("fragment-main-body", DocumentRoot::MainBody, "mainBody", "BODY\ntext"),
        text_case(
            "fragment-debate-body",
            DocumentRoot::DebateBody,
            "debateBody",
            "BODY\nDEBATESECTION 1 - Debate\n  SPEECH\n    FROM Speaker\n    NARRATIVE Hello",
        ),
        text_case(
            "fragment-conclusions",
            DocumentRoot::Conclusions,
            "conclusions",
            "CONCLUSIONS\nhello",
        ),
        text_case(
            "fragment-introduction",
            DocumentRoot::Introduction,
            "introduction",
            "INTRODUCTION\nhello",
        ),
        text_case(
            "fragment-background",
            DocumentRoot::Background,
            "background",
            "BACKGROUND\nhello",
        ),
        text_case(
            "fragment-arguments",
            DocumentRoot::Arguments,
            "arguments",
            "ARGUMENTS\nhello",
        ),
        text_case(
            "fragment-remedies",
            DocumentRoot::Remedies,
            "remedies",
            "REMEDIES\nhello",
        ),
        text_case(
            "fragment-motivation",
            DocumentRoot::Motivation,
            "motivation",
            "MOTIVATION\nhello",
        ),
        text_case(
            "fragment-decision",
            DocumentRoot::Decision,
            "decision",
            "DECISION\nhello",
        ),
        text_case(
            "inline-refs-images-remarks",
            DocumentRoot::Statement,
            "statement",
            "P A {{>#sec_1 reference}} and {{IMG /foo.png description}} and {{*remark}}.",
        ),
        text_case(
            "inline-nested-and-escaped",
            DocumentRoot::Statement,
            "statement",
            "P some **bold //italics// text** and escaped \\{\\{ curlies \\}\\}.",
        ),
        text_case(
            "inline-remark-nested-ref",
            DocumentRoot::Statement,
            "statement",
            "P {{*[{{>https://example.com a link}}]}} and **bold {{^super {{*[foo {{>/bar link}} end]}}}} {{*[and another]}}**",
        ),
        text_case(
            "inline-ref-edge-cases",
            DocumentRoot::Statement,
            "statement",
            "P {{>https://example.com  a link{{^2}} **with stuff**}} {{>https://example.com}} {{> link text}}",
        ),
        text_case(
            "inline-image-edge-cases",
            DocumentRoot::Statement,
            "statement",
            "P {{IMG /foo.png}} {{IMG/foo.png}} {{IMGfoo.png}} {{IMG /foo.png  description text }} {{IMG }} {{IMG}}",
        ),
        text_case(
            "inline-sup-sub-ins-del",
            DocumentRoot::Statement,
            "statement",
            "P {{^super {{_s}ub}} **bo*ld**}} and {{+ ins {{- de}l}} **bo*ld**}}",
        ),
        text_case(
            "hierarchy-unnumbered-duplicates",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC - Heading\n  text\nSEC - Heading\n  more text",
        ),
        text_case(
            "hierarchy-heading-adjacent-inline-spacing",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 8B. - Taxation of {{term{refersTo #term-employee} employee}} {{term{refersTo #term-share} share}} plan\n  text",
        ),
        text_case(
            "hierarchy-crossheading-containers",
            DocumentRoot::Act,
            "act",
            "BODY\nCROSSHEADING first\nCROSSHEADING second\n\ntext\n\nPART 1\n  ITEMS\n    ITEM\n      item 1\n  CROSSHEADING inside\n  wrap",
        ),
        text_case(
            "hierarchy-mixed-intro-interstitial-wrapup",
            DocumentRoot::Act,
            "act",
            "BODY\nPART\n  some intro text\n  SECTION 1\n    section 1 text\n  some interstitial text\n  SECTION 2\n    section 2 text\n  conclusion",
        ),
        text_case(
            "hierarchy-empty-heading-num",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  PART\n    no num no heading\n  PART 1. -\n    no heading\n  PART -\n    no num no heading\n  PART 2.\n    no heading\n  PART - heading\n    no num\n  PART 3-a - head-ing and - here\n    dash in num and heading",
        ),
        text_case(
            "hierarchy-escaped-hyphen-nums",
            DocumentRoot::Act,
            "act",
            "BODY\nPART\n  SEC 1-\n    no escape no heading\n  SEC 1\\-\n    escape no heading\n  SEC 1 \\-\n    escape no heading\n  SEC 2\\- - heading\n    with heading\n  SEC \\-6\n    preceding slash\n  SEC 6\\-\\-7\n    multi",
        ),
        text_case(
            "hierarchy-empty-elements",
            DocumentRoot::Act,
            "act",
            "BODY\nPART\n  SEC 1 - heading\n  SEC\n    SUBHEADING subheading\n  PART\n  CHAPTER - heading",
        ),
        text_case(
            "block-list-with-subheading",
            DocumentRoot::Statement,
            "statement",
            "ITEMS\n  intro\n  ITEM (a)\n    first\n  ITEM (b)\n    SUBHEADING sub\n    second\n  wrap",
        ),
        text_case(
            "block-list-footnotes",
            DocumentRoot::Statement,
            "statement",
            "ITEMS\n  some intro with {{FOOTNOTE 1}} and {{FOOTNOTE 2}}\n  FOOTNOTE 1\n    footnote 1\n  FOOTNOTE 2\n    footnote 2\n  ITEM (a)\n    item a\n  wrap up with {{FOOTNOTE 3}}\n  FOOTNOTE 3\n    footnote 3",
        ),
        text_case(
            "block-list-nested",
            DocumentRoot::Statement,
            "statement",
            "ITEMS\n  some intro\n  ITEM (a)\n    ITEMS{foo bar}\n      item a\n      ITEM (i)\n        item a(i)\n      and a wrap up\n  ITEM (b)\n    item b",
        ),
        text_case(
            "block-list-broken-empty-item",
            DocumentRoot::Statement,
            "statement",
            "ITEMS\n  ITEM (a)",
        ),
        text_case(
            "block-container-and-quote",
            DocumentRoot::Statement,
            "statement",
            "BLOCKS.cls{a b}\n  some block text\n  QUOTE{startQuote \"|endQuote \"}\n    quoted text",
        ),
        text_case(
            "invalid-xml-attribute-names",
            DocumentRoot::Statement,
            "statement",
            "QUOTE{\" foo|@ bar|1baz qux|foo:bar namespace|boom bang|éclair oui|名 value|á accent|quote \"}\n  quoted text",
        ),
        text_case(
            "block-container-generic",
            DocumentRoot::Act,
            "act",
            "BODY\nPART A\n  BLOCKS.cls{a b}\n    foo\n    ITEMS\n      ITEM bar\n      ITEM baz\n    end\n  BLOCKS\n    foo\n    bar\n  tail",
        ),
        text_case(
            "block-attrs-longtitle-crossheading",
            DocumentRoot::Act,
            "act",
            "BODY\nPART A\n  P.baz{class foo bar} text with classes\n  P{style text-align: center} text with style tag\n  LONGTITLE test\n  CROSSHEADING crossheading",
        ),
        text_case(
            "containers-indent-and-conclusions",
            DocumentRoot::Act,
            "act",
            "PREAMBLE\n  not indented\n    indented\nBODY\n  body\nCONCLUSIONS\n    PART 1\n    text\n    ITEMS\n      ITEM (a)\n        item a",
        ),
        text_case(
            "tables-and-bullets",
            DocumentRoot::Statement,
            "statement",
            "BULLETS\n  * one\n  * two\nTABLE.my-table\n  TR\n    TH\n      heading\n    TC{colspan 2}\n      cell",
        ),
        text_case(
            "bullets-nested-and-mixed",
            DocumentRoot::Statement,
            "statement",
            "BULLETS{class spiffy}\n  * item 1\n  * item 2\n    BULLETS\n      * item 2a\n      * item 2b\n  *\n  * an empty item (valid)\n  *\n    an item that starts empty",
        ),
        text_case(
            "bullets-non-starred-items",
            DocumentRoot::Statement,
            "statement",
            "BULLETS\n  * bullet 1\n    with multiple lines\n  no star 1\n\n  no star 2\n    with indent\n  * a star\n\n  no star 3",
        ),
        text_case(
            "bullets-bad-hier-fallback",
            DocumentRoot::Judgment,
            "judgment",
            "BULLETS\n  PARA 24.\n    SUBPARA i.\n      Bar",
        ),
        text_case(
            "table-attrs-and-broken-fallback",
            DocumentRoot::Act,
            "act",
            "BODY\nSECTION 1.\n  SUBSECTION (a)\n    TABLE{class my-table}\n      TR\n        TC{colspan 2}\n          r1c1\n        TC{rowspan 1 | colspan 3\"}\n          r1c2\n  bar\n  SUBSECTION (b)\n    TABLE\n      TR\n  baz",
        ),
        text_case(
            "judgment-no-explicit-structure",
            DocumentRoot::Judgment,
            "judgment",
            "hello\n\nthere",
        ),
        text_case(
            "subflows-footnotes",
            DocumentRoot::Judgment,
            "judgment",
            "BACKGROUND\n  hello {{FOOTNOTE 1}} there\n  FOOTNOTE 1\n    footnote text\nARGUMENTS\n  argument",
        ),
        text_case(
            "subflows-footnote-complex-content",
            DocumentRoot::Act,
            "act",
            "BODY\nPART 1\n  this section [{{FOOTNOTE 1}}] uses a footnote.\n  FOOTNOTE 1\n    some text\n    PART 1\n      ITEMS\n        ITEM (a)\n          item",
        ),
        text_case(
            "subflows-quote-embedded-structure",
            DocumentRoot::Judgment,
            "judgment",
            "INTRODUCTION\n  some text\n  QUOTE\n    quoted\n    ITEMS\n      ITEM (a)\n        list item\n    PART 1 - Heading\n      part 1 text\n  something else",
        ),
        text_case(
            "attachments-nested-metadata",
            DocumentRoot::Judgment,
            "judgment",
            "ARGUMENTS\n  argument\nANNEXURE Annex 1\n  annex text\nAPPENDIX Appendix 1\n  APPENDIX Nested\n    nested text",
        ),
        text_case(
            "attachments-multiple-crossheading",
            DocumentRoot::Act,
            "act",
            "BODY\n  body\nANNEXURE a heading\n  SUBHEADING subheading\n  some text\n  CROSSHEADING crossheading\nCROSSHEADING crossheading2\nSCHEDULE heading\n  schedule text",
        ),
        text_case(
            "attachments-no-indent",
            DocumentRoot::Act,
            "act",
            "BODY\n  body\nANNEXURE a heading\nSUBHEADING not matched as a subheading\n\n  some text\nSCHEDULE heading\n\nschedule text",
        ),
        text_case(
            "debate-speech",
            DocumentRoot::Debate,
            "debate",
            "DEBATESECTION 1 - Debate\n  SPEECH num - heading\n    SUBHEADING sub-heading\n    FROM THE PRESIDENT:\n    NARRATIVE Hello",
        ),
        text_case(
            "rtl-and-attrs",
            DocumentRoot::Statement,
            "statement",
            "P.rtl{a b|foo bar|baz boom} טקסט כלשהו",
        ),
        text_case("empty-act", DocumentRoot::Act, "act", ""),
        text_case("empty-bill", DocumentRoot::Bill, "bill", ""),
        text_case("empty-debate", DocumentRoot::Debate, "debate", ""),
        text_case(
            "empty-debate-report",
            DocumentRoot::DebateReport,
            "debateReport",
            "",
        ),
        text_case("empty-doc", DocumentRoot::Doc, "doc", ""),
        text_case("empty-judgment", DocumentRoot::Judgment, "judgment", ""),
        text_case("empty-statement", DocumentRoot::Statement, "statement", ""),
        text_case(
            "preface-preamble-conclusions",
            DocumentRoot::Act,
            "act",
            "PREFACE\n  preface\nPREAMBLE\n  preamble\nBODY\n  body\nCONCLUSIONS\n  done",
        ),
        text_case(
            "missing-footnote-content",
            DocumentRoot::Statement,
            "statement",
            "P hello {{FOOTNOTE 99}} there",
        ),
        text_case(
            "footnote-orphan-content",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  text\n  FOOTNOTE *\n    orphan footnote text",
        ),
        text_case(
            "footnote-two-refs-one-content",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  a {{FOOTNOTE 1}} and b {{FOOTNOTE 1}}\n  FOOTNOTE 1\n    only one",
        ),
        text_case(
            "footnote-nested-orphans",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  text\n  FOOTNOTE 1\n    outer\n    FOOTNOTE 2\n      inner",
        ),
        text_case(
            "footnote-orphan-inside-used",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  a {{FOOTNOTE 1}}\n  FOOTNOTE 1\n    outer\n    FOOTNOTE 2\n      inner orphan",
        ),
        text_case(
            "crlf-line-endings",
            DocumentRoot::Act,
            "act",
            "BODY\r\nSEC 1. - Heading\r\n  Some text.\r\n",
        ),
        text_case(
            "cr-only-line-endings",
            DocumentRoot::Act,
            "act",
            "BODY\rSEC 1.\r  text\r",
        ),
        text_case(
            "control-char-edges",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  text\u{1c}",
        ),
        text_case(
            "trailing-space-before-cr",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  a \r\n  b",
        ),
        text_case(
            "unicode-whitespace-in-text",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC 1.\n  a\u{a0}b and\u{2003}c\n  \u{a0}leading nbsp\n\u{2003}leading em space",
        ),
        text_case(
            "attr-value-with-cr",
            DocumentRoot::Statement,
            "statement",
            "P{style a\rb} text",
        ),
        text_case(
            "xml-special-chars",
            DocumentRoot::Statement,
            "statement",
            "P a & b < c > d \"quoted\" '&amp;' {{term{refersTo #a&b<c>\"d} text}}",
        ),
        text_case(
            "bullets-crlf",
            DocumentRoot::Statement,
            "statement",
            "BULLETS\r\n  *\r\n  * item\r\n    more\r\n",
        ),
        uri_text_case(
            "frbr-uri-subtype",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/gn/2022/r1234",
        ),
        uri_text_case(
            "frbr-uri-locality-subtype",
            DocumentRoot::Act,
            "act",
            "/akn/za-cpt/act/by-law/2016/control",
        ),
        uri_text_case(
            "frbr-uri-language",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/2022/1/afr",
        ),
        uri_text_case(
            "frbr-uri-expression-date",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/2022/1/eng@2023-01-01",
        ),
        uri_text_case(
            "frbr-uri-actor",
            DocumentRoot::Statement,
            "statement",
            "/akn/aa-au/statement/deliberation/mpc/2011/24",
        ),
        uri_text_case(
            "frbr-uri-full-date",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/2022-03-01/12",
        ),
        uri_text_case(
            "frbr-uri-no-akn-prefix",
            DocumentRoot::Act,
            "act",
            "/za/act/2022/1",
        ),
        text_case(
            "duplicate-numbered-hierarchy",
            DocumentRoot::Act,
            "act",
            "BODY\nPART 1\n  SEC 1\n    first\n  SEC 1\n    second",
        ),
        text_case(
            "eids-doc-no-num-and-duplicates",
            DocumentRoot::Doc,
            "doc",
            "PARA\n  Intro\nPARA 1.\n  First para\nPARA 1A.\n  Added in later\nPARA\n  Unnumbered\nPARA 2.\n  Second para.\nPARA 2.\n  Another para with the num 2.\nPARA 2.3..74.5.\n  Interesting number.\nPARA 2.3..74.5.\n  Duplicate interesting number.",
        ),
        text_case(
            "eids-backslash-punctuation",
            DocumentRoot::Doc,
            "doc",
            "PARA 5\\\n  trailing backslash\nPARA \\5\n  leading backslash\nPARA 5\\6\n  middle backslash",
        ),
        text_case(
            "eids-doc-nn-collisions",
            DocumentRoot::Doc,
            "doc",
            "PARA\n  Unnumbered para.\nPARA\n  Second unnumbered para.\nPARA (nn)\n  Perfectly possible paragraph numbering.\nPARA nn_2\n  Para nn_2, which is the second para's eId.\nPARA nn_2\n  Para nn_2, which is a dup of the second para's eId.\nPARA nn-2\n  Para nn-2, which we do support because we support hyphens in numbers",
        ),
    ]
}

fn file_case(
    name: String,
    root: DocumentRoot,
    python_root: &'static str,
    frbr_uri: String,
    path: PathBuf,
) -> ParityCase {
    ParityCase {
        name,
        root,
        python_root,
        frbr_uri,
        eid_prefix: String::new(),
        input: CaseInput::File(path),
    }
}

fn xml_fixture_case(
    name: String,
    root: DocumentRoot,
    python_root: &'static str,
    frbr_uri: String,
    path: PathBuf,
) -> ParityCase {
    ParityCase {
        name,
        root,
        python_root,
        frbr_uri,
        eid_prefix: String::new(),
        input: CaseInput::XmlFixture(path),
    }
}

fn text_case(
    name: &'static str,
    root: DocumentRoot,
    python_root: &'static str,
    text: &'static str,
) -> ParityCase {
    ParityCase {
        name: name.to_string(),
        root,
        python_root,
        frbr_uri: default_frbr_uri(root).to_string(),
        eid_prefix: String::new(),
        input: CaseInput::Text(text),
    }
}

fn prefixed_text_case(
    name: &'static str,
    root: DocumentRoot,
    python_root: &'static str,
    eid_prefix: &'static str,
    text: &'static str,
) -> ParityCase {
    ParityCase {
        name: name.to_string(),
        root,
        python_root,
        frbr_uri: default_frbr_uri(root).to_string(),
        eid_prefix: eid_prefix.to_string(),
        input: CaseInput::Text(text),
    }
}

/// A case that exercises meta generation for a specific FRBR URI shape,
/// including attachment metadata.
fn uri_text_case(
    name: &'static str,
    root: DocumentRoot,
    python_root: &'static str,
    frbr_uri: &'static str,
) -> ParityCase {
    ParityCase {
        name: name.to_string(),
        root,
        python_root,
        frbr_uri: frbr_uri.to_string(),
        eid_prefix: String::new(),
        input: CaseInput::Text(
            "BODY\nSEC 1. - Heading\n  Some text.\nSCHEDULE First Schedule\n  schedule text",
        ),
    }
}

fn default_frbr_uri(root: DocumentRoot) -> &'static str {
    match root {
        DocumentRoot::Act => "/akn/za/act/2009/10",
        DocumentRoot::Bill => "/akn/za/bill/2009/10",
        DocumentRoot::Debate => "/akn/za/debate/2009/10",
        DocumentRoot::DebateReport => "/akn/za/debateReport/2009/10",
        DocumentRoot::Doc => "/akn/za/doc/2009/10",
        DocumentRoot::Judgment => "/akn/za/judgment/2009/10",
        DocumentRoot::Statement => "/akn/za/statement/2009/10",
        _ => "/akn/za/act/2009/10",
    }
}

impl CaseInput {
    fn read(&self, name: &str) -> String {
        match self {
            CaseInput::File(path) => fs::read_to_string(path)
                .unwrap_or_else(|err| panic!("failed to read {name}: {err}")),
            CaseInput::XmlFixture(path) => {
                let xml = fs::read_to_string(path)
                    .unwrap_or_else(|err| panic!("failed to read {name}: {err}"));
                unparse(&xml).unwrap_or_else(|err| panic!("failed to unparse {name}: {err}"))
            }
            CaseInput::Text(text) => text.to_string(),
        }
    }
}

fn python_parse_to_xml(case: &ParityCase, text: &str) -> String {
    let text_path = write_temp_file(&case.name, "input.txt", text);
    // read_bytes + decode: read_text would translate \r\n to \n (universal
    // newlines) and hide line-ending behaviour from the parity check
    let script = format!(
        "from pathlib import Path\nfrom bluebell.parser import AkomaNtosoParser\nfrom cobalt import FrbrUri\nfrom lxml import etree\np=AkomaNtosoParser(FrbrUri.parse({uri:?}), {eid_prefix:?})\nxml=p.parse_to_xml(Path({text:?}).read_bytes().decode('utf-8'), {root:?})\nprint(etree.tostring(xml, encoding='unicode'), end='')\n",
        uri = case.frbr_uri,
        eid_prefix = case.eid_prefix,
        text = text_path.display().to_string(),
        root = case.python_root,
    );
    run_python(&script, &case.name, "python parse_to_xml")
}

fn python_parse_to_xml_with_source(
    case: &ParityCase,
    text: &str,
    source: &MetadataSource,
) -> String {
    let text_path = write_temp_file(&case.name, "input.txt", text);
    let script = format!(
        "from pathlib import Path\nfrom bluebell.parser import AkomaNtosoParser\nfrom cobalt import FrbrUri\nfrom cobalt.akn import AkomaNtosoDocument\nfrom lxml import etree\nold_source = AkomaNtosoDocument.source\nAkomaNtosoDocument.source = [{show_as:?}, {eid:?}, {href:?}]\ntry:\n    p=AkomaNtosoParser(FrbrUri.parse({uri:?}), {eid_prefix:?})\n    xml=p.parse_to_xml(Path({text:?}).read_bytes().decode('utf-8'), {root:?})\n    print(etree.tostring(xml, encoding='unicode'), end='')\nfinally:\n    AkomaNtosoDocument.source = old_source\n",
        show_as = source.show_as,
        eid = source.eid,
        href = source.href,
        uri = case.frbr_uri,
        eid_prefix = case.eid_prefix,
        text = text_path.display().to_string(),
        root = case.python_root,
    );
    run_python(&script, &case.name, "python parse_to_xml with source")
}

fn python_canonicalize(xml: &str, name: &str, label: &str) -> String {
    let xml_path = write_temp_file(name, &format!("{label}.xml"), xml);
    let script = format!(
        "from pathlib import Path\nfrom lxml import etree\nprint(etree.canonicalize(Path({xml:?}).read_text()), end='')\n",
        xml = xml_path.display().to_string(),
    );
    run_python(&script, name, "canonicalize")
}

fn write_failure_artifacts(case: &ParityCase, rust_xml: &str, python_xml: &str) {
    let dir = artifact_dir(&case.name);
    fs::create_dir_all(&dir).expect("failed to create parity artifact dir");
    fs::write(
        dir.join("rust.xml"),
        pretty_xml(rust_xml, &case.name, "rust"),
    )
    .expect("failed to write rust parity artifact");
    fs::write(
        dir.join("python.xml"),
        pretty_xml(python_xml, &case.name, "python"),
    )
    .expect("failed to write python parity artifact");
    fs::write(dir.join("input.txt"), case.input.read(&case.name))
        .expect("failed to write parity input artifact");
}

fn pretty_xml(xml: &str, name: &str, label: &str) -> String {
    let xml_path = write_temp_file(name, &format!("{label}-pretty.xml"), xml);
    let script = format!(
        "from pathlib import Path\nfrom lxml import etree\nroot=etree.fromstring(Path({xml:?}).read_bytes())\nprint(etree.tostring(root, pretty_print=True, encoding='unicode'), end='')\n",
        xml = xml_path.display().to_string(),
    );
    run_python(&script, name, "pretty print")
}

fn run_python(script: &str, case_name: &str, action: &str) -> String {
    let output = Command::new(python())
        .arg("-c")
        .arg(script)
        .env("PYTHONPATH", python_path())
        .output()
        .unwrap_or_else(|err| panic!("{action} failed for {case_name}: {err}"));
    assert!(
        output.status.success(),
        "{action} failed for {case_name}:\nstdout:\n{}\nstderr:\n{}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    String::from_utf8(output.stdout).expect("python emitted non-UTF-8 output")
}

fn write_temp_file(case_name: &str, filename: &str, content: &str) -> PathBuf {
    let dir = artifact_dir(case_name);
    fs::create_dir_all(&dir).expect("failed to create parity temp dir");
    let path = dir.join(filename);
    fs::write(&path, content).expect("failed to write parity temp file");
    path
}

fn artifact_dir(case_name: &str) -> PathBuf {
    Path::new("/tmp/bluebell-rs-parity").join(case_name)
}

fn python() -> &'static str {
    "python"
}
