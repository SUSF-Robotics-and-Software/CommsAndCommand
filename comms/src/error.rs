
pub type Result<T> = std::result::Result<T, Error>;

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("Unable to send command to server background thread: {0}")]
    ServerStateSendError(std::sync::mpsc::SendError<crate::server::ServerStates>),

    #[error("Background thread is not running")]
    BgThreadNotRunning,

    #[error("Error joining thread: {0:?}")]
    ThreadJoinError(Box<dyn std::any::Any + Send + 'static>),

    #[error("Error receiving from channel")]
    ChannelReceiveError(std::sync::mpsc::RecvError)
}