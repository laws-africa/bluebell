# Advanced Topics

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
