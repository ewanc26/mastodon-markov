//! Timing and scheduling helpers for the main loop.
//!
//! The bot runs on a randomised refresh interval so its posting
//! pattern isn't trivially predictable.

use chrono::{DateTime, Duration, Local};
use rand::Rng;
use tokio::time::sleep;
use tracing::warn;

// ── Interval calculation ──────────────────────────────────────────

/// Pick a randomised refresh interval in seconds.
///
/// Range: 30 minutes to 3 hours. The jitter means the bot doesn't
/// post on a cron-like beat that followers could game.
pub fn calculate_refresh_interval() -> i64 {
    let mut rng = rand::thread_rng();
    rng.gen_range(1800..10800)
}

/// Compute the absolute time of the next refresh from now.
pub fn calculate_next_refresh(
    current_time: DateTime<Local>,
    refresh_interval: i64,
) -> DateTime<Local> {
    current_time + Duration::seconds(refresh_interval)
}

// ── Sleep until scheduled time ────────────────────────────────────

/// Block (async) until `next_refresh` arrives.
///
/// If the scheduled time is already past, logs a warning and returns
/// immediately rather than sleeping.
pub async fn sleep_until_next_refresh(next_refresh: DateTime<Local>) {
    let current_time = Local::now();
    let time_remaining = next_refresh - current_time;

    if time_remaining.num_seconds() > 0 {
        sleep(tokio::time::Duration::from_secs(
            time_remaining.num_seconds() as u64,
        ))
        .await;
    } else {
        warn!("Next refresh time is in the past.");
    }
}
