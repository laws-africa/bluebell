from unittest import TestCase
import random
import string

from bluebell.akn import ParseError
from .support import ParserSupport


class FuzzingTestCase(TestCase, ParserSupport):
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
    CHAPTER
    CONCLUSIONS
    CROSSHEADING
    DECISION
    HEADING
    INTRODUCTION
    MOTIVATION
    PART
    PREAMBLE
    PREFACE
    REMEDIES
    SCHEDULE
    SECTION
    SUBHEADING
    SUBSECTION
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

        keywords = self.keywords + [''] * 3

        for length in random.sample(range(self.max_snippets), self.num_strings):
            lines = ''.join([
                random.choice(self.separators) +
                random.choice(keywords) + ' ' +
                ' '.join(random.sample(words, random.randint(1, 10)))
                for x in range(length)
            ])
            if lines.strip():
                yield lines

    def test_fuzzing(self):
        for text in self.make_strings():
            for root in self.roots:
                try:
                    self.parse(text, root, block=True)
                except ParseError as e:
                    self.fail(f"Failed to parse root {root} with text: {text}")
