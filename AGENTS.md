# AGENTS.md

Guidance for agents working on the Rust Mastodon Markov bot.

## Invariants

- `src/` owns configuration, source-status collection, cleanup, Markov generation, posting, scheduling, and logging.
- Preserve source/destination account separation and Mastodon instance configurability.
- Exclude boosts, replies, content warnings, HTML artifacts, or visibility classes according to explicit policy; do not accidentally ingest private/direct statuses.
- Generated posts must fit the destination instance limit and respect configured visibility/content-warning behavior.
- Validate delay ranges, schedule one next action, use bounded retry, and respect rate-limit responses.
- Never log access tokens or private status content.

## Validation

Run `cargo fmt --check`, `cargo clippy --all-targets --all-features`, `cargo test`, and `cargo build --release`. Mock the Mastodon API, clock, and randomness for pagination, privacy filtering, empty corpus, HTML/Unicode cleanup, over-limit generation, authentication failure, write failure, retry bounds, and shutdown. Live posts require a dedicated test account; never commit `.env` or logs.
