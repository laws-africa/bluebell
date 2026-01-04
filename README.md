# Bluebell

![Bluebell icon](https://laws.africa/img/icons/bluebell.png)

Bluebell is a (fairly) generic Akoma Ntoso 3 parser, supporting all hierarchical elements and multiple document types.

Bluebell supports these Akoma Ntoso (AKN) root document types:

* act, bill (hierarchicalStructure → `<Act>` / `<Bill>`)
* debateReport, doc, statement (openStructure → `<DebateReport>`, `<Doc>`, `<Statement>`)
* debate (debateStructure → `<Debate>`)
* judgment (judgmentStructure → `<Judgment>`)

Bluebell tries to walk the line between being expressive and supporting a range of AKN documents and structures,
while being simple to use and not requiring that authors have an in-depth knowledge of AKN.

Bluebell will always produce structurally valid Akoma Ntoso, no matter what input is given. It will never refuse to parse
malformed input. If it does, it's a bug.

Full documentation: https://laws.africa/bluebell/

## Usage

See https://laws.africa/bluebell/ for installation, CLI usage, and grammar guides.

### Quick start

Install from PyPI:

```
pip install bluebell-akn
```

From the commandline, parse an `act` in `act.txt` and output pretty XML:

```
bluebell /za/act/2020/1 act act.txt --pretty
```

From Python code, parse the same file:

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

## Development

1. We use a version of `canopy` from github, so clone it into the same directory as this directory: `git clone https://github.com/jcoglan/canopy.git`
2. Build canopy: `cd canopy; npm install; make; cd ..`
3. Build grammar changes with `make`, which runs our Makefile to compile the grammar
4. Run tests with: `python -m unittest`

## Releasing a new version

1. Update the version by changing the `__version__` variable in `bluebell/__init__.py`
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
