import object.{GloomAffinity, GloomObject}
import gleam_value.{FloatValue, IntValue}
import dtype.{GloomNumber}
import gleam/map.{Map}

pub type GloomNumberObject {
  IntNumberObject(
    value: Int,
    affinity: GloomAffinity,
    properties: Map(GloomObject, GloomObject),
    selectors: Map(GloomObject, GloomObject),
    handlers: Map(GloomObject, GloomObject),
  )
  FloatNumberObject(
    value: Float,
    affinity: GloomAffinity,
    properties: Map(GloomObject, GloomObject),
    selectors: Map(GloomObject, GloomObject),
    handlers: Map(GloomObject, GloomObject),
  )
}

pub fn to_gleam(object: GloomNumberObject) {
  case object {
    IntNumberObject(value: value, ..) -> IntValue(value: value)
    FloatNumberObject(value: value, ..) -> FloatValue(value: value)
  }
}

pub fn to_gloom_object(object: GloomNumberObject) {
  GloomObject(
    value: object.value
    |> to_gloom_value,
    affinity: object.affinity,
    datatype: GloomNumber,
    properties: object.properties
    |> to_gloom_map_value,
    selectors: object.selectors
    |> to_gloom_map_value,
    handlers: object.handlers
    |> to_gloom_map_value,
  )
}
