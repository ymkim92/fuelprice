run-test:
    pytest -svv
run-test-filter TEST:
    pytest -svv tests/*{{TEST}}*
