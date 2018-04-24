default: deps test run
deps:
ifeq ($(ENV),"prod")
	pip install -U -r requirements.txt
else
	pip install -U -r requirements.txt -r test-requirements.txt
endif
run:
	python main.py
test:
	pytest test.py
