from bluebell.parser import pre_parse, parse_with_failure


def print_with_lines(text):
    for i, line in enumerate(text.split('\n')):
        i = i + 1
        print(f'{i:02}: {line}', file=sys.stderr)


class ParserSupport:
    def parse(self, text, root, block=False):
        text = pre_parse(text.lstrip(), indent='{', dedent='}')
        if not block:
            # strip (indent + newline) and (dedent + newline) markers around text
            text = text[2:-2]

        try:
            return parse_with_failure(text, root)
        except:
            print_with_lines(text)
            raise
