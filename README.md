Install the dependencies:

```shell
python -m pip install -r requirements.txt
```

Run the tests:

```shell
python -m unittest discover -s tests -v
```

GitHub Actions runs the tests and checks Python syntax on Python 3.10 through
3.13 for every push and pull request.