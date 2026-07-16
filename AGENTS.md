# AGENTS.md

Guidance for agents working on the Rust Mastodon Markov bot. The README marks it unmaintained.

## Current implementation

- `src/main.rs` configures console plus daily file logging, loads separate source/destination endpoints and tokens, and runs a randomized local-time loop.
- The network path is not implemented: `fetch_account_posts` always returns an empty vector, `get_account_id` returns `None`, `clean_content` is a pass-through, and `post_to_mastodon` only logs `Would post`. Preserve these as honest stubs until real `mammut` calls and error handling exist; never describe the current binary as publishing.
- `refresh_markov_data` feeds posts into the existing chain rather than replacing it, despite its comment. Resolve that semantic mismatch deliberately when implementing refresh.
- Scheduling chooses 1,800 through 10,799 seconds and immediately loops if a computed local time is already past.

## Invariants

- Preserve source/destination separation and instance configurability. Never log access tokens or private status content.
- Before implementing fetch, define filtering for boosts, replies, content warnings, HTML, and visibility; never ingest private/direct statuses accidentally.
- The intended hard-coded post limit is 500 characters, but the stub does not truncate. Enforce the destination limit before a real write.
- Network failures need bounded retry and rate-limit handling rather than termination or a tight loop.

## Validation

Run `cargo fmt --check`, `cargo clippy --all-targets --all-features`, `cargo test`, and `cargo build --release`. Current verification must confirm stub behavior and avoid claiming integration coverage. When implementing the missing path, add mocked tests for pagination, privacy filtering, empty corpora, cleanup, length enforcement, auth/write errors, scheduling, and shutdown. Live posts require a dedicated test account; never commit `.env` or `log/`.
