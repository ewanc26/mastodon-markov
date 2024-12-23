import warnings_manager
import env_loader
import mastodon_client
import text_cleaner
import markov_manager
import post_manager
import refresh_schedule
from datetime import datetime

# Ignore warnings
warnings_manager.ignore_future_warnings()

# Load environment variables
env_loader.load_environment_variables()

# Source Mastodon API
mastodon_base_url = env_loader.get_env_variable("MASTODON_BASE_URL", "Enter your Mastodon base URL: ")
mastodon_access_token = env_loader.get_env_variable("MASTODON_ACCESS_TOKEN", "Enter your Mastodon access token: ")
mastodon_api = mastodon_client.init_mastodon(mastodon_base_url, mastodon_access_token)

# Destination Mastodon API
destination_base_url = env_loader.get_env_variable("DESTINATION_MASTODON_BASE_URL", "Enter the destination Mastodon base URL: ")
destination_access_token = env_loader.get_env_variable("DESTINATION_MASTODON_ACCESS_TOKEN", "Enter the destination Mastodon access token: ")
char_limit = int(env_loader.get_env_variable("DESTINATION_MASTODON_CHAR_LIMIT", "Enter the destination Mastodon character limit: "))
destination_api = mastodon_client.init_mastodon(destination_base_url, destination_access_token)

# Source account ID
source_account = env_loader.get_env_variable("SOURCE_MASTODON_ACCOUNT_ID")
if not source_account:
    source_username = input("Enter the source Mastodon account username: ")
    source_account = mastodon_client.get_account_id(mastodon_api, source_username)
    if source_account:
        env_loader.save_env_variable("SOURCE_MASTODON_ACCOUNT_ID", source_account)

# Initialise Markov model
markov = markov_manager.init_markov_model()

# Main loop
try:
    while True:
        current_time = datetime.now()
        refresh_interval = refresh_schedule.calculate_refresh_interval()
        next_refresh = refresh_schedule.calculate_next_refresh(current_time, refresh_interval)

        # Refresh Markov dataset
        posts = mastodon_client.fetch_account_posts(mastodon_api, source_account, text_cleaner.clean_content)
        markov_manager.refresh_markov_data(markov, posts)

        # Generate and post example
        generated_text = markov()
        post_manager.post_to_mastodon(destination_api, generated_text, char_limit)

        # Sleep until next refresh
        refresh_schedule.sleep_until_next_refresh(next_refresh)

except KeyboardInterrupt:
    print("\nExiting...")