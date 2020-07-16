use std::thread;
use std::net::{TcpListener, TcpStream};
use std::io::{Read};
use std::sync::mpsc;
use std::time::Duration;
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


pub enum ServerStates {
    RUN,
    STOP
}


pub struct Server {
    handle: thread::JoinHandle<()>,
    // msg_tx: mpsc::Sender<String>,
    msg_rx: mpsc::Receiver<String>,
    control_tx: mpsc::Sender<ServerStates>,
    // control_rx: mpsc::Receiver<ServerStates>
}

impl Server{
    pub fn init() -> Server{
        let (msg_tx, msg_rx): (mpsc::Sender<String>, mpsc::Receiver<String>) = mpsc::channel();
        let (control_tx, control_rx):  (mpsc::Sender<ServerStates>, mpsc::Receiver<ServerStates>) = mpsc::channel();
    
        
        let server_info: ServerInfo = ServerInfo {
            msg_tx: msg_tx.clone(),
            control_rx: control_rx
        };
        
        let handle = thread::spawn(move || _server_task(server_info));
    
        let server: Server = Server {
            handle: handle,
            // msg_tx: msg_tx,
            msg_rx: msg_rx,
            control_tx: control_tx
            // control_rx: control_rx
        };
        server
    }

    pub fn stop(&mut self) {
        &self.control_tx.send(ServerStates::STOP);
    }

    pub fn recv(&mut self) -> String{
        let out_string = self.msg_rx.recv().unwrap();
        out_string
    }

    pub fn join(self) {
        self.handle.join().unwrap();
    }
}




struct ServerInfo {
    msg_tx: mpsc::Sender<String>,
    control_rx: mpsc::Receiver<ServerStates>
}


pub fn init_server() -> Server {
    let (msg_tx, msg_rx): (mpsc::Sender<String>, mpsc::Receiver<String>) = mpsc::channel();
    let (control_tx, control_rx):  (mpsc::Sender<ServerStates>, mpsc::Receiver<ServerStates>) = mpsc::channel();

    
    let server_info: ServerInfo = ServerInfo {
        msg_tx: msg_tx.clone(),
        control_rx: control_rx
    };
    
    let handle = thread::spawn(move || _server_task(server_info));

    let server: Server = Server {
        handle: handle,
        // msg_tx: msg_tx,
        msg_rx: msg_rx,
        control_tx: control_tx
        // control_rx: control_rx
    };
    server
}


fn _server_task(server_info: ServerInfo) {
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
        ServerStates::RUN => return true,
        ServerStates::STOP => return false
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
                let str_msg = from_utf8(&buf[0..msg_size]).unwrap();
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
    let mut last_server_instruction: ServerStates = ServerStates::RUN;
    while inspect_server_state(&last_server_instruction) {
        // get a message from the socket and send it to the main thread
        handle_incoming_msg(&server_info, &conn);

        // check to see if the main thread has disabled the server, and 
        // update the state accordingly
        last_server_instruction = check_control(&server_info, last_server_instruction);
    }
}
