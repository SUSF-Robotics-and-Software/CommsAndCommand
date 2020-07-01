use std::thread;
use std::net::{TcpListener, TcpStream, Shutdown};
use std::io::{Read, Write};
use std::vec::Vec;
use std::str;



pub struct Server {
    listener: Option<TcpListener>,
    stream: Option<TcpStream>,
    thread: Option<thread::JoinHandle<()>>,
    bytebuff: Vec<u8>,
    run: bool
}


impl Server {
    pub fn accept(&mut self) {
         let connection_state = match self.listener.as_mut() {
            Some(listener) => {
                let result = listener.accept();
                result
            },
            None => {
                // pass
                Err(std::io::Error::new(std::io::ErrorKind::Other, "SERVER:Socket machine broke"))
            }
        };
        match connection_state {
            Ok((stream, _)) => {
                self.stream = Some(stream);
            },
            Err(e) => {
                println!("SERVER: big error {}", e);
            }
        }

    }

    pub fn recieve(&mut self) {
        match &mut self.stream {
            Some(stream) => {
                // server has a connection, and we want to read from it
                read(stream);
                // TODO: update the server's buffer object with read info
            }
            None => {
                // server has no such connection, and as such we can't get a connection from it
            }
        }
        // self.bytebuff
    }

}


fn read(stream: &mut TcpStream) {
    let mut buf = [0; 1024];
    match stream.read(&mut buf) {
        Ok(size) => {
            // can read up to 1024 bytes from the stream
            if let Ok(s) = str::from_utf8(&buf[0..size]) {
                println!("SERVER: success, recieved string: {}", s);
            }
        }
        Err(e) => {
            println!("SERVER: warning, failed to read from stream: {}", e);
        }
    }
}



fn _server_thread(server: &mut Server) {
    let mut runchk = server.run;
    while runchk {
        // accept connections
        server.accept();
        // recieve data from connection
        runchk = server.run;
    }
}



// pub fn init_server() -> Server {
// }