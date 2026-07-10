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
    Arguments,
    Attachment,
    Attachments,
    Background,
    Bill,
    BlockElement,
    BlockElements,
    BlockList,
    BlockListItem,
    BlockQuote,
    Blocks,
    Body,
    BulletList,
    BulletListItem,
    Conclusions,
    Crossheading,
    Debate,
    DebateBody,
    DebateReport,
    Decision,
    Doc,
    HierBlockElement,
    HierBlockIndent,
    HierElement,
    HierElementBlock,
    HierIndent,
    Introduction,
    Judgment,
    Line,
    Longtitle,
    MainBody,
    Motivation,
    P,
    Preamble,
    Preface,
    Remedies,
    SpeechBlock,
    SpeechContainer,
    SpeechContainerIndent,
    SpeechGroup,
    SpeechHierBlockElement,
    Statement,
    Table,
    TableCell,
    TableRow,
}

impl DocumentRoot {
    pub fn from_name(root: &str) -> Option<Self> {
        match root {
            "act" => Some(Self::Act),
            "arguments" => Some(Self::Arguments),
            "attachment" => Some(Self::Attachment),
            "attachments" => Some(Self::Attachments),
            "background" => Some(Self::Background),
            "bill" => Some(Self::Bill),
            "block_element" => Some(Self::BlockElement),
            "block_elements" => Some(Self::BlockElements),
            "block_list" => Some(Self::BlockList),
            "block_list_item" => Some(Self::BlockListItem),
            "block_quote" => Some(Self::BlockQuote),
            "blocks" => Some(Self::Blocks),
            "body" => Some(Self::Body),
            "bullet_list" => Some(Self::BulletList),
            "bullet_list_item" => Some(Self::BulletListItem),
            "conclusions" => Some(Self::Conclusions),
            "crossheading" => Some(Self::Crossheading),
            "debate" => Some(Self::Debate),
            "debateBody" => Some(Self::DebateBody),
            "debateReport" | "debatereport" => Some(Self::DebateReport),
            "decision" => Some(Self::Decision),
            "doc" => Some(Self::Doc),
            "hier_block_element" => Some(Self::HierBlockElement),
            "hier_block_indent" => Some(Self::HierBlockIndent),
            "hier_element" => Some(Self::HierElement),
            "hier_element_block" => Some(Self::HierElementBlock),
            "hier_indent" => Some(Self::HierIndent),
            "introduction" => Some(Self::Introduction),
            "judgment" => Some(Self::Judgment),
            "line" => Some(Self::Line),
            "longtitle" => Some(Self::Longtitle),
            "mainBody" => Some(Self::MainBody),
            "motivation" => Some(Self::Motivation),
            "p" => Some(Self::P),
            "preamble" => Some(Self::Preamble),
            "preface" => Some(Self::Preface),
            "remedies" => Some(Self::Remedies),
            "speech_block" => Some(Self::SpeechBlock),
            "speech_container" => Some(Self::SpeechContainer),
            "speech_container_indent" => Some(Self::SpeechContainerIndent),
            "speech_group" => Some(Self::SpeechGroup),
            "speech_hier_block_element" => Some(Self::SpeechHierBlockElement),
            "statement" => Some(Self::Statement),
            "table" => Some(Self::Table),
            "table_cell" => Some(Self::TableCell),
            "table_row" => Some(Self::TableRow),
            _ => None,
        }
    }

    pub fn is_document(self) -> bool {
        matches!(
            self,
            Self::Act
                | Self::Bill
                | Self::Debate
                | Self::DebateReport
                | Self::Doc
                | Self::Judgment
                | Self::Statement
        )
    }
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
        DocumentRoot::Arguments => Rule::arguments_root,
        DocumentRoot::Attachment => Rule::attachment_root,
        DocumentRoot::Attachments => Rule::attachments_root,
        DocumentRoot::Background => Rule::background_root,
        DocumentRoot::Bill => Rule::bill_doc,
        DocumentRoot::BlockElement => Rule::block_element_root,
        DocumentRoot::BlockElements => Rule::block_elements_root,
        DocumentRoot::BlockList => Rule::block_list_root,
        DocumentRoot::BlockListItem => Rule::block_list_item_root,
        DocumentRoot::BlockQuote => Rule::block_quote_root,
        DocumentRoot::Blocks => Rule::blocks_root,
        DocumentRoot::Body => Rule::body_root,
        DocumentRoot::BulletList => Rule::bullet_list_root,
        DocumentRoot::BulletListItem => Rule::bullet_list_item_root,
        DocumentRoot::Conclusions => Rule::conclusions_root,
        DocumentRoot::Crossheading => Rule::crossheading_root,
        DocumentRoot::Debate => Rule::debate_doc,
        DocumentRoot::DebateBody => Rule::debate_body_root,
        DocumentRoot::DebateReport => Rule::debate_report_doc,
        DocumentRoot::Decision => Rule::decision_root,
        DocumentRoot::Doc => Rule::doc_doc,
        DocumentRoot::HierBlockElement => Rule::hier_block_element_root,
        DocumentRoot::HierBlockIndent => Rule::hier_block_indent_root,
        DocumentRoot::HierElement => Rule::hier_element_root,
        DocumentRoot::HierElementBlock => Rule::hier_element_block_root,
        DocumentRoot::HierIndent => Rule::hier_indent_root,
        DocumentRoot::Introduction => Rule::introduction_root,
        DocumentRoot::Judgment => Rule::judgment_doc,
        DocumentRoot::Line => Rule::line_root,
        DocumentRoot::Longtitle => Rule::longtitle_root,
        DocumentRoot::MainBody => Rule::main_body_root,
        DocumentRoot::Motivation => Rule::motivation_root,
        DocumentRoot::P => Rule::p_root,
        DocumentRoot::Preamble => Rule::preamble_root,
        DocumentRoot::Preface => Rule::preface_root,
        DocumentRoot::Remedies => Rule::remedies_root,
        DocumentRoot::SpeechBlock => Rule::speech_block_root,
        DocumentRoot::SpeechContainer => Rule::speech_container_root,
        DocumentRoot::SpeechContainerIndent => Rule::speech_container_indent_root,
        DocumentRoot::SpeechGroup => Rule::speech_group_root,
        DocumentRoot::SpeechHierBlockElement => Rule::speech_hier_block_element_root,
        DocumentRoot::Statement => Rule::statement_doc,
        DocumentRoot::Table => Rule::table_root,
        DocumentRoot::TableCell => Rule::table_cell_root,
        DocumentRoot::TableRow => Rule::table_row_root,
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
