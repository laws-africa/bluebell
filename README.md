# Bluebell

![Bluebell icon](https://laws.africa/img/icons/bluebell.png)

Bluebell is a (fairly) generic Akoma Ntoso 3 parser, supporting all hierarchical elements and multiple document types.

Bluebell supports the following Akoma Ntoso (AKN) document types:

* act, bill (hierarchicalStructure)
* debateReport, doc, statement (openStructure)
* judgment (judgmentStructure)

Bluebell tries to walk the line between being expressive and supporting a range of AKN documents and structures,
while being simple to use and not requiring that authors have an in-depth knowledge of AKN.

Bluebell will always produce structurally valid Akoma Ntoso, no matter what input is given. It will never refuse to parse
malformed input. If it does, it's a bug.

## Getting started

1. Install from pypi: `pip install bluebell-akn`
2. Create an `AkomaNtosoParser` object with a valid FRBR URI, and parse your text:

```python
from bluebell.parser import AkomaNtosoParser
from cobalt.uri import FrbrUri
from lxml import etree

frbr_uri = FrbrUri.parse("/akn/za/act/2009/1")
parser = AkomaNtosoParser(frbr_uri)
xml = parser.parse_to_xml("""
CHAPTER 1
1. Section 1
Some text""", "act")
print(etree.tostring(xml, encoding='unicode'))
```

## Elements

### Preface, preamble and conclusions

These are semi-structured content blocks that are indicated with a keyword. Use the `BODY` keyword
to indicate where the preface and/or preamble end, and the body starts.

```
PREFACE
  ...
  
PREAMBLE
  ...
  
BODY
  ...
  
CONCLUSIONS
  ...
```

### Judgments

Judgments are broken into various sections which are indicated with a keyword.

```
INTRODUCTION
  ...
  
BACKGROUND
  ...
  
ARGUMENTS
  ...
  
REMEDIES
  ...
  
MOTIVATION
  ...
  
DECISION
  ...
```

### Hierarchical elements

All AKN hierarchical elements are supported.

**Format**

```
<hier><attribs>
  ...
  
<hier><attribs>
  SUBHEADING <subheading>
  ...
  
<hier><attribs> <num>
  ...
  
<hier><attribs> <num> - <heading>
  ...
  
<hier><attribs> - <heading>
  ...
```

* `<hier>` is a hierarchical element keyword or synonym, such as `CHAPTER`, `PART`, `SECTION`, `PARA` etc.
* `<attribs>` are attributes (optional)
* `<num>` is an optional number, eg `2` or `2a` or `2(bis)`
* `<heading>` is an optional heading
* `<subheading>` is an optional subheading

#### Synonyms

The following synonyms are supported for hierarchical elements:

* `ART` (`ARTICLE`)
* `CHAP` (`CHAPTER`)
* `PARA` (`PARAGRAPH`)
* `SEC` (`SECTION`)
* `SUBCHAP` (`SUBCHAPTER`)
* `SUBPARA` (`SUBPARAGRAPH`)
* `SUBSEC` (`SUBSECTION`)

##### Crossheading

A crossheading is a special heading element that can be used between hierarchical elements, without
creating a new element in the hierarchy.

```
CROSSHEADING <heading>
```

### Attachments

All document types support attachments, which can also be nested. Attachments must come at the end
of a document.

The keywords `APPENDIX`, `SCHEDULE` and `ANNEXURE` can also be used instead of `ATTACHMENT`.

```
ATTACHMENT <heading>
  ...
  
ATTACHMENT <heading>
  SUBHEADING <subheading>
  ...

```

* `<heading>` (optional) a heading for the attachment
* `<subheading>` a subheading heading for the attachment

### Block elements

#### Numbered list

General number lists that are not part of the hierarchy.

```
ITEMS
  <introductory text>
  
  ITEM
    SUBHEADING <subheading>
    ...
  
  ITEM <num>
    ...
    
  ITEM <num> - <heading>
    ...
    
  ITEM - <heading>
    ...
    
  <wrap-up text>

```

* `<introductory text>` is optional plain text before the first item
* `<num>` is an optional item number, such as `(a)` or `2bis`
* `<heading>` is an optional item heading
* `<subheading>` is an optional item subheading
* `<wrap-up text>` is optional plain text after the last item

#### Bulleted list

An un-numbered bulleted list that is not part of the hierarchy.

```
BULLETS
  * item 1
  * item 2 with text
    on multiple lines
```

#### Block quote

A block quotation. Use the `startQuote` to indicate the quote starting prefix, such as `"`

```
QUOTE<attribs>
  ...
  
QUOTE{startQuote "}
  ...
```

* `<attribs>` are attributes (optional)

#### Table

A table is made up of rows and cells.

```
TABLE<attribs>
  TR
    TH<attribs>
      A table heading cell
      
    TC
      A regular table cell
      
  TR
    TC{colspan 2}
      Cell in the second row that spans columns
```

* `<attribs>` are attributes (optional)

#### Longtitle

A special block element for the long title of a legislation document.

```
LONGTITLE <long title>
```

### Inline elements

General formatting elements:

```
**bold**
//italics//
__underline__
{{^superscript}}
{{_subscript}}
```

#### Abbreviations

Abbreviations include the full expansion of the abbreviation using the `title` attribute.

```
{{abbr{title Akoma Ntoso} AKN}}
```

#### Editorial remarks

Editorial remarks are for content not originally included by the document author. Editorial remarks can
contain other inline elements, such as links and formatting. Remarks may span multiple lines.

```
{{*remark content}}

A {{*remark may
span

multiple lines.}}
```

#### Emphasis

Emphasis is not always the same as italics and may be formatted differently.

```
{{em<attribs> text}}
```

* `<attribs>` are attributes (optional)

#### Footnotes

Footnotes are made up of two components: the footnote marker and the footnote content. The marker
is often in superscript `{{^...}}` but this not required.

The marker is indicated with `{{FOOTNOTE <symbol>}}`.

* `<symbol>` is the footnote symbol, such as `*` or `1`.

The footnote content comes after the line with the marker, at the same indent level. The symbols must match.

```
This sentence includes the {{^{{FOOTNOTE *}}}} marker.

FOOTNOTE *
  This is the footnote content.
```

#### Generic inline

A generic inline element must be identified with the `name` attribute.

```
{{inline{name <name>} text}}
```

* `<name>` the inline name (required)

#### Images

Embed an image as follows:

```
{{IMG <src> <description>}}
```

* `<src>` is the relative or absolute URL to the image file
* `<description>` is the alternate text that describes the image

#### References (links)

References are for internal and external links.

```
{{>https://example.com link text}}
```

#### Term

A defined term. This usually has the `refersTo` attribute.

```
{{term<attribs> term}}

{{term{refersTo #special-term} special term}}
```

* `<attribs>` are attributes (optional)

## Attributes

When `<attribs>` is supported, it is a list of attributes to be applied to the XML element.
Attributes are `<name> <value>` pairs. Multiple attributes are separate with `|`.

```
{attr value}

{attr1 value1|attr2 value2}
```

The `class` attribute can be added using dot-notation before the attributes:

```
.class1.class2{attr value}
```

This is equivalent to:

```
{class class1 class2|attr value}
```

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

1. We use a version of `canopy` from github, so clone it into the same directory as this directory: `git clone https://github.com/jcoglan/canopy.git`
2. Build canopy: `cd canopy; npm install; make; cd ..`
3. Build grammar changes with `make`, which runs our Makefile to compile the grammar
4. Run tests with: `python -m unittest`

## Releasing a new version

1. Update the version by changing the `__version__` variable in [bluebell/__init__.py](bluebell/__init__.py)
2. Commit your changes and push to the master branch on GitHub
3. Create a release in GitHub and it will automatically be pushed to PyPi

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
