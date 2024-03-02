from dotenv import load_dotenv
from markovchain.text import MarkovText
from mastodon import Mastodon
from html import unescape
import os
import re
import random
import time
from datetime import datetime

# Load variables from .env file
load_dotenv()

# Function to clean HTML content and special characters from posts
def clean_content(content):
    # Remove HTML tags
    cleaned_content = re.sub('<[^<]+?>', '', content)
    # Decode HTML entities
    cleaned_content = unescape(cleaned_content)
    # Remove usernames
    cleaned_content = re.sub(r'@\w+', '', cleaned_content)
    # Remove special characters except standard punctuation
    cleaned_content = re.sub(r'[^\w\s.,!?;:]', '', cleaned_content)
    # Remove words enclosed with colons
    cleaned_content = re.sub(r':\w+:', '', cleaned_content)
    return cleaned_content

# Function to get Mastodon account posts
def get_account_posts(account_id):
    try:
        # Fetch recent posts from the timeline of the specified account
        posts = mastodon_api.account_statuses(account_id)
        return [clean_content(status["content"]) for status in posts]
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to generate and post an example while considering character and word limits
def generate_and_post_example():
    # Generate text
    generated_text = markov()

    # Ensure the generated text meets the character limit
    if len(generated_text) > 11000:
        generated_text = generated_text[:11000]

    # Split the generated text into words
    words = generated_text.split()

    # Post generated text to destination Mastodon account
    try:
        response = destination_mastodon_api.status_post(
            status=generated_text,
            spoiler_text="Markov-generated post",
            language="EN",
            visibility="unlisted"
        )
        post_link = response['url']
        print(f"Posted to destination Mastodon account successfully: {post_link}")
    except Exception as e:
        print(f"Error posting to destination Mastodon account: {e}")

# Initialize Mastodon API for source account
mastodon_base_url = os.getenv("MASTODON_BASE_URL")
mastodon_access_token = os.getenv("MASTODON_ACCESS_TOKEN")

if not (mastodon_base_url and mastodon_access_token):
    # Prompt the user to enter Mastodon variables
    mastodon_base_url = input("Enter your Mastodon base URL: ")
    mastodon_access_token = input("Enter your Mastodon access token: ")

    # Save Mastodon variables in .env file
    with open('.env', 'a') as env_file:
        env_file.write(f"\nMASTODON_BASE_URL={mastodon_base_url}")
        env_file.write(f"\nMASTODON_ACCESS_TOKEN={mastodon_access_token}")

mastodon_api = Mastodon(
    access_token=mastodon_access_token,
    api_base_url=mastodon_base_url
)

# Initialize Mastodon API for destination account
destination_base_url = os.getenv("DESTINATION_MASTODON_BASE_URL")
destination_access_token = os.getenv("DESTINATION_MASTODON_ACCESS_TOKEN")

if not (destination_base_url and destination_access_token):
    # Prompt the user to enter Mastodon variables for destination account
    destination_base_url = input("Enter the destination Mastodon base URL: ")
    destination_access_token = input("Enter the destination Mastodon access token: ")

    # Save destination Mastodon variables in .env file
    with open('.env', 'a') as env_file:
        env_file.write(f"\nDESTINATION_MASTODON_BASE_URL={destination_base_url}")
        env_file.write(f"\nDESTINATION_MASTODON_ACCESS_TOKEN={destination_access_token}")

destination_mastodon_api = Mastodon(
    access_token=destination_access_token,
    api_base_url=destination_base_url
)

# Check if source Mastodon account ID is already present in .env file, if not, prompt the user
source_account = os.getenv("SOURCE_MASTODON_ACCOUNT_ID")
if not source_account:
    source_username = input("Enter the source Mastodon account username: ")
    source_account = mastodon_api.account_search(source_username)[0]["id"]
    if not source_account:
        print("Error: Failed to retrieve source account ID.")
        exit()
    with open('.env', 'a') as env_file:
        env_file.write(f"\nSOURCE_MASTODON_ACCOUNT_ID={source_account}")

# Initialize MarkovText
markov = MarkovText()

# Fetch Mastodon posts for source account
source_posts = get_account_posts(source_account)

# Add source Mastodon posts to MarkovText
for post in source_posts:
    markov.data(post, part=True)

markov.data('', part=False)

# Generate and post an example at random intervals between 1 and 3 hours
try:
    while True:
        generate_and_post_example()
        # Sleep for a random time between 1 and 3 hours
        sleep_time = random.randint(3600, 10800)  # Random time between 1 and 3 hours in seconds
        time.sleep(sleep_time)

        # Check if it's time to update the dataset (every day)
        current_time = datetime.now()
        if current_time.hour == 0 and current_time.minute == 0:
            # Save the Markov dataset to JSON
            dataset_filename = 'markov_dataset.json'
            markov.save(dataset_filename)
            print(f"Dataset saved to {dataset_filename}")

except KeyboardInterrupt:
    # Save the Markov dataset to JSON before exiting
    dataset_filename = 'markov_dataset.json'
    markov.save(dataset_filename)
    print(f"\nDataset saved to {dataset_filename}")
    print("\nExiting...")
