import Std

namespace PackingNine

set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- Exactly the four edges of the undirected integer distance graph D(1,9). -/
def Adj (x y : Int) : Prop :=
  y = x + 1 ∨ y = x - 1 ∨ y = x + 9 ∨ y = x - 9

/-- A walk remembers its length, including zero-length walks. -/
inductive Walk (x : Int) : Nat → Int → Prop where
  | nil : Walk x 0 x
  | step {n : Nat} {y z : Int} : Walk x n y → Adj y z → Walk x (n+1) z

def Packing (k : Nat) (f : Int → Nat) : Prop :=
  (∀ x, 1 ≤ f x ∧ f x ≤ k) ∧
  ∀ (x y : Int) (n : Nat), x ≠ y → f x = f y → Walk x n y → f x < n

/-- The four inequalities say |a|+|b| ≤ n without absolute values. -/
def Budget (a b n : Int) : Prop :=
  a + b ≤ n ∧ a - b ≤ n ∧ -a + b ≤ n ∧ -a - b ≤ n

theorem netSteps {x y : Int} {n : Nat} (h : Walk x n y) :
    ∃ a b : Int, y = x + a + 9*b ∧ Budget a b n := by
  induction h with
  | nil => exact ⟨0, 0, by omega, by unfold Budget; omega⟩
  | step _ edge ih =>
    obtain ⟨a,b,hy,hb⟩ := ih
    unfold Budget at hb ⊢
    rcases edge with e | e | e | e
    · exact ⟨a+1,b,by omega,by omega⟩
    · exact ⟨a-1,b,by omega,by omega⟩
    · exact ⟨a,b+1,by omega,by omega⟩
    · exact ⟨a,b-1,by omega,by omega⟩

def lower (d : Nat) : Nat := d / 9 + min (d % 9) (10 - d % 9)

theorem metricBound (d n : Nat) (a b : Int) (he : (d : Int) = a+9*b)
    (hb : Budget a b n) : lower d ≤ n := by
  unfold Budget at hb
  unfold lower
  have h₁ := Nat.min_le_left (d%9) (10-d%9)
  have h₂ := Nat.min_le_right (d%9) (10-d%9)
  by_cases h : b ≤ (d / 9 : Nat)
  · omega
  · omega

/- Five bits per label, least significant label first. -/
def packed : Nat := 0x504a1204c118441184413848170521184411844158581284c11844118441384a1205a1184411844140481504c1184411844138521286011844118441204a1784c118441184413850158481184411844128581484c1184411844138541204a1184411844168481404c11844118441385c1285211844118441584a1204c118441184413848178501184411844150581284c11844118441384a1205a1184411844148481584c1184411844138501286011844118441204a1704c118441184413852150481184411844128581404c1184411844138561204a1184411844168481484c11844118441385e1285011844118441

def entry (r : Nat) : Nat := (packed >>> (5*r)) % 32

def color (x : Int) : Nat := entry ((x % 384).toNat)

def bounded : Bool := (List.range 384).all fun r =>
  decide (1 ≤ entry r ∧ entry r ≤ 16)

def rowOK (r : Nat) : Bool := (List.range 145).all fun d =>
  decide (d = 0 ∨ entry r ≠ entry ((r+d)%384) ∨ entry r < lower d)

theorem boundsChecked : bounded = true := by decide +kernel

theorem tableChecked : (List.range 384).all rowOK = true := by decide +kernel

theorem labelRange (x : Int) : 1 ≤ color x ∧ color x ≤ 16 := by
  have h := (List.all_eq_true.mp boundsChecked) ((x%384).toNat)
    (List.mem_range.mpr (by omega))
  exact of_decide_eq_true h

theorem positiveSeparation (x y : Int) (n : Nat) (hxy : x < y)
    (same : color x = color y) (a b : Int) (he : y = x+a+9*b)
    (hb : Budget a b n) : color x < n := by
  by_cases hn : 16 < n
  · have h := (labelRange x).2
    omega
  let d := (y-x).toNat
  let r := (x%384).toNat
  have he' : (d : Int) = a+9*b := by dsimp [d]; omega
  have hmet := metricBound d n a b he' hb
  have hd : d < 145 := by
    unfold Budget at hb
    omega
  have hr : r < 384 := by dsimp [r]; omega
  have hrow := List.all_eq_true.mp tableChecked r (List.mem_range.mpr hr)
  have hdigit := List.all_eq_true.mp hrow d (List.mem_range.mpr hd)
  have htab : d = 0 ∨ entry r ≠ entry ((r+d)%384) ∨ entry r < lower d :=
    of_decide_eq_true hdigit
  have hy : (y%384).toNat = (r+d)%384 := by dsimp [r,d]; omega
  change entry r = entry ((y%384).toNat) at same
  rw [hy] at same
  change entry r < n
  have hdpos : 0 < d := by dsimp [d]; omega
  omega

theorem witness : Packing 16 color := by
  refine ⟨labelRange, ?_⟩
  intro x y n hn hc hw
  obtain ⟨a,b,he,hb⟩ := netSteps hw
  by_cases h : x < y
  · exact positiveSeparation x y n h hc a b he hb
  · have hneg : Budget (-a) (-b) n := by unfold Budget at *; omega
    rw [hc]
    exact positiveSeparation y x n (by omega) hc.symm (-a) (-b) (by omega) hneg

theorem exists_packing_16 : ∃ f : Int → Nat, Packing 16 f := ⟨color, witness⟩

#print axioms exists_packing_16
end PackingNine
