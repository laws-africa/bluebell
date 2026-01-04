# Troubleshooting

Use these checks when the parser raises errors or emits unexpected XML.

## ParseError Messages

`ParseError` includes the failing line number and the tokens the grammar expected next. Typical causes:

- **Unknown keyword**: a heading that does not match the grammar (typo, lowercase, unsupported synonym).
- **Indent mismatch**: nested content not indented with two spaces, or tabs sneaking into the text.
- **Unexpected EOF**: the file lacks a trailing newline or an unclosed structure.

Fix the offending line and rerun the CLI or your integration to verify the change.

## Verify the Root Type

Ensure the `root` argument matches the document you are parsing. Using `act` for a judgment (or vice versa) can lead to
missing elements or outright failures. Lowercase aliases such as `debatereport` are automatically capitalised, but other
misspellings are not.

## Inspect Intermediate Output

When debugging, the CLI can emit the parse tree as JSON:

```bash
bluebell /akn/za/act/2009/1 act sample.txt --json | jq .
```

This reveals how headings and paragraphs were recognised before converting to XML.

## Round-Trip to Text

If you have XML produced elsewhere and want to see how Bluebell would express it as text, use `AkomaNtosoParser.unparse`
to generate editable plaintext. Comparing that output to your source can highlight structural differences you need to
address.
