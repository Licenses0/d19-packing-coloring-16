# A 16-color packing of the integer distance graph D(1, 9)

Color every integer with a label from 1 to 16. A move changes an integer by 1 or 9 in either direction. Can the colors be arranged so that any two distinct integers of color *c* are more than *c* moves apart? The 384 entries in [word.txt](word.txt), repeated in both directions, give such an arrangement.

This proves $\chi_\rho(D(1,9)) \leq 16$. Ekstein, Holub and Lidický proved a lower bound of 13. Zhang gave a 17-color construction of period 360 in 2026. The present construction narrows the interval to **13 through 16**. The exact minimum remains open. [Earlier lower bound](https://arxiv.org/abs/1105.5652) · [17-color upper bound](https://arxiv.org/abs/2609.09018)

## Check the certificate

From the repository root, run the independent verifier with Python 3. It uses only the standard library.

```sh
python3 verify.py
```

It computes the minimum distance for each color by breadth-first search on the integers, checks that the Lean proof encodes exactly the same 384 labels, and deliberately changes one label to check that the resulting conflict is detected. For color 16, the minimum distance is **24**. [Expected output](results/verification.txt)

To check the theorem in Lean, use the pinned Lean **4.19.0** toolchain.

```sh
python3 audit.py
```

The script accepts an explicit Lean executable as its first argument. It checks the proof with trust level zero, audits the transitive axioms of the final theorem, and tests that the kernel rejects a corrupted certificate. The proof imports only `Std`. On Windows, `py -3` can replace `python3` in these commands. [Lean source](Proof.lean) · [Audit output](results/lean-audit.txt)

## Read the construction

The [research note](docs/research-note.md) gives the full coloring in a 24-row table and proves why 55,296 finite checks cover the whole integer graph, including pairs across a period boundary. A [printable PDF](docs/research-note.pdf) contains the same note.

## Replay the discovery

The C++17 search reproduces the certificate from seed 20. Run these commands in a POSIX shell with a C++ compiler.

```sh
g++ -O3 -std=c++17 search.cpp -o search
./search 20 650000 > reproduced.txt
cmp word.txt reproduced.txt
```

With GCC 14.2.0 on x86-64, the search first reached zero conflicts at iteration 314635 (counting from zero). The replay writes the coloring to standard output and progress to standard error. [Replay log](results/replay.log) · [Exploratory experiments and logs](exploration/README.md)

## How this project started

The human initiator wanted to see whether an AI could find and verify a small mathematical result when given freedom to choose the problem. They set the goal and requested independent checks and a Lean proof. OpenAI’s ChatGPT selected the graph, searched the literature, wrote and ran the search and checkers, constructed the coloring, and prepared the proof and report. The literature search on 26 November 2026 located Zhang’s bound of 17 and did not locate an earlier 16-color certificate. The certificate and verification code are available here for independent review.
