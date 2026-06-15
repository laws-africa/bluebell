use std::fs;
use std::path::PathBuf;
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
            let xml = fs::read_to_string(&input)
                .with_context(|| format!("failed to read {}", input.display()))?;
            let start = Instant::now();
            let text = bluebell_rs::unparse(&xml).context("failed to apply akn_text.xsl")?;
            let unparse_elapsed = start.elapsed();
            println!("xslt_unparse_ms={}", unparse_elapsed.as_millis());
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
