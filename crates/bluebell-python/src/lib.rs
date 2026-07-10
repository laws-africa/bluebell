use bluebell_core::{parse_to_xml_document_or_fragment_with_eid_prefix, DocumentRoot};
use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyBytes;

#[pyfunction]
#[pyo3(signature = (text, root, frbr_uri, eid_prefix = ""))]
fn parse_to_xml<'py>(
    py: Python<'py>,
    text: &str,
    root: &str,
    frbr_uri: &str,
    eid_prefix: &str,
) -> PyResult<Bound<'py, PyBytes>> {
    let root = document_root(root)?;
    let xml = parse_to_xml_document_or_fragment_with_eid_prefix(text, root, frbr_uri, eid_prefix)
        .map_err(|err| PyRuntimeError::new_err(err.to_string()))?;
    Ok(PyBytes::new(py, xml.as_bytes()))
}

#[pymodule]
fn _bluebell_rs(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_to_xml, module)?)?;
    Ok(())
}

fn document_root(root: &str) -> PyResult<DocumentRoot> {
    DocumentRoot::from_name(root)
        .ok_or_else(|| PyValueError::new_err(format!("unsupported Bluebell root: {root}")))
}
