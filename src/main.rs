//! mastodon-markov — Markov chain bot for Mastodon.
//!
//! Reads posts from a source account, builds a Markov model from
//! their content, and periodically posts generated text to a
//! destination account.  Two-account separation lets the source
//! be any account while the bot owns the destination.

pub mod clean;
pub mod markov_manager;
pub mod mastodon_client;
pub mod post_manager;
pub mod time;

use anyhow::{Context, Result};
use chrono::Local;
use dotenvy::dotenv;
use std::env;
use std::path::Path;
use tracing::info;
use tracing_subscriber::{fmt, prelude::*, EnvFilter};

#[tokio::main]
async fn main() -> Result<()> {
    // ── Logging setup ────────────────────────────────────────────

    // Ensure the log directory exists
    let log_directory = "log";
    if !Path::new(log_directory).exists() {
        std::fs::create_dir_all(log_directory)?;
    }

    // Set up tracing with file and console output
    let file_appender = tracing_appender::rolling::daily(log_directory, "general.log");
    let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);

    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::registry()
        .with(filter)
        .with(fmt::layer().with_writer(std::io::stdout))
        .with(fmt::layer().with_writer(non_blocking).with_ansi(false))
        .init();

    info!("NEW EXECUTION OF APPLICATION");
    println!("Mastodon Markov Bot started.");

    // ── Environment ──────────────────────────────────────────────

    // Load environment variables
    dotenv().ok();

    let mastodon_base_url =
        env::var("MASTODON_BASE_URL").context("MASTODON_BASE_URL not set")?;
    let mastodon_access_token =
        env::var("MASTODON_ACCESS_TOKEN").context("MASTODON_ACCESS_TOKEN not set")?;

    let mastodon_api =
        mastodon_client::init_mastodon(&mastodon_base_url, &mastodon_access_token);

    let destination_base_url =
        env::var("DESTINATION_MASTODON_BASE_URL").context("DESTINATION_MASTODON_BASE_URL not set")?;
    let destination_access_token = env::var("DESTINATION_MASTODON_ACCESS_TOKEN")
        .context("DESTINATION_MASTODON_ACCESS_TOKEN not set")?;

    let destination_api =
        mastodon_client::init_mastodon(&destination_base_url, &destination_access_token);

    let source_account =
        env::var("SOURCE_MASTODON_ACCOUNT_ID").context("SOURCE_MASTODON_ACCOUNT_ID not set")?;

    let mut markov_chain = markov::Chain::new();

    // ── Main loop ────────────────────────────────────────────────
    //
    // Each iteration: fetch source posts, rebuild the chain, generate
    // one post, publish it, then sleep until the next scheduled refresh.

    loop {
        let current_time = Local::now();
        let refresh_interval = time::calculate_refresh_interval();
        let next_refresh = time::calculate_next_refresh(current_time, refresh_interval);

        // Fetch and refresh
        let posts = mastodon_client::fetch_account_posts(
            &mastodon_api,
            &source_account,
            clean::clean_content,
        );
        markov_chain = markov_manager::refresh_markov_data(markov_chain, posts);

        info!("Markov dataset refreshed.");
        println!("Markov dataset refreshed.");

        let generated_text = markov_chain.generate_str();

        // Post
        info!("Generated text: {}", generated_text);
        println!("Generated text: {}", generated_text);

        post_manager::post_to_mastodon(&destination_api, generated_text, 500);

        time::sleep_until_next_refresh(next_refresh).await;
    }
}
