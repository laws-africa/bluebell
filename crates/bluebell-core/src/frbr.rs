//! FRBR URI parsing and serialization, ported from cobalt's `FrbrUri` so that
//! generated `meta` elements match Python Bluebell exactly.

use regex::Regex;
use std::sync::OnceLock;

// Port of cobalt's FRBR_URI_RE.
const FRBR_URI_PATTERN: &str = concat!(
    r"^(/(?P<prefix>akn))?",                               // optional 'akn' prefix
    r"/(?P<country>[a-z]{2})",                             // country
    r"(-(?P<locality>[^/]+))?",                            // locality code
    r"/(?P<doctype>[^/]+)",                                // document type
    r"(/(?P<subtype>[^0-9][^/]*))?",                       // subtype, cannot start with a number
    r"(/(?P<actor>[^0-9][^/]*))?",                         // actor, cannot start with a number
    r"/(?P<date>[0-9]{4}(-[0-9]{2}(-[0-9]{2})?)?)",        // date
    r"/(?P<number>[^/]+)",                                 // number
    r"(/(?P<language>[a-z]{3})(?P<expression_date>[@:][^/]*)?)?", // expression language and date
    r"(/(!(?P<work_component>[^~.]+?))?(~(?P<portion>[^.]+))?)?", // component and portion
    r"(\.(?P<format>[a-z0-9]+))?",                         // format
    r"$",
);

fn frbr_uri_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(FRBR_URI_PATTERN).expect("invalid FRBR URI regex"))
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct FrbrUri {
    pub prefix: Option<String>,
    pub country: String,
    pub locality: Option<String>,
    pub doctype: String,
    pub subtype: Option<String>,
    pub actor: Option<String>,
    pub date: String,
    pub number: String,
    pub work_component: Option<String>,
    pub language: String,
    pub expression_date: Option<String>,
    pub portion: Option<String>,
    pub format: Option<String>,
}

#[derive(Debug, thiserror::Error)]
#[error("Invalid FRBR URI: {0}")]
pub struct InvalidFrbrUri(pub String);

impl FrbrUri {
    pub fn parse(uri: &str) -> Result<Self, InvalidFrbrUri> {
        let uri = uri.trim_end_matches('/');
        let captures = frbr_uri_re()
            .captures(uri)
            .ok_or_else(|| InvalidFrbrUri(uri.to_string()))?;
        let get = |name: &str| captures.name(name).map(|m| m.as_str().to_string());
        Ok(Self {
            prefix: get("prefix"),
            country: get("country").expect("country is a required group"),
            locality: get("locality"),
            doctype: get("doctype").expect("doctype is a required group"),
            subtype: get("subtype"),
            actor: get("actor"),
            date: get("date").expect("date is a required group"),
            number: get("number").expect("number is a required group"),
            work_component: get("work_component"),
            language: get("language").unwrap_or_else(|| "eng".to_string()),
            expression_date: get("expression_date"),
            portion: get("portion"),
            format: get("format"),
        })
    }

    /// Full place code, including both country and locality (if present).
    pub fn place(&self) -> String {
        match &self.locality {
            Some(locality) => format!("{}-{}", self.country, locality),
            None => self.country.clone(),
        }
    }

    /// String form of the work URI.
    pub fn work_uri(&self, work_component: bool) -> String {
        let mut parts: Vec<&str> = vec![""];
        if let Some(prefix) = &self.prefix {
            parts.push(prefix);
        }
        let place = self.place();
        parts.push(&place);
        parts.push(&self.doctype);
        if let Some(subtype) = &self.subtype {
            parts.push(subtype);
            if let Some(actor) = &self.actor {
                parts.push(actor);
            }
        }
        parts.push(&self.date);
        parts.push(&self.number);
        let component;
        if work_component {
            if let Some(wc) = &self.work_component {
                component = format!("!{wc}");
                parts.push(&component);
            }
        }
        parts.join("/")
    }

    /// String form of the expression URI.
    pub fn expression_uri(&self, work_component: bool) -> String {
        let mut uri = format!("{}/{}", self.work_uri(false), self.language);
        if let Some(expression_date) = &self.expression_date {
            uri.push_str(expression_date);
        }
        let mut slashed = false;
        if work_component {
            if let Some(wc) = &self.work_component {
                slashed = true;
                uri.push_str("/!");
                uri.push_str(wc);
            }
        }
        if let Some(portion) = &self.portion {
            if !slashed {
                uri.push('/');
            }
            uri.push('~');
            uri.push_str(portion);
        }
        uri
    }

