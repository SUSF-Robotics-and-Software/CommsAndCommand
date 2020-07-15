use std::thread;
use std::net::{TcpListener, TcpStream};
use std::io::{Read};
use std::sync::mpsc;
use std::time::Duration;

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
    pub handle: thread::JoinHandle<()>,
    // msg_tx: mpsc::Sender<String>,
    pub msg_rx: mpsc::Receiver<String>,
    pub control_tx: mpsc::Sender<ServerStates>,
    // control_rx: mpsc::Receiver<ServerStates>
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
    // println!("SERVER: hi from thread");
    // create socket
    let sock: TcpListener = TcpListener::bind("127.0.0.1:5000").unwrap();
    // two senarios:
    // 1) Fails to bind the socket => try again.
    // 2) Manages to do it =>  yay
    let (conn, _addr) = sock.accept().unwrap();
    // println!("SERVER: Got connection from {}", addr);
    recv_cylce(server_info, conn);
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
    let mut buf = String::new();
    match conn.read_to_string(&mut buf) {
        Ok(msg_size) => {
            // message recieved from socket, update send back to main thread
            if msg_size > 0 {
                // println!("SERVER: Got msg {}", &buf);
                // send msg to sever
                server_info.msg_tx.send(buf).unwrap();
            }
            
        },
        Err(_) => {
            // println!("SERVER: failed to recieve, ending");
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
