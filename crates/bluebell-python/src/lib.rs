use bluebell_core::{parse_to_akn_xml, DocumentRoot};
use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyBytes;

#[pyfunction]
#[pyo3(signature = (text, root, frbr_uri))]
fn parse_to_xml<'py>(
    py: Python<'py>,
    text: &str,
    root: &str,
    frbr_uri: &str,
) -> PyResult<Bound<'py, PyBytes>> {
    let root = document_root(root)?;
    let xml = parse_to_akn_xml(text, root, frbr_uri)
        .map_err(|err| PyRuntimeError::new_err(err.to_string()))?;
    Ok(PyBytes::new(py, xml.as_bytes()))
}

#[pymodule]
fn _bluebell_rs(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_to_xml, module)?)?;
    Ok(())
}

fn document_root(root: &str) -> PyResult<DocumentRoot> {
    match root {
        "act" => Ok(DocumentRoot::Act),
        "bill" => Ok(DocumentRoot::Bill),
        "debate" => Ok(DocumentRoot::Debate),
        "debateReport" | "debatereport" => Ok(DocumentRoot::DebateReport),
        "doc" => Ok(DocumentRoot::Doc),
        "judgment" => Ok(DocumentRoot::Judgment),
        "statement" => Ok(DocumentRoot::Statement),
        _ => Err(PyValueError::new_err(format!(
            "unsupported Bluebell root: {root}"
        ))),
    }
}
