import gleam_value.{something}
import repr.{print}
import dtype.{Number}

pub fn main() {
  let o = something(Number)
  print(o)
}
