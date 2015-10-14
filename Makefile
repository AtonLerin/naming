help:
	@echo 'Makefile for naming.py                                                 '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make test                test runner (uses coverage when available) '
	@echo '   make docs                (re)generate the documentation             '
	@echo '   make clean               remove generated docs                      '
	@echo '   make help                show this help message                     '
	@echo '                                                                       '

docs: clean
	pycco naming.py

clean:
	rm -rf ./docs/*.*

test:
ifeq (, $(shell coverage --version 2> /dev/null))
	clear && python -m unittest discover
else
	coverage erase && clear && coverage run --source "${PWD##*/}" -m unittest discover && coverage report -m
endif
