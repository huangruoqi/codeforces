setup:
	poetry install
	poetry run python -B codeforces/index.py setup 

black:
	poetry run black ./

# If the first argument is "init"
ifeq (init,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
init:
	poetry run python -B codeforces/index.py init $(RUN_ARGS)

# If the first argument is "run"
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
run:
	poetry run python -B codeforces/index.py run $(RUN_ARGS)
