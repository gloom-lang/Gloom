import gleam/map
import gleam/string

fn template_replace(template: String, parameter: String, value: String) {
  string.replace(template, "{" <> parameter <> "}", value)
}

pub fn template_replace_all(
  template: String,
  parameter_mappings: map.Map(String, String),
) {
  map.fold(parameter_mappings, template, template_replace)
}
