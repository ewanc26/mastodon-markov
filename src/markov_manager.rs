use markov::Chain;

pub fn init_markov_model() -> Chain<String> {
    Chain::new()
}

pub fn refresh_markov_data(mut chain: Chain<String>, posts: Vec<String>) -> Chain<String> {
    for post in posts {
        chain.feed_str(&post);
    }
    chain
}
