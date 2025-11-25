# Poetry commands

```shell
poetry add boto3 dacite ## add new dependencies
poetry config pypi-token.pypi pypi-XXXXXX ## config your pypip token
poetry publish --build ## publich the package to pypip
poetry config repositories.testpypi https://test.pypi.org/legacy/ ## config for pypip test
poetry publish --build -r testpypi # publish to pypip test
poetry run python3 src/cloudsnake/__main__.py --help # run cloudsnake locally using poetry
```
