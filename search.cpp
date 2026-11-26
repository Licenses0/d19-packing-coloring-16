// Reproduce the successful 16-color search on the odd positions of D(1,9).
// Usage: ./search [seed] [iterations] > discovered.txt
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>

int main(int argc, char** argv) {
    const unsigned seed = argc > 1 ? std::stoul(argv[1]) : 20;
    const int iterations = argc > 2 ? std::stoi(argv[2]) : 650000;
    constexpr int period = 192, first = 4, last = 16, width = last + 1;
    std::mt19937 random(seed);
    std::vector<int> positions;
    std::vector<int> slot(period, -1);
    for (int x = 0; x < period; ++x) {
        if (x % 8 >= 4) {
            slot[x] = static_cast<int>(positions.size());
            positions.push_back(x);
        }
    }
    const int count = static_cast<int>(positions.size());
    // neighbors[i*width+c] contains slots that cannot share color c with i.
    std::vector<std::vector<int>> neighbors(count * width);
    for (int color = first; color <= last; ++color) {
        std::vector<bool> forbidden(period);
        for (int a = -color; a <= color; ++a) {
            for (int b = std::abs(a) - color; b <= color - std::abs(a); ++b) {
                const int delta = a + 9 * b;
                if (delta <= 0 || delta % 2 != 0) continue;
                const int d = (delta / 2) % period;
                forbidden[d] = forbidden[(period - d) % period] = true;
            }
        }
        if (forbidden[0]) return 2;
        for (int i = 0; i < count; ++i) {
            for (int j = 0; j < count; ++j) {
                const int d = (period + positions[i] - positions[j]) % period;
                if (i != j && forbidden[d]) neighbors[i * width + color].push_back(j);
            }
        }
    }
    std::vector<int> colors(count), conflicts(count * width), tabuUntil(count * width);
    auto assign = [&](int i, int color) {
        for (int j : neighbors[i * width + colors[i]]) --conflicts[j * width + colors[i]];
        colors[i] = color;
        for (int j : neighbors[i * width + color]) ++conflicts[j * width + color];
    };
    auto randomColor = [&]() { return first + random() % (width - first); };
    for (int i = 0; i < count; ++i) assign(i, randomColor());

    int record = 10000, overall = 10000, lastImprovement = 0;
    std::vector<int> incumbent;
    for (int step = 0; step < iterations; ++step) {
        int bad = 0;
        for (int i = 0; i < count; ++i) bad += conflicts[i * width + colors[i]];
        bad /= 2;
        if (bad < record) {
            record = bad;
            lastImprovement = step;
            incumbent = colors;
            if (bad < overall) {
                overall = bad;
                if (bad <= 4) std::cerr << "iteration " << step << ", conflicts " << bad << '\n';
            }
            if (!bad) {
                for (int x = 0; x < period; ++x) {
                    const int c = slot[x] < 0 ? 2 + x % 2 : colors[slot[x]];
                    std::cout << "1 " << c << (x + 1 == period ? '\n' : ' ');
                }
                return 0;
            }
        }
        if (step - lastImprovement > 1600 + count * 3) {
            for (int i = 0; i < count; ++i) assign(i, incumbent[i]);
            // Keep the original sampling rule: redraw the stopping test at each pass.
            for (int j = 0; j < 2 + static_cast<int>(random() % (count / 12 + 1)); ++j) {
                const int color = randomColor();
                const int i = random() % count;
                assign(i, color);
            }
            lastImprovement = step;
            if (random() % 7 == 0) record = 9999;
            continue;
        }
        int bestDelta = 999, chosen = -1, nextColor = 0, ties = 0;
        for (int i = 0; i < count; ++i) {
            const int old = conflicts[i * width + colors[i]];
            if (!old) continue;
            for (int c = first; c <= last; ++c) {
                if (c == colors[i]) continue;
                const int delta = conflicts[i * width + c] - old;
                if (tabuUntil[i * width + c] > step && delta + bad >= record) continue;
                if (delta < bestDelta) {
                    bestDelta = delta;
                    chosen = i;
                    nextColor = c;
                    ties = 1;
                } else if (delta == bestDelta && random() % (++ties) == 0) {
                    chosen = i;
                    nextColor = c;
                }
            }
        }
        if (chosen < 0) continue;
        tabuUntil[chosen * width + colors[chosen]] = step + 4 + random() % 9 + std::min(20, bad / 4);
        assign(chosen, nextColor);
    }
    std::cerr << "No certificate within budget. Best conflict count " << overall << '\n';
    return 1;
}
