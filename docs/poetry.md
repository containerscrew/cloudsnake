<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Poetry commands](#poetry-commands)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Poetry commands

```shell
poetry add boto3 dacite ## add new dependencies
poetry config pypi-token.pypi pypi-XXXXXX ## config your pypip token
poetry publish --build ## publich the package to pypip
poetry config repositories.testpypi https://test.pypi.org/legacy/ ## config for pypip test
poetry publish --build -r testpypi # publish to pypip test
```
