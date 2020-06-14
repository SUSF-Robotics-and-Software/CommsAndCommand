use std::net::{TcpListener, TcpStream, SocketAddrV4, Ipv4Addr};
use std::io::{Read, Write};
use std;

use std::sync::mpsc::{Sender, Receiver};
use std::sync::mpsc;
use std::{thread, time};

// #[macro_use]
// extern crate json;


static CPORT: u16 = 12864;
static SPORT: u16 = CPORT + 1;
static DESTADDR: Ipv4Addr =  Ipv4Addr::new(127,0,0,1);
// static MAX_TRIES: u32 = 1000;

#[derive(Copy, Clone)]
pub struct Buffer {
    pub buf: [u8; 128]
}

impl Buffer {
    pub fn new () -> Buffer {
        let buf = [0 as u8; 128];
        Buffer { buf }
    }

    pub fn setstring(mut self, string: String) {
        for (i, c) in string.bytes().enumerate() {
            self.buf[i] = c;
        }
    }
}


struct Server {
    listener: TcpListener,
    tx: Sender<Buffer>
}

impl Server{
    fn new (listener: TcpListener, tx: Sender<Buffer>) -> Server{
        Server {listener, tx}
    }
}

struct Client {
    target_socket: SocketAddrV4,
    rx: Receiver<Buffer>,
}

impl Client {
    fn new(ipaddr: Ipv4Addr, rx: Receiver<Buffer>) -> Client {
        let target_socket = SocketAddrV4::new(ipaddr, SPORT);
        Client {target_socket, rx}
    }
}

pub struct SenderReciever {
    pub rx: Receiver<Buffer>,
    pub tx: Sender<Buffer>
}


fn server_thread_main(server: &mut Server) {
    // accept connections
    let mut buffer = Buffer::new();
    println!("SERVER: accepting connections");
    while  match server.listener.accept() {
        Ok((mut stream, _)) => {
            println!("SERVER: Got connection!");
            loop {
                match stream.read(&mut buffer.buf) {
                    Ok(data) => {
                        println!("SERVER: data {}", data);
                    }
                    Err(e) => {
                        println!("SERVER: error on rcv {}", e);
                    }
                }
                match server.tx.send(buffer) {
                    Ok(()) => {
                        println!("SERVER: sent to main");
                    }
                    Err(e) => {
                        println!("SERVER: error on tx {}", e);
                    }
                }
            }
            // false
        }
        Err(e) => {
            println!("SERVER: Failed: {}, retrying", e);
            true 
        }
    } {
        // pass
    }
    println!("SERVER: Thread finished");
    // let (mut stream, _) = server.listener.accept().unwrap();
}


pub fn init_server() -> Receiver<Buffer> {
    let (tx, rx): (Sender<Buffer>, Receiver<Buffer>) = mpsc::channel();
    let listener = TcpListener::bind(format!("127.0.0.1:{}", SPORT)).unwrap();
    let mut server = Server::new(listener, tx);
    thread::spawn(move || {
        server_thread_main(&mut server);
    });
    rx
}


fn client_thread_main(client: &mut Client) {
    // let mut stream: TcpStream;
    let mut buf: Buffer;
    // Tries to connect until conneciton is obtained
    while match TcpStream::connect(client.target_socket) {
        Ok(mut stream) => {
            println!("CLIENT: Connected to server");
            loop {
                buf = client.rx.recv().unwrap();
                stream.write(&buf.buf).unwrap();
            }
        },
        Err(e) => {
            println!("CLIENT: Failed to connect: {}. Waiting to retry...", e);
            thread::sleep(time::Duration::from_secs(1));
            true
        }
    } {
        // pass
    }
    // stream.write(buf: &[u8]);
}


pub fn init_client() -> Sender<Buffer> {
    // create address
    let (tx, rx): (Sender<Buffer>, Receiver<Buffer>) = mpsc::channel();
    let mut client = Client::new(DESTADDR, rx);
    thread::spawn(move|| {
        client_thread_main(&mut client);
    });
    tx
}


pub fn init() -> SenderReciever {
    // init client
    let tx = init_client();
    // init server 
    let rx = init_server();
    // return Ok or on Error
    SenderReciever {rx, tx}
}


pub fn write_buf() -> std::io::Result<()> {
    //
    Ok(())
}


pub fn read_buf() -> std::io::Result<()> {
    Ok(())
}

