//! Text cleaning utilities for post content before Markov ingestion.
//!
//! HTML stripping, normalisation, and any sanitisation the source
//! account's posts need before they're fed into the chain.

/// Clean a raw post string for Markov ingestion.
///
/// Currently a pass-through; the source account's content format may
/// not need stripping yet.
pub fn clean_content(text: &str) -> String {
    // Placeholder for cleaning logic
    text.to_string()
}
