PDFLATEX = pdflatex
BIBTEX = bibtex
TEXFILE = final_report_atishaya

all: $(TEXFILE).pdf

$(TEXFILE).pdf: $(TEXFILE).tex
	$(PDFLATEX) $(TEXFILE)
	$(BIBTEX) $(TEXFILE)
	$(PDFLATEX) $(TEXFILE)
	$(PDFLATEX) $(TEXFILE)

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.pdf

.PHONY: all clean
