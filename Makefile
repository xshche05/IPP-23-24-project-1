
PY_FILES = $(wildcard *.py)

all: zip

odevzdani: rozsireni readme1.md $(PY_FILES)
	mkdir odevzdani
	cp *.py ./odevzdani
	cp rozsireni ./odevzdani
	cp readme1.md ./odevzdani

zip: odevzdani
	dos2unix ./odevzdani/*
	cd odevzdani && zip ../xshche05.zip *
