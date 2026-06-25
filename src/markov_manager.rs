//! Markov chain lifecycle — init, feed, refresh.
//!
//! Wraps the `markov` crate's `Chain` so the main loop only deals
//! with seed strings and a ready-to-generate model.

use markov::Chain;

/// Create a fresh, empty Markov chain.
pub fn init_markov_model() -> Chain<String> {
    Chain::new()
}

/// Feed a batch of posts into the chain, replacing the old model.
///
/// Called on every refresh cycle. The old chain is consumed and
/// a new one rebuilt from the latest fetched posts.
pub fn refresh_markov_data(mut chain: Chain<String>, posts: Vec<String>) -> Chain<String> {
    for post in posts {
        chain.feed_str(&post);
    }
    chain
}
