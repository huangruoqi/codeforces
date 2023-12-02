# codeforces
### steps:
0. Install xcode, python3, and your language of choice
1. Fork this repo
2. Clone your repo to local
3. Setup execution commands and file extension for your language in `codeforces/settings.py`
4. Edit the template code in `codeforces/source.template`

### codeforces coding utilities
- `make init <contest_id>` to generate new contest folder
- `make run <problem_id>` to run script with io-tests
- `make push` to push contest to GitHub

### Examples
```python
make init 500
make run A
...
make push
```
