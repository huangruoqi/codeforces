export PYTHONDONTWRITEBYTECODE=1
setup:
	poetry install
	poetry run python codeforces/index.py setup 

black:
	poetry run black ./

test:
	poetry run pytest ./codeforces/test

# If the first argument is "init"
ifeq (init,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
init:
	poetry run python codeforces/index.py init $(RUN_ARGS)


# If the first argument is "run"
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
run:
	poetry run python codeforces/index.py run $(RUN_ARGS)

# If the first argument is "submit"
ifeq (submit,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
submit:
	poetry run python codeforces/index.py submit $(RUN_ARGS)

push:
	poetry run black ./
	git add .
	poetry run python codeforces/index.py push
