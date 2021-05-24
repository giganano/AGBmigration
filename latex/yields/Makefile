
TEXCOMPILER 		:= pdflatex 
BIBCOMPILER 		:= bibtex 
TEXSOURCES 			:= $(wildcard *.tex) 
TEXOUTPUTS 			:= $(TEXSOURCES:.tex=.pdf) 

all: $(TEXOUTPUTS) 

%.pdf: %.tex ../notes.bib 
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
	@ for i in $(TEXOUTPUTS) ; do \
		rm -f $$i ; \
	done 	

