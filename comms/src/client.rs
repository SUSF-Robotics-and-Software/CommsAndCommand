use std::thread;
use std::net::TcpStream;
use std::io::{Write};
use std::sync::mpsc::{Sender, Receiver, channel};
use std::time::Duration;

/* 
    b-but Richard, this is really similar to the server file, why not create
    primatives in the "shared.rs" file?

    Because, dear reader, if one had to differentiate it slightly, one would
    have a much harder time completely re-implementing the new system

    Why would you have to differentiate it?

    Well, the sockets break in different ways and require different responses.
    You probably could make generics, you definately could in python.
    But This ain't python, and I don't want to get Tetanus.
    Also, there's a bunch of unwraps here because I don't want to have to count
    my errors before they hatch? yeah.
*/ 


enum ClientStates {
    RUN,
    STOP
}


struct ClientInfo {
    msg_rx: Receiver<String>,
    control_rx: Receiver<ClientStates>
}


pub struct Client {
    handle: thread::JoinHandle<()>,
    msg_tx: Sender<String>,
    control_tx: Sender<ClientStates>
}


impl Client {
    pub fn init() -> Client {
        let (msg_tx, msg_rx): (Sender<String>, Receiver<String>) = channel();
        let (control_tx, control_rx): (Sender<ClientStates>, Receiver<ClientStates>) = channel();
        let client_info: ClientInfo = ClientInfo {
            msg_rx: msg_rx,
            control_rx: control_rx
        };
        let handle = std::thread::spawn(move || client_task(client_info));

        let client: Client = Client {
            handle: handle,
            msg_tx: msg_tx.clone(),
            control_tx: control_tx
        };
        client
    }

    pub fn stop(&mut self) {
        self.control_tx.send(ClientStates::STOP).unwrap();
    }

    pub fn send(&mut self, string: String) {
        // println!("MAIN: Client starting to send...");
        self.msg_tx.send(string).unwrap();
        // println!("MAIN: Client send complete");
    }
    
    pub fn join(self) {
        self.handle.join().unwrap();
    }
}

fn inspect_client_state(client_state: &ClientStates) -> bool {
    match client_state {
        ClientStates::RUN => return true,
        ClientStates::STOP => return false
    }
}


fn check_control(client_info: &ClientInfo, last_client_instruction: ClientStates) -> ClientStates {
    // again, no generic because ClientStates will probs be extended
    match  client_info.control_rx.recv_timeout(Duration::from_millis(10)) {
        Ok(new_client_instruction) => {
            return new_client_instruction;
        }
        Err(_) => {
            return last_client_instruction;
        }
    }
}


fn check_messages(client_info: &ClientInfo, mut sock: &TcpStream) {
    match client_info.msg_rx.recv_timeout(Duration::from_millis(1000)) {
        Ok(msg) => {
            &sock.write(msg.as_bytes()).unwrap();
        },
        Err(_) => {
            // don't send a message...
        }
    }
}

fn client_task(client_info: ClientInfo) {
    println!("CLIENT: Thread started");
    // connect to the server, localhost port 5000 
    let sock: TcpStream = TcpStream::connect("127.0.0.1:5000").unwrap();
    let mut last_client_instruction: ClientStates = ClientStates::RUN;
    while inspect_client_state(&last_client_instruction) {
        // wait for message with blocking recv
        check_messages(&client_info, &sock);
        // now update the control state. Still gotta do the 5ms timeout
        // thing, because while the 'send' recv can be blocking, the
        // control one cannot be, just in case you want to actually
        // send.
        last_client_instruction = check_control(&client_info, last_client_instruction);
    }
    println!("CLIENT: stopped");
}
