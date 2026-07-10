use bluebell_core::{
    parse_to_xml_document_or_fragment_with_eid_prefix_and_source, DocumentRoot, MetadataSource,
};
use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyBytes, PyDict, PyList, PyTuple};

#[pyfunction]
#[pyo3(signature = (text, root, frbr_uri, eid_prefix = "", source = None))]
fn parse_to_xml<'py>(
    py: Python<'py>,
    text: &str,
    root: &str,
    frbr_uri: &str,
    eid_prefix: &str,
    source: Option<&Bound<'_, PyAny>>,
) -> PyResult<Bound<'py, PyBytes>> {
    let root = document_root(root)?;
    let source = metadata_source(source)?;
    let xml = parse_to_xml_document_or_fragment_with_eid_prefix_and_source(
        text, root, frbr_uri, eid_prefix, &source,
    )
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

fn metadata_source(source: Option<&Bound<'_, PyAny>>) -> PyResult<MetadataSource> {
    let Some(source) = source else {
        return Ok(MetadataSource::default());
    };
    if source.is_none() {
        return Ok(MetadataSource::default());
    }
    if let Ok(dict) = source.cast::<PyDict>() {
        return metadata_source_from_dict(dict);
    }
    if let Ok(tuple) = source.cast::<PyTuple>() {
        return metadata_source_from_tuple(tuple);
    }
    if let Ok(list) = source.cast::<PyList>() {
        return metadata_source_from_list(list);
    }
    Err(PyValueError::new_err(
        "source must be None, a dict, or a 3-item tuple/list",
    ))
}

fn metadata_source_from_dict(dict: &Bound<'_, PyDict>) -> PyResult<MetadataSource> {
    let show_as = dict_string_item(dict, "show_as")?
        .or(dict_string_item(dict, "showAs")?)
        .ok_or_else(|| PyValueError::new_err("source must include show_as or showAs"))?;
    let eid = dict_string_item(dict, "eid")?
        .ok_or_else(|| PyValueError::new_err("source must include eid"))?;
    let href = dict_string_item(dict, "href")?
        .ok_or_else(|| PyValueError::new_err("source must include href"))?;
    Ok(MetadataSource::new(show_as, eid, href))
}

fn dict_string_item(dict: &Bound<'_, PyDict>, key: &str) -> PyResult<Option<String>> {
    dict.get_item(key)?
        .map(|value| {
            value
                .extract::<String>()
                .map_err(|_| source_field_error(key))
        })
        .transpose()
}

fn metadata_source_from_tuple(tuple: &Bound<'_, PyTuple>) -> PyResult<MetadataSource> {
    if tuple.len() != 3 {
        return Err(PyValueError::new_err(
            "source tuple/list must contain show_as, eid, and href",
        ));
    }
    Ok(MetadataSource::new(
        py_string(&tuple.get_item(0)?, "source[0]")?,
        py_string(&tuple.get_item(1)?, "source[1]")?,
        py_string(&tuple.get_item(2)?, "source[2]")?,
    ))
}

fn metadata_source_from_list(list: &Bound<'_, PyList>) -> PyResult<MetadataSource> {
    if list.len() != 3 {
        return Err(PyValueError::new_err(
            "source tuple/list must contain show_as, eid, and href",
        ));
    }
    Ok(MetadataSource::new(
        py_string(&list.get_item(0)?, "source[0]")?,
        py_string(&list.get_item(1)?, "source[1]")?,
        py_string(&list.get_item(2)?, "source[2]")?,
    ))
}

fn py_string(value: &Bound<'_, PyAny>, field: &str) -> PyResult<String> {
    value
        .extract::<String>()
        .map_err(|_| source_field_error(field))
}

fn source_field_error(field: &str) -> PyErr {
    PyValueError::new_err(format!("{field} must be a string"))
}
