pub mod eid;
pub mod frbr;
pub mod parser;
pub mod preprocess;
pub mod xml;

pub use eid::IdGenerator;
pub use parser::{parse, parse_preprocessed, DocumentRoot, ParseError};
pub use preprocess::{pre_parse, DEDENT, INDENT};
pub use xml::{
    parse_preprocessed_to_akn_xml, parse_preprocessed_to_akn_xml_with_eid_prefix,
    parse_preprocessed_to_xml, parse_preprocessed_to_xml_document_or_fragment,
    parse_preprocessed_to_xml_document_or_fragment_with_eid_prefix,
    parse_preprocessed_to_xml_with_eid_prefix, parse_to_akn_xml, parse_to_akn_xml_with_eid_prefix,
    parse_to_xml, parse_to_xml_document_or_fragment,
    parse_to_xml_document_or_fragment_with_eid_prefix, parse_to_xml_with_eid_prefix, XmlElement,
    XmlNode,
};
