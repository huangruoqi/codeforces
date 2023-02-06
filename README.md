# codeforces
### template:
* `ii()` returns a list of integers
* `ii(1)` returns an integer
* `input()` return a string
### steps:
* **Windows**
  * Enable long path for windows in powershell
    * https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell
    ```
    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
    -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
    ```
  * run in powershell to install `poetry`
    ```
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python
    ```
1. Make a new repo with any name you like in GitHub
  ![image](https://user-images.githubusercontent.com/44049919/188018539-768fff42-4c24-477a-a875-01aeeac92159.png)
2. Run `make setup` for your CF info
3. Copy your new repo's url & paste it to `Github repo URL: `
  ![image](https://user-images.githubusercontent.com/44049919/188018697-9d02859d-63db-41be-befc-5be502f7218f.png)
4. You are all set

### codeforces coding utilities
- `make setup` for one time only
- `make init <contest_id>` to generate new contest folder
- `make run <problem_id>` to run script with io-tests
- `make black` to reformat
- `make push` to push contest to GitHub

### Examples
```python
make init 500
make run A
```