    /// String form of the manifestation URI.
    pub fn manifestation_uri(&self, work_component: bool) -> String {
        let mut uri = self.expression_uri(work_component);
        if let Some(format) = &self.format {
            uri.push('.');
            uri.push_str(format);
        }
        uri
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Expected values generated with cobalt's FrbrUri.
    #[test]
    fn parses_and_serializes_like_cobalt() {
        let cases: Vec<(&str, [&str; 6], [&str; 4])> = vec![
            (
                "/akn/za/act/2022/1",
                [
                    "/akn/za/act/2022/1",
                    "/akn/za/act/2022/1",
                    "/akn/za/act/2022/1/eng",
                    "/akn/za/act/2022/1/eng",
                    "/akn/za/act/2022/1/eng",
                    "/akn/za/act/2022/1/eng",
                ],
                ["za", "2022", "1", "eng"],
            ),
            (
                "/akn/za/act/gn/2022/r1234",
                [
                    "/akn/za/act/gn/2022/r1234",
                    "/akn/za/act/gn/2022/r1234",
                    "/akn/za/act/gn/2022/r1234/eng",
                    "/akn/za/act/gn/2022/r1234/eng",
                    "/akn/za/act/gn/2022/r1234/eng",
                    "/akn/za/act/gn/2022/r1234/eng",
                ],
                ["za", "2022", "r1234", "eng"],
            ),
            (
                "/akn/aa-au/statement/deliberation/mpc/2011/24",
                [
                    "/akn/aa-au/statement/deliberation/mpc/2011/24",
                    "/akn/aa-au/statement/deliberation/mpc/2011/24",
                    "/akn/aa-au/statement/deliberation/mpc/2011/24/eng",
                    "/akn/aa-au/statement/deliberation/mpc/2011/24/eng",
                    "/akn/aa-au/statement/deliberation/mpc/2011/24/eng",
                    "/akn/aa-au/statement/deliberation/mpc/2011/24/eng",
                ],
                ["aa-au", "2011", "24", "eng"],
            ),
            (
                "/akn/za/act/2022/1/eng@2023-01-01",
                [
                    "/akn/za/act/2022/1",
                    "/akn/za/act/2022/1",
                    "/akn/za/act/2022/1/eng@2023-01-01",
                    "/akn/za/act/2022/1/eng@2023-01-01",
                    "/akn/za/act/2022/1/eng@2023-01-01",
                    "/akn/za/act/2022/1/eng@2023-01-01",
                ],
                ["za", "2022", "1", "eng"],
            ),
            (
                "/akn/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/!main~part_1.xml",
                [
                    "/akn/za-jhb/act/by-law/2003/public-health/!main",
                    "/akn/za-jhb/act/by-law/2003/public-health",
                    "/akn/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/!main~part_1",
                    "/akn/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/~part_1",
                    "/akn/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/!main~part_1.xml",
                    "/akn/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/~part_1.xml",
                ],
                ["za-jhb", "2003", "public-health", "eng"],
            ),
            (
                "/akn/za/act/2022-03-01/12",
                [
                    "/akn/za/act/2022-03-01/12",
                    "/akn/za/act/2022-03-01/12",
                    "/akn/za/act/2022-03-01/12/eng",
                    "/akn/za/act/2022-03-01/12/eng",
                    "/akn/za/act/2022-03-01/12/eng",
                    "/akn/za/act/2022-03-01/12/eng",
                ],
                ["za", "2022-03-01", "12", "eng"],
            ),
            (
                "/za/act/2022/1",
                [
                    "/za/act/2022/1",
                    "/za/act/2022/1",
                    "/za/act/2022/1/eng",
                    "/za/act/2022/1/eng",
                    "/za/act/2022/1/eng",
                    "/za/act/2022/1/eng",
                ],
                ["za", "2022", "1", "eng"],
            ),
            (
                "/akn/za/act/2022/1/",
                [
                    "/akn/za/act/2022/1",
                    "/akn/za/act/2022/1",
                    "/akn/za/act/2022/1/eng",
                    "/akn/za/act/2022/1/eng",
                    "/akn/za/act/2022/1/eng",
                    "/akn/za/act/2022/1/eng",
                ],
                ["za", "2022", "1", "eng"],
            ),
        ];

        for (uri, [work_t, work_f, expr_t, expr_f, manif_t, manif_f], [place, date, number, language]) in
            cases
        {
            let parsed = FrbrUri::parse(uri).unwrap_or_else(|err| panic!("{uri}: {err}"));
            assert_eq!(work_t, parsed.work_uri(true), "{uri} work_uri(true)");
            assert_eq!(work_f, parsed.work_uri(false), "{uri} work_uri(false)");
            assert_eq!(expr_t, parsed.expression_uri(true), "{uri} expression_uri(true)");
            assert_eq!(expr_f, parsed.expression_uri(false), "{uri} expression_uri(false)");
            assert_eq!(manif_t, parsed.manifestation_uri(true), "{uri} manifestation_uri(true)");
            assert_eq!(manif_f, parsed.manifestation_uri(false), "{uri} manifestation_uri(false)");
            assert_eq!(place, parsed.place(), "{uri} place");
            assert_eq!(date, parsed.date, "{uri} date");
            assert_eq!(number, parsed.number, "{uri} number");
            assert_eq!(language, parsed.language, "{uri} language");
        }
    }

    #[test]
    fn rejects_invalid_uris_like_cobalt() {
        for uri in [
            "/akn/z/act/2022/1",
            "akn/za/act/2022/1",
            "/akn/za/act/22/1",
            "/akn/za/act/2022",
        ] {
            assert!(FrbrUri::parse(uri).is_err(), "{uri} should be invalid");
        }
    }
}
