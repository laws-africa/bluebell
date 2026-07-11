# Bluebell

This repository contains the Python Bluebell library and a Rust workspace for a
faster parse path. Bluebell parses the Bluebell markup language into Akoma Ntoso
XML. The Python library is the reference implementation; the Rust
`bluebell-core` crate exists so the same parse operation can run faster while
producing substitutable XML.

The required compatibility contract is exact parsed XML parity with Python
Bluebell after XML canonicalization. Do not treat "valid Akoma Ntoso" as enough:
for parsed Bluebell text, Rust must produce the same XML tree that Python
Bluebell produces.

## Canonical Sources

- Python parser and grammar behavior: `bluebell/` and `bluebell/parser.py`.
- Python parser tests and fixtures: `tests/`.
- Canonical XML to Bluebell unparse: `bluebell/akn_text.xsl`.
- Rust parser and XML writer: `crates/bluebell-core/src/`.
- Rust CLI: `crates/bluebell-cli/`.
- Optional Python native extension: `crates/bluebell-python/`.
- Browser/Node WebAssembly bindings: `crates/bluebell-wasm/`.
- Rust parity coverage: `crates/bluebell-core/tests/python_xml_parity.rs`.
- Rust schema fixtures and validation:
  `crates/bluebell-core/tests/schema_fixtures.rs` and
  `crates/bluebell-core/schemas/`.

The Rust implementation must not grow an independent unparse model. If unparse
is supported, it should apply `bluebell/akn_text.xsl`; otherwise omit unparse
rather than maintaining a second source of truth.

## When Python Bluebell Changes

When the Python library gets a grammar change, parser bugfix, node override
change, or new language feature, update the Rust port by following this loop:

1. Read the Python change first.
   Identify whether it changes grammar recognition, node interpretation, XML
   construction, language-specific text, schema expectations, or only tests.

2. Add or update Python-side fixtures/tests if the behavior is not already
   covered.
   The Python implementation is the reference, so its expected output should be
   established before changing Rust.

3. Add the same scenario to `crates/bluebell-core/tests/python_xml_parity.rs`.
   Prefer the smallest focused Bluebell input that exposes the behavior, plus a
   fixture case when the change affects a realistic document shape.

4. Run the parity test and inspect the generated diff artifacts.
   On mismatch, `crates/bluebell-core/tests/python_xml_parity.rs` writes:

   - `/tmp/bluebell-rs-parity/<case>/input.txt`
   - `/tmp/bluebell-rs-parity/<case>/python.xml`
   - `/tmp/bluebell-rs-parity/<case>/rust.xml`

   Diff `python.xml` against `rust.xml` and change Rust to match Python unless
   the Python output is being intentionally changed by the current work.

5. Implement the Rust change in the smallest matching layer.
   Keep grammar recognition, parse tree interpretation, XML assembly, and schema
   validation responsibilities separate. Avoid broad rewrites unless the Python
   change requires them.

6. Re-run the full verification set before declaring the Rust port updated.

## Required Verification

From the repository root:

```sh
poe lint
cargo test
python -m unittest discover -s tests -t .
```

Run `poe lint` before declaring any Python change complete. This includes
supporting modules and generated-code-adjacent helpers, not only parser files.

CI (`.github/workflows/test.yml`) runs these suites through the poe tasks
defined in `pyproject.toml` (`poe test-py`, `poe test-rust`, `poe test-wasm`;
`poe test` runs all three, and `poe` lists every task), so the task
definitions are the source of truth for the exact invocations. The raw test
commands above are their equivalents for environments without `poe` installed;
run the configured linter separately in that case. If a task definition
changes, keep these instructions in sync.

When a change touches `crates/bluebell-wasm` or the core parse path it exposes,
also run the wasm binding tests (requires the `wasm32-unknown-unknown` rustup
target, `wasm-pack`, and Node):

```sh
cd crates/bluebell-wasm && wasm-pack test --node
```

To test the installed Python extension path locally, build it into the active
Python environment with:

```sh
cd crates/bluebell-python && maturin develop
```

The top-level Python functions should use `_bluebell_rs` when it is installed
and fall back to the pure Python parser when it is not. `parse_to_xml()`
returns an lxml element, `parse_to_xml_str()` returns `str`, and
`parse_to_xml_bytes()` returns UTF-8 `bytes`. `AkomaNtosoParser.parse_to_xml()`
remains the reference Python implementation and should not be changed to
delegate to Rust.

The extension distribution is intentionally separate from the main
`bluebell-akn` Python package. Its crate-local `pyproject.toml` builds
`bluebell-akn-rs`, which installs the `_bluebell_rs` module. Do not build a
root `bluebell-akn` wheel with maturin unless the packaging strategy is being
changed deliberately; a root maturin build can produce a wheel that has the
project name but omits the Python `bluebell` package.

For focused parity work:

```sh
cargo test -p bluebell-core --test python_xml_parity -- --nocapture
```

For large real-document parity, run the ignored `income-tax.xml` check
explicitly:

```sh
cargo test -p bluebell-core --test python_xml_parity income_tax_xml_roundtrip_parse_matches_python -- --ignored --nocapture
```

This test applies the canonical XSLT unparse to
`crates/bluebell-core/tests/fixtures/income-tax.xml`, parses the generated
Bluebell with both Python and Rust, then compares canonical XML. It is ignored
by default because it takes roughly one to two minutes. Run it when a change
touches grammar recognition, pre-processing, inline/text handling, hierarchy
construction, `eId` generation, attachments, XSLT unparse integration, or
anything else that could affect realistic act-sized documents. Also run it
before claiming a broad parity milestone or before using the Rust parser for
benchmarking.

The Python test command uses `-t .` so tests with package-relative imports are
loaded correctly.

## Versioning

The Python package version lives in `bluebell/__init__.py` as `__version__`.
The Rust workspace version lives in the repository root `Cargo.toml` under
`[workspace.package].version`; Rust crates inherit it with
`version.workspace = true`.

For releases, bump both values in the same change and keep them identical. Do
not make the installed Python package depend on reading `Cargo.toml`; wheels and
other distribution formats should be self-contained. The full release process
is documented in `RELEASING.md`.

## Exact XML Parity Notes

- Compare canonical XML trees, not pretty-printed strings.
- Attribute order and insignificant formatting should not matter.
- Element names, namespaces, text, tail text, attributes, generated `eId`s,
  default containers, and omitted empty grammar nodes do matter.
- A schema-valid Rust document can still be wrong if it differs from Python.
- If the Python behavior looks odd, preserve it in Rust unless the task is
  explicitly to change the reference behavior.

## Schema Validation

The Rust crate validates against the checked-in schemas in
`crates/bluebell-core/schemas/`, including the lenient Akoma Ntoso schema used
by the Rust tests. Keep schema files that the Rust crate needs in source
control. Do not rely on untracked root-level copies.

The Python library does not use these local Rust schema files directly; it uses
its own validation path through the Python dependencies.

## Practical Update Checklist

- Identify the Python behavior change.
- Add or update parity coverage.
- Make Rust output match Python canonical XML.
- Validate generated XML with the Rust schema tests.
- Run Rust and Python test suites.
- Leave unrelated local files and untracked fixtures alone unless the task
  explicitly asks to clean them up.
