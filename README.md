# Mastodon Markov Bot

This Python script generates Markov chain text based on the posts of a Mastodon account and posts them to another Mastodon account. It also periodically updates its dataset and posts a new status.

## Setup

1. Clone this repository or download the script `chain.py`.

2. Install the required dependencies by running:

   ```bash
   pip install markovchain mastodon.py python-dotenv
   ```

3. Create a `.env` file in the same directory as the script and add the following variables:

   ```env
   MASTODON_BASE_URL=<source Mastodon instance base URL>
   MASTODON_ACCESS_TOKEN=<source Mastodon account access token>
   DESTINATION_MASTODON_BASE_URL=<destination Mastodon instance base URL>
   DESTINATION_MASTODON_ACCESS_TOKEN=<destination Mastodon account access token>
   SOURCE_MASTODON_ACCOUNT_ID=<source Mastodon account ID>
   ```

## Usage

1. Run the script by executing:

   ```bash
   python mastodon_markov_bot.py
   ```

2. The script will fetch recent posts from the source Mastodon account, generate Markov chain text, and post it to the destination Mastodon account at random intervals between 1 and 3 hours.

3. Press `Ctrl+C` to stop the script.

## Notes

- Ensure that both the source and destination Mastodon accounts have appropriate permissions and visibility settings for posting.
- If you need to change any Mastodon or environment variables, update them in the `.env` file.
- Make sure to customize the script according to your needs, such as adjusting the character limit for generated text or the update interval for the dataset.
