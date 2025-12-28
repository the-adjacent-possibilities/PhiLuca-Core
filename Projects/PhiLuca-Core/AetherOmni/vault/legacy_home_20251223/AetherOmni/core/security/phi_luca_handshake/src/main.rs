use phi_luca_handshake::PhiLucaPeer;

fn main() {
    let peer = PhiLucaPeer::new();
    match peer.finalize() {
        Ok(msg) => println!("{}", msg),
        Err(e) => eprintln!("Security Error: {}", e),
    }
}
