# bluebell-wasm

WebAssembly bindings for the Bluebell parser: parse Bluebell markup into Akoma
Ntoso XML from browser or Node.js JavaScript.

This crate is a thin `wasm-bindgen` wrapper around `bluebell-core`. It is not
published to crates.io; it exists only to produce the
`@lawsafrica/bluebell-wasm` npm package.

## API

```ts
// Parse Bluebell markup into an Akoma Ntoso XML string.
// root is one of: "act", "bill", "debate", "debateReport", "doc",
// "judgment", "statement".
// Throws an Error for an unknown root, an invalid FRBR URI, or a parse
// failure.
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

From this directory (`crates/bluebell-wasm`):

```sh
# for bundlers (webpack, vite, rollup) — the default
wasm-pack build --target bundler --scope lawsafrica

# for plain browser ES modules (no bundler)
wasm-pack build --target web --scope lawsafrica

# for Node.js
wasm-pack build --target nodejs --scope lawsafrica
```

Each build writes an npm package to `pkg/` (git-ignored) named
`@lawsafrica/bluebell-wasm`, including TypeScript definitions. The `--scope`
flag is what puts the package in the `@lawsafrica` npm scope; wasm-pack
derives the rest of the name from the crate name.

Optimised release builds are the default for `wasm-pack build`; add `--dev`
for faster, unoptimised builds while developing.

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

### With a bundler (webpack, vite, rollup)

```sh
npm install @lawsafrica/bluebell-wasm
```

```js
import { parseToXml, version } from "@lawsafrica/bluebell-wasm";

const xml = parseToXml(
  "SEC 1. - Heading\n\n  Some content.",
  "act",
  "/akn/za/act/2022/1",
);
```

Most modern bundlers handle the `.wasm` file automatically; vite needs
`vite-plugin-wasm` or a build from `--target web`.

### Plain browser, no bundler (`--target web` build)

```html
<script type="module">
  import init, { parseToXml } from "./pkg/bluebell_wasm.js";

  // init() fetches and instantiates the .wasm file; call it once before
  // using any other export.
  await init();

  const xml = parseToXml(
    "SEC 1. - Heading\n\n  Some content.",
    "act",
    "/akn/za/act/2022/1",
  );
  const doc = new DOMParser().parseFromString(xml, "text/xml");
</script>
```

### Node.js (`--target nodejs` build)

```js
const { parseToXml } = require("@lawsafrica/bluebell-wasm");
```

## Errors

`parseToXml` throws a JavaScript `Error` whose message describes the problem:
an unsupported root name, an invalid FRBR URI, or a Bluebell parse failure.
Rust panics (which should not happen) are reported to the browser console via
`console_error_panic_hook` instead of an opaque wasm trap.
