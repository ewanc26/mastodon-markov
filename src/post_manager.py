def post_to_mastodon(api, text, char_limit):
    try:
        if len(text) > char_limit:
            text = text[:char_limit]
        response = api.status_post(status=text, spoiler_text="Markov-generated post", language="EN", visibility="unlisted")
        print(f"Posted successfully: {response['url']}")
    except Exception as e:
        print(f"Error posting to Mastodon: {e}")