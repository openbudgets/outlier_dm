init:
	pip3 install -r requirements.txt
	pip3 install .
	git clone https://github.com/openbudgets/preprocessing_dm.git
	cd preprocessing_dm
	pip3 install -r requirements.txt
	pip3 install .
	cd ..

test:
	nosetests tests
