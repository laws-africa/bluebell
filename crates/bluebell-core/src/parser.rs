use pest::Parser;
use pest_derive::Parser;
use thiserror::Error;

use crate::preprocess::pre_parse;

#[derive(Parser)]
#[grammar = "grammar.pest"]
pub(crate) struct BluebellParser;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum DocumentRoot {
    Act,
    Bill,
    Debate,
    DebateReport,
    Doc,
    Judgment,
    Statement,
}

#[derive(Debug, Eq, PartialEq)]
pub struct ParsedDocument {
    pub root: DocumentRoot,
    pub preprocessed_len: usize,
}

#[derive(Debug, Error)]
pub enum ParseError {
    #[error("{0}")]
    Pest(#[from] Box<pest::error::Error<Rule>>),
}

impl From<pest::error::Error<Rule>> for ParseError {
    fn from(value: pest::error::Error<Rule>) -> Self {
        Self::Pest(Box::new(value))
    }
}

pub fn parse(text: &str, root: DocumentRoot) -> Result<ParsedDocument, ParseError> {
    let preprocessed = pre_parse(text);
    parse_preprocessed(&preprocessed, root)
}

pub fn parse_preprocessed(text: &str, root: DocumentRoot) -> Result<ParsedDocument, ParseError> {
    parse_pairs_preprocessed(text, root)?;
    Ok(ParsedDocument {
        root,
        preprocessed_len: text.len(),
    })
}

pub(crate) fn parse_pairs_preprocessed(
    text: &str,
    root: DocumentRoot,
) -> Result<pest::iterators::Pairs<'_, Rule>, ParseError> {
    let rule = match root {
        DocumentRoot::Act => Rule::act_doc,
        DocumentRoot::Bill => Rule::bill_doc,
        DocumentRoot::Debate => Rule::debate_doc,
        DocumentRoot::DebateReport => Rule::debate_report_doc,
        DocumentRoot::Doc => Rule::doc_doc,
        DocumentRoot::Judgment => Rule::judgment_doc,
        DocumentRoot::Statement => Rule::statement_doc,
    };

    Ok(BluebellParser::parse(rule, text)?)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_simple_act() {
        let parsed = parse(
            "CHAPTER 1 - Heading\n\n  SECTION 1 - Short title\n\n    Some text.",
            DocumentRoot::Act,
        )
        .unwrap();
        assert_eq!(DocumentRoot::Act, parsed.root);
    }

    #[test]
    fn parses_simple_statement() {
        let parsed = parse("P Hello **there**", DocumentRoot::Statement).unwrap();
        assert_eq!(DocumentRoot::Statement, parsed.root);
    }
}
