use std::thread;
use std::net::{TcpListener, TcpStream, Shutdown};
use std::io::{Read, Write};
// use std::vec::Vec;
use std::str;

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

pub struct Server {
    thread: Option<thread::JoinHandle<()>>,
}

impl Server {
    pub fn new() -> Server {
        let server: Server = Server {thread: None};
        server
    }

    pub fn init_server() -> std::io::Result<Server> {
        let mut serverInfo: ServerInfo = ServerInfo::new();
        let mut server = Server::new();
        // ServerInfo.thread = Some(thread::spawn(move || _ServerInfo_thread(&mut ServerInfo)));
        Ok(server)
    }
}



struct ServerInfo {
    listener: Option<TcpListener>,
    stream: Option<TcpStream>,
    run: bool
}


impl ServerInfo {
    pub fn new() -> ServerInfo {
        let serverInfo: ServerInfo = ServerInfo {
            listener: None,
            stream: None,
            run: false
        };
        serverInfo
    }


    pub fn accept(&mut self) {
         let connection_state = match self.listener.as_mut() {
            Some(listener) => {
                let result = listener.accept();
                result
            },
            None => {
                // pass
                Err(std::io::Error::new(std::io::ErrorKind::Other, "ServerInfo:Socket machine broke"))
            }
        }; // end match listener
        match connection_state {
            Ok((stream, _)) => {
                self.stream = Some(stream);
            },
            Err(e) => {
                println!("ServerInfo: big error {}", e);
            }
        } // end match conneciton state
    }


    pub fn recieve(&mut self) {
        match &mut self.stream {
            Some(stream) => {
                // ServerInfo has a connection, and we want to read from it
                read(stream);
                // TODO: update the ServerInfo's buffer object with read info
            },
            None => {
                // ServerInfo has no such connection, and as such we can't get a connection from it
            } 
        } // end match(self.stream)
    }

}


fn read(stream: &mut TcpStream) {
    let mut buf = [0; 1024];
    match stream.read(&mut buf) {
        Ok(size) => {
            // can read up to 1024 bytes from the stream
            if let Ok(s) = str::from_utf8(&buf[0..size]) {
                println!("ServerInfo: success, recieved string: {}", s);
            }
        }
        Err(e) => {
            println!("ServerInfo: warning, failed to read from stream: {}", e);
        }
    }
}



fn _ServerInfo_thread(serverInfo: &mut ServerInfo) {
    let mut runchk = serverInfo.run;
    while runchk {
        // accept connections
        serverInfo.accept();
        // recieve data from connection
        runchk = serverInfo.run;
    }
}


