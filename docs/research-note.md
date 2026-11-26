# A periodic 16-color packing of D(1, 9)

Computational research note · 26 November 2026

**Theorem.** The integer distance graph D(1, 9) admits a packing coloring with 16 colors and period 384.

## The problem

The vertices of D(1, 9) are the integers. An edge joins two vertices whose absolute difference is 1 or 9. In a packing coloring, any two distinct vertices of color *c* must have graph distance strictly greater than *c*. The packing chromatic number is the smallest possible number of colors.

Ekstein, Holub and Lidický proved a lower bound of 13 in Lemma 6. Zhang gave a period-360 coloring with 17 colors in Theorem 24 and Supplement S7. The construction here improves that upper bound by one, giving **13 ≤ χρ(D(1, 9)) ≤ 16**. The lower bound comes from the literature. The exact minimum remains open. [Ekstein, Holub and Lidický](https://arxiv.org/abs/1105.5652) · [Zhang](https://arxiv.org/abs/2609.09018)

## Why a finite check proves the theorem

Let *w* be the 384-entry word in the certificate below. For each integer *x*, give it the color at index *x* mod 384 in *w*, using residues 0 through 383. This defines the coloring at negative integers as well.

Suppose a conflict exists. Its endpoints would have the same color *c* and be joined by a walk of at most *c* steps. Each step changes the integer by at most 9, so their positive displacement *d* would satisfy 1 ≤ *d* ≤ 9*c* ≤ 144. Translate the smaller endpoint to one of the 384 start residues. The larger endpoint may cross the period boundary, so its index must also be reduced modulo 384.

The distance for a positive displacement can be computed exactly. Write *d* = 9*q* + *r*, with 0 ≤ *r* < 9. If *b* is the net number of forward nine-steps, the shortest walk with that value of *b* has length |*b*| + |*d* − 9*b*|. On the integer range *b* ≤ *q*, the minimum occurs at *q*. On the range *b* ≥ *q* + 1, the minimum occurs at *q* + 1. Therefore

**dist(0, d) = q + min(r, 10 − r).**

For each of 384 start residues and each of 144 positive displacements, the certificate either assigns different colors or gives a distance greater than the common color. These 55,296 comparisons, together with the color-range check, establish the theorem on the full graph.

## The certificate

Write the residue of a vertex modulo 384 as 16*j* + *s*, where 0 ≤ *j* < 24 and 0 ≤ *s* < 16. Every even *s* has color 1. Offsets 1 and 5 have color 2, and offsets 3 and 7 have color 3. This fixes 288 entries. The table supplies the remaining 96. The left and right halves list blocks 0–11 and 12–23, respectively.

| Block | s = 9 | 11 | 13 | 15 | Block | s = 9 | 11 | 13 | 15 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 8 | 5 | 15 | 7 | 12 | 9 | 5 | 14 | 7 |
| 1 | 6 | 9 | 4 | 13 | 13 | 6 | 8 | 4 | 13 |
| 2 | 5 | 4 | 11 | 7 | 14 | 5 | 4 | 10 | 7 |
| 3 | 6 | 8 | 12 | 5 | 15 | 6 | 9 | 12 | 5 |
| 4 | 4 | 10 | 9 | 7 | 16 | 4 | 11 | 8 | 7 |
| 5 | 6 | 14 | 5 | 4 | 17 | 6 | 15 | 5 | 4 |
| 6 | 16 | 5 | 8 | 7 | 18 | 16 | 5 | 9 | 7 |
| 7 | 6 | 11 | 4 | 9 | 19 | 6 | 10 | 4 | 8 |
| 8 | 13 | 4 | 5 | 7 | 20 | 13 | 4 | 5 | 7 |
| 9 | 6 | 5 | 12 | 10 | 21 | 6 | 5 | 12 | 11 |
| 10 | 8 | 15 | 4 | 7 | 22 | 9 | 14 | 4 | 7 |
| 11 | 6 | 4 | 5 | 11 | 23 | 6 | 4 | 5 | 10 |

For example, color 16 occurs at residues 105 and 297. Their displacement is 192 = 21 × 9 + 3. The distance formula gives 24 steps, attained by 21 nine-steps and three one-steps.

### Same-color distances

An independent Python implementation starts at 0 and explores the four legal moves by breadth-first search through distance 32 on the integers. For every color it finds a same-color pair within that radius. Exploring complete layers gives the exact minimum in each case, including pairs spanning two periods.

| Color | Count per period | Minimum distance | Color | Count per period | Minimum distance |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 192 | 2 | 9 | 7 | 10 |
| 2 | 48 | 4 | 10 | 5 | 12 |
| 3 | 48 | 4 | 11 | 5 | 12 |
| 4 | 16 | 6 | 12 | 4 | 14 |
| 5 | 16 | 6 | 13 | 4 | 14 |
| 6 | 12 | 8 | 14 | 3 | 16 |
| 7 | 12 | 8 | 15 | 3 | 16 |
| 8 | 7 | 10 | 16 | 2 | 24 |

## How the coloring was found

The human initiator asked whether an AI could select an open problem and make verifiable progress on it. ChatGPT chose this graph after comparing candidates in the Erdős Problems database with open distance-graph coloring problems. The search of the literature on 26 November 2026 found Zhang's 17-color construction and did not locate an earlier 16-color certificate. The human initiator supplied the research brief. The AI carried out the mathematical and computational work. [Distance-graph problem listing](https://www.emergentmind.com/open-problems/exact-packing-chromatic-numbers-d1-6-d1-8-d1-9) · [Number-theory candidate considered](https://www.erdosproblems.com/123)

Fix color 1 on even vertices and index the odd vertices by writing them as 2*u* + 1. For two odd vertices, any walk between them has even length. Thus, for both color 2 and color 3, a conflict can occur at two steps, giving forbidden positive differences 1, 4, 5 and 9 in the compressed index. A finite enumeration modulo 40 gave three two-color occupancy patterns up to translation and reflection. The successful period-eight pattern places colors 2, 3, 2, 3 on its first four positions and reserves its last four for higher colors.

A budget-limited SAT screen returned an undetermined result on all 92 runs. A C++ tabu search then varied assignments to the remaining positions. At compressed period 192 and seed 20, iteration 279008 had one conflict left. Iteration 314635 reached zero, giving period 384 on the original integer graph. A separate replay of the successful branch reproduced the word byte for byte.

The follow-up search tested 15 colors in 108 runs of 250,000 iterations each. Its best assignment still had three conflicting pairs. This leaves the possibility of a 15-color packing open.

## Formal verification

The Lean 4.19.0 development defines the four edges on the integers and defines walks inductively with their lengths. Its final theorem, `PackingNine.exists_packing_16`, asserts that a coloring exists with values from 1 to 16, and that every walk between distinct same-color vertices has length greater than their color. The proof establishes the metric lower bound needed for this statement and checks the finite certificate with `decide +kernel`.

The audit builds with trust level zero and treats warnings as errors. The transitive axiom report lists only `propext`, `Classical.choice` and `Quot.sound`. There are no proof placeholders, user-declared axioms or native-computation axioms in the proof. Changing the color at vertex 1 from 2 to 1 makes Lean reject the finite-table theorem. The Python verifier independently identifies the conflicting edge from 0 to 1.

## References

1. Jan Ekstein, Přemysl Holub and Bernard Lidický. *Packing Chromatic Number of Distance Graphs.* See Lemma 6 for the lower bound 13. [arXiv:1105.5652](https://arxiv.org/abs/1105.5652)
2. Enkai Zhang. *Density regions, integer certificates and packing colorings of distance graphs.* See Theorem 24 and Supplements S7–S8 for the period-360 upper-bound witness and its checked distances. [arXiv:2609.09018](https://arxiv.org/abs/2609.09018) · [Supporting data](https://zenodo.org/records/22651508)
