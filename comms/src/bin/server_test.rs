use comms::server;

fn main() {
    let handle = server::init_server();
    handle.join().unwrap();
}