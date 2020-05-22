# Generic AKN parser

Generic Akoma Ntoso 3 parser.

Supports the following Akoma Ntoso document types:

* act, bill (hierarchicalStructure)
* debateReport, doc, statement (openStructure)
* judment (judgmentStructure)

## Usage

### From Python

Use the parser from python as follows:

```python
from lxml import etree
import json
from bluebell.parser import parse, parse_tree_to_xml

tree = parse(text, 'act')

# transforms to json
print(json.dumps(tree))

# transforms to xml
xml = parse_tree_to_xml(tree)
print(etree.tostring(xml, pretty_print=True, encoding='unicode'))
```

### Commandline

In general, see `python parse.py --help`

Parse an `act` in `act.txt` and output pretty XML: `python parse.py act act.txt --pretty`

Use `--json` for intermediat json output.


## Development

1. Install customised Canopy as per below

### Canopy

Install customised canopy from github:

```
npm install git://github.com/laws-africa/canopy.git#lawsafrica
```

TODO: you may need to check it out elsewhere and compile it

### Compiling a grammar

```
npx canopy akn.peg --lang python
```

will produce akn.py

## Output structure

The parser produces a dict (Python) or object (Javascript) parse tree.

```
{
  type: 'type of the element, such as "hier", "block" etc.',
  name: 'name of the element, such as "body", "part" or "p",
  attribs: {
    key1: value1,
    key2: value2,
  },
  children: [],
}
```

Valid types:

* `hier`: hierarchical elemnt
* `block`: block element
* `inline`: inline content
* `text`: plain text
* `marker`: a marker element

### Children

Most elements can contain children. This is an array of elements.

These elements cannot contain children: `text`, `marker`.

### Text elements (`text`)

The content of a text element is in the `value` attribute.

An element that contains a single, pure-text child, can instead have a `text` attribute containing the equivalent of the `value`
attribute of the text element.

### Inline elements (`inline`)

Inline elements such as `b` and `term` may have other inline or text children,
or a single `text` attribute.

### Block elements (`block`)

Block elements cannot have `hier` children.

* `num`: number; inline element

### Hierarchical elements (`hier`)

* `heading`: heading element; a block element
* `subheading`: subheading element; a block element
* `num`: number; inline element

### Footnotes

Footnotes are treated specially because they are a subflow element that appears inline.
The are split into two parts: a reference to the footnote inline, and the footnote content:

    This text[++FN 1++] has a footnote.
    
    FOOTNOTE 1
    
      the content of the footnote

When converting the parse tree into XML, the footnote content must be inserted into
the point where it is referenced. This is done by post-processing the XML. A special non-AKN
`<displaced name="footnote" marker="1">...</displaced>` element is inserted in the
XML where the footnote content appears. The reference to the footnote inline is an
appropriate `authorialNote` element with a `displaced="footnote"` attribute.

Post-processing code then matches the `<displaced>` element with its `<authorialNote>`
using the name and marker, moves the children of the `displaced` into the `authorialNote`,
and removes the `displaced` element.

## Example

```javascript
{
  type: 'hier',
  name: 'chapter',
  num: '1',
  heading: 'Definitions and fundamental principles',
  children: [{
    type: 'hier',
    name: 'section',
    num: '1.',
    heading: 'Definitions',
    children: [{
      type: 'inline',
      name: 'p',
      text: 'In this By-law, unless the context indicates otherwise -',
    }, {
      type: 'inline',
      name: 'p',
      text: '"Air Quality" means:',
    }, {
      type: 'block',
      name: 'list',
      children: [{
        type: 'block',
        name: 'item',
        num: '(a)',
        children: [{
          type: 'inline',
          name: 'p',
          children: [{
            type: 'text',
            value: 'something with '
          }, {
            type: 'inline',
            name: 'b',
            text: 'bold',
          }, {
            type: 'text',
            value: ' in it.'
          }],
        }],
      }, {
        type: 'block',
        name: 'item',
        num: '(b)',
        children: [{
          type: 'inline',
          name: 'p',
          children: [{
            type: 'text',
            value: 'text with a',
          }, {
            type: 'marker',
            name: 'eol',
          }, {
            type: 'text',
            value: 'newline in it.',
          }],
        }],
      }],
    }],
  }],
}
```
