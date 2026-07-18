import Lake
open Lake DSL

package «inv_tail_closure» where

@[default_target]
lean_lib «InvTailClosure» where
  roots := #[`InvTailClosure]
