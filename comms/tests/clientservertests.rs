use comms;
// use std::time::Duration;
// use std::thread;

#[test]
fn basic_function() {
    let send_string = "Hello World!".to_string();
    let mut server = comms::Server::init();
    let mut client = comms::Client::init();
    client.send(send_string.clone());
    println!("MAIN: sent msg, recving now...");
    let recvd_string = server.recv().expect("Recieve error");
    println!("MAIN: Got message in main thread: {}", recvd_string);
    server.stop().expect("Error stopping server");
    client.stop();
    client.join();
    assert_eq!(recvd_string, send_string);
}
