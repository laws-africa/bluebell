use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use bluebell_rs::{parse_to_akn_xml, DocumentRoot};

struct ParityCase {
    name: &'static str,
    root: DocumentRoot,
    python_root: &'static str,
    frbr_uri: &'static str,
    input: CaseInput,
}

enum CaseInput {
    File(&'static str),
    Text(&'static str),
}

#[test]
fn parsed_bluebell_xml_matches_python() {
    for case in parity_cases() {
        let text = case.input.read(case.name);
        let rust_xml = parse_to_akn_xml(&text, case.root, case.frbr_uri)
            .unwrap_or_else(|err| panic!("Rust failed to parse {}: {err}", case.name));
        let python_xml = python_parse_to_xml(&case, &text);

        let rust_c14n = python_canonicalize(&rust_xml, case.name, "rust");
        let python_c14n = python_canonicalize(&python_xml, case.name, "python");

        if rust_c14n != python_c14n {
            write_failure_artifacts(&case, &rust_xml, &python_xml);
        }
        assert_eq!(
            python_c14n, rust_c14n,
            "XML parity failed for {}",
            case.name
        );
    }
}

fn parity_cases() -> Vec<ParityCase> {
    let mut cases = vec![
        file_case(
            "roundtrip-act-empty",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act-empty.txt",
        ),
        file_case(
            "roundtrip-act-escapes",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act-escapes.txt",
        ),
        file_case(
            "roundtrip-act-footnotes",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act-footnotes.txt",
        ),
        file_case(
            "roundtrip-act",
            DocumentRoot::Act,
            "act",
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act.txt",
        ),
        file_case(
            "roundtrip-debate-report",
            DocumentRoot::DebateReport,
            "debateReport",
            "/akn/za/debateReport/2022/1",
            "../tests/roundtrip/debate-report.txt",
        ),
        file_case(
            "roundtrip-eids",
            DocumentRoot::Statement,
            "statement",
            "/akn/za/statement/2022/1",
            "../tests/roundtrip/eids.txt",
        ),
        file_case(
            "roundtrip-hansard",
            DocumentRoot::Debate,
            "debate",
            "/akn/za/debate/2022/1",
            "../tests/roundtrip/hansard.txt",
        ),
        file_case(
            "roundtrip-judgment-attachments",
            DocumentRoot::Judgment,
            "judgment",
            "/akn/za/judgment/2022/1",
            "../tests/roundtrip/judgment-attachments.txt",
        ),
        file_case(
            "roundtrip-judgment",
            DocumentRoot::Judgment,
            "judgment",
            "/akn/za/judgment/2022/1",
            "../tests/roundtrip/judgment.txt",
        ),
        file_case(
            "roundtrip-nested-attachments",
            DocumentRoot::Statement,
            "statement",
            "/akn/za/statement/2022/1",
            "../tests/roundtrip/nested_attachments.txt",
        ),
    ];

    cases.extend(focused_cases());
    cases
}

fn focused_cases() -> Vec<ParityCase> {
    vec![
        text_case(
            "inline-standard-elements",
            DocumentRoot::Statement,
            "statement",
            "P Text with {{term{refersTo #foo}a term}} and {{abbr{title Laws.Africa}LA}} and {{em emphasized}} and {{inline{name x}named}}.",
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
            "hierarchy-unnumbered-duplicates",
            DocumentRoot::Act,
            "act",
            "BODY\nSEC - Heading\n  text\nSEC - Heading\n  more text",
        ),
        text_case(
            "block-list-with-subheading",
            DocumentRoot::Statement,
            "statement",
            "ITEMS\n  intro\n  ITEM (a)\n    first\n  ITEM (b)\n    SUBHEADING sub\n    second\n  wrap",
        ),
        text_case(
            "block-container-and-quote",
            DocumentRoot::Statement,
            "statement",
            "BLOCKS.cls{a b}\n  some block text\n  QUOTE{startQuote \"|endQuote \"}\n    quoted text",
        ),
        text_case(
            "tables-and-bullets",
            DocumentRoot::Statement,
            "statement",
            "BULLETS\n  * one\n  * two\nTABLE.my-table\n  TR\n    TH\n      heading\n    TC{colspan 2}\n      cell",
        ),
        text_case(
            "subflows-footnotes",
            DocumentRoot::Judgment,
            "judgment",
            "BACKGROUND\n  hello {{FOOTNOTE 1}} there\n  FOOTNOTE 1\n    footnote text\nARGUMENTS\n  argument",
        ),
        text_case(
            "attachments-nested-metadata",
            DocumentRoot::Judgment,
            "judgment",
            "ARGUMENTS\n  argument\nANNEXURE Annex 1\n  annex text\nAPPENDIX Appendix 1\n  APPENDIX Nested\n    nested text",
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
            "duplicate-numbered-hierarchy",
            DocumentRoot::Act,
            "act",
            "BODY\nPART 1\n  SEC 1\n    first\n  SEC 1\n    second",
        ),
    ]
}

fn file_case(
    name: &'static str,
    root: DocumentRoot,
    python_root: &'static str,
    frbr_uri: &'static str,
    path: &'static str,
) -> ParityCase {
    ParityCase {
        name,
        root,
        python_root,
        frbr_uri,
        input: CaseInput::File(path),
    }
}

fn text_case(
    name: &'static str,
    root: DocumentRoot,
    python_root: &'static str,
    text: &'static str,
) -> ParityCase {
    ParityCase {
        name,
        root,
        python_root,
        frbr_uri: default_frbr_uri(root),
        input: CaseInput::Text(text),
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
    }
}

impl CaseInput {
    fn read(&self, name: &str) -> String {
        match self {
            CaseInput::File(path) => fs::read_to_string(path)
                .unwrap_or_else(|err| panic!("failed to read {name}: {err}")),
            CaseInput::Text(text) => text.to_string(),
        }
    }
}

fn python_parse_to_xml(case: &ParityCase, text: &str) -> String {
    let text_path = write_temp_file(case.name, "input.txt", text);
    let script = format!(
        "from pathlib import Path\nfrom bluebell.parser import AkomaNtosoParser\nfrom cobalt import FrbrUri\nfrom lxml import etree\np=AkomaNtosoParser(FrbrUri.parse({uri:?}))\nxml=p.parse_to_xml(Path({text:?}).read_text(), {root:?})\nprint(etree.tostring(xml, encoding='unicode'), end='')\n",
        uri = case.frbr_uri,
        text = text_path.display().to_string(),
        root = case.python_root,
    );
    run_python(&script, case.name, "python parse_to_xml")
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
    let dir = artifact_dir(case.name);
    fs::create_dir_all(&dir).expect("failed to create parity artifact dir");
    fs::write(
        dir.join("rust.xml"),
        pretty_xml(rust_xml, case.name, "rust"),
    )
    .expect("failed to write rust parity artifact");
    fs::write(
        dir.join("python.xml"),
        pretty_xml(python_xml, case.name, "python"),
    )
    .expect("failed to write python parity artifact");
    fs::write(dir.join("input.txt"), case.input.read(case.name))
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
        .env("PYTHONPATH", "..")
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
    if Path::new("../.env/bin/python").exists() {
        "../.env/bin/python"
    } else {
        "python"
    }
}
