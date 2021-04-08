from unittest import TestCase
import random
import string

from bluebell.akn import ParseError
from tests.support import ParserSupport


class FuzzingTestCase(ParserSupport, TestCase):
    """ This test case creates random strings, using various grammar components, and ensures that
    each grammar still matches.

    This helps us to ensure that we handle any input provided, and still create valid AKN.
    """
    roots = ['hierarchical_structure', 'judgment', 'open_structure']

    keywords = """
    ANNEXURE
    APPENDIX
    ARGUMENTS
    ATTACHMENT
    BACKGROUND
    BODY
    BULLETS
    *
    CHAPTER
    CONCLUSIONS
    CROSSHEADING
    DECISION
    HEADING
    INTRODUCTION
    ITEMS
    ITEM
    MOTIVATION
    PART
    PREAMBLE
    PREFACE
    REMEDIES
    SCHEDULE
    SECTION
    SUBHEADING
    SUBSECTION
    TABLE
    TR
    TH
    TC
    {{
    {{^
    {{_
    {{IMG
    {{>
    }}
    \\
    """.strip().split()

    separators = [
        '\n  ',
        '\n    ',
        '\n',
        ' ',
    ]

    min_snippets = 1
    max_snippets = 100
    word_min = 1
    word_max = 7

    # total number of strings to generate
    num_strings = 50

    def make_strings(self):
        # random words
        words = [
            ''.join(random.choices(string.ascii_lowercase, k=random.randint(self.word_min, self.word_max)))
            for x in range(500)
        ]

        # when choosing keywords, also have a bit of a chance of choosing none
        keywords = self.keywords + [''] * 3

        # generate lines of random length
        for length in random.sample(range(self.max_snippets), self.num_strings):
            lines = ''.join([
                # newline / indent
                random.choice(self.separators) +
                # optional keyword
                random.choice(keywords) + ' ' +
                # some text
                ' '.join(random.sample(words, random.randint(0, 10)))
                for x in range(length)
            ])
            if lines.strip():
                yield lines

    def test_fuzzing(self):
        for text in self.make_strings():
            for root in self.roots:
                try:
                    self.parse(text, root)
                except ParseError as e:
                    self.fail(f"Failed to parse root {root} with text: {text}")
