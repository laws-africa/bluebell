use bluebell_core::{parse, DocumentRoot};

mod support;
use support::repo_path;

#[test]
fn parses_roundtrip_text_fixtures() {
    let fixtures = [
        (DocumentRoot::Act, "tests/roundtrip/act-attributes.txt"),
        (DocumentRoot::Act, "tests/roundtrip/act-empty.txt"),
        (DocumentRoot::Act, "tests/roundtrip/act-escapes.txt"),
        (DocumentRoot::Act, "tests/roundtrip/act-footnotes.txt"),
        (DocumentRoot::Act, "tests/roundtrip/act.txt"),
        (
            DocumentRoot::DebateReport,
            "tests/roundtrip/debate-report.txt",
        ),
        (DocumentRoot::Statement, "tests/roundtrip/eids.txt"),
        (DocumentRoot::Debate, "tests/roundtrip/hansard.txt"),
        (
            DocumentRoot::Judgment,
            "tests/roundtrip/judgment-attachments.txt",
        ),
        (DocumentRoot::Judgment, "tests/roundtrip/judgment.txt"),
        (
            DocumentRoot::Statement,
            "tests/roundtrip/nested_attachments.txt",
        ),
    ];

    for (root, path) in fixtures {
        let text = std::fs::read_to_string(repo_path(path)).unwrap_or_else(|err| {
            panic!("failed to read {path}: {err}");
        });
        parse(&text, root).unwrap_or_else(|err| {
            panic!("failed to parse {path} as {root:?}: {err}");
        });
    }
}
