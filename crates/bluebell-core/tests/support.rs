#![allow(dead_code)]

use std::io::Write;
use std::path::{Path, PathBuf};
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

pub fn repo_path(path: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .join(path)
}

pub fn python_path() -> &'static str {
    "../.."
}

fn stylesheet_path() -> PathBuf {
    repo_path("bluebell/akn_text.xsl")
}
