VENV=rt-venv
INVENV = $(shell pip3 -V | grep $(VENV))

BLACK        := $(shell tput -Txterm setaf 0)
RED          := $(shell tput -Txterm setaf 1)
GREEN        := $(shell tput -Txterm setaf 2)
YELLOW       := $(shell tput -Txterm setaf 3)
LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
PURPLE       := $(shell tput -Txterm setaf 5)
BLUE         := $(shell tput -Txterm setaf 6)
WHITE        := $(shell tput -Txterm setaf 7)
RESET 	     := $(shell tput -Txterm sgr0)

all: FORCE
	@echo
	@echo "${GREEN}This is fairly general Makefile that does the same job as the makefiles in previous projects. You can add new things, modify it, or just delete it if you don't need it. At the very least, you can use it to set up your virtual environment.${RESET}"
	@echo

venvcheck:
ifeq ($(INVENV),)
	$(error ${RED}You should only run this from within the venv. Use '${YELLOW}. ./$(VENV)/bin/activate${RED}'${RESET})
else
	@echo "${GREEN}venv check passed${RESET}"
	@echo
endif


test: FORCE message venvcheck
	py.test -v  tests/ 

docs: FORCE message venvcheck
	pdoc  --html ./src/*.py --force


message: FORCE
	@echo
	@echo "${RED}If you don't have pytest or pdoc3 installed, you will need to install them globally or inside a virtualenv.  This Makefile can build the venv for you, if you use '${YELLOW}make venv${RED}' followed by '${YELLOW}. ./${VENV}/bin/activate${RED}' and finally '${YELLOW}make prereqs${RED}'${RESET}"
	@echo


venv: FORCE
	python3 -m venv $(VENV)

prereqs: FORCE venvcheck
	pip install -r requirements.txt


FORCE:
