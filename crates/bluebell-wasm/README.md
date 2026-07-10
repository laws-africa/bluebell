# bluebell-wasm

WebAssembly bindings for the Bluebell parser: parse Bluebell markup into Akoma
Ntoso XML from browser or Node.js JavaScript.

This crate is a thin `wasm-bindgen` wrapper around `bluebell-core`. It is not
published to crates.io; it exists only to produce the
`@lawsafrica/bluebell-wasm` npm package.

## API

```ts
// Parse Bluebell markup into an Akoma Ntoso XML string.
// root is one of: "act", "bill", "debate", "debateReport", "doc", "judgment", "statement".
// Throws an Error for an unknown root, an invalid FRBR URI, or a parse failure.
function parseToXml(text: string, root: string, frbr_uri: string): string;

// The crate/package version, e.g. "4.0.0".
function version(): string;
```

The XML is returned as a string. In the browser, feed it to `DOMParser` if you
need a document tree:

```js
const doc = new DOMParser().parseFromString(xml, "text/xml");
```

## Prerequisites

- A rustup-managed Rust toolchain with the wasm target:
  `rustup target add wasm32-unknown-unknown`
- [wasm-pack](https://rustwasm.github.io/wasm-pack/): `cargo install wasm-pack`
  or `brew install wasm-pack`
- Node.js (to run the tests)

Note: a Homebrew-installed Rust (`brew install rust`) does not ship the
wasm32 standard library and cannot build this crate. If both are installed,
make sure the rustup toolchain's `cargo` is first on your `PATH` when running
the commands below, e.g.
`export PATH="$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin:$PATH"`.

## Building

The published npm package is built with `--target web` (via the `build-wasm`
poe task, see below), because the docs site loads it directly in the browser
with no bundler, and a `--target web` build also works when consumed through
a bundler. The other targets remain available for local builds aimed at a
specific consumer:

From this directory (`crates/bluebell-wasm`):

```sh
# published target: plain browser ES modules, also works with bundlers
wasm-pack build --target web --scope lawsafrica

# for bundlers (webpack, vite, rollup) only
wasm-pack build --target bundler --scope lawsafrica

# for Node.js
wasm-pack build --target nodejs --scope lawsafrica
```

Each build writes an npm package to `pkg/` (git-ignored) named
`@lawsafrica/bluebell-wasm`, including TypeScript definitions. The `--scope`
flag is what puts the package in the `@lawsafrica` npm scope; wasm-pack
derives the rest of the name from the crate name.

Optimised release builds are the default for `wasm-pack build`; add `--dev`
for faster, unoptimised builds while developing.

From the repository root, `poe build-wasm` runs the same `--target web` build
into `crates/bluebell-wasm/pkg` (see `pyproject.toml`).

## Testing

Tests live in `tests/wasm.rs` and use `wasm-bindgen-test`, which compiles the
tests to wasm and executes them in a real JavaScript runtime — this is the
standard way to test wasm-bindgen crates. From this directory:

```sh
# run in Node (no browser needed)
wasm-pack test --node

# or in a headless browser
wasm-pack test --headless --chrome
```

A plain `cargo test -p bluebell-wasm` from the repo root compiles the crate
natively but runs no wasm tests; the real coverage of the parse logic itself
lives in `bluebell-core`'s test suite, so these tests only need to cover the
JS binding surface (root mapping, error conversion, string round-tripping).

## Using the package

The published `@lawsafrica/bluebell-wasm` package is a `--target web` build,
so its **default export** is the loader function that fetches and
instantiates the `.wasm` file; call it (and await it) once before using any
other export.

Note: the module also has a separate *named* export called `init` — that's
the crate's own `#[wasm_bindgen(start)]` function (it forwards Rust panics
to the console) and runs automatically on load, so you never need to call it
yourself. When you `import init, { parseToXml } from "..."`, the local name
`init` refers to the *default* export (the loader), not this named one — the
same name, two different functions. Naming the local default-import binding
something like `initWasm` avoids the ambiguity if it's confusing.

### Plain browser, no bundler (the published package)

```html
<script type="module">
  import initWasm, { parseToXml } from "https://cdn.jsdelivr.net/npm/@lawsafrica/bluebell-wasm@4/bluebell_wasm.js";

  // initWasm() fetches and instantiates the .wasm file; call it once before
  // using any other export.
  await initWasm();

  const xml = parseToXml(
    "SEC 1. - Heading\n\n  Some content.",
    "act",
    "/akn/za/act/2022/1",
  );
  const doc = new DOMParser().parseFromString(xml, "text/xml");
</script>
```

The same code works after `npm install @lawsafrica/bluebell-wasm`, importing
from `@lawsafrica/bluebell-wasm/bluebell_wasm.js` instead of the CDN URL —
most modern bundlers accept a `--target web` build directly, awaiting the
default export the same way.

### With a bundler that needs a bundler-target package

If a bundler cannot consume the `--target web` output directly (some webpack
configurations, for example), build a `--target bundler` package locally
instead of using the published one — see "Building" above — and consume it
without an explicit loader call:

```js
import { parseToXml, version } from "@lawsafrica/bluebell-wasm";

const xml = parseToXml(
  "SEC 1. - Heading\n\n  Some content.",
  "act",
  "/akn/za/act/2022/1",
);
```

### Node.js (`--target nodejs` build)

Build locally with `--target nodejs` (the published package does not target
Node):

```js
const { parseToXml } = require("@lawsafrica/bluebell-wasm");
```

## Errors

`parseToXml` throws a JavaScript `Error` whose message describes the problem:
an unsupported root name, an invalid FRBR URI, or a Bluebell parse failure.
Rust panics (which should not happen) are reported to the browser console via
`console_error_panic_hook` instead of an opaque wasm trap.

## Testing the demo locally

The MkDocs live demo (`docs/demo.md` / `docs/js/demo.js`) loads
`@lawsafrica/bluebell-wasm` from jsDelivr. Since the package isn't published
yet (and even once it is, you'll want to test local changes before a
release), the demo also supports loading a locally built copy: visit the
demo page with a `?local-wasm` query parameter and it loads the module from
`docs/js/bluebell-wasm/` (git-ignored) instead of the CDN.

```sh
poe build-wasm   # builds --target web into crates/bluebell-wasm/pkg
cp -r crates/bluebell-wasm/pkg docs/js/bluebell-wasm
mkdocs serve     # then open http://127.0.0.1:8000/bluebell/demo/?local-wasm
```
