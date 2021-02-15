
all: yields.pdf 
texcompiler = pdflatex 
bibcompiler = bibtex 

yields.pdf: yields.tex yields.bib 
	@ $(texcompiler) yields 
	@ $(bibcompiler) yields 
	@ $(texcompiler) yields  
	@ $(texcompiler) yields 

.PHONY: clean 
clean: 
	@ rm -f *.aux 
	@ rm -f *.bbl 
	@ rm -f *.blg 
	@ rm -f *.log 
	@ rm -f *.out 
	@ rm -f yields.pdf 
