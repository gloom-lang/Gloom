import gleam/float
import gleeunit/should
import gleam_value.{
  FloatValue, StringValue, empty_number, from_list, get, insert,
}

pub fn implicit_insert_map_conversion_test() {
  let s = FloatValue(1.0)
  let key = StringValue("hello")
  let value = StringValue("world")
  let expected =
    [#(empty_number(), s), #(key, value)]
    |> from_list
  // If we try to insert into a float as if it were a map, 
  // the float gets silently converted to a map so that the 
  // operation succeeds. yay! :)
  s
  |> insert(key, value)
  |> should.equal(expected)
}

pub fn implicit_get_map_conversion_test() {
  let s = FloatValue(1.0)
  let key = StringValue("hello")

  // If we try to get a key from a float as if it were a map,
  // we do our best to please despite the difficult circumstances
  // and so return a float value that gives empty vibes instead
  let value =
    s
    |> get(key)

  let assert FloatValue(x) = value
  x
  |> float.loosely_equals(0.0, 0.0001)
  |> should.be_true
}
