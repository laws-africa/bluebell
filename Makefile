SHELL := /bin/bash

.PHONY: compile

hierarchicalStructure.py: hierarchicalStructure.peg
	npx canopy $< --lang python

compile: hierarchicalStructure.py
