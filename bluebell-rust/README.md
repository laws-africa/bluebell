# bluebell-rs

Experimental Rust implementation of the Bluebell parser.

Current status:

- `pre_parse` is implemented and covered against the Python examples.
- `bluebell/akn.peg` has been ported to a `pest` grammar.
- The CLI can parse Bluebell text for the supported document roots.
- The CLI can emit native Rust XML for a growing core subset: empty roots, paragraphs, hierarchy, block/bullet lists, tables, common inline elements, refs/images, block attributes, and generated eIds.
- The CLI can unparse the current native Rust XML subset back to Bluebell text.
- The CLI can emit full `<akomaNtoso>` XML with a minimal FRBR metadata block via `to-akn-xml`; simple output validates against `akomantoso30.xsd`.
- `bench-income-tax` uses the existing Python/XSLT unparse path as an oracle, then benchmarks the Rust preprocessing and pest parse.

Not implemented yet:

- Full typed model parity for all Bluebell constructs.
- Full XML generation parity for attachment metadata, complex nested attachment/debate cases, and remaining post-processing details.
- Full native Rust unparse parity with `bluebell/akn_text.xsl`.

Useful commands:

```sh
cargo test
cargo run -- parse act ../tests/roundtrip/act.txt
cargo run -- to-xml act ../tests/roundtrip/act.txt
cargo run -- to-akn-xml /akn/za/act/2022/1 act ../tests/roundtrip/act.txt
cargo run -- unparse some-akn.xml
cargo run -- bench-income-tax ../income-tax.xml
```
