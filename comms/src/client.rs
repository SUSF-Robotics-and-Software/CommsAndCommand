use std::thread;
use std::net::TcpStream;
use std::io::{Write};
// use std::str::from_utf8;

pub fn init_client() -> thread::JoinHandle<()> {
    let handle = thread::spawn(_client_task);
    handle
}

fn _client_task() {
    println!("CLIENT: Thread started");
    // connect to the server, localhost port 5000 
    let mut sock: TcpStream = TcpStream::connect("127.0.0.1:5000").unwrap();
    // now it's connected, let's send a message.
    sock.write("Hello World!".as_bytes()).unwrap();
    println!("CLIENT: sent msg");
    // done.
}

