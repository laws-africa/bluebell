# Commandline Usage

The `bluebell` command converts plaintext files into Akoma Ntoso XML (or an intermediate JSON tree) using the same
parser the library exposes.

## Basic Syntax

```bash
bluebell <frbr_uri> <root> <input-file> [--json] [--pretty]
```

- `<frbr_uri>`: FRBR URI describing the work, e.g. `/akn/za/act/2009/1`. It is parsed with `cobalt.FrbrUri` and is
  required for proper metadata in the output document.
- `<root>`: the document type to parse (`act`, `bill`, `judgment`, `debateReport`, `doc`, `statement`, etc.). Aliases such
  as `debatereport` are also recognised.
- `<input-file>`: path to the plaintext source you want to parse.
- `--json`: emit the intermediate parse tree as JSON instead of XML.
- `--pretty`: pretty-print the XML output (ignored when `--json` is set).

## Example

```bash
bluebell /akn/za/act/2009/1 act samples/act.txt --pretty > act.xml
```

The command reads `samples/act.txt`, parses it using the `act` grammar, and writes formatted Akoma Ntoso XML to STDOUT.
Redirect output to capture the XML.

## Error Behaviour

If parsing fails, the CLI prints the numbered source lines to STDERR before raising the error. Use this context to locate
and fix structural issues (indentation, missing headings, invalid keywords). Once the input matches the grammar, rerun
the command to produce XML.
