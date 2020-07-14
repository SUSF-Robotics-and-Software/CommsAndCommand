use comms;
// use std::time::Duration;
// use std::thread;

#[test]
fn basic_function() {
    let serverhandle = comms::server::init_server();
    let clienthandle = comms::client::init_client();
    serverhandle.join().unwrap();
    clienthandle.join().unwrap();
}
