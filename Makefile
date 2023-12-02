export PYTHONDONTWRITEBYTECODE=1
setup:
	pip install -r requirements.txt

test:
	pytest ./codeforces

# If the first argument is "init"
ifeq (init,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
init:
	python3 index.py init $(RUN_ARGS)


# If the first argument is "run"
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
run:
	python3 index.py run $(RUN_ARGS)

push:
	black ./
	git add .
	python3 index.py push
