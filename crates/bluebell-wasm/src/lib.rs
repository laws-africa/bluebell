//! WebAssembly bindings for the Bluebell Akoma Ntoso parser.
//!
//! This crate is a thin `wasm-bindgen` wrapper around `bluebell-core`. It
//! exposes a single string-in/string-out parse function so that browser and
//! Node.js JavaScript can turn Bluebell markup into Akoma Ntoso XML without
//! depending on any Rust-specific types.
//!
//! `bluebell-core` stays dependency-light and wasm-agnostic; all
//! `wasm-bindgen` glue lives here.

use bluebell_core::{
    parse_to_xml_document_or_fragment_with_eid_prefix_and_source, DocumentRoot, MetadataSource,
};
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
/// - `root`: the Python-compatible grammar root to parse with, such as
///   `"act"`, `"statement"`, `"hier_element_block"`, or `"attachment"`.
/// - `frbr_uri`: the FRBR work URI for the document, e.g.
///   `"/akn/za/act/2022/1"`.
/// - `eid_prefix`: optional `eId` prefix.
/// - `source`: optional metadata source object with `showAs`, `eid`, and
///   `href` string fields. `show_as` is also accepted.
///
/// Returns the generated XML as a string. Document roots return a full
/// `<akomaNtoso>` document; fragment roots return the fragment element. Throws
/// a JS exception (via `JsError`) if `root` is not recognised, if `frbr_uri` is
/// not a valid FRBR URI, or if `text` fails to parse as Bluebell markup.
#[wasm_bindgen(js_name = parseToXml)]
pub fn parse_to_xml(
    text: &str,
    root: &str,
    frbr_uri: &str,
    eid_prefix: Option<String>,
    source: Option<JsValue>,
) -> Result<String, JsError> {
    let root = document_root(root)?;
    let source = metadata_source(source)?;
    parse_to_xml_document_or_fragment_with_eid_prefix_and_source(
        text,
        root,
        frbr_uri,
        eid_prefix.as_deref().unwrap_or(""),
        &source,
    )
    .map_err(|err| JsError::new(&err.to_string()))
}

/// Returns the crate version, e.g. `"4.0.0"`. Useful for confirming which
/// build of the wasm package is loaded at runtime.
#[wasm_bindgen]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

fn document_root(root: &str) -> Result<DocumentRoot, JsError> {
    DocumentRoot::from_name(root)
        .ok_or_else(|| JsError::new(&format!("unsupported Bluebell root: {root}")))
}

fn metadata_source(source: Option<JsValue>) -> Result<MetadataSource, JsError> {
    let Some(source) = source else {
        return Ok(MetadataSource::default());
    };
    if source.is_null() || source.is_undefined() {
        return Ok(MetadataSource::default());
    }

    let show_as = js_string_property(&source, "showAs")?
        .or(js_string_property(&source, "show_as")?)
        .ok_or_else(|| JsError::new("source must include string showAs"))?;
    let eid = js_string_property(&source, "eid")?
        .ok_or_else(|| JsError::new("source must include string eid"))?;
    let href = js_string_property(&source, "href")?
        .ok_or_else(|| JsError::new("source must include string href"))?;

    Ok(MetadataSource::new(show_as, eid, href))
}

fn js_string_property(source: &JsValue, key: &str) -> Result<Option<String>, JsError> {
    let value = js_sys::Reflect::get(source, &JsValue::from_str(key))
        .map_err(|_| JsError::new("source must be an object"))?;
    if value.is_null() || value.is_undefined() {
        return Ok(None);
    }
    value
        .as_string()
        .map(Some)
        .ok_or_else(|| JsError::new(&format!("source.{key} must be a string")))
}
