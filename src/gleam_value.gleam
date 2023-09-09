import dtype.{GloomType, Number, String, Table}
import gleam/map
import gleam/string
import gleam/int
import gleam/float

pub type GleamValue {
  IntValue(value: Int)
  FloatValue(value: Float)
  StringValue(value: String)
  MapValue(value: map.Map(GleamValue, GleamValue))
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
    // make it a map :) that way everyone is happy
    _ ->
      ensure_map(maybe_map)
      |> insert(key, value)
  }
}

pub fn ensure_map(value: GleamValue) -> GleamValue {
  case value {
    // Yay! We got a map!! Nothing weird has to happen
    MapValue(_) -> value
    // This is fine too, just a little more work
    _ -> {
      // Perfectly sensible behavior here is to turn the non-map
      // gleam value into a map with the gleam value
      // as value, and the key is something that exudes
      // emptiness. That makes everyone is happy
      let empty_gloom_value =
        value
        |> gloom_type
        |> empty_value
      empty_map()
      |> insert(empty_gloom_value, value)
    }
  }
}

pub fn get(maybe_map: GleamValue, key: GleamValue) {
  let assert MapValue(gleam_map) = ensure_map(maybe_map)
  case map.get(gleam_map, key) {
    Ok(value) -> value
    Error(Nil) -> empty_number()
  }
}
