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

pub fn new_map() -> GleamValue {
  MapValue(value: map.new())
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

pub fn insert_map_unsafe(
  maybe_map: GleamValue,
  key: GleamValue,
  value: GleamValue,
) -> GleamValue {
  case maybe_map {
    MapValue(gleam_map) -> {
      MapValue(map.insert(gleam_map, key, value))
    }
    _ -> new_map()
  }
}
