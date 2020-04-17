SHELL := /bin/bash

.PHONY: compile

bluebell/akn.py: bluebell/akn.peg
	npx canopy $< --lang python

compile: akn/bluebell.py
