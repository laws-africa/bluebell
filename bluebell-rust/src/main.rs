use std::fs;
use std::path::PathBuf;
use std::process::Command as ProcessCommand;
use std::time::Instant;

use anyhow::Context;
use clap::{Parser, Subcommand, ValueEnum};

use bluebell_rs::{parse, pre_parse, DocumentRoot};

#[derive(Debug, Parser)]
#[command(name = "bluebell-rs")]
#[command(about = "Experimental Rust parser for Bluebell Akoma Ntoso markup")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    Preparse {
        input: PathBuf,
    },
    Parse {
        #[arg(value_enum)]
        root: RootArg,
        input: PathBuf,
    },
    ToXml {
        #[arg(value_enum)]
        root: RootArg,
        input: PathBuf,
    },
    ToAknXml {
        frbr_uri: String,
        #[arg(value_enum)]
        root: RootArg,
        input: PathBuf,
    },
    Unparse {
        input: PathBuf,
    },
    BenchText {
        #[arg(value_enum)]
        root: RootArg,
        input: PathBuf,
    },
    BenchIncomeTax {
        input: PathBuf,
    },
}

#[derive(Clone, Debug, ValueEnum)]
enum RootArg {
    Act,
    Bill,
    Debate,
    DebateReport,
    Doc,
    Judgment,
    Statement,
}

impl From<RootArg> for DocumentRoot {
    fn from(value: RootArg) -> Self {
        match value {
            RootArg::Act => DocumentRoot::Act,
            RootArg::Bill => DocumentRoot::Bill,
            RootArg::Debate => DocumentRoot::Debate,
            RootArg::DebateReport => DocumentRoot::DebateReport,
            RootArg::Doc => DocumentRoot::Doc,
            RootArg::Judgment => DocumentRoot::Judgment,
            RootArg::Statement => DocumentRoot::Statement,
        }
    }
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Command::Preparse { input } => {
            let text = fs::read_to_string(&input)
                .with_context(|| format!("failed to read {}", input.display()))?;
            print!("{}", pre_parse(&text));
        }
        Command::Parse { root, input } => {
            let text = fs::read_to_string(&input)
                .with_context(|| format!("failed to read {}", input.display()))?;
            let parsed = parse(&text, root.into())?;
            println!(
                "root={:?} preprocessed_bytes={}",
                parsed.root, parsed.preprocessed_len
            );
        }
        Command::ToXml { root, input } => {
            let text = fs::read_to_string(&input)
                .with_context(|| format!("failed to read {}", input.display()))?;
            println!("{}", bluebell_rs::parse_to_xml(&text, root.into())?);
        }
        Command::ToAknXml {
            frbr_uri,
            root,
            input,
        } => {
            let text = fs::read_to_string(&input)
                .with_context(|| format!("failed to read {}", input.display()))?;
            println!(
                "{}",
                bluebell_rs::parse_to_akn_xml(&text, root.into(), &frbr_uri)?
            );
        }
        Command::Unparse { input } => {
            let xml = fs::read_to_string(&input)
                .with_context(|| format!("failed to read {}", input.display()))?;
            print!("{}", bluebell_rs::unparse(&xml)?);
        }
        Command::BenchText { root, input } => {
            let text = fs::read_to_string(&input)
                .with_context(|| format!("failed to read {}", input.display()))?;
            bench_text(&text, root.into())?;
        }
        Command::BenchIncomeTax { input } => {
            let xml_path = input
                .canonicalize()
                .with_context(|| format!("failed to resolve {}", input.display()))?;
            let script = format!(
                "from pathlib import Path\nfrom bluebell.parser import AkomaNtosoParser\nfrom cobalt import FrbrUri\np=AkomaNtosoParser(FrbrUri.parse('/akn/za/act/1962/58'))\nprint(p.unparse(Path({xml_path:?}).read_bytes()), end='')\n",
                xml_path = xml_path.display().to_string()
            );
            let start = Instant::now();
            let output = ProcessCommand::new("python")
                .arg("-c")
                .arg(script)
                .env("PYTHONPATH", python_oracle_path()?)
                .output()
                .context("failed to run Python unparse oracle")?;
            if !output.status.success() {
                anyhow::bail!(
                    "Python unparse oracle failed: {}",
                    String::from_utf8_lossy(&output.stderr)
                );
            }
            let unparse_elapsed = start.elapsed();
            let text = String::from_utf8(output.stdout).context("oracle emitted non-UTF-8 text")?;
            println!("oracle_unparse_ms={}", unparse_elapsed.as_millis());
            bench_text(&text, DocumentRoot::Act)?;
        }
    }

    Ok(())
}

fn bench_text(text: &str, root: DocumentRoot) -> anyhow::Result<()> {
    let start = Instant::now();
    let preprocessed = pre_parse(text);
    let preparse_elapsed = start.elapsed();

    let start = Instant::now();
    let parsed = bluebell_rs::parse_preprocessed(&preprocessed, root)?;
    let parse_elapsed = start.elapsed();

    println!("root={:?}", parsed.root);
    println!("input_bytes={}", text.len());
    println!("preprocessed_bytes={}", preprocessed.len());
    println!("preparse_ms={}", preparse_elapsed.as_millis());
    println!("parse_ms={}", parse_elapsed.as_millis());
    Ok(())
}

fn python_oracle_path() -> anyhow::Result<PathBuf> {
    let cwd = std::env::current_dir().context("failed to inspect current directory")?;
    if cwd.join("bluebell").is_dir() {
        return Ok(cwd);
    }
    if let Some(parent) = cwd.parent() {
        if parent.join("bluebell").is_dir() {
            return Ok(parent.to_path_buf());
        }
    }
    Ok(cwd)
}
