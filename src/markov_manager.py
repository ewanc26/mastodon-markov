from markovchain.text import MarkovText

def init_markov_model():
    return MarkovText()

def refresh_markov_data(markov, posts):
    for post in posts:
        markov.data(post, part=True)
    markov.data('', part=False)