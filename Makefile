init:
	virtualenv -ppython3 venv
	source venv/bin/activate
	pip install -r requirements.txt

test:
	python -m unittest discover -p '*_test.py'

.PHONY: init test
