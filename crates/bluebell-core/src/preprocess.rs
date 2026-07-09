pub const INDENT: char = '\u{000E}';
pub const DEDENT: char = '\u{000F}';

const INDENT_SIZE: usize = 2;

pub fn pre_parse(text: &str) -> String {
    pre_parse_with_markers(text, INDENT, DEDENT, INDENT_SIZE)
}

pub fn pre_parse_with_markers(
    text: &str,
    indent: char,
    dedent: char,
    indent_size: usize,
) -> String {
    let text = text.replace('\t', &" ".repeat(indent_size));
    let text = text.trim_matches(is_python_whitespace);
    if text.is_empty() {
        return String::new();
    }

    // Split on newlines only: like Python, \r is not a line terminator and is
    // preserved in the text.
    let lines: Vec<&str> = text
        .split('\n')
        .map(|line| line.trim_end_matches(' '))
        .collect();

    let mut out = String::new();
    let mut stack: Vec<f64> = vec![-1.0];

    for line in lines {
        if line.is_empty() {
            out.push('\n');
            continue;
        }

        let leading_spaces = line.chars().take_while(|c| *c == ' ').count();
        let rest = &line[leading_spaces..];
        let level = leading_spaces as f64 / indent_size as f64;
        let current = *stack.last().expect("indentation stack is never empty");

        if (level - current).abs() < f64::EPSILON {
            out.push_str(rest);
            out.push('\n');
        } else if level > current {
            stack.push(level);
            out.push(indent);
            out.push('\n');
            out.push_str(rest);
            out.push('\n');
        } else {
            stack.pop();
            if level > *stack.last().expect("indentation stack is never empty") {
                stack.push(level);
                out.push_str(rest);
                out.push('\n');
            } else {
                loop {
                    out.push(dedent);
                    out.push('\n');
                    if level >= *stack.last().expect("indentation stack is never empty") {
                        break;
                    }
                    stack.pop();
                }
                out.push_str(rest);
                out.push('\n');
            }
        }
    }

    for _ in 1..stack.len() {
        out.push(dedent);
        out.push('\n');
    }

    let skip = indent.len_utf8() + 1;
    let end = out.len().saturating_sub(skip);
    out[skip..end].to_string()
}

/// Whitespace as Python's str.strip() sees it: Unicode whitespace plus the
/// C0 separator control characters \x1c-\x1f, which Rust's char::is_whitespace
/// does not include.
fn is_python_whitespace(c: char) -> bool {
    c.is_whitespace() || ('\u{1c}'..='\u{1f}').contains(&c)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_inputs_match_python() {
        assert_eq!("", pre_parse(""));
        assert_eq!("", pre_parse(" "));
        assert_eq!("", pre_parse("\n"));
        assert_eq!("", pre_parse("  \n  "));
    }

    #[test]
    fn tabs_and_leading_whitespace_match_python() {
        assert_eq!("a  b\n", pre_parse("\ta\tb"));
        assert_eq!(
            "b\nanother line\n",
            pre_parse("  \n  \t\n  \n\t\n b\nanother line\n")
        );
    }

    #[test]
    fn custom_markers_match_python_examples() {
        assert_eq!("hello\n", pre_parse_with_markers("  hello", '{', '}', 2));
        assert_eq!(
            "one\n{\ntwo\nthree\n}\n",
            pre_parse_with_markers("\none\n  two\n three\n  \n\n", '{', '}', 2)
        );
    }

    #[test]
    fn carriage_returns_are_preserved_like_python() {
        // \r is not a line terminator: it survives mid-line and mid-document,
        // and is only stripped at the document edges (Python str.strip).
        assert_eq!("BODY\r\ntext\n", pre_parse("BODY\r\ntext\r\n"));
        assert_eq!("a\rb\n", pre_parse("a\rb"));
        // trailing spaces are only stripped before a newline, not before a \r
        assert_eq!("a \r\nb\n", pre_parse("a \r\nb"));
    }

    #[test]
    fn control_char_whitespace_matches_python() {
        // \x0b, \x0c and \x1c-\x1f count as whitespace at the document edges
        // (\x1c-\x1f are whitespace to Python's str.strip but not to
        // char::is_whitespace)
        assert_eq!("a\n", pre_parse("\u{1c}a\u{1f}"));
        assert_eq!("a\n", pre_parse("\u{0b}a\u{0c}"));
        // but they are preserved inside the document
        assert_eq!("a\u{1c}b\n", pre_parse("a\u{1c}b"));
    }

    #[test]
    fn unicode_whitespace_matches_python() {
        // unicode whitespace is stripped at the document edges
        assert_eq!("a\n", pre_parse("\u{a0}a\u{a0}"));
        assert_eq!("a\n", pre_parse("\u{85}a"));
        // but is not treated as indentation and is preserved in text
        assert_eq!("a\n\u{a0} b\n", pre_parse("a\n\u{a0} b"));
        assert_eq!("a\n\u{2003}b\n", pre_parse("a\n\u{2003}b"));
    }

    #[test]
    fn inconsistent_nesting_matches_python() {
        assert_eq!(
            "one\n{\ntwo\nthree\n{\nfour\n}\n}\nfive\n",
            pre_parse_with_markers("\none\n    two\n  three\n      four\n five\n", '{', '}', 4)
        );
    }
}
