
use std::{
    thread,
    net::{TcpListener, TcpStream},
    io::Read,
    sync::mpsc::{Receiver, Sender, channel},
    time::Duration
};

use crate::error::*;

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


/// TODO: Add doc
pub enum ServerStates {
    Run,
    Stop
}


/// TODO: Add doc
pub struct Server {
    handle: Option<thread::JoinHandle<()>>,
    msg_rx: Receiver<String>,
    control_tx: Sender<ServerStates>,
}

impl Server {
    /// TODO: Add doc
    pub fn init() -> Self {
        let (msg_tx, msg_rx): (Sender<String>, Receiver<String>) = channel();
        let (control_tx, control_rx):  (Sender<ServerStates>, Receiver<ServerStates>) = channel();
    
        
        let server_info: ServerInfo = ServerInfo {
            msg_tx: msg_tx.clone(),
            control_rx
        };
        
        let handle = thread::spawn(move || server_task(server_info));
    
        Server {
            handle: Some(handle),
            msg_rx,
            control_tx
        }
    }

    /// TODO: Add doc
    pub fn stop(&mut self) -> Result<()> {
        self.control_tx.send(ServerStates::Stop)
            .map_err(|e| Error::ServerStateSendError(e))?;

        self.handle
            .take().map_or_else(|| Err(Error::BgThreadNotRunning), |j| Ok(j))?
            .join().map_err(|e| Error::ThreadJoinError(e))?;
        
        Ok(())
    }

    /// TODO: Add doc
    pub fn recv(&mut self) -> Result<String> {

        self.msg_rx.recv().map_err(|e| Error::ChannelReceiveError(e))

    }
}

/// TODO: Add doc
struct ServerInfo {
    msg_tx: Sender<String>,
    control_rx: Receiver<ServerStates>
}

pub fn _init_server() -> Server {
    let (msg_tx, msg_rx): (Sender<String>, Receiver<String>) = channel();
    let (control_tx, control_rx):  (Sender<ServerStates>, Receiver<ServerStates>) = channel();

    
    let server_info: ServerInfo = ServerInfo {
        msg_tx: msg_tx.clone(),
        control_rx
    };
    
    let handle = thread::spawn(move || server_task(server_info));

    let server: Server = Server {
        handle: Some(handle),
        msg_rx,
        control_tx
    };
    server
}


fn server_task(server_info: ServerInfo) {
    println!("SERVER: Thread started");
    // create socket
    let sock: TcpListener = TcpListener::bind("127.0.0.1:5000").unwrap();
    // two senarios:
    // 1) Fails to bind the socket => try again.
    // 2) Manages to do it =>  yay
    let (conn, _addr) = sock.accept().unwrap();
    conn.set_read_timeout(Some(Duration::from_millis(100))).unwrap();
    println!("SERVER: Got connection from {}", _addr);
    recv_cylce(server_info, conn);
    println!("SERVER: stopped.");
}

fn _wait_for_connection(sock: TcpListener) -> Option<TcpStream> {
    let mut conn: Option<TcpStream> = None;
    while match sock.accept() {
        Ok((lcl_conn, _addr)) => {
            // println!("SERVER: Got connection from {}", _addr);
            conn = Some(lcl_conn);
            false
        },
        Err(_) => {
            true
        }
    } {}
    conn
}

fn inspect_server_state(server_state: &ServerStates) -> bool {
    match server_state {
        ServerStates::Run => return true,
        ServerStates::Stop => return false
    }
}

fn handle_incoming_msg(server_info: &ServerInfo, mut conn: &TcpStream) {
    // let mut buf = String::new();
    let mut buf: [u8; 2048] = [0; 2048];
    // println!("SERVER: listening...");
    match conn.read(&mut buf) {
        Ok(msg_size) => {
            // message recieved from socket, update send back to main thread
            if msg_size > 0 {
                let str_msg = std::str::from_utf8(&buf[0..msg_size]).unwrap();
                // println!("SERVER: Got msg on socket {}", str_msg);
                // send msg to sever
                server_info.msg_tx.send(str_msg.to_string()).unwrap();
            }
            
        },
        Err(_) => {
            // println!("SERVER: failed to recieve: {}", e);
            // TODO - depends on the error. if it's "stream doesn't exist"
            // the state needs to change.
        }
    }
}

fn check_control(sever_info: &ServerInfo, last_server_instruction: ServerStates) -> ServerStates {
    match  sever_info.control_rx.recv_timeout(Duration::from_millis(10)) {
        Ok(new_server_state) => {
            return new_server_state;
        }
        Err(_) => {
            return last_server_instruction;
        }
    }
}


fn recv_cylce(server_info: ServerInfo, conn: TcpStream){
    // let mut bufstring = String::new();
    let mut last_server_instruction: ServerStates = ServerStates::Run;
    while inspect_server_state(&last_server_instruction) {
        // get a message from the socket and send it to the main thread
        handle_incoming_msg(&server_info, &conn);

        // check to see if the main thread has disabled the server, and 
        // update the state accordingly
        last_server_instruction = check_control(&server_info, last_server_instruction);
    }
}
