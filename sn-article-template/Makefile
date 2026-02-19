# LaTeX + BibTeX の正しいビルド順序:
# 1. pdflatex → .aux に \citation を書き出す
# 2. bibtex → .bbl を生成（BSTINPUTS で bst/ を参照）
# 3. pdflatex × 2 → 参照・文献を確定

MAIN = sn-article
BSTINPUTS := bst/:

.PHONY: all clean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex sn-bibliography.bib
	pdflatex -synctex=1 -interaction=nonstopmode $(MAIN).tex
	BSTINPUTS="$(BSTINPUTS)" bibtex $(MAIN)
	pdflatex -synctex=1 -interaction=nonstopmode $(MAIN).tex
	pdflatex -synctex=1 -interaction=nonstopmode $(MAIN).tex

clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out $(MAIN).toc
	rm -f $(MAIN).lof $(MAIN).lot $(MAIN).loa $(MAIN).synctex.gz
