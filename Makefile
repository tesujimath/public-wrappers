# Makefile for documentation

README.pdf: README.rst
	pandoc $< -o $@
