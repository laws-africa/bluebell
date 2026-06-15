This directory contains schema files used by the Rust test suite.

The Python Bluebell package validates through `cobalt.schemas.assert_validates(..., strict=False)`
and does not load these local files directly.

`akomantoso30-lenient.xsd` is a local test schema for Rust-generated Akoma Ntoso XML. It imports
`xml.xsd`, so both files must stay together.
