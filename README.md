# Mastodon Markov Bot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

This Python project generates Markov chain text based on the posts of a Mastodon account and posts them to another Mastodon account. It also periodically updates its dataset and posts a new status.

## Setup

1. Clone this repository and navigate to the `/src/` directory containing the modular scripts.

2. Install the required dependencies by running:

   ```bash
   pip install markovchain mastodon.py python-dotenv
   ```

3. Create a `.env` file in the root directory of the project and add the following variables:

   ```env
   MASTODON_BASE_URL=<source Mastodon instance base URL>
   MASTODON_ACCESS_TOKEN=<source Mastodon account access token>
   DESTINATION_MASTODON_BASE_URL=<destination Mastodon instance base URL>
   DESTINATION_MASTODON_ACCESS_TOKEN=<destination Mastodon account access token>
   DESTINATION_MASTODON_CHAR_LIMIT=<destination Mastodon character limit>
   SOURCE_MASTODON_ACCOUNT_ID=<source Mastodon account ID>
   ```

## Usage

1. Run the `main.py` script located in the `/src/` directory by executing:

   ```bash
   python src/main.py
   ```

2. The script will fetch recent posts from the source Mastodon account, generate Markov chain text, and post it to the destination Mastodon account at random intervals between 30 minutes and 3 hours.

3. Press `Ctrl+C` to stop the script.

## File Structure

- `/src/`
  - `warnings_manager.py`: Handles suppression of specific warnings.
  - `env_loader.py`: Loads and manages environment variables.
  - `mastodon_client.py`: Interfaces with the Mastodon API for fetching and posting data.
  - `text_cleaner.py`: Cleans and preprocesses text content.
  - `markov_manager.py`: Manages Markov chain generation and dataset refreshing.
  - `post_manager.py`: Handles posting generated content to Mastodon.
  - `refresh_schedule.py`: Calculates refresh intervals and manages scheduling.
  - `main.py`: Orchestrates the entire process by tying together all modules.

## Notes

- Ensure that both the source and destination Mastodon accounts have appropriate permissions and visibility settings for posting.
- If you need to change any Mastodon or environment variables, update them in the `.env` file.
- The modular structure allows customisation and scaling of specific functionalities by modifying the respective scripts in the `/src/` directory.