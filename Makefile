LINTER=black
LINTERFLAGS=-l 100 --preview
FORMATTER=pylint
MAIN=src/main.py
PYTHON=python3

run:
	mkdir -p datastore
	$(PYTHON) $(MAIN)

build: 
	$(PYTHON) pip install -r requirements.txt

lint:
	$(LINTER) $(LINTERFLAGS) $(MAIN)
	pylint $(MAIN)

clean:
	rm -rf datastore
