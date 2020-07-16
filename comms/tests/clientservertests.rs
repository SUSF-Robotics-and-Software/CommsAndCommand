use comms;
// use std::time::Duration;
// use std::thread;

#[test]
fn basic_function() {
    let send_string = "Hello World!".to_string();
    let mut server = comms::server::Server::init();
    let mut client = comms::client::Client::init();
    client.send(send_string.clone());
    println!("MAIN: sent msg, recving now...");
    let recvd_string = server.recv();
    println!("MAIN: Got message in main thread: {}", recvd_string);
    server.stop();
    server.join();
    client.stop();
    client.join();
    assert_eq!(recvd_string, send_string);
}
