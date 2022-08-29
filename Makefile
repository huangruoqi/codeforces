setup:
	poetry install
	poetry run python -B codeforces/index.py setup 

# If the first argument is "init"
ifeq (init,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
init:
	poetry run python -B codeforces/index.py init $(RUN_ARGS)

black:
	poetry run black ./
