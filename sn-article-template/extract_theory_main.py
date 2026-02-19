#!/usr/bin/env python3
"""Extract 5_theory-27_en.tex with all proof blocks removed. Output for sn-article.tex."""
import re

# Proof blocks (1-based line ranges to remove, inclusive)
# \begin{proof}...\end{proof} and \paragraph{Proof of...}\begin{proof}...\end{proof}
SKIP_RANGES = [
    (473, 829),   # first big proof (Lemma PN-TR uniform)
    (832, 876),   # Proof of Theorem pntr-estimation
    (1053, 1369), # uPU-TR Lemma proof
    (1377, 1409), # Proof of Theorem uputr-estimation
    (1582, 1979), # Proof of Lemma nnputr-unif-jp
    (1982, 2014), # Proof of Theorem nnputr-estimation
    (2140, 2154), # last proof (sufficient condition)
]

def main():
    base = "/Users/ryoshibazaki/698ab7786f65e1726124883e"
    src = f"{base}/5_theory-27_en.tex"
    out = f"{base}/sn-article-template/theory_main_only.tex"

    with open(src, "r", encoding="utf-8") as f:
        lines = f.readlines()

    def should_skip(line1):
        for a, b in SKIP_RANGES:
            if a <= line1 <= b:
                return True
        return False

    kept = []
    for i, line in enumerate(lines, start=1):
        if should_skip(i):
            continue
        # Use \section for journal (sn-article uses \section, not \chapter)
        if i == 1 and line.strip().startswith(r"\chapter{"):
            line = line.replace(r"\chapter{", r"\section{", 1)
        kept.append(line)

    with open(out, "w", encoding="utf-8") as f:
        f.writelines(kept)
    print(f"Wrote {len(kept)} lines to {out}")

if __name__ == "__main__":
    main()
