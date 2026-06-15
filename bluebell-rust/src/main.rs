use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command as ProcessCommand;
use std::time::{Duration, Instant};

use anyhow::Context;
use clap::{Parser, Subcommand, ValueEnum};

use bluebell_rs::{parse, pre_parse, DocumentRoot};

#[derive(Debug, Parser)]
#[command(name = "bluebell-rs")]
#[command(about = "Experimental Rust parser for Bluebell Akoma Ntoso markup")]
#[command(
    long_about = "Experimental Rust implementation of Bluebell parsing.\n\nUse `to-akn-xml` when you want output comparable to Python Bluebell's parse_to_xml. Use `unparse` to apply the canonical bluebell/akn_text.xsl stylesheet to Akoma Ntoso XML."
)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    /// Run Bluebell preprocessing and print the preprocessed text.
    Preparse {
        /// Bluebell input file.
        #[arg(value_name = "INPUT")]
        input: PathBuf,
    },
    /// Parse Bluebell text and print parser statistics without XML output.
    Parse {
        /// Document root rule to parse with.
        #[arg(value_enum)]
        root: RootArg,
        /// Bluebell input file.
        #[arg(value_name = "INPUT")]
        input: PathBuf,
    },
    /// Parse Bluebell text to the document element only.
    ///
    /// This is mainly useful for debugging the Rust XML generator. For full
    /// Akoma Ntoso XML with metadata, use `to-akn-xml`.
    ToXml {
        /// Document root to emit, such as `act`, `statement`, or `judgment`.
        #[arg(value_enum)]
        root: RootArg,
        /// Bluebell input file.
        #[arg(value_name = "INPUT")]
        input: PathBuf,
    },
    /// Parse Bluebell text to full Akoma Ntoso XML.
    ///
    /// This wraps the document element in `<akomaNtoso>` and inserts generated
    /// FRBR metadata based on the supplied URI.
    ToAknXml {
        /// FRBR work URI, for example `/akn/za/act/2022/1`.
        #[arg(value_name = "FRBR_URI")]
        frbr_uri: String,
        /// Document root to emit, such as `act`, `statement`, or `judgment`.
        #[arg(value_enum)]
        root: RootArg,
        /// Bluebell input file.
        #[arg(value_name = "INPUT")]
        input: PathBuf,
    },
    /// Convert Akoma Ntoso XML to Bluebell text with bluebell/akn_text.xsl.
    Unparse {
        /// Akoma Ntoso XML input file.
        #[arg(value_name = "INPUT")]
        input: PathBuf,
    },
    /// Benchmark preprocessing and parsing for an existing Bluebell text file.
    BenchText {
        /// Document root rule to parse with.
        #[arg(value_enum)]
        root: RootArg,
        /// Bluebell input file.
        #[arg(value_name = "INPUT")]
        input: PathBuf,
    },
    /// Benchmark income-tax.xml against Rust and Python after canonical XSLT unparse.
    BenchIncomeTax {
        /// Akoma Ntoso XML input file.
        #[arg(value_name = "INPUT")]
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
            let rust = bench_text(&text, DocumentRoot::Act)?;
            let python = bench_python_parse(&text, "act", "/akn/za/act/1962/58")?;
            println!("python_parse_ms={}", python.as_millis());
            if python.as_nanos() > 0 {
                println!(
                    "rust_parse_speedup={:.2}x",
                    python.as_secs_f64() / rust.parse.as_secs_f64()
                );
            }
        }
    }

    Ok(())
}

struct RustBench {
    parse: Duration,
}

fn bench_text(text: &str, root: DocumentRoot) -> anyhow::Result<RustBench> {
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
    Ok(RustBench {
        parse: parse_elapsed,
    })
}

fn bench_python_parse(text: &str, python_root: &str, frbr_uri: &str) -> anyhow::Result<Duration> {
    let text_path = std::env::temp_dir().join("bluebell-rs-bench-income-tax.txt");
    fs::write(&text_path, text)
        .with_context(|| format!("failed to write {}", text_path.display()))?;
    let script = format!(
        "from pathlib import Path\nfrom bluebell.parser import AkomaNtosoParser\nfrom cobalt import FrbrUri\np=AkomaNtosoParser(FrbrUri.parse({uri:?}))\np.parse_to_xml(Path({text:?}).read_text(), {root:?})\n",
        uri = frbr_uri,
        text = text_path.display().to_string(),
        root = python_root,
    );

    let start = Instant::now();
    let output = ProcessCommand::new(python())
        .arg("-c")
        .arg(script)
        .env("PYTHONPATH", python_path())
        .output()
        .context("failed to run Python Bluebell benchmark")?;
    let elapsed = start.elapsed();
    if !output.status.success() {
        anyhow::bail!(
            "Python Bluebell benchmark failed:\nstdout:\n{}\nstderr:\n{}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
    }
    Ok(elapsed)
}

fn python() -> &'static str {
    "python"
}

fn python_path() -> &'static str {
    if Path::new("bluebell").exists() {
        "."
    } else {
        ".."
    }
}
