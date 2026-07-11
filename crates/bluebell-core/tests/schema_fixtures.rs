use std::fs;
use std::path::Path;
use std::process::Command;

use bluebell_core::{parse, parse_to_akn_xml, parse_to_xml, DocumentRoot};
use libxml::parser::Parser;
use libxml::schemas::{SchemaParserContext, SchemaValidationContext};

mod support;
use support::{python_path, repo_path, unparse};

#[test]
fn proviso_xslt_unparses_and_reparses() {
    let source = "PROVISO 1 - Savings\n\n  This rule applies.\n\n";
    let xml = parse_to_xml(source, DocumentRoot::HierElementBlock)
        .expect("Rust failed to parse PROVISO");

    let unparsed = unparse(&xml).expect("XSLT failed to unparse PROVISO");
    assert_eq!(unparsed, source);

    let reparsed = parse_to_xml(&unparsed, DocumentRoot::HierElementBlock)
        .expect("Rust failed to reparse unparsed PROVISO");
    assert_eq!(reparsed, xml);
}

#[test]
fn roundtrip_text_fixtures_emit_schema_valid_akn() {
    let fixtures = [
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/act-empty.txt",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/act-escapes.txt",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/act-footnotes.txt",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/act.txt",
        ),
        (
            DocumentRoot::DebateReport,
            "/akn/za/debateReport/2022/1",
            "tests/roundtrip/debate-report.txt",
        ),
        (
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
            "tests/roundtrip/eids.txt",
        ),
        (
            DocumentRoot::Debate,
            "/akn/za/debate/2022/1",
            "tests/roundtrip/hansard.txt",
        ),
        (
            DocumentRoot::Judgment,
            "/akn/za/judgment/2022/1",
            "tests/roundtrip/judgment-attachments.txt",
        ),
        (
            DocumentRoot::Judgment,
            "/akn/za/judgment/2022/1",
            "tests/roundtrip/judgment.txt",
        ),
        (
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
            "tests/roundtrip/nested_attachments.txt",
        ),
    ];

    for (root, frbr_uri, path) in fixtures {
        let text = fs::read_to_string(repo_path(path))
            .unwrap_or_else(|err| panic!("failed to read {path}: {err}"));
        let xml = parse_to_akn_xml(&text, root, frbr_uri)
            .unwrap_or_else(|err| panic!("failed to parse {path}: {err}"));
        assert_schema_valid(&xml, path);
        let unparsed =
            unparse(&xml).unwrap_or_else(|err| panic!("failed to unparse {path}: {err}"));
        parse(&unparsed, root)
            .unwrap_or_else(|err| panic!("failed to parse Rust-unparsed XML for {path}: {err}"));
    }
}

#[test]
fn xml_fixtures_xslt_unparse_back_to_schema_valid_akn() {
    let fixtures = [
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/attribs.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/eids_basic.xml",
        ),
        (
            DocumentRoot::DebateReport,
            "/akn/za/debateReport/2022/1",
            "tests/roundtrip/eids_debatereport.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/eids_edge.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/escapes.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "tests/roundtrip/nested_attachments.xml",
        ),
    ];

    for (root, frbr_uri, path) in fixtures {
        let xml = fs::read_to_string(repo_path(path))
            .unwrap_or_else(|err| panic!("failed to read {path}: {err}"));
        let text = unparse(&xml).unwrap_or_else(|err| panic!("failed to unparse {path}: {err}"));
        parse(&text, root)
            .unwrap_or_else(|err| panic!("failed to parse XSLT unparse for {path}: {err}"));
        let regenerated = parse_to_akn_xml(&text, root, frbr_uri)
            .unwrap_or_else(|err| panic!("failed to regenerate {path}: {err}"));
        assert_schema_valid(&regenerated, path);
    }
}

#[test]
fn xslt_unparse_matches_python_unparse() {
    let fixtures = [
        "tests/roundtrip/attribs.xml",
        "tests/roundtrip/eids_basic.xml",
        "tests/roundtrip/eids_debatereport.xml",
        "tests/roundtrip/eids_edge.xml",
        "tests/roundtrip/escapes.xml",
        "tests/roundtrip/nested_attachments.xml",
    ];

    for path in fixtures {
        let xml = fs::read_to_string(repo_path(path))
            .unwrap_or_else(|err| panic!("failed to read {path}: {err}"));
        let rust_text =
            unparse(&xml).unwrap_or_else(|err| panic!("failed to unparse {path}: {err}"));
        let python_text = python_unparse(&xml, path);
        assert_eq!(python_text, rust_text, "XSLT unparse mismatch for {path}");
    }
}

fn assert_schema_valid(xml: &str, label: &str) {
    let parser = Parser::default();
    let doc = parser
        .parse_string(xml)
        .unwrap_or_else(|err| panic!("{label} failed XML parsing before schema validation: {err}"));

    let schema_path = repo_path("crates/bluebell-core/schemas/akomantoso30-lenient.xsd");
    let mut schema_parser = SchemaParserContext::from_file(
        schema_path
            .to_str()
            .expect("schema path should be valid UTF-8"),
    );
    let mut validation = SchemaValidationContext::from_parser(&mut schema_parser)
        .unwrap_or_else(|errors| panic!("failed to parse lenient AKN schema: {errors:?}"));

    validation
        .validate_document(&doc)
        .unwrap_or_else(|errors| panic!("{label} failed schema validation: {errors:?}"));
}

fn python_unparse(xml: &str, label: &str) -> String {
    let dir = tempfile_dir();
    fs::create_dir_all(dir).expect("failed to create temp dir");
    let xml_path = dir.join("unparse.xml");
    fs::write(&xml_path, xml).expect("failed to write temp xml");
    let script = format!(
        "from pathlib import Path\nfrom bluebell.parser import AkomaNtosoParser\nfrom cobalt import FrbrUri\np=AkomaNtosoParser(FrbrUri.parse('/akn/za/act/2022/1'))\nprint(p.unparse(Path({xml:?}).read_bytes()), end='')\n",
        xml = xml_path.display().to_string()
    );
    let output = Command::new(python())
        .arg("-c")
        .arg(script)
        .env("PYTHONPATH", python_path())
        .output()
        .unwrap_or_else(|err| panic!("failed to run python unparse for {label}: {err}"));
    assert!(
        output.status.success(),
        "{label} failed python unparse:\nstdout:\n{}\nstderr:\n{}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    String::from_utf8(output.stdout).expect("python unparse emitted non-UTF-8 output")
}

fn python() -> &'static str {
    "python"
}

fn tempfile_dir() -> &'static Path {
    Path::new("/tmp/bluebell-rs-schema-fixture")
}
