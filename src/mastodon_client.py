from mastodon import Mastodon

def init_mastodon(api_base_url, access_token):
    return Mastodon(access_token=access_token, api_base_url=api_base_url)

def get_account_id(api, username):
    try:
        account = api.account_search(username)[0]
        return account['id']
    except Exception as e:
        print(f"Error retrieving account ID for {username}: {e}")
        return None

def fetch_account_posts(api, account_id, clean_func):
    try:
        posts = []
        max_id = None
        while True:
            batch = api.account_statuses(account_id, max_id=max_id, exclude_reblogs=True, exclude_replies=False)
            if not batch:
                break
            posts.extend([clean_func(status["content"]) for status in batch])
            max_id = batch[-1]["id"]
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []
