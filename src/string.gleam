import gleam_value.{GleamValue, StringValue}
import dtype.{GloomType}
import table.{GloomTableObject}
import object.{GloomAffinity, GloomObject}
import gleam/map.{Map}

pub type GloomStringObject {
  GloomStringObject(
    value: String,
    affinity: GloomAffinity,
    datatype: GloomType,
    properties: GloomTableObject,
    selectors: GloomTableObject,
    handlers: GloomTableObject,
  )
}

pub fn to_gleam(object: GloomStringObject) {
  StringValue(object.value)
}

pub fn to_gloom_object(object: GloomStringObject) {
  GloomObject(
    value: object.value
    |> to_string_value,
    affinity: object.affinity,
    datatype: GloomString,
    properties: object.properties
    |> to_gloom_map_value,
    selectors: object.selectors
    |> to_gloom_map_value,
    handlers: object.handlers
    |> to_gloom_map_value,
  )
}
