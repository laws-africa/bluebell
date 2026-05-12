# bluebell-rs

Experimental Rust implementation of the Bluebell parser.

Current status:

- `pre_parse` is implemented and covered against the Python examples.
- `bluebell/akn.peg` has been ported to a `pest` grammar.
- The CLI can parse Bluebell text for the supported document roots.
- The CLI can emit native Rust XML for a growing core subset: empty roots, paragraphs, hierarchy, block/bullet lists, tables, common inline elements, refs/images, block attributes, and generated eIds.
- `bench-income-tax` uses the existing Python/XSLT unparse path as an oracle, then benchmarks the Rust preprocessing and pest parse.

Not implemented yet:

- Full typed model parity for all Bluebell constructs.
- Full XML generation parity for attachments, debate structures, matched displaced footnotes, metadata insertion, and post-processing.
- Native Rust unparse from Akoma Ntoso XML back to Bluebell text.

Useful commands:

```sh
cargo test
cargo run -- parse act ../tests/roundtrip/act.txt
cargo run -- to-xml act ../tests/roundtrip/act.txt
cargo run -- bench-income-tax ../income-tax.xml
```
