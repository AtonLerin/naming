docs: clear
	pycco naming.py

clear:
	rm -rf ./docs/*.*

httpserver: docs
	python -m SimpleHTTPServer

unittest:
ifeq (, $(shell coverage --version 2> /dev/null))
	clear && python -m unittest discover
else
	coverage erase && clear && coverage run --source "${PWD##*/}" -m unittest discover && coverage report -m
endif
