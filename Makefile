SHELL := /bin/bash

.PHONY: compile

bluebell/akn.py: bluebell/akn.peg
	canopy/bin/canopy $< --lang python

compile: akn/bluebell.py
