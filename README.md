# Bluebell

Bluebell is a (fairly) generic Akoma Ntoso 3 parser, supporting all hierarchical elements and multiple document types.

Bluebell supports the following Akoma Ntoso (AKN) document types:

* act, bill (hierarchicalStructure)
* debateReport, doc, statement (openStructure)
* judgment (judgmentStructure)

Bluebell tries to walk the line between being expressive and supporting a range of AKN documents and structures,
while being simple to use and not requiring that authors have an in-depth knowledge of AKN.

Bluebell will always produce structurally valid Akoma Ntoso, no matter what input is given. It will never refuse to parse
malformed input. If it does, it's a bug.

## Usage

### From Python

Use the parser from Python as follows:

```python
from lxml import etree
import json
from bluebell.parser import AkomaNtosoParser

parser = AkomaNtosoParser()

# parse text to xml
xml = parser.parse_to_xml(text, 'act')
print(etree.tostring(xml, pretty_print=True, encoding='unicode'))

# parse text to intermediate dict format
tree = parser.parse(text, 'act')
print(json.dumps(tree.to_dict()))
```

### Commandline

In general, see `bluebell --help`

Parse an `act` in `act.txt` and output pretty XML: `bluebell /za/act/2020/1 act act.txt --pretty`

Use `--json` for intermediat json output.

## Grammar examples

The document type (act, judgment, etc.) determines the top-level elements of the text. Most other elements (hierarchical containers, tables, etc.)
are common to all document types.

Here's an example act:

    PREFACE
    
    This is in the preface
    
    PREAMBLE
    
    This is in the preamble
    
    BODY
    
    Introductory text in the body.
    
    SECTION 1.
    
      Text in section one, with some list items:
            
      SUBSECTION (a)
      
        cheese
        
      SUBSECTION (b)
      
        fish, both:
        
        SUBSECTION (i)
        
          fresh, and
          
        SUBSECTION (ii)
        
          tinned.
          
    PART 1 - The First Part
      SUBHEADING Very exciting
      
      SECTION 2.
      
        This is the second section inside part 1.
        
    SCHEDULE - First Schedule
      SUBHEADING With a subheading
      
      Text of the schedule

Key points:

* Keywords are in ALL CAPS, so that it's harder to mistake them for actual text
* Hierarchical elements all follow the same pattern, and support a number, heading and subheading, all of which are optional
* Content inside a hierarchical element is always nested
* Content inside a block element at the top level is usually nested, but Bluebell is forgiving and
  makes a best effort if you don't nest it.
* If Bluebell finds something it doesn't understand, it includes it as text and continues.

## Intermediate output structure

The parser produces a dict (Python) parse tree, which is later transformed into XML.
This intermediate step makes it easier to adapt the parser's output it AKN's sometimes finnicky requirements.

You can see an example of this structure by running `bluebell act act.txt --json`

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

* `element`: simple element
* `hier`: hierarchical element
* `block`: block element
* `content`: content element, such as `p` or `listIntroduction`
* `inline`: inline element, such as `b` or `ref`
* `text`: plain text
* `marker`: a marker element that cannot contain children, such as `img`

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
