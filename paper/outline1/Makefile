
TEXSOURCES 		:= $(wildcard *.tex) 
TEXCOMPILER		:= pdflatex 
BIBCOMPILER 	:= bibtex 

all: ms.pdf 

ms.pdf: ms.bib $(TEXSOURCES) *.pdf 
	@ $(TEXCOMPILER) $(basename $<) 
	@ $(BIBCOMPILER) $(basename $<) 
	@ $(TEXCOMPILER) $(basename $<) 
	@ $(TEXCOMPILER) $(basename $<) 

.PHONY: clean 
clean: 
	@ rm -rf *.aux 
	@ rm -rf *.log 
	@ rm -rf *.out 
	@ rm -rf ms.pdf 


