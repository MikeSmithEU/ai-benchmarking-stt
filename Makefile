.PHONY: docs test clean gh-pages

test:
	pytest --verbose

docs: html

html:
	cd docs/ && make clean html && touch build/html/.nojekyll

man: build-man
	cp resources/manpage/*.1 /usr/local/share/man/man1

build-man:
	cd docs/ && make clean man
	cp docs/build/man/* resources/manpage/

clean:
	cd docs/ && make clean

gh-pages: # docs
	TMPDIR=`mktemp -d` || exit 1; \
	trap 'rm -rf "$$TMPDIR"' EXIT; \
	echo $$TMPDIR; \
	GITORIGIN=$(shell git remote get-url origin); \
	git clone "$$GITORIGIN" -b gh-pages --single-branch "$$TMPDIR"; \
	rm "$$TMPDIR/*"; \
	echo "conferatur.mikesmith.eu" > "$$TMPDIR/CNAME"; \
	cp -r docs/build/html/* "$$TMPDIR"; \
	cd "$$TMPDIR" ;\
	git add -A && git commit -a -m 'update docs' && git push --set-upstream origin gh-pages


