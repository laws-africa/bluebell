# bluebell rust

Rust implementation of the Bluebell parse path: Bluebell markup to Akoma Ntoso XML.

This is a fast parser that can be used from:

- the Python `bluebell` package through an optional native extension,
- browser JavaScript through WebAssembly, and
- a development-only rust CLI.

Unparse is not a production goal for the Rust core. The canonical unparse implementation remains `bluebell/akn_text.xsl`
in the Python Bluebell project. The current Rust CLI has an XSLT-backed `unparse` command for testing, benchmarking, and
parity fixture generation, but production Rust/Python/WASM packaging should not depend on XSLT or `xsltproc`.

## Workspace Layout

The repository root is a Cargo workspace:

```text
./
  Cargo.toml
  crates/
    bluebell-core/      # parse, preprocess, eId, XML generation
    bluebell-cli/       # bluebell-rs binary
    bluebell-python/    # optional Python extension module
    bluebell-wasm/      # browser/WebAssembly bindings
```

The binding crates are thin wrappers around `bluebell-core`:

* the Python extension uses `pyo3` (built with `maturin`),
* the WASM crate uses `wasm-bindgen` and `console_error_panic_hook` with a string-in/string-out API
  (no `serde` layer needed), and
* the CLI uses `clap`/`anyhow`.

Each crate's `Cargo.toml` is the source of truth for its dependencies.

`bluebell-core` stays parse-only and dependency-light. It must not depend on `clap`, `pyo3`, `wasm-bindgen`,
`libxml`, or XSLT tooling; schema validation (`libxml`) is a dev-dependency used only by native tests, and is not
required by the Python extension or the WASM package.

The Python package exposes a function API that delegates to the Rust extension when installed, and falls back to the
existing Python implementation when it is not available. The function API is:

```python
from bluebell import parse_to_xml, parse_to_xml_bytes, parse_to_xml_str

xml = parse_to_xml(text, root="act", frbr_uri="/akn/za/act/2022/1")
xml_text = parse_to_xml_str(text, root="act", frbr_uri="/akn/za/act/2022/1")
xml_bytes = parse_to_xml_bytes(text, root="act", frbr_uri="/akn/za/act/2022/1")
```

## Useful Commands

Most of these are wrapped as poe tasks in the root `pyproject.toml` (`poe`
lists them; `poe test` runs the Python, Rust, and WASM suites). The raw
commands, from the repository root:

```sh
cargo test
cargo run -p bluebell-rs -- parse act tests/roundtrip/act.txt
cargo run -p bluebell-rs -- to-xml act tests/roundtrip/act.txt
cargo run -p bluebell-rs -- to-akn-xml /akn/za/act/2022/1 act tests/roundtrip/act.txt
cargo run -p bluebell-rs -- bench-income-tax crates/bluebell-core/tests/fixtures/income-tax.xml
cd crates/bluebell-python && maturin develop
cd crates/bluebell-wasm && wasm-pack test --node
cd crates/bluebell-wasm && wasm-pack build --target web --scope lawsafrica
```

The large real-document parity test is ignored by default:

```sh
cargo test -p bluebell-core --test python_xml_parity income_tax_xml_roundtrip_parse_matches_python -- --ignored --nocapture
```

Run it before claiming broad parity milestones or before relying on benchmark results.

## Releasing

Wheels (`bluebell-akn`, `bluebell-akn-rs`) and the npm WASM package are published automatically when a GitHub release is
created; see `RELEASING.md` at the repository root. Keep the Rust workspace version in root `Cargo.toml` aligned with
Python `bluebell.__version__` for releases.

## Outstanding Work

- Add build and release automation for CLI binaries.
