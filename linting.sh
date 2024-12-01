#!/bin/bash
echo "---- Running black ----"
black .

echo "---- Running flake8 ---"
flake8 .

echo "---- Running isort ----"
isort .

echo "---- Running pylint ----"
find . -type f -name "*.py" | xargs pylint
