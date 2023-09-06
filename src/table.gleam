import gleam_value.{GleamValue, MapValue, insert_map_unsafe, new_map}
import object.{GloomAffinity, GloomObject, nothing}
import gleam/map.{Map, new}

pub type GloomPointer

pub type TableValue {
  TableValue(mapping: Map(GloomObject, GloomObject))
}

fn insert_tv(table_value: TableValue, key: GloomObject, value: GloomObject) {
  TableValue(mapping: map.insert(table_value.mapping, key, value))
}

fn new_tv() {
  TableValue(mapping: map.new())
}

fn get_tv(table_value: TableValue, key: GloomObject) -> GloomObject {
  let maybe_value =
    table_value.mapping
    |> map.get(key)
  case maybe_value {
    Ok(value) -> value
    Error(Nil) -> nothing()
  }
}

fn fold_tv(
  over table_value: TableValue,
  from initial: c,
  with fun: fn(c, GloomObject, GloomObject) -> c,
) -> c {
  map.fold(table_value.mapping, initial, fun)
}

fn size_tv(table_value: TableValue) {
  table_value.mapping
  |> map.size
}

pub type GloomTableObject {
  GloomTableObject(
    value: TableValue,
    affinity: GloomAffinity,
    properties: TableValue,
    selectors: TableValue,
    handlers: TableValue,
  )
}

pub fn new(affinity: GloomAffinity) {
  GloomTableObject(
    value: new_tv(),
    affinity: affinity,
    properties: new_tv(),
    selectors: new_tv(),
    handlers: new_tv(),
  )
}

pub fn insert(table: GloomTableObject, key: GloomObject, value: GloomObject) {
  GloomTableObject(
    ..table,
    value: table.value
    |> insert_tv(key, value),
  )
}

pub fn get(table: GloomTableObject, key: GloomObject) {
  table.value
  |> get_tv(key)
}

fn fold(
  over table_value: GloomTableObject,
  from initial: c,
  with fun: fn(c, GloomObject, GloomObject) -> c,
) -> c {
  fold_tv(table_value.value, initial, fun)
}

pub fn size(table: GloomTableObject) {
  table.value
  |> size_tv
}

pub fn to_gleam(table: GloomTableObject) {
  fold(table, new_map(), insert_map_unsafe)
}

pub fn to_object(table: GloomTableObject) {
  GloomObject(
    value: table
    |> to_gleam,
    datatype: GloomTable,
  )
}
