PY := .venv/bin/python

.PHONY: help install build serve new hands-on note personal clean

help:
	@echo "make install                     create .venv and install the build dependencies"
	@echo "make build                       build the site into _site/ (fails on broken content)"
	@echo "make serve                       build with drafts and serve on http://localhost:8000"
	@echo "make new SLUG=name TITLE='...'   scaffold content/projects/name/index.md (draft)"
	@echo "make hands-on SLUG=name TITLE='...' [NB=file.ipynb]   Hands-On entry (README / notebook)"
	@echo "make note SLUG=name TITLE='...' [URL=press-article]     Notes entry (article, opinion)"
	@echo "make personal SLUG=name TITLE='...'                   Personal entry (essay, other topics)"
	@echo "make clean                       remove _site/"

$(PY):
	python3 -m venv .venv
	$(PY) -m pip install -q -r requirements.txt

install: $(PY)

build: $(PY)
	$(PY) scripts/build.py

serve: $(PY)
	$(PY) scripts/build.py --drafts --serve

new: $(PY)
	@test -n "$(SLUG)" || (echo "usage: make new SLUG=my-project TITLE='My title' [REPO=url]"; exit 1)
	$(PY) scripts/new_project.py "$(SLUG)" "$(TITLE)" $(if $(REPO),--repo "$(REPO)")

hands-on: $(PY)
	@test -n "$(SLUG)" || (echo "usage: make hands-on SLUG=my-entry TITLE='My title' [NB=path/to/notebook.ipynb]"; exit 1)
	$(PY) scripts/new_entry.py hands-on "$(SLUG)" "$(TITLE)" $(if $(NB),--ipynb "$(NB)")

note: $(PY)
	@test -n "$(SLUG)" || (echo "usage: make note SLUG=my-note TITLE='My title' [URL=https://press-article]"; exit 1)
	$(PY) scripts/new_entry.py notes "$(SLUG)" "$(TITLE)" $(if $(URL),--press "$(URL)")

personal: $(PY)
	@test -n "$(SLUG)" || (echo "usage: make personal SLUG=my-essay TITLE='My title'"; exit 1)
	$(PY) scripts/new_entry.py personal "$(SLUG)" "$(TITLE)"

clean:
	rm -rf _site
