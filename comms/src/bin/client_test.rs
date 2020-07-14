use comms::client;
// use std::time::Duration;
// use std::thread;

fn main() {
    let handle = client::init_client();
    handle.join().unwrap();
}

