# Mastodon Markov Bot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

A Rust tool to create and post Markov chain-generated content to a Mastodon account.

## Requirements

- Rust 1.85+ (Cargo)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ewanc26/mastodon-markov.git
   cd mastodon-markov
   ```

2. Build the project:

   ```bash
   cargo build --release
   ```

3. Configuration:
   Create a `.env` file in the root directory with the following variables:
   ```plaintext
   MASTODON_BASE_URL=...
   MASTODON_ACCESS_TOKEN=...
   DESTINATION_MASTODON_BASE_URL=...
   DESTINATION_MASTODON_ACCESS_TOKEN=...
   SOURCE_MASTODON_ACCOUNT_ID=...
   ```

## Usage

Run the bot:

```bash
cargo run --release
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
