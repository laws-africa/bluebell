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
    let mut text = text.replace('\t', &" ".repeat(indent_size));
    text = text.trim().to_string();

    let lines: Vec<String> = text
        .lines()
        .map(|line| line.trim_end_matches(' ').to_string())
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

    if out.is_empty() {
        return out;
    }

    let skip = indent.len_utf8() + 1;
    let end = out.len().saturating_sub(skip);
    out[skip..end].to_string()
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
    fn inconsistent_nesting_matches_python() {
        assert_eq!(
            "one\n{\ntwo\nthree\n{\nfour\n}\n}\nfive\n",
            pre_parse_with_markers("\none\n    two\n  three\n      four\n five\n", '{', '}', 4)
        );
    }
}
