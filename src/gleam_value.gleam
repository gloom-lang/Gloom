import dtype.{GloomType, Number, String, Table}
import affinity.{Everything, GloomAffinity, Nothing, Something}
import gleam/map
import gleam/string
import gleam/int
import gleam/float

pub type GloomObject {
  GloomObject(
    name: String,
    datatype: GloomType,
    affinity: GloomAffinity,
    properties: GleamValue,
  )
}

pub type GleamValue {
  IntValue(value: Int)
  FloatValue(value: Float)
  StringValue(value: String)
  MapValue(value: map.Map(GleamValue, GleamValue))
  ObjectValue(value: GloomObject)
}

pub fn from_list(list: List(#(GleamValue, GleamValue))) -> GleamValue {
  MapValue(map.from_list(list))
}

pub fn empty_number() {
  FloatValue(0.0)
}

pub fn empty_string() {
  StringValue("")
}

pub fn empty_map() {
  MapValue(map.new())
}

pub fn from_string(string: String) {
  StringValue(string)
}

pub fn from_float(float: Float) {
  FloatValue(float)
}

pub fn from_int(int: Int) {
  IntValue(int)
}

pub fn empty_value(datatype: GloomType) {
  case datatype {
    Number -> empty_number()
    String -> empty_string()
    Table -> empty_map()
  }
}

pub fn gloom_type(gleam_value: GleamValue) {
  case gleam_value {
    IntValue(_) -> Number
    FloatValue(_) -> Number
    StringValue(_) -> String
    MapValue(_) -> Table
    ObjectValue(object) -> object.datatype
  }
}

pub fn length(value: GleamValue) -> Int {
  case value {
    IntValue(gleam_value) ->
      gleam_value
      |> int.to_string
      |> string.length
    FloatValue(gleam_value) ->
      gleam_value
      |> float.to_string
      |> string.length
    StringValue(gleam_value) ->
      gleam_value
      |> string.length
    MapValue(gleam_value) ->
      gleam_value
      |> map.size
    ObjectValue(object) ->
      object.properties
      |> length
  }
}

pub fn ensure_map_value(value: GleamValue) -> GleamValue {
  case value {
    // Yay! We got a map!! Nothing weird has to happen
    MapValue(_) -> value
    // This is fine too, just a little more work
    _ -> {
      // Perfectly sensible behavior here is to turn the non-map
      // gleam value into a map with the gleam value
      // as value, and the key is something that exudes
      // emptiness. That makes everyone happy
      let empty_gloom_value =
        value
        |> gloom_type
        |> empty_value
      empty_map()
      |> insert(empty_gloom_value, value)
    }
  }
}

pub fn ensure_object_value(value: GleamValue) -> GleamValue {
  case value {
    ObjectValue(_) -> value
    _ ->
      value
      |> gloom_type
      |> something
      |> set_property(
        "value"
        |> from_string,
        value,
      )
      |> ObjectValue
  }
}

pub fn insert(
  maybe_map: GleamValue,
  key: GleamValue,
  value: GleamValue,
) -> GleamValue {
  case maybe_map {
    // Happy case! It's a map! Insert the nice key and value
    // and go on with our lives
    MapValue(gleam_map) -> {
      MapValue(map.insert(gleam_map, key, value))
    }
    // Sad case. It's not a map. But we live to please. So we 
    // make it a map :) that way everyone is happy :)
    _ ->
      ensure_map_value(maybe_map)
      |> insert(key, value)
  }
}

pub fn get(maybe_map: GleamValue, key: GleamValue) {
  let assert MapValue(gleam_map) = ensure_map_value(maybe_map)
  case map.get(gleam_map, key) {
    Ok(value) -> value
    Error(Nil) -> empty_number()
  }
}

pub fn set_property(object: GloomObject, key: GleamValue, value: GleamValue) {
  GloomObject(
    ..object,
    properties: object.properties
    |> insert(key, value),
  )
}

pub fn get_property(object: GloomObject, key: GleamValue) {
  let raw_value =
    object.properties
    |> get(key)
  case raw_value {
    ObjectValue(value) -> value
    _ -> nothing(object.datatype)
  }
}

pub fn nothing(datatype: GloomType) -> GloomObject {
  GloomObject(
    name: "object",
    datatype: datatype,
    affinity: Nothing,
    properties: empty_map(),
  )
}

pub fn something(datatype: GloomType) -> GloomObject {
  GloomObject(
    name: "object",
    datatype: datatype,
    affinity: Something,
    properties: empty_map(),
  )
}

pub fn everything(datatype: GloomType) -> GloomObject {
  GloomObject(
    name: "object",
    datatype: datatype,
    affinity: Everything,
    properties: empty_map(),
  )
}
