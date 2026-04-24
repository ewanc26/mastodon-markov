# Mastodon Markov Bot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

This Python project fetches posts from one Mastodon account, cleans the content, trains a Markov chain on it, and posts generated output to another Mastodon account on a repeating random schedule.

> 🧶 Also available on [Tangled](https://tangled.org/ewancroft.uk/mastodon-markov)

## Features

- Logs into separate source and destination Mastodon accounts
- Pulls recent source posts and cleans the HTML before training the model
- Generates Markov text with the `markovchain` library
- Posts to the destination account with a configurable character limit
- Waits a random 30 minutes to 3 hours between iterations
- Stores logs in `log/general.log`

## Requirements

- Python 3.x
- `markovchain`
- `mastodon.py`
- `python-dotenv`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the repository root with:

```env
MASTODON_BASE_URL=https://source.instance
MASTODON_ACCESS_TOKEN=source_access_token
DESTINATION_MASTODON_BASE_URL=https://destination.instance
DESTINATION_MASTODON_ACCESS_TOKEN=destination_access_token
DESTINATION_MASTODON_CHAR_LIMIT=500
SOURCE_MASTODON_ACCOUNT_ID=123456
```

If `SOURCE_MASTODON_ACCOUNT_ID` is missing, the bot will prompt for a source username and save the resolved ID back to `.env`.

## Usage

Run the bot from the repository root:

```bash
python src/main.py
```

The bot will:

1. Load environment variables
2. Log into the source and destination Mastodon accounts
3. Refresh the Markov dataset from the source account
4. Generate a post and publish it to the destination account
5. Sleep until the next random refresh interval

Press `Ctrl+C` to stop the loop.

## Project structure

```text
src/
├── env_loader.py         # Load and persist environment variables
├── warning_manager.py    # Suppress unwanted warnings
├── mastodon_client.py    # Mastodon API helpers
├── text_cleaner.py       # Clean source post HTML/content
├── markov_manager.py     # Markov training and generation helpers
├── post_manager.py       # Destination posting helper
├── refresh_schedule.py   # Random interval scheduling helpers
└── main.py               # Orchestrates the full bot
```

## Notes

- The bot writes logs to `log/general.log`.
- The source and destination access tokens should be app-specific tokens, not account passwords.
- If the source account ID is not set, the script can resolve it from a username interactively.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ☕ Support

If you found this useful, consider [buying me a ko-fi](https://ko-fi.com/ewancroft)!