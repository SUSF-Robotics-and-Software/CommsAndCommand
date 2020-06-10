use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std;
use std::str::from_utf8;


fn send_msg(stream: &mut  TcpStream, buf: &[u8]) -> std::io::Result<()> {
    stream.write(&buf)?;
    Ok(())
}

fn read_msg(stream: &mut TcpStream) -> std::io::Result<()> {
    let mut buf = [0 as u8; 128];
    match stream.read(&mut buf) {
        Ok(size) => {
            println!("server: got msg {}", from_utf8(&buf[0..size]).unwrap())
        },
        Err(e) => {
            println!("server: failed {}", e)
        }
    }
    Ok(())
}


pub fn run_client() -> std::io::Result<()> {
    let msg = b"hello world";

    let mut stream = TcpStream::connect("localhost:12864")?;
    send_msg(&mut stream, &msg[0..11])?;
    println!("client: sent message!");
    Ok(())
}


pub fn run_server() -> std::io::Result<()> {
    let listener = TcpListener::bind("localhost:12864")?;
    match listener.accept() {
        Ok((mut stream, addr)) => {
            println!("New connection from {}", addr);
            read_msg(&mut stream)?;
        },
        Err(_) => {
            println!("No connection recieved");
        }
    }
    Ok(())
}
