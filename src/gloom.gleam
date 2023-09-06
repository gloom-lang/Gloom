import gleam/io
import gleam/map
import object.{
  Everything, GloomObject, Nothing, Something, everything, get, get_property,
  new_table, number_from_float, number_from_int, print_object, string,
  table_from_list, template_replace_all, update_property,
}
import message.{
  BinaryMessage, GloomMessage, MessageHandler, NamedMessage, UnaryMessage,
  affinity_table_max,
}

pub fn main() {
  let whatever =
    table_from_list(
      [
        #(number_from_int(1, Nothing), string("hi there world!", Something)),
        #(number_from_int(2, Nothing), string("hi there world!", Something)),
        #(number_from_int(3, Nothing), string("hi there world!", Something)),
      ],
      Something,
    )
  let hello_world =
    table_from_list(
      [
        #(number_from_int(1, Something), string("hello world!", Something)),
        #(number_from_int(2, Something), whatever),
        #(
          number_from_int(3, Nothing),
          string("mutability is a dream", Something),
        ),
        #(number_from_int(4, Everything), string("goodbye world!", Something)),
      ],
      Something,
    )
  print_object(hello_world)
  //let name = string("hello_world", Something)
  //print_object(name)
  //print_object(hello_world)
  //print_object(gloom_everything)
  //let s =
  //  gloom_everything
  //  |> update_property(name, hello_world)
  //  |> get_property(name)

  //print_object(s)
}
