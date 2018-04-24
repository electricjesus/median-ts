default: deps test run
deps:
	pip install -U -r requirements.txt
run:
	python main.py
test:
	pytest test.py
