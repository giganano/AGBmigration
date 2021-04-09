
TEXCOMPILER := pdflatex 
BIBCOMPILER := bibtex 
TEXSOURCES := $(wildcard *.tex) 
SUBSOURCES := $(wildcard */*.tex) 
TARGETS := $(TEXSOURCES:.tex=.pdf) 
SUBDIRS := $(wildcard */) 

all: $(TARGETS) $(SUBDIRS) 

%.pdf: $(TEXSOURCES) $(SUBSOURCES) notes.bib 
	@ $(TEXCOMPILER) $(basename $<) 
	@ $(BIBCOMPILER) $(basename $<) 
	@ $(TEXCOMPILER) $(basename $<) 
	@ $(TEXCOMPILER) $(basename $<) 

.PHONY: $(SUBDIRS) 
$(SUBDIRS): 
	$(MAKE) -C $@ 

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
