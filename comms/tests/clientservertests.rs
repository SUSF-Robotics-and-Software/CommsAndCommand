use comms;
use std::str;

// #[test]
// fn hello_world() {
//     println!("Hello world!");
//     true;
// }

#[test]
fn server_test() {
    let rx = comms::init_server();
    // let buf = comms::Buffer::new();
    match rx.recv() {
        Ok(buf) => {
            if let Ok(astring) = str::from_utf8(&buf.buf) {
                println!("Server: Revieved {}", astring);
            }
        },
        Err(e) => {
            println!("Server: Failed to recieve {}", e);
        }
    }
}


#[test]
fn client_test() {
    let tx = comms::init_client();
    let buf = comms::Buffer::new();
    buf.setstring(String::from("Hello World!"));
    tx.send(buf).unwrap();
}


#[test]
fn single_excutable_test() {
    let tx = comms::init_client();
    let rx = comms::init_server();

    // send 
    let buf = comms::Buffer::new();
    buf.setstring(String::from("Hello World!"));
    tx.send(buf).unwrap();
    // println!{"TEST: send done"};
    // recieve
    match rx.recv() {
        Ok(buf) => {
            // if let Ok(astring) = str::from_utf8(&buf.buf) {
            //     println!("Server: Recieved {}", astring);
            // }
            // match str::from_utf8(&buf.buf) {
            //     Ok(resstring) => {
            //         println!("Server: Recieved {}", resstring);
            //     }
            //     Err(e) => {
            //         println!("Server: Error {}", e);
            //     }
            // }
            println!("Server: recieved: {:#?}", &buf.buf[0..16]);
        },
        Err(e) => {
            println!("Server: Failed to recieve {}", e);
        }
    }
}