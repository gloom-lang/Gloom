import gleam/map
import gleam/string
import gleam/io
import gleam/int
import gleam/float
import gleam/list
import gleam/string_builder
import template.{template_replace_all}
import gleam_value.{
  FloatValue, GleamValue, IntValue, MapValue, StringValue, length, new_map,
}
import dtype.{GloomNumber, GloomString, GloomTable, GloomType}

pub type GloomObject {
  GloomObject(
    datatype: GloomType,
    affinity: GloomAffinity,
    properties: GleamValue,
    selectors: GleamValue,
    handlers: GleamValue,
  )
}

pub type GloomAffinity {
  Nothing
  Everything
  Something
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
    GloomNumber -> "number"
    GloomString -> "string"
    GloomTable -> "table"
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
    GloomTable -> {
      let len = length(object.value)
      let header_template =
        "\n({affinity} {datatype} containing {length} elements):\n \n {value}"
      template_replace_all(
        header_template,
        map.from_list([
          #("value", value_repr(object.value)),
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
          #("value", value_repr(object.value)),
          #("datatype", datatype_repr(object.datatype)),
          #("affinity", affinity_repr(object.affinity)),
        ]),
      )
    }
  }
}

pub fn print_object(object: GloomObject) {
  object
  |> object_repr
  |> io.println
}

pub fn nothing() -> GloomObject {
  GloomObject(
    value: IntValue(value: 0),
    datatype: GloomNumber,
    affinity: Nothing,
    properties: new_map(),
    selectors: new_map(),
    handlers: new_map(),
  )
}

pub fn everything() -> GloomObject {
  GloomObject(
    value: IntValue(value: 1),
    datatype: GloomNumber,
    affinity: Everything,
    properties: new_map(),
    selectors: new_map(),
    handlers: new_map(),
  )
}
