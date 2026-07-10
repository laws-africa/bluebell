# Releasing Bluebell

One GitHub release publishes three artifacts, all carrying the same version:

| Artifact | Registry | Built from | Workflow job |
|---|---|---|---|
| `bluebell-akn` (pure Python) | PyPI | repo root | `pypi-publish` |
| `bluebell-akn-rs` (optional Rust extension) | PyPI | `crates/bluebell-python` | `rust-wheels` / `rust-sdist` / `rust-pypi-publish` |
| `@lawsafrica/bluebell-wasm` (WebAssembly) | npm | `crates/bluebell-wasm` | `npm-publish` |

The Rust crates are deliberately **not** published to crates.io
(`bluebell-wasm` is marked `publish = false`; the others are simply never
published).

## Release steps

1. Bump the version in **both** places, keeping them identical:
   - `bluebell/__init__.py` — `__version__`
   - root `Cargo.toml` — `[workspace.package].version`
     (all Rust crates inherit it, and `cargo build` will refresh `Cargo.lock`)

2. Run the full verification set (`poe test` runs all three):

   ```sh
   cargo test
   python -m unittest discover -s tests -t .
   cd crates/bluebell-wasm && wasm-pack test --node && cd ../..
   ```

   If the release includes parser changes, also run the large-document parity
   test:

   ```sh
   cargo test -p bluebell-core --test python_xml_parity income_tax_xml_roundtrip_parse_matches_python -- --ignored --nocapture
   ```

3. Commit, push, and create a GitHub release (with a `vX.Y.Z` tag). Creating
   the release triggers `.github/workflows/publish.yml`, which runs all the
   publish jobs above.

4. Confirm the results:
   - https://pypi.org/p/bluebell-akn
   - https://pypi.org/p/bluebell-akn-rs
   - https://www.npmjs.com/package/@lawsafrica/bluebell-wasm

## What the workflow publishes

- **`bluebell-akn`**: sdist + pure wheel via `python -m build`, uploaded with PyPI trusted publishing (GitHub
  environment `pypi`).
- **`bluebell-akn-rs`**: abi3 wheels for Linux (x86_64, aarch64 manylinux), macOS (universal2), and Windows (x64), built
  with maturin. abi3 means one wheel per platform covers CPython 3.12+, so new Python versions don't need new wheels. An
  sdist is also uploaded so other platforms can compile from source. Uploaded with PyPI trusted publishing (GitHub
  environment `pypi-rs`).
- **`@lawsafrica/bluebell-wasm`**: the wasm tests run first, then `wasm-pack build --target web` produces the package
  and `npm publish` uploads it with provenance. The `--target web` build is published because the docs site loads it
  directly in the browser with no bundler, and it also works when consumed through a bundler (see
  `crates/bluebell-wasm/README.md`).

## One-time setup

These must exist before the first automated release:

- **PyPI trusted publisher for `bluebell-akn-rs`**: on PyPI, add a trusted
  publisher for the `bluebell-akn-rs` project pointing at this repository,
  workflow `publish.yml`, environment `pypi-rs`. (The `bluebell-akn` publisher
  with environment `pypi` already exists.)
- **GitHub environments**: create the `pypi-rs` environment in the repo
  settings (alongside the existing `pypi` one).
- **npm**: the `lawsafrica` npm organisation must exist, and an automation
  token with publish rights must be stored as the `NPM_TOKEN` repository
  secret. The first publish of a scoped package must be public, which the
  workflow's `--access public` flag handles.

## Manual fallback

If the workflow is unavailable, each artifact can be published by hand:

```sh
# bluebell-akn
python -m build && twine upload dist/*

# bluebell-akn-rs (current platform only)
cd crates/bluebell-python && maturin build --release && maturin upload

# @lawsafrica/bluebell-wasm
cd crates/bluebell-wasm
wasm-pack test --node
wasm-pack build --release --target web --scope lawsafrica
npm publish pkg/ --access public
```

Note for macOS with a Homebrew rust installed: wasm builds need the rustup
toolchain first on `PATH` (see `crates/bluebell-wasm/README.md`).
