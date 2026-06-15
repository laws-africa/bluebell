# bluebell-rs

Rust implementation of the Bluebell parse path: Bluebell markup to Akoma Ntoso
XML.

The production goal is a fast parser that can be used from:

- a Rust CLI,
- the Python `bluebell` package through an optional native extension, and
- browser JavaScript through WebAssembly.

Unparse is not a production goal for the Rust core. The canonical unparse
implementation remains `bluebell/akn_text.xsl` in the Python Bluebell project.
The current Rust CLI has an XSLT-backed `unparse` command for testing,
benchmarking, and parity fixture generation, but production Rust/Python/WASM
packaging should not depend on XSLT or `xsltproc`.

## Current Status

- `pre_parse` is implemented and covered against Python examples.
- `bluebell/akn.peg` has been ported to a `pest` grammar.
- Rust parse XML output matches Python Bluebell canonical XML for:
  - discovered `tests/roundtrip/*.txt` fixtures,
  - discovered `tests/roundtrip/*.xml` fixtures after canonical XSLT unparse,
  - focused parser edge cases from the Python test suite, and
  - the ignored large `income-tax.xml` parity test.
- Full `<akomaNtoso>` XML generation is implemented for supported document
  roots and validates against `schemas/akomantoso30-lenient.xsd` in fixture
  tests.
- `bench-income-tax` benchmarks Rust parse and Python parse on the same
  XSLT-generated Bluebell input.

## Production Plan

The repository root is now a Cargo workspace:

```text
./
  Cargo.toml
  crates/
    bluebell-core/      # parse, preprocess, eId, XML generation
    bluebell-cli/       # bluebell-rs binary
    bluebell-python/    # optional Python extension module
    bluebell-wasm/      # browser/WebAssembly bindings
```

`bluebell-core` should stay parse-only and dependency-light. It should not
depend on `clap`, `pyo3`, `wasm-bindgen`, `libxml`, or XSLT tooling.

The Python package should expose a new function API, rather than changing
`AkomaNtosoParser.parse_to_xml()` to delegate internally:

```python
from bluebell import parse_to_xml

xml = parse_to_xml(text, root="act", frbr_uri="/akn/za/act/2022/1")
```

That function uses the Rust extension when installed and falls back to the
existing Python implementation when it is not available. Existing
`AkomaNtosoParser` users can keep working unchanged while callers migrate to the
function API deliberately.

## Likely Crates

Core:

- `pest`
- `pest_derive`
- `thiserror`

CLI:

- `bluebell-core`
- `clap`
- `anyhow`

Python extension:

- `bluebell-core`
- `pyo3`
- `maturin`

WASM:

- `bluebell-core`
- `wasm-bindgen`
- `serde-wasm-bindgen`
- `console_error_panic_hook`

Schema validation can remain test-only/native-only. It should not be required
for the Python extension or WASM package.

## Useful Commands

From the repository root:

```sh
cargo test
cargo run -p bluebell-rs -- parse act tests/roundtrip/act.txt
cargo run -p bluebell-rs -- to-xml act tests/roundtrip/act.txt
cargo run -p bluebell-rs -- to-akn-xml /akn/za/act/2022/1 act tests/roundtrip/act.txt
cargo run -p bluebell-rs -- bench-income-tax crates/bluebell-core/tests/fixtures/income-tax.xml
cd crates/bluebell-python && maturin develop
```

The large real-document parity test is ignored by default:

```sh
cargo test -p bluebell-core --test python_xml_parity income_tax_xml_roundtrip_parse_matches_python -- --ignored --nocapture
```

Run it before claiming broad parity milestones or before relying on benchmark
results.

## Outstanding Work

- Add release automation for the optional `bluebell-akn-rs` extension wheel.
- Add the WASM package exposing parse-to-XML for browser use.
- Keep the Rust workspace version in root `Cargo.toml` aligned with Python
  `bluebell.__version__` for releases.
- Add build and release automation for wheels, CLI binaries, and WASM artifacts.
