import Lake
open Lake DSL

package asymptoticSpine where

require staircaseLogic from "../staircase_logic"

@[default_target]
lean_lib AsymptoticSpine where
  roots := #[`AsymptoticSpine]
