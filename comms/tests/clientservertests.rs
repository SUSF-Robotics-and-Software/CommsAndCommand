use comms;

// #[test]
// fn hello_world() {
//     println!("Hello world!");
//     true;
// }

#[test]
fn clientside() {
    comms::run_client().unwrap();
}


#[test]
fn serverside(){
    comms::run_server().unwrap();
}

