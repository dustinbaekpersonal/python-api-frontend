pip-tools:
	pip install pip-tools>=7.0.0 setuptools>=68.0.0

pip-tools-dev:
	pip-compile requirements/prod.in && pip-compile requirements/test.in && pip-compile requirements/dev.in
	pip-sync requirements/dev.txt

delete-git-branch:
	git remote prune origin
	git fetch --prune