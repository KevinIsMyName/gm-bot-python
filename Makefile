LINTER=black
LINTERFLAGS=-l 100 --preview
FORMATTER=pylint
FILE=src/main.py

run:
	mkdir -p datastore
	python3 $(FILE)

build: 
	pip install python-dotenv black

lint:
	$(LINTER) $(LINTERFLAGS) $(FILE)
	pylint $(FILE)

clean:
	rm -rf datastore
