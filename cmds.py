import json
import logging
import os.path

import click

from src import parse, download, catch_state, utils
from src.calculate import longest_fail_user


def state(file: str):
    catch_state.manual_save_state(file, "https://game.maj-soul.com/1/", timeout=60 * 1000)


def download_all(logs_dir: str, state_file: str, profile: str, scripts_dir: str, data_file: str):
    ids = utils.read_ids_from_file(data_file)
    logging.debug(f"ids: {ids}")
    download.download_all_logs(profile, state_file, logs_dir, scripts_dir, ids)


def download_log(logs_dir: str, state_file: str, profile: str, scripts_dir: str, log_id: str):
    download.download_all_logs(profile, state_file, logs_dir, scripts_dir, [log_id, ])


def calculate_longest_fail(logs_dir: str, output_dir: str) -> (int, list, dict):
    user_result = parse.parse_user_result_list(parse.get_user_time_result(logs_dir))
    longest, users, m = longest_fail_user(user_result)
    with open(os.path.join(output_dir, "longest_fail.json"), "w", encoding="utf8") as f:
        json.dump(m, f, ensure_ascii=False)
    with open(os.path.join(output_dir, "longest_fail.txt"), "w", encoding="utf8") as f:
        for k in sorted(m.keys(), reverse=True):
            f.write(f"{k} {m[k]}\n")

    return longest, users, m


def __logs_diff(files: list, output_dir: str, data: str):
    ids = utils.read_ids_from_file(data)
    logging.debug(f"ids: {ids}")
    files_ids = [f.split('.')[0] for f in files]
    logging.debug(f"files_ids: {files_ids}")

    lack_ids = set(ids) - set(files_ids)
    extra_ids = set(files_ids) - set(ids)
    logging.debug(f"lack_ids: {lack_ids}")
    logging.debug(f"extra_ids: {extra_ids}")

    with open(os.path.join(output_dir, "diff.txt"), "w", encoding="utf8") as f:
        f.write("lack ids(need to download):\n")
        for i in lack_ids:
            f.write(f"{i}\n")
        f.write("extra ids(need to delete):\n")
        for i in extra_ids:
            f.write(f"{i}\n")


def logs(logs_dir: str, output_dir: str, diff: bool, data: str):
    files = os.listdir(logs_dir)
    if diff:
        __logs_diff(files, output_dir, data)
    else:
        for f in files:
            click.secho(f, fg="green")
