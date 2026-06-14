use chrono::{DateTime, Local, Duration};
use rand::Rng;
use tracing::{warn};
use tokio::time::sleep;

pub fn calculate_refresh_interval() -> i64 {
    let mut rng = rand::thread_rng();
    rng.gen_range(1800..10800)
}

pub fn calculate_next_refresh(current_time: DateTime<Local>, refresh_interval: i64) -> DateTime<Local> {
    current_time + Duration::seconds(refresh_interval)
}

pub async fn sleep_until_next_refresh(next_refresh: DateTime<Local>) {
    let current_time = Local::now();
    let time_remaining = next_refresh - current_time;

    if time_remaining.num_seconds() > 0 {
        sleep(tokio::time::Duration::from_secs(time_remaining.num_seconds() as u64)).await;
    } else {
        warn!("Next refresh time is in the past.");
    }
}
