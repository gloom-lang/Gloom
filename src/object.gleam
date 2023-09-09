import gleam/map
import gleam/string
import gleam/io
import gleam/int
import gleam/float
import gleam/list
import gleam/string_builder
import template.{template_replace_all}
import affinity.{Everything, GloomAffinity, Nothing, Something}
import gleam_value.{
  FloatValue, GleamValue, IntValue, MapValue, StringValue, empty_map, ensure_map,
  insert, length,
}
import dtype.{GloomType, Number, String, Table}

pub type GloomObject {
  GloomObject(
    datatype: GloomType,
    affinity: GloomAffinity,
    properties: GleamValue,
    selectors: GleamValue,
    handlers: GleamValue,
  )
}

pub opaque type GloomTable {
  GloomTable(map.Map(GloomObject, GloomObject))
}

fn gloom_table_list_repr(table: map.Map(GleamValue, GleamValue)) {
  let key_value_repr = fn(item) {
    let #(key, value) = item
    string_builder.from_string(value_repr(key))
    |> string_builder.append(" =>")
    |> string_builder.append(value_repr(value))
    |> string_builder.append("\n")
  }
  table
  |> map.to_list
  |> list.map(key_value_repr)
  |> string_builder.concat
  |> string_builder.to_string
}

fn value_repr(gloom_value: GleamValue) {
  case gloom_value {
    IntValue(value) -> int.to_string(value)
    FloatValue(value) -> float.to_string(value)
    StringValue(value) -> "'" <> value <> "'"
    MapValue(value) -> gloom_table_list_repr(value)
  }
}

fn datatype_repr(datatype: GloomType) {
  case datatype {
    Number -> "number"
    String -> "string"
    Table -> "table"
  }
}

fn affinity_repr(affinity: GloomAffinity) {
  case affinity {
    Nothing -> "Nothing"
    Everything -> "Everything"
    Something -> "Something"
  }
}

pub fn object_repr(object: GloomObject) {
  case object.datatype {
    Table -> {
      let len = length(object.properties)
      let header_template =
        "\n({affinity} {datatype} containing {length} elements):\n \n {value}"
      template_replace_all(
        header_template,
        map.from_list([
          #("value", value_repr(object.properties)),
          #("datatype", datatype_repr(object.datatype)),
          #("affinity", affinity_repr(object.affinity)),
          #("length", int.to_string(len)),
        ]),
      )
    }
    _ -> {
      let header_template = "\t{value}:{affinity} "
      template_replace_all(
        header_template,
        map.from_list([
          #("value", value_repr(object.properties)),
          #("datatype", datatype_repr(object.datatype)),
          #("affinity", affinity_repr(object.affinity)),
        ]),
      )
    }
  }
}

pub fn print(object: GloomObject) {
  object
  |> object_repr
  |> io.println
}

pub fn nothing(datatype: GloomType) -> GloomObject {
  GloomObject(
    datatype: datatype,
    affinity: Nothing,
    properties: empty_map(),
    selectors: empty_map(),
    handlers: empty_map(),
  )
}

pub fn something(datatype: GloomType) -> GloomObject {
  GloomObject(
    datatype: datatype,
    affinity: Something,
    properties: empty_map(),
    selectors: empty_map(),
    handlers: empty_map(),
  )
}

pub fn everything(datatype: GloomType) -> GloomObject {
  GloomObject(
    datatype: datatype,
    affinity: Everything,
    properties: empty_map(),
    selectors: empty_map(),
    handlers: empty_map(),
  )
}
