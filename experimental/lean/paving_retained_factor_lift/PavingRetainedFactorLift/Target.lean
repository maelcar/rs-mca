/-!
# Typed target for the original RF3/RF3' retained-factor lift

This file deliberately introduces no axiom.  It provides a proposition-valued
interface in which a future formalization can package the finite-field,
polynomial, slope, and chosen-support data from
`ass:retained-factor-lift`.  The target remains an explicit hypothesis of the
only theorem that consumes it.  The paper-proved RF3'' global-degree bridge has
a separate typed interface in `GlobalDegreeBridge.lean`.
-/

namespace PavingRetainedFactorLift.Target

set_option autoImplicit false

universe u

/-- Abstract interface for instances of the v9.2 retained-factor-lift claim.
`antecedent` is intended to hold RF1--RF3' plus the polynomial/root/support
data; `simultaneouslyExplained` is its asserted conclusion. -/
structure RetainedFactorLiftInterface (Instance : Type u) where
  antecedent : Instance → Prop
  simultaneouslyExplained : Instance → Prop

/-- The unresolved original RF3/RF3' proposition corresponding to
`ass:retained-factor-lift`.  Merely defining this proposition does not assert
or prove it; it is distinct from the conservative RF3'' bridge. -/
def RetainedFactorLiftTarget {Instance : Type u}
    (I : RetainedFactorLiftInterface Instance) : Prop :=
  ∀ x, I.antecedent x → I.simultaneouslyExplained x

/-- Honest conditional consumer: a retained-lift conclusion follows only when
the target itself is supplied as a hypothesis. -/
theorem useRetainedFactorLiftTarget {Instance : Type u}
    (I : RetainedFactorLiftInterface Instance)
    (hLift : RetainedFactorLiftTarget I)
    (x : Instance) (hx : I.antecedent x) :
    I.simultaneouslyExplained x :=
  hLift x hx

#print axioms useRetainedFactorLiftTarget

end PavingRetainedFactorLift.Target
