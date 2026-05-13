use std::fs;
use std::path::Path;
use std::process::Command;

use bluebell_rs::{parse, parse_to_akn_xml, unparse, DocumentRoot};

#[test]
fn roundtrip_text_fixtures_emit_schema_valid_akn() {
    let fixtures = [
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act-empty.txt",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act-escapes.txt",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act-footnotes.txt",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/act.txt",
        ),
        (
            DocumentRoot::DebateReport,
            "/akn/za/debateReport/2022/1",
            "../tests/roundtrip/debate-report.txt",
        ),
        (
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
            "../tests/roundtrip/eids.txt",
        ),
        (
            DocumentRoot::Debate,
            "/akn/za/debate/2022/1",
            "../tests/roundtrip/hansard.txt",
        ),
        (
            DocumentRoot::Judgment,
            "/akn/za/judgment/2022/1",
            "../tests/roundtrip/judgment-attachments.txt",
        ),
        (
            DocumentRoot::Judgment,
            "/akn/za/judgment/2022/1",
            "../tests/roundtrip/judgment.txt",
        ),
        (
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
            "../tests/roundtrip/nested_attachments.txt",
        ),
    ];

    for (root, frbr_uri, path) in fixtures {
        let text =
            fs::read_to_string(path).unwrap_or_else(|err| panic!("failed to read {path}: {err}"));
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
fn xml_fixtures_native_unparse_back_to_schema_valid_akn() {
    let fixtures = [
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/attribs.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/eids_basic.xml",
        ),
        (
            DocumentRoot::DebateReport,
            "/akn/za/debateReport/2022/1",
            "../tests/roundtrip/eids_debatereport.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/eids_edge.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/escapes.xml",
        ),
        (
            DocumentRoot::Act,
            "/akn/za/act/2022/1",
            "../tests/roundtrip/nested_attachments.xml",
        ),
    ];

    for (root, frbr_uri, path) in fixtures {
        let xml =
            fs::read_to_string(path).unwrap_or_else(|err| panic!("failed to read {path}: {err}"));
        let text = unparse(&xml).unwrap_or_else(|err| panic!("failed to unparse {path}: {err}"));
        parse(&text, root)
            .unwrap_or_else(|err| panic!("failed to parse native unparse for {path}: {err}"));
        let regenerated = parse_to_akn_xml(&text, root, frbr_uri)
            .unwrap_or_else(|err| panic!("failed to regenerate {path}: {err}"));
        assert_schema_valid(&regenerated, path);
    }
}

fn assert_schema_valid(xml: &str, label: &str) {
    let dir = tempfile_dir();
    fs::create_dir_all(dir).expect("failed to create temp dir");
    let xml_path = dir.join("doc.xml");
    fs::write(&xml_path, xml).expect("failed to write temp xml");
    let script = format!(
        "from lxml import etree\nschema=etree.XMLSchema(etree.parse('../akomantoso30-lenient.xsd'))\ndoc=etree.parse({xml:?})\nvalid=schema.validate(doc)\nprint(valid)\nif not valid:\n print(schema.error_log.last_error)\n raise SystemExit(1)\n",
        xml = xml_path.display().to_string()
    );
    let python = if Path::new("../.env/bin/python").exists() {
        "../.env/bin/python"
    } else {
        "python"
    };
    let output = Command::new(python)
        .arg("-c")
        .arg(script)
        .output()
        .expect("failed to run python schema validation");
    assert!(
        output.status.success(),
        "{label} failed schema validation:\nstdout:\n{}\nstderr:\n{}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
}

fn tempfile_dir() -> &'static Path {
    Path::new("/tmp/bluebell-rs-schema-fixture")
}
