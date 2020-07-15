use comms;
// use std::time::Duration;
// use std::thread;

#[test]
fn basic_function() {
    let serverhandle = comms::server::init_server();
    let clienthandle = comms::client::init_client();
    #[allow(unused_assignments)]
    let mut recvd_string = String::new();
    recvd_string = serverhandle.msg_rx.recv().unwrap();
    println!("MAIN: Got message in main thread: {}", recvd_string);
    serverhandle.control_tx.send(comms::server::ServerStates::STOP).unwrap();
    serverhandle.handle.join().unwrap();
    clienthandle.join().unwrap();
    assert_eq!(recvd_string, "Hello World!")
}
