# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = FeatureToggle
SOURCEDIR     = .
BUILDDIR      = _build
TMP_GH_PAGES = tmp_gh_pages

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

   gh-pages:
	make html
	cp -rf $(BUILDDIR)/html/* ../_$(TMP_GH_PAGES)
	git checkout gh-pages
	cp -rf _$(TMP_GH_PAGES)/* .
	rm -rf _$(TMP_GH_PAGES)
	git add -A
	git ci -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master
