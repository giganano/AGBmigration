
TEXCOMPILER := pdflatex 
BIBCOMPILER := bibtex 
TEXSOURCES := $(wildcard *.tex) 
TARGETS := $(TEXSOURCES:.tex=.pdf) 

all: $(TARGETS) 

%.pdf: $(TEXSOURCES) ../notes.bib 
	@ $(TEXCOMPILER) $(basename $<) 
	@ $(BIBCOMPILER) $(basename $<) 
	@ $(TEXCOMPILER) $(basename $<) 
	@ $(TEXCOMPILER) $(basename $<)  

.PHONY: clean 
clean: 
	@ rm -f *.aux 
	@ rm -f *.bbl 
	@ rm -f *.blg 
	@ rm -f *.log 
	@ rm -f *.out 
	@ rm -f onezone.pdf 
