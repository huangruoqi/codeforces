# codeforces
### steps:
0. Install xcode(for maketools), python3, and your language of choice
1. Fork this repo
2. Clone your repo to local
3. Setup in `codeforces/settings.py`
- Language
- IDE open command
  - **vscode** recommended
    - after install -> <command+shift+p> -> type "install code" to add to path
5. Edit the template code in `codeforces/source.template`

### codeforces coding utilities
- `make init <contest_id>` to generate new contest folder
  - contest_id can be found in the website url
- `make run <problem_id>` to run script with io-tests
- `make push` to push contest to GitHub

### Examples
```python
make init 500
make run A
...
make push
```
