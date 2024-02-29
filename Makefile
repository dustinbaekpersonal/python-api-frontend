delete-git-branch:
	git remote prune origin
	git fetch --prune

uv-setup:
	pip install uv
	uv venv

uv-dev:
	uv pip compile requirements/prod.in && uv pip compile requirements/test.in && uv pip compile requirements/dev.in
	uv pip sync requirements/dev.txt