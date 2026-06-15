# Bluebell Rust Port

This crate is a Rust implementation of the Python Bluebell parser output path.
Bluebell parses the Bluebell markup language into Akoma Ntoso XML. The Python
library is the reference implementation; this Rust crate exists so the same
parse operation can run faster while producing substitutable XML.

The required compatibility contract is exact parsed XML parity with Python
Bluebell after XML canonicalization. Do not treat "valid Akoma Ntoso" as enough:
for parsed Bluebell text, Rust must produce the same XML tree that Python
Bluebell produces.

## Canonical Sources

- Python parser and grammar behavior: `../bluebell/` and `../bluebell/parser/`.
- Python parser tests and fixtures: `../tests/`.
- Canonical XML to Bluebell unparse: `../bluebell/akn_text.xsl`.
- Rust parser and XML writer: `src/`.
- Rust parity coverage: `tests/python_xml_parity.rs`.
- Rust schema fixtures and validation: `tests/schema_fixtures.rs` and
  `schemas/`.

The Rust implementation must not grow an independent unparse model. If unparse
is supported, it should apply `../bluebell/akn_text.xsl`; otherwise omit unparse
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

3. Add the same scenario to `tests/python_xml_parity.rs`.
   Prefer the smallest focused Bluebell input that exposes the behavior, plus a
   fixture case when the change affects a realistic document shape.

4. Run the parity test and inspect the generated diff artifacts.
   On mismatch, `tests/python_xml_parity.rs` writes:

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
cargo test --manifest-path bluebell-rust/Cargo.toml
python -m unittest discover -s tests -t .
```

For focused parity work:

```sh
cargo test --manifest-path bluebell-rust/Cargo.toml --test python_xml_parity -- --nocapture
```

For large real-document parity, run the ignored `income-tax.xml` check
explicitly:

```sh
cargo test --manifest-path bluebell-rust/Cargo.toml --test python_xml_parity income_tax_xml_roundtrip_parse_matches_python -- --ignored --nocapture
```

This test applies the canonical XSLT unparse to
`tests/fixtures/income-tax.xml`, parses the generated Bluebell with both Python
and Rust, then compares canonical XML. It is ignored by default because it takes
roughly one to two minutes. Run it when a change touches grammar recognition,
pre-processing, inline/text handling, hierarchy construction, `eId` generation,
attachments, XSLT unparse integration, or anything else that could affect
realistic act-sized documents. Also run it before claiming a broad parity
milestone or before using the Rust parser for benchmarking.

The Python test command uses `-t .` so tests with package-relative imports are
loaded correctly.

## Exact XML Parity Notes

- Compare canonical XML trees, not pretty-printed strings.
- Attribute order and insignificant formatting should not matter.
- Element names, namespaces, text, tail text, attributes, generated `eId`s,
  default containers, and omitted empty grammar nodes do matter.
- A schema-valid Rust document can still be wrong if it differs from Python.
- If the Python behavior looks odd, preserve it in Rust unless the task is
  explicitly to change the reference behavior.

## Schema Validation

The Rust crate validates against the checked-in schemas in `schemas/`, including
the lenient Akoma Ntoso schema used by the Rust tests. Keep schema files that the
Rust crate needs in source control. Do not rely on untracked root-level copies.

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
