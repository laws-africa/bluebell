use std::io::Write;
use std::path::PathBuf;
use std::process::{Command, Stdio};

#[derive(Debug, thiserror::Error)]
pub enum UnparseError {
    #[error("canonical unparse stylesheet not found at {0}")]
    MissingStylesheet(PathBuf),
    #[error("failed to run xsltproc: {0}")]
    Io(#[from] std::io::Error),
    #[error("xsltproc failed: {0}")]
    Xslt(String),
    #[error("xsltproc emitted non-UTF-8 output: {0}")]
    Utf8(#[from] std::string::FromUtf8Error),
}

pub fn unparse(xml: &str) -> Result<String, UnparseError> {
    let stylesheet = stylesheet_path();
    if !stylesheet.exists() {
        return Err(UnparseError::MissingStylesheet(stylesheet));
    }

    let mut child = Command::new("xsltproc")
        .arg(stylesheet)
        .arg("-")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    if let Some(mut stdin) = child.stdin.take() {
        stdin.write_all(xml.as_bytes())?;
    }

    let output = child.wait_with_output()?;
    if !output.status.success() {
        return Err(UnparseError::Xslt(
            String::from_utf8_lossy(&output.stderr).trim().to_string(),
        ));
    }

    Ok(String::from_utf8(output.stdout)?)
}

fn stylesheet_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap_or_else(|| std::path::Path::new("."))
        .join("bluebell")
        .join("akn_text.xsl")
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::xml::parse_to_akn_xml;
    use crate::DocumentRoot;

    #[test]
    fn unparse_uses_canonical_stylesheet() {
        let xml = parse_to_akn_xml(
            "P Hello **bold**",
            DocumentRoot::Statement,
            "/akn/za/statement/2022/1",
        )
        .unwrap();
        assert_eq!("Hello **bold**\n\n", unparse(&xml).unwrap());
    }
}
