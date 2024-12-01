run-test:
    pytest -svv
run-test-filter TEST:
    pytest -svv tests/*{{TEST}}*
coverage:
    pytest --cov=fuel_price
coverage-html:
    # check htmlcov folder
    pytest --cov=fuel_price --cov-report=html
lint:
    ./linting.sh
mypy:
    ./mypy.sh
install-requirement:
    pip install -r requirements.txt
all:
    ./linting.sh && pytest -svv && ./mypy.sh
