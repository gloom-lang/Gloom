import gleam_value.{GloomObject}

pub type GloomMessage {
  UnaryMessage(selector: String)
  BinaryMessage(selector: String, argument: GloomObject)
  NamedMessage(arguments: GloomObject)
  Noop
}

pub type MessageSend {
  MessageSend(recipient: GloomObject, message: GloomMessage)
}

pub type MessageHandler =
  fn(GloomObject, GloomMessage) -> GloomObject
// every computation with an everything object is inplace
// something objects can be modified, but only explicitly
// nothing objects are no-op. they are the only truly safe objects. 
// 
//              everything something nothing
//  everything  everything everything nothing
//  something   everything something nothing
//  nothing     nothing    nothing   nothing

// nothing > everything > something
// [0, 1, 2, 3, 4, 5, 6, 7, 8]
//
// :set x :to 1.
// x + 2. // x is now equal to 3
// x :become Something.
// x + 2. // x is still 3.
// :set x :to x + 2. // x is now 5
// x :become Nothing.
// :set x :to x + 5. // x is still 5
// x :print. // nothing happens

//pub fn set_affinities(new_affinity: GloomAffinity, message_send: MessageSend) {
//  let MessageSend(recipient, message) = message_send
//  case message {
//    UnaryMessage(_) -> message_send
//    BinaryMessage(_, argument) -> {
//      MessageSend(
//        recipient: GloomObject(..recipient, affinity: new_affinity),
//        message: GloomObject(..argument, affinity: new_affinity),
//      )
//    }
//} }

//pub fn dominant_affinity(message_send: MessageSend) {
//  let MessageSend(recipient, message) = message_send
//  case message {
//    UnaryMessage(_) -> message_send
//    BinaryMessage(_, argument) -> {
//     let max_affinity = affinity_max(recipient.affinity, argument.affinity)
//      MessageSend(
//        recipient: GloomObject(..recipient, affinity: max_affinity),
//       message: GloomObject(..argument, affinity: max_affinity),
//     )
//   }
//   NamedMessage(arguments)
//  }
//}
