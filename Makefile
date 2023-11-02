# SPDX-License-Identifier: AGPL-3.0-or-later

SHELL=/bin/bash
.DEFAULT_GOAL=help

PYDIST = ./dist

# wrap ./prj script
# -----------------

PRJ += help env.build
PRJ += doc.html doc.live doc.gh-pages doc.prebuild doc.clean

PHONY += $(PRJ)
$(PRJ):
	@./prj $@

# local TOPTARGETS
test clean build::
	@./prj $@

# Python Package Index (PyPI)
# ---------------------------

PHONY += upload-pypi upload-pypi-test

upload-pypi: clean env.build build
	@./prj cmd msg.build PYPI "build and upload python packages"
	@./prj cmd twine upload $(PYDIST)/*

upload-pypi-test: clean env.build build
	@./prj cmd msg.build PYPI "build and upload python packages (TEST)"
	@./prj cmd twine upload -r testpypi $(PYDIST)/*


# run make in subdirectories
# --------------------------

# Makefiles in subdirs needs to define TOPTARGETS::
#    .PHONY: all clean test build

TOPTARGETS := all clean test build
SUBDIRS := $(dir $(wildcard */Makefile))
PHONY += $(TOPTARGETS)

$(TOPTARGETS)::
	@for dir in $(SUBDIRS); do \
	    $(MAKE) -C $$dir $@ || exit $$?; \
	done; \

.PHONY: $(PHONY)
