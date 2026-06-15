# bluebell-rs

Experimental Rust implementation of the Bluebell parser.

Current status:

- `pre_parse` is implemented and covered against the Python examples.
- `bluebell/akn.peg` has been ported to a `pest` grammar.
- The CLI can parse Bluebell text for the supported document roots.
- The CLI can emit native Rust XML for the round-trip text fixtures, matching Python canonical XML output for those fixtures.
- The CLI can unparse XML by applying the canonical `bluebell/akn_text.xsl` stylesheet through `xsltproc`; there is no separate Rust-native unparse implementation.
- The CLI can emit full `<akomaNtoso>` XML with a minimal FRBR metadata block via `to-akn-xml`; fixture output validates against `schemas/akomantoso30-lenient.xsd`.
- `bench-income-tax` applies `bluebell/akn_text.xsl` through the Rust unparse wrapper, then benchmarks Rust preprocessing and pest parse.

Not implemented yet:

- Full typed model parity for all Bluebell constructs.
- Broader XML generation parity against the full Python test corpus, beyond the round-trip text fixtures.
- Removing the `xsltproc` process dependency if a suitable Rust/libxslt binding is chosen later.
- bluebell python should automatically use the rust parser when available
- library and cli versioning that matches the bluebell version
- clean build and release process and documentation

Useful commands:

```sh
cargo test
cargo run -- parse act ../tests/roundtrip/act.txt
cargo run -- to-xml act ../tests/roundtrip/act.txt
cargo run -- to-akn-xml /akn/za/act/2022/1 act ../tests/roundtrip/act.txt
cargo run -- unparse some-akn.xml
cargo run -- bench-income-tax tests/fixtures/income-tax.xml
```
