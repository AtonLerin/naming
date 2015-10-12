docs: clear
	pycco naming.py

clear:
	rm -rf ./docs/*.*

gh-pages: docs
	git commit -a
	git checkout gh-pages
	git merge refactor
	git push
	git checkout refactor

httpserver: docs
	python -m SimpleHTTPServer
