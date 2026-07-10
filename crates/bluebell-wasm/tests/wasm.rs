//! wasm-bindgen-test suite for `bluebell-wasm`.
//!
//! Run with `wasm-pack test --node crates/bluebell-wasm` (or from inside the
//! crate directory: `wasm-pack test --node`).

use wasm_bindgen::{JsError, JsValue};
use wasm_bindgen_test::*;

const ACT_TEXT: &str = "PREAMBLE\n\n  some preamble text\n\nBODY\n\nSEC 1. - Heading\n\n  Some content.\n";
const FRBR_URI: &str = "/akn/za/act/2022/1";

#[wasm_bindgen_test]
fn parses_a_small_act() {
    let xml = bluebell_wasm::parse_to_xml(ACT_TEXT, "act", FRBR_URI)
        .expect("a minimal act should parse successfully");

    assert!(
        xml.starts_with("<akomaNtoso"),
        "expected output to start with <akomaNtoso, got: {xml}"
    );
    assert!(
        xml.contains(r#"<FRBRuri value="/akn/za/act/2022/1"/>"#),
        "expected output to contain the FRBR URI, got: {xml}"
    );
    assert!(
        xml.contains("<section eId=\"sec_1\">"),
        "expected output to contain the parsed section, got: {xml}"
    );
    assert!(
        xml.contains("<heading>Heading</heading>"),
        "expected output to contain the parsed heading, got: {xml}"
    );
}

#[wasm_bindgen_test]
fn rejects_an_unsupported_root() {
    let err = bluebell_wasm::parse_to_xml(ACT_TEXT, "not-a-real-root", FRBR_URI)
        .expect_err("an unrecognised root should raise an error");

    let message = js_error_message(err);
    assert!(
        message.contains("unsupported Bluebell root"),
        "expected an unsupported-root message, got: {message}"
    );
    assert!(
        message.contains("not-a-real-root"),
        "expected the message to name the bad root, got: {message}"
    );
}

// This exercises the other reachable error path in `parse_to_akn_xml`:
// `XmlError::FrbrUri`. The Bluebell grammar itself is intentionally lenient
// (mirroring the Python PEG grammar) and treats almost any text as valid
// fallback block content, so a `ParseError::Pest` failure is not reachable
// through realistic top-level document input; the invalid-FRBR-URI and
// unsupported-root cases above and below are the errors JS callers will
// actually encounter in practice.
#[wasm_bindgen_test]
fn rejects_an_invalid_frbr_uri() {
    let err = bluebell_wasm::parse_to_xml(ACT_TEXT, "act", "not a valid frbr uri")
        .expect_err("an invalid FRBR URI should raise an error");

    let message = js_error_message(err);
    assert!(
        message.contains("Invalid FRBR URI"),
        "expected an invalid-FRBR-URI message, got: {message}"
    );
}

#[wasm_bindgen_test]
fn reports_the_crate_version() {
    let version = bluebell_wasm::version();
    assert_eq!(version, env!("CARGO_PKG_VERSION"));
}

fn js_error_message(err: JsError) -> String {
    js_sys::Error::from(JsValue::from(err)).message().into()
}
