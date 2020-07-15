use comms::server;

fn main() {
    let recv_server = server::init_server();
    recv_server.handle.join().unwrap();
}