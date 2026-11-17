PY := .venv/bin/python

.PHONY: help install build serve new clean

help:
	@echo "make install                     create .venv and install the build dependencies"
	@echo "make build                       build the site into _site/ (fails on broken content)"
	@echo "make serve                       build with drafts and serve on http://localhost:8000"
	@echo "make new SLUG=name TITLE='...'   scaffold content/projects/name/index.md (draft)"
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

clean:
	rm -rf _site
