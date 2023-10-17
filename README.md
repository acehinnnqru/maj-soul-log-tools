# maj-soul-log-tools
A tool for Maj-Soul log analysis.

## Disclaimer
This project is only for personal use, and it is not recommended to use it for commercial purposes.

**If it is used for commercial purposes, the author will not be responsible for any problems caused by it.**

Also, if this project harms the interests of the game company, the author will delete this project.

## Usage
### Install Dependencies
```shell
pip install -r requirements.txt
```

### Help

**!!! Support Chrome only**

```shell
python main.py --help
```

### Save current state for your account
This command will open the browser then you should enter your account and password in the browser. The default timeout is 60 seconds.
```shell
python main.py state --help
```

The argument "file" is the path of the file to save the state. The default value is "state.json".

### Download Logs

**!!! Require state file**

Download logs with state file and chrome profile dir.

```shell
python main.py dl --profile {chrome profile dir} log_id/log_ids_file
```

log_id is the id of the log you want to download.

log_ids_file is the path of the file which contains the ids of the logs you want to download.

`log_ids_file` example:
```
xxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxx
```

### Logs Tool

#### List Logs
```shell
python main.py logs --logs_dir {logs dir}
```

### Check diff ids between data file and logs dir

The data is the data file which contains the ids of the logs you want to check.

```shell
python main.py logs --diff --data {data file} --logs_dir {logs dir} --output_dir {output dir}
```

The output will be the `diff.txt` in the `output_dir` dir.

### Calculate Tools

#### Longest Fail User
```shell
python main.py cal longest_fail --logs_dir {logs dir} --output_dir {output dir}
```

This command will calculate the longest fail user and save the middle result to the output dir (`longest_fail.json` and `longest_fail.txt`).

The final result will appear in the console.