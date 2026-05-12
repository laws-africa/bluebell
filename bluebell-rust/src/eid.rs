#[derive(Debug, Default)]
pub struct IdGenerator;

impl IdGenerator {
    pub fn clean_num(&self, num: &str) -> String {
        let chars: Vec<char> = num.chars().collect();
        let start = chars
            .iter()
            .position(|c| !is_stripped_edge_char(*c))
            .unwrap_or(chars.len());
        let end = chars
            .iter()
            .rposition(|c| !is_stripped_edge_char(*c))
            .map(|idx| idx + 1)
            .unwrap_or(start);

        let mut out = String::new();
        let mut previous_was_punctuation = false;
        for c in &chars[start..end] {
            if c.is_whitespace() {
                continue;
            }
            if is_punctuation(*c) {
                if !previous_was_punctuation {
                    out.push('-');
                    previous_was_punctuation = true;
                }
            } else {
                out.push(*c);
                previous_was_punctuation = false;
            }
        }
        out
    }
}

fn is_stripped_edge_char(c: char) -> bool {
    c.is_whitespace() || is_punctuation(c)
}

fn is_punctuation(c: char) -> bool {
    matches!(
        c,
        '\u{2000}'..='\u{206f}'
            | '\u{2e00}'..='\u{2e7f}'
            | '!'..='/'
            | ':'..='@'
            | '['..='`'
            | '{'..='~'
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn clean_num_matches_python_cases() {
        let ids = IdGenerator;
        assert_eq!("", ids.clean_num(""));
        assert_eq!("", ids.clean_num(" "));
        assert_eq!("", ids.clean_num("( )"));
        assert_eq!("123-4-5", ids.clean_num("(123.4-5)"));
        assert_eq!("312-32-7", ids.clean_num("312.32.7"));
        assert_eq!("312-32-7", ids.clean_num("312-32-7"));
        assert_eq!("312-32-7", ids.clean_num("312_32_7"));
        assert_eq!("6", ids.clean_num("(6)"));
        assert_eq!("16", ids.clean_num("[16]"));
        assert_eq!("i", ids.clean_num("(i)"));
        assert_eq!("i", ids.clean_num("[i]"));
        assert_eq!("2bis", ids.clean_num("(2bis)"));
        assert_eq!("1-2", ids.clean_num("\"1.2."));
        assert_eq!("1-2", ids.clean_num("1.2."));
        assert_eq!("2-3", ids.clean_num("“2.3"));
        assert_eq!("2-3", ids.clean_num("2,3"));
        assert_eq!("2-3-4", ids.clean_num("2,3, 4,"));
        assert_eq!("3abis", ids.clean_num("3a bis"));
        assert_eq!("3é", ids.clean_num("3é"));
        assert_eq!("3a-4-9", ids.clean_num(" -3a--4,9"));
        assert_eq!("א", ids.clean_num("(א)"));
        assert_eq!("三", ids.clean_num("(三)"));
    }
}
