# Grammar

Bluebell targets the Akoma Ntoso 3 grammar using its own well-structured plaintext format. Authors describe hierarchy
with indentation and headings (think of it as “Markdown for AKN”), and the parser turns that structure into Akoma Ntoso
XML. Understanding the document types, structural keywords, inline markup, and footnotes will help you prepare input
that round-trips cleanly.

## Document Types

Choose the root type that matches your document. The root determines which structural keywords are recognised and which
containers must appear. Inline markup is largely shared across types, but hierarchical and block elements vary.

| Root               | AKN structure            | Description                                                |
| ------------------ | ------------------------ | ---------------------------------------------------------- |
| `act`, `bill`      | `hierarchicalStructure`  | Statutes with chapters, parts, sections, etc.              |
| `judgment`         | `judgmentStructure`      | Judgments split into INTRODUCTION/BACKGROUND/etc.          |
| `debateReport`     | `openStructure`          | Hansard-style debate reports.                              |
| `doc`, `statement` | `openStructure`          | Open, lightly structured narrative documents.             |
| `debate`           | `debateStructure`        | Parliamentary debates with speech containers and groups.   |

All document types support attachments and inline markup. Acts/bills and judgments enforce stricter hierarchical rules
than the open/debate structures.

## Containers & Hierarchy

Bluebell expresses structure through indentation: every hierarchical or block element contains indented child content.
Use consistent two-space indentation for nested paragraphs, lists, tables, and speech blocks.

### Indentation Tips

1. Use two spaces per indent level (tabs are converted automatically, but consistent spaces make intent clearer).
2. Dedent only when closing the current container; do not skip levels.
3. Ensure the file ends with a newline so trailing containers close properly.

### Preface, Preamble, Body, Conclusions

These container keywords bracket introductory and closing material:

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

`BODY` marks where the main hierarchy (sections, parts, etc.) begins. `CONCLUSIONS` is optional but recommended for
closing remarks.

### Judgment Sections

Judgment documents use labelled sections:

```
INTRODUCTION
BACKGROUND
ARGUMENTS
REMEDIES
MOTIVATION
DECISION
```

The order is important.

### Hierarchical Elements

These keywords indicate hierarchical containers:

- `ALINEA`
- `ARTICLE`, `ART`
- `BOOK`
- `CHAPTER`, `CHAP`
- `CLAUSE`
- `DIVISION`
- `INDENT`
- `LEVEL`
- `LIST`
- `PARAGRAPH`, `PARA`
- `PART`
- `POINT`
- `PROVISO`
- `RULE`
- `SECTION`, `SEC`
- `SUBCHAPTER`, `SUBCHAP`
- `SUBCLAUSE`
- `SUBDIVISION`
- `SUBLIST`
- `SUBPARAGRAPH`, `SUBPARA`
- `SUBPART`
- `SUBRULE`
- `SUBSECTION`, `SUBSEC`
- `SUBTITLE`
- `TITLE`
- `TOME`
- `TRANSITIONAL`

All AKN hierarchical containers (CHAPTER, PART, SECTION, ARTICLE, etc.) follow the same syntax:

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

- `<hier>`: uppercase keyword such as `CHAPTER`, `SECTION`, `PARAGRAPH`, or a synonym.
- `<attribs>`: optional `{attr value|...}` block (see attributes section below).
- `<num>`: optional number (`1`, `1A`, `2(bis)`, etc.).
- `<heading>`: optional heading text after ` - `.
- `SUBHEADING` provides an optional subheading within the container.

#### Crossheading

Use `CROSSHEADING <heading>` between hierarchical elements when you need a heading but not a new container.

### Attachments

All document types may end with attachments (which can nest). Keywords such as `APPENDIX`, `SCHEDULE`, and `ANNEXURE`
are aliases for `ATTACHMENT`.

```
ATTACHMENT <heading>
  ...

ATTACHMENT <heading>
  SUBHEADING <subheading>
  ...
```

### Block Elements

Block elements indicate structure within sections and also rely on indentation.

#### Numbered Lists

```
ITEMS
  introductory text

  ITEM (a)
    ...

  ITEM (b) - Heading
    SUBHEADING Subheading
    ...
```

#### Bulleted Lists

```
BULLETS
  * Item 1
  * Item 2 spanning
    multiple lines
```

#### Block Quotes

```
QUOTE{startQuote "}
  Quoted material
```

#### Tables

```
TABLE.class-name
  TR
    TH{colspan 2}
      Heading cell
    TC
      Cell text
```

#### Longtitle

```
LONGTITLE The long title of an Act
```

## Inline Markup

Apart from a few shorthand formats (`**bold**`, `//italics//`, `__underline__`, `{{^superscript}}`, `{{_subscript}}`),
inline markup uses `{{ ... }}` blocks. Nest inline elements freely within paragraphs, headings, and list items.

### Abbreviations

```
{{abbr{title Akoma Ntoso} AKN}}
```

### Editorial Remarks

```
{{*remark content}}

A {{*remark may
span multiple lines.}}
```

### Emphasis

```
{{em{type strong} Important text}}
```

### Images

```
{{IMG /images/figure.png Figure description}}
```

### References (Links)

```
{{>https://example.com link text}}
```

### Terms

```
{{term{refersTo #definition-term} defined term}}
```

### Generic Inline Elements

```
{{inline{name custom} text}}
```

## Footnotes

Footnotes use two parts: an inline marker and a matching `FOOTNOTE` block at the same indent level.

```
This sentence includes the {{^{{FOOTNOTE *}}}} marker.

FOOTNOTE *
  This is the footnote content.
```

- The marker is `{{FOOTNOTE <symbol>}}`, often wrapped in superscript (`{{^...}}`).
- The block must appear immediately after the paragraph (no indentation change) and reuse the same symbol.
- Footnotes can contain block and inline markup just like body content.

## Attributes

Any element that accepts attributes can use `{name value|name2 value2}` immediately after the keyword. Class attributes can
be written with dot notation preceding the attribute block.

```
SECTION.class-one.class-two{status amended}
  ...
```

This is equivalent to `{class class-one class-two|status amended}`.

## Example Act Snippet

```
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
```

## Practical Tips

- Keywords are uppercase to avoid clashing with body text.
- When in doubt, inspect the generated XML to confirm the hierarchy and headings appear as expected.
- If Bluebell encounters unknown constructs, it keeps the text so you can edit and re-run the parser.
