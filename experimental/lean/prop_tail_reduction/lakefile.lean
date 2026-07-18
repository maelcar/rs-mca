import Lake
open Lake DSL

package «prop_tail_reduction» where

@[default_target]
lean_lib «PropTailReduction» where
  roots := #[`PropTailReduction]
