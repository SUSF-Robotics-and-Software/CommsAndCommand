use std::thread;
use std::net::{TcpListener, TcpStream, Shutdown};
use std::io::{Read, Write};
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

pub fn init_server() {    
    std::thread::spawn(move || _server_task);
}


fn _server_task() {
    // create socket
    let sock: TcpListener = TcpListener::bind("127.0.0.1:5000").unwrap();
    // two senarios:
    // 1) Fails to bind the socket => try again.
    // 2) Manages to do it =>  yay


    // get connection
    // let mut connection: Option<TcpStream> = _wait_for_connection(sock);
    
    // match connection {
    //     Some(conn) => {
    //         // recv
    //     },
    //     None => println!("SERVER: Connection died")
    // }
    let (conn, addr) = sock.accept().unwrap();
    println!("Got connection from {}", addr);
    recv_cylce(conn);

}

fn _wait_for_connection(sock: TcpListener) -> Option<TcpStream> {
    let mut conn: Option<TcpStream> = None;
    while match sock.accept() {
        Ok((lcl_conn, addr)) => {
            println!("Got connection from {}", addr);
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
    let mut buf = Vec::new();
    loop {
        match conn.read(&mut buf) {
            Ok(msg_size) => {
                // send to channel
                println!("Got msg, {}", from_utf8(&buf[0..msg_size]).unwrap());
            },
            Err(e) => {
                // do didly
            }
        }
    }
}
