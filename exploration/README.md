# Discovery experiments

The search treated the even integers as color 1 and indexed odd vertices by writing them as $2u+1$. Periods in these logs refer to the compressed index *u*. A period of 192 in the successful run therefore gives a period of 384 on the original graph.

| Stage | Code and recorded output | Outcome |
| --- | --- | --- |
| Low-color patterns | [tilings.py](tilings.py) | Enumerated exact covers modulo 40. There were eight single-color covers, 20 unordered disjoint pairs and three union patterns up to rotation and reflection. These counts concern the finite enumeration. |
| SAT screening | [sat_search.py](sat_search.py), [sat-results.txt](sat-results.txt) | All 92 budget-limited runs returned `None`, meaning the solver exhausted its budget with the answer undetermined. |
| Initial tabu search | [original_search.cpp](original_search.cpp), [batch.py](batch.py), [huntlog](huntlog) | Tested several templates and periods with 16 and 17 colors. |
| Focused 16-color search | [focus.py](focus.py), [focuslog](focuslog) | Compressed period 192, template 0, seed 20. The successful assignment appears as a zero-conflict line. |
| Follow-up 15-color search | [try15.py](try15.py), [15log](15log) | 108 runs of 250,000 iterations each. The smallest residual conflict count was three. The existence of a 15-color packing remains open. |

## Reading the logs

For a progress line, the columns are compressed period, color limit, template number, random seed, zero-based iteration and conflict count. A line beginning with `end` gives the best conflict count after a run used its budget. The full word used in the proof is [word.txt](../word.txt).

The five templates, in order, are `####....`, `##.#..#.`, `#.`, `####.....`, and `.`. A hash marks a position reserved for the low colors. A dot marks a search position. In the successful template, colors 2 and 3 occupy the first four positions of each eight-position block in the order 2, 3, 2, 3. The other four positions take colors 4 through 16.

## Replaying the experiments

For the single successful branch, use the [short replay in the main README](../README.md#replay-the-discovery). The following optional commands reproduce the exploratory setup on a POSIX system. Run them from the repository root, starting with a fresh `tmp/` directory. The batch scripts append to logs and the focused scripts stop scheduling work once they see a matching witness. Concurrent runs may finish in a different order.

```sh
mkdir -p tmp
g++ -O3 -std=c++17 exploration/original_search.cpp -o tmp/hunt
python3 exploration/tilings.py
python3 exploration/batch.py
python3 exploration/focus.py
python3 exploration/try15.py
```

The optional SAT stage used `python-sat==1.9.dev25` and CaDiCaL 1.9.5. With that Python package installed and `tmp/` present, run `python3 exploration/sat_search.py 1200`. The 1200 argument is a conflict budget for each solver call. The main certificate checks use Python's standard library and Lean's bundled libraries.
