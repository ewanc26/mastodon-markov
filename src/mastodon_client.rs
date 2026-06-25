//! Mastodon API interaction — auth, fetching, and posting.
//!
//! Thin wrappers over the `mammut` client library. The source
//! account provides the corpus; the destination account publishes.

use mammut::{Data, Mastodon};
use std::borrow::Cow;

/// Build a `Mastodon` client from base URL and access token.
///
/// Only `base` and `token` are required for token-authenticated access;
/// the other `Data` fields are left empty.
pub fn init_mastodon(base_url: &str, access_token: &str) -> Mastodon {
    Mastodon::from_data(Data {
        base: Cow::Owned(base_url.to_string()),
        client_id: Cow::Borrowed(""),
        client_secret: Cow::Borrowed(""),
        redirect: Cow::Borrowed(""),
        token: Cow::Owned(access_token.to_string()),
    })
}

/// Resolve a Mastodon account ID from a username.
///
/// Placeholder — the actual API lookup isn't wired yet.
pub fn get_account_id(_client: &Mastodon, _username: &str) -> Option<String> {
    None // Placeholder
}

/// Fetch all recent posts from an account, cleaning each one.
///
/// Placeholder — the paginated API call isn't wired yet.
/// `cleaner` is a function that strips/normalises each post's text.
pub fn fetch_account_posts<F>(
    _client: &Mastodon,
    _account_id: &str,
    _cleaner: F,
) -> Vec<String>
where
    F: Fn(&str) -> String,
{
    Vec::new() // Placeholder
}
