use std::thread;
use std::net::{TcpListener, TcpStream};
use std::io::{Read};
// use std::vec::Vec;
use std::str::from_utf8;

/*
       __       __
      / <`     '> \
     (  / @   @ \  )
      \(_ _\_/_ _)/
    (\ `-/     \-' /)
     "===\     /==="
      .==')___(`==.
     ' .='     `=.
*/

pub fn init_server() -> thread::JoinHandle<()> {
    let handle = thread::spawn(_server_task);
    handle
}


fn _server_task() {
    println!("SERVER: hi from thread");
    // create socket
    let sock: TcpListener = TcpListener::bind("127.0.0.1:5000").unwrap();
    // two senarios:
    // 1) Fails to bind the socket => try again.
    // 2) Manages to do it =>  yay
    let (conn, addr) = sock.accept().unwrap();
    println!("SERVER: Got connection from {}", addr);
    recv_cylce(conn);
}

fn _wait_for_connection(sock: TcpListener) -> Option<TcpStream> {
    let mut conn: Option<TcpStream> = None;
    while match sock.accept() {
        Ok((lcl_conn, addr)) => {
            println!("SERVER: Got connection from {}", addr);
            conn = Some(lcl_conn);
            false
        },
        Err(_) => {
            true
        }
    } {}
    conn
}


fn recv_cylce(mut conn: TcpStream){
    // let mut bufstring = String::new();
    let mut buf = String::new();
    loop {
        match conn.read_to_string(&mut buf) {
            Ok(msg_size) => {
                // send to channel
                if msg_size > 0 {
                    println!("SERVER: Got msg {}", &buf);
                }
                // TEMP
                // break;
            },
            Err(_) => {
                // do didly
                println!("SERVER: failed to recieve, ending");
            }
        }
    }
}
