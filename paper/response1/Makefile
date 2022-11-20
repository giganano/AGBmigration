
TEXCOMPILER := pdflatex

all: response1.pdf

%.pdf: %.tex
	@ $(TEXCOMPILER) $<
	@ $(TEXCOMPILER) $<

.PHONY: clean
clean:
	@ rm -f response1.aux
	@ rm -f response1.log
	@ rm -f response1.out
	@ rm -f response1.pdf
