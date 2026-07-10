//! WebAssembly bindings for the Bluebell Akoma Ntoso parser.
//!
//! This crate is a thin `wasm-bindgen` wrapper around `bluebell-core`. It
//! exposes a single string-in/string-out parse function so that browser and
//! Node.js JavaScript can turn Bluebell markup into Akoma Ntoso XML without
//! depending on any Rust-specific types.
//!
//! `bluebell-core` stays dependency-light and wasm-agnostic; all
//! `wasm-bindgen` glue lives here.

use bluebell_core::{parse_to_akn_xml_with_eid_prefix, DocumentRoot};
use wasm_bindgen::prelude::*;

/// Runs once when the wasm module is instantiated. Forwards Rust panics to
/// the JS console instead of the default opaque "unreachable" trap, which
/// makes debugging panics from JS much easier.
#[wasm_bindgen(start)]
pub fn init() {
    console_error_panic_hook::set_once();
}

/// Parses Bluebell markup into Akoma Ntoso XML.
///
/// - `text`: the Bluebell markup source.
/// - `root`: the document root, one of `"act"`, `"bill"`, `"debate"`,
///   `"debateReport"` (or `"debatereport"`), `"doc"`, `"judgment"`, or
///   `"statement"`.
/// - `frbr_uri`: the FRBR work URI for the document, e.g.
///   `"/akn/za/act/2022/1"`.
/// - `eid_prefix`: optional `eId` prefix.
///
/// Returns the generated `<akomaNtoso>` XML document as a string. Throws a
/// JS exception (via `JsError`) if `root` is not recognised, if `frbr_uri`
/// is not a valid FRBR URI, or if `text` fails to parse as Bluebell markup.
#[wasm_bindgen(js_name = parseToXml)]
pub fn parse_to_xml(
    text: &str,
    root: &str,
    frbr_uri: &str,
    eid_prefix: Option<String>,
) -> Result<String, JsError> {
    let root = document_root(root)?;
    parse_to_akn_xml_with_eid_prefix(text, root, frbr_uri, eid_prefix.as_deref().unwrap_or(""))
        .map_err(|err| JsError::new(&err.to_string()))
}

/// Returns the crate version, e.g. `"4.0.0"`. Useful for confirming which
/// build of the wasm package is loaded at runtime.
#[wasm_bindgen]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

fn document_root(root: &str) -> Result<DocumentRoot, JsError> {
    match root {
        "act" => Ok(DocumentRoot::Act),
        "bill" => Ok(DocumentRoot::Bill),
        "debate" => Ok(DocumentRoot::Debate),
        "debateReport" | "debatereport" => Ok(DocumentRoot::DebateReport),
        "doc" => Ok(DocumentRoot::Doc),
        "judgment" => Ok(DocumentRoot::Judgment),
        "statement" => Ok(DocumentRoot::Statement),
        _ => Err(JsError::new(&format!("unsupported Bluebell root: {root}"))),
    }
}
