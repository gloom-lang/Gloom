pub type GloomAffinity {
  Nothing
  Everything
  Something
}

pub fn affinity_max(left: GloomAffinity, right: GloomAffinity) -> GloomAffinity {
  case left, right {
    Nothing, _ -> left
    _, Nothing -> right
    Everything, Everything -> left
    Everything, Something -> left
    Something, Everything -> right
    Something, Something -> left
  }
}
