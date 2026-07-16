import Lake
open Lake DSL

package «product_profile_transfer» where

@[default_target]
lean_lib «ProductProfileTransfer» where
  roots := #[`ProductProfileTransfer]
