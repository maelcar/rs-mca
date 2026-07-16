import Lake
open Lake DSL

package «shell_mass_spectral_law» where

@[default_target]
lean_lib «ShellMassSpectralLaw» where
  roots := #[`ShellMassSpectralLaw]
