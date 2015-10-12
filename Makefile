html: clear
	pycco naming.py

clear:
	rm -rf ./docs/*.*

gh_pages: html
	git checkout -b gh_pages
	git merge refactor
	git push
	git checkout refactor

httpserver: html
	python -m SimpleHTTPServer
