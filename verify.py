"""Check a periodic word for D(1,9) using breadth-first search on the integers."""
from collections import deque
from pathlib import Path
import argparse
import hashlib
import re


def distances(radius):
    result = {0: 0}
    queue = deque([0])
    while queue:
        x = queue.popleft()
        if result[x] == radius:
            continue
        for step in (-9, -1, 1, 9):
            y = x + step
            if y not in result:
                result[y] = result[x] + 1
                queue.append(y)
    return result


def check(word):
    if len(word) != 384 or set(word) != set(range(1, 17)):
        raise ValueError("Expected a 384-letter word using exactly 1 through 16")
    # Radius 32 exceeds all minima in this certificate. A discovered minimum
    # is exact because BFS processes complete distance layers on Z.
    dist = distances(32)
    best = {}
    for i, color in enumerate(word):
        for offset, length in dist.items():
            if offset <= 0 or word[(i + offset) % len(word)] != color:
                continue
            if color not in best or length < best[color][0]:
                best[color] = (length, i, offset)
    if len(best) != 16:
        raise ValueError("Increase BFS radius to find every exact minimum")
    for color, (length, start, offset) in best.items():
        if length <= color:
            raise ValueError(f"Conflict: color {color} at {start} and {start+offset}, distance {length}")
    return best


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parent
    parser.add_argument("word", type=Path, nargs="?", default=root / "word.txt")
    parser.add_argument("--lean", type=Path, default=root / "Proof.lean")
    args = parser.parse_args()
    word = list(map(int, args.word.read_text().split()))
    result = check(word)
    lean = args.lean.read_text()
    match = re.search(r"def packed : Nat := (0x[0-9a-fA-F]+)", lean)
    if not match or int(match[1], 16) != sum(c << (5*i) for i,c in enumerate(word)):
        raise ValueError("The Lean word differs from the independent certificate")
    print("color count minimum_distance starting_point positive_displacement")
    for color in sorted(result):
        print(color, word.count(color), *result[color])
    damaged = word.copy()
    damaged[1] = 1
    try:
        check(damaged)
    except ValueError as err:
        print("Negative control:", err)
    else:
        raise RuntimeError("The negative control unexpectedly passed")
    print("SHA-256(word.txt):", hashlib.sha256(args.word.read_bytes()).hexdigest())
