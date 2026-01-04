# Bluebell

<div style="display: flex; gap: 2em; align-items: center;">
  <img src="https://laws.africa/img/icons/bluebell.png" alt="Bluebell logo" style="height: 5em;">
  <img src="https://laws.africa/img/logo.png" alt="Laws.Africa logo" style="height: 5em;">
</div>

Bluebell is both a markup language format and a library for parsing that format into/from Akoma Ntoso XML. It is
created and maintaned by [Laws.Africa](https://laws.africa).


Bluebell converts the highly structured Bluebell text format into valid [Akoma Ntoso 3](https://www.akomantoso.org/)
XML. Its syntax works a bit like Markdown but is purpose-built for AKN: editors use keywords to indicate hierarchical
elements (chapters, parts, sections, subsections), block elements (lists, crossheadings) and inline elements
(bold, italics, references). The parser turns that input into valid Akoma Ntoso XML, even when the input is imperfect.

Bluebell can also unparse Akoma Ntoso XML back into Bluebell text, enabling round-tripping workflows for editing and
publishing.

## Highlights

- Supports Akoma Ntoso root types: acts and bills (hierarchicalStructure), judgments, debate reports/docs/statements
  (openStructure), and debates (debateStructure).
- Flexible, human-friendly plaintext syntax with minimal markup.
- Always produces valid Akoma Ntoso 3 XML, even from imperfect input.
- Provides a CLI for batch conversion and a programmatic API for pipelines, editors, and publishing workflows.

## Installation

Install from PyPI to get both the CLI and the Python API:

```bash
pip install bluebell-akn
```

After installing, call the `bluebell` command or import `AkomaNtosoParser` from `bluebell.parser`.

## Quick Start

### Command Line

1. Create a text file with Bluebell syntax (two spaces per indent, uppercase headings, etc.):
   ```text
   cat <<'EOF' > sample-act.txt
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
   EOF
   ```
2. Parse it:
   ```bash
   bluebell /akn/za/act/2009/1 act sample-act.txt --pretty > act.xml
   ```

`act.xml` now contains your act in Akoma Ntoso XML.

### Python

```python
from bluebell.parser import AkomaNtosoParser
from cobalt.uri import FrbrUri

frbr_uri = FrbrUri.parse("/akn/za/act/2009/1")
parser = AkomaNtosoParser(frbr_uri)
xml = parser.parse_to_xml("""
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
""")
print(xml)
```

## Where to Next?

- [Grammar](grammar.md) – study the Bluebell grammar and learn the keywords each document type expects.
- [Commandline Usage](cli.md) – run the parser on files and capture XML or JSON output.
- [Library Usage](library.md) – embed Bluebell in Python projects, including round-tripping text and XML.
- [Troubleshooting](troubleshooting.md) – interpret parser errors and fix common input issues.
