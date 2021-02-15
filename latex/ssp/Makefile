
all: ssp.pdf 
texcompiler = pdflatex 
bibcompiler = bibtex 

ssp.pdf: ssp.tex 
	@ $(texcompiler) ssp 
	@ $(bibcompiler) ssp 
	@ $(texcompiler) ssp 
	@ $(texcompiler) ssp 

.PHONY: clean 
clean: 
	@ rm -f *.aux 
	@ rm -f *.bbl 
	@ rm -f *.blg 
	@ rm -f *.log 
	@ rm -f *.out 
	@ rm -f ssp.pdf 
