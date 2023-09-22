import affinity.{Everything, Nothing, Something, affinity_max}

pub fn affinity_max_test() {
  let assert Nothing = affinity_max(Nothing, Nothing)
  let assert Nothing = affinity_max(Nothing, Something)
  let assert Nothing = affinity_max(Something, Nothing)
  let assert Nothing = affinity_max(Nothing, Everything)
  let assert Nothing = affinity_max(Everything, Nothing)

  let assert Something = affinity_max(Something, Something)
  let assert Everything = affinity_max(Something, Everything)
  let assert Everything = affinity_max(Everything, Something)

  let assert Everything = affinity_max(Everything, Everything)
}
