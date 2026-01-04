# Library Usage

Import `AkomaNtosoParser` when you need to integrate Bluebell into pipelines, web apps, or editors.

```python
from bluebell.parser import AkomaNtosoParser
from cobalt.uri import FrbrUri

frbr_uri = FrbrUri.parse("/akn/za/act/2009/1")
parser = AkomaNtosoParser(frbr_uri)
xml = parser.parse_to_xml(source_text, "act")
```

## Creating a Parser

```python
parser = AkomaNtosoParser(frbr_uri, eid_prefix="example")
```

- `frbr_uri` must be a `cobalt.FrbrUri` describing the work you are converting.
- `eid_prefix` is optional and lets you customise automatically generated `eId` values in the XML.

## Parsing Text

Use the convenience method to go straight to XML:

```python
xml_element = parser.parse_to_xml(text, root)
```

- `text`: Unicode string containing the document body.
- `root`: grammar root (`act`, `bill`, `judgment`, `debateReport`, `doc`, `statement`, etc.). Aliases like
  `debatereport` resolve automatically.

If you only need the intermediate parse tree (for custom transformations) call `parse(text, root)`. The CLI uses this
path before converting the tree to XML or JSON.

## Handling Errors

`parser.parse` and `parser.parse_to_xml` raise `bluebell.akn.ParseError` when the text violates the grammar. Catch it to
provide user-friendly feedback:

```python
from bluebell.akn import ParseError

try:
    xml = parser.parse_to_xml(text, "act")
except ParseError as exc:
    print(exc)  # includes the failure line and expected tokens
```

## Converting XML Back to Text

`AkomaNtosoParser.unparse(xml)` applies the built-in XSLT (`bluebell/akn_text.xsl`) to generate editable text from an
Akoma Ntoso document or fragment:

```python
with open("act.xml") as fh:
    text = parser.unparse(fh.read())
```

This is useful for round-tripping content through Bluebell—parse user-edited text to XML, process it, and later turn the
XML back into a text representation for further editing.
