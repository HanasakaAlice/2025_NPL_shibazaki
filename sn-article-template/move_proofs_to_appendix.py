#!/usr/bin/env python3
"""
Move all proof blocks from main text to Appendix in sn-article.tex.
Run from sn-article-template/ as: python3 move_proofs_to_appendix.py
Backup is written to sn-article.tex.bak
"""
def main():
    with open("sn-article.tex") as f:
        content = f.read()

    # Backup
    with open("sn-article.tex.bak", "w") as f:
        f.write(content)

    lines = content.splitlines(keepends=True)
    n = len(lines)

    # Define blocks (1-indexed line ranges inclusive): (start, end), and whether to include paragraph above
    # Block: (start_line, end_line) - we remove these and append to appendix_texts
    blocks = [
        (999, 1355),   # 1: Proof of Lemma pntr-unif-jp
        (1358, 1402),  # 2: \paragraph{Proof of Theorem pntr-estimation} + proof
        (1579, 1895),  # 3: Proof of Lemma uputr-unif-jp
        (1903, 1935),  # 4: \paragraph{Proof of Theorem uputr-estimation} + proof
        (2108, 2505),  # 5: \paragraph{Proof of Lemma nnputr-unif-jp} + proof
        (2508, 2540),  # 6: \paragraph{Proof of Theorem nnputr-estimation} + proof
        (2666, 2680),  # 7: Proof of sufficient condition theorem
    ]

    appendix_texts = []
    for start, end in blocks:
        if start < 1 or end > n:
            print(f"Block {start}-{end} out of range (file has {n} lines). Skip or fix line numbers.")
            continue
        chunk = "".join(lines[i] for i in range(start - 1, end))
        appendix_texts.append(chunk)

    # Remove blocks from end to start so indices don't shift
    for start, end in reversed(blocks):
        if start < 1 or end > len(lines):
            continue
        # 0-indexed
        lines = lines[: start - 1] + lines[end:]

    # Build new content
    new_content = "".join(lines)

    # Replace the whole appendices block
    start_marker = "\\begin{appendices}"
    idx = new_content.find(start_marker)
    if idx == -1:
        print("Could not find \\begin{appendices}")
        return
    end_idx = new_content.find("\\end{appendices}", idx)
    if end_idx == -1:
        print("Could not find \\end{appendices}")
        return
    new_appendices_block = (
        "\\begin{appendices}\n\n"
        "\\section{Appendix}\\label{sec:appendix}\n\n"
        "This appendix contains proofs that are omitted from the main text.\n\n"
        + "\n\n".join(appendix_texts)
        + "\n\n\\end{appendices}"
    )
    new_content = (
        new_content[:idx]
        + new_appendices_block
        + new_content[end_idx + len("\\end{appendices}"):]
    )

    with open("sn-article.tex", "w") as f:
        f.write(new_content)
    print("Done. Proofs moved to Appendix. Backup: sn-article.tex.bak")

if __name__ == "__main__":
    main()
