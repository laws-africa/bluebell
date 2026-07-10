# Bluebell

<img src="https://laws.africa/static/img/icons/bluebell.svg" alt="Bluebell icon" width="64" height="64">

Bluebell is a (fairly) generic Akoma Ntoso 3 parser, supporting all hierarchical elements and multiple document types.

Bluebell supports these Akoma Ntoso (AKN) root document types:

* act, bill (hierarchicalStructure → `<Act>` / `<Bill>`)
* debateReport, doc, statement (openStructure → `<DebateReport>`, `<Doc>`, `<Statement>`)
* debate (debateStructure → `<Debate>`)
* judgment (judgmentStructure → `<Judgment>`)

Bluebell tries to walk the line between being expressive and supporting a range of AKN documents and structures,
while being simple to use and not requiring that authors have an in-depth knowledge of AKN.

Bluebell will always produce structurally valid Akoma Ntoso, no matter what input is given. It will never refuse to parse
malformed input. If it does, it's a bug.

Full documentation: https://laws.africa/bluebell/

## Flavours

Bluebell is available in four forms, all producing the same Akoma Ntoso XML output. Choose based on your platform and use case:

| Flavour | Where | Use it when |
|---------|-------|------------|
| **Python** — `bluebell-akn` | PyPI | You need Python, want the full API including unparse, or prefer the reference implementation. |
| **Python with Rust** — `bluebell-akn-rs` | PyPI | You want the Python API but need the speed of Rust parsing. |
| **Browser / WebAssembly** — `@lawsafrica/bluebell-wasm` | npm | You need parsing in the browser or Node.js JavaScript. |
| **Rust** — `crates/` workspace | Source | You want a fast native CLI, or to embed the parser in a Rust program. |

### Python — `bluebell-akn`

The reference implementation. Supports both parsing Bluebell markup to XML and unparsing XML back to Bluebell text.

Install from PyPI:

```
pip install bluebell-akn
```

From the command line, parse an `act` in `act.txt` and output pretty XML:

```
bluebell /za/act/2020/1 act act.txt --pretty
```

From Python code:

```python
from bluebell import parse_to_xml, parse_to_xml_bytes, parse_to_xml_str

xml = parse_to_xml_str("""
CHAPTER 1 - Heading

  SECTION 1 - Short title

    Some introductory text.

  SECTION 2

    This section has two items:

    ITEMS
      ITEM (a)
        Here is item (a) text.

      ITEM (B)
        Here is item (b) text.
""", "act", "/akn/za/act/2009/1")
print(xml)
```

For unparse and more examples, see https://laws.africa/bluebell/.

### Python with Rust — `bluebell-akn-rs`

An optional native extension that accelerates the Python API using Rust.

Install both packages:

```
pip install bluebell-akn bluebell-akn-rs
```

No code changes needed — `parse_to_xml()` and friends automatically use the Rust parser when the extension is installed, and fall back to pure Python when it isn't. (`AkomaNtosoParser` always remains pure Python.)

The extension is in [crates/bluebell-python/](crates/bluebell-python/).

### Browser / WebAssembly — `@lawsafrica/bluebell-wasm`

The Rust parser compiled to WebAssembly. Load directly in the browser (no bundler) from a CDN, or install via npm.

Install from npm:

```
npm install @lawsafrica/bluebell-wasm
```

Minimal browser example (no bundler):

```html
<script type="module">
  import initWasm, { parseToXml } from "https://cdn.jsdelivr.net/npm/@lawsafrica/bluebell-wasm@4/bluebell_wasm.js";
  await initWasm();
  const xml = parseToXml("SEC 1. - Heading\n\n  Some content.", "act", "/akn/za/act/2022/1");
</script>
```

For details and the Node.js API, see [crates/bluebell-wasm/README.md](crates/bluebell-wasm/README.md). The live demo at https://laws.africa/bluebell/demo/ runs on this package.

### Rust — `crates/` workspace

Parse-only Rust implementation, available as both a library (`bluebell-core`) and a CLI (`bluebell-rs`). Not published to crates.io; build from source in the repository.

From the command line:

```
cargo run -p bluebell-rs -- to-akn-xml /akn/za/act/2022/1 act tests/roundtrip/act.txt
```

For the current status, parity testing, and full command reference, see [crates/README.md](crates/README.md).


## Development

1. We use a version of `canopy` from github, so clone it into the same directory as this directory: `git clone https://github.com/jcoglan/canopy.git`
2. Build canopy: `cd canopy; npm install; make; cd ..`
3. Build grammar changes with `make`, which runs our Makefile to compile the grammar
4. Install the dev tools with `pip install -e '.[dev]'`
5. Run all the test suites (Python, Rust, WASM) with: `poe test`

Common development commands are defined as [poe](https://poethepoet.natn.io/)
tasks in `pyproject.toml`; run `poe` with no arguments to list them. The
Python suite alone is just `python -m unittest`.

## Releasing a new version

See [RELEASING.md](RELEASING.md). In short: bump the version in both `bluebell/__init__.py` and the root `Cargo.toml`
`[workspace.package]` (they must match), run `poe test`, then create a GitHub release, which publishes `bluebell-akn`
and `bluebell-akn-rs` to PyPI and `@lawsafrica/bluebell-wasm` to npm.

# License

Copyright 2020 Laws.Africa.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
