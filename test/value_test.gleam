import gleam/map
import gleeunit/should
import gleam_value.{FloatValue, MapValue, StringValue, empty_number, insert}

pub fn implicit_value_conversion_test() {
  let s = FloatValue(1.0)
  let key = StringValue("hello")
  let value = StringValue("world")

  let expected =
    [#(empty_number(), s), #(key, value)]
    |> map.from_list
    |> MapValue

  // If we try to insert into a float, it gets converted
  // to a map so that the operation succeeds
  s
  |> insert(key, value)
  |> should.equal(expected)
}
