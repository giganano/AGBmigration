
TEXCOMPILER 		:= pdflatex 
BIBCOMPILER 		:= bibtex 
TEXSOURCES 			:= $(wildcard *.tex */*.tex) 
SUBDIRS 			:= $(wildcard */) 

all: notes.pdf $(SUBDIRS) 

notes.pdf: notes.tex notes.bib $(TEXSOURCES) 
	@ $(TEXCOMPILER) notes 
	@ $(BIBCOMPILER) notes 
	@ $(TEXCOMPILER) notes 
	@ $(TEXCOMPILER) notes 

.PHONY: $(SUBDIRS) 
$(SUBDIRS): 
	@ $(MAKE) -C $@ 

.PHONY: clean 
clean: 
	@ rm -f *.aux 
	@ rm -f *.bbl 
	@ rm -f *.blg 
	@ rm -f *.log 
	@ rm -f *.out 
	@ rm -f notes.pdf 
	@ for i in $(SUBDIRS) ; do \
		$(MAKE) -C $$i clean ; \
	done 
