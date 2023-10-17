import datetime
import json
import logging
import os
from collections import defaultdict


def parse_user_result_list(user_time_result: dict):
    ret = defaultdict(list)
    for user in user_time_result:
        sorted_keys = sorted(user_time_result[user].keys())
        for t in sorted_keys:
            ret[user].extend(user_time_result[user][t])
    return ret


def get_user_time_result(directory: str):
    fs = os.listdir(directory)

    user_time_result = defaultdict(lambda: defaultdict(list))
    for f in fs:
        with open(os.path.join(directory, f), "r") as fobj:
            data = json.load(fobj)
            user_result, t = review_data(data)
            for user, result in user_result.items():
                user_time_result[user][t] = result

    return user_time_result


# dict format
# {
#     "ref": str,
#     "log": list[list[list]],
#     "name": list,
#     "title": ["title", time("m/d/y, HH:MM:SS %p")],
# }
# return:
# { "user": list(int) }, int
def review_data(data: dict) -> (dict, int):
    names = data["name"]
    logs = data["log"]
    t = datetime.datetime.strptime(data["title"][1], "%m/%d/%Y, %I:%M:%S %p")
    logging.debug(t, names)

    user_result = defaultdict(list)
    for log in logs:
        result = log[-1]
        logging.debug(result)
        if result[0] == "和了":
            logging.debug("和了")
            status = 0
        elif result[0] in {"Ryuukyoku", "Nagashi Mangan", "Kyuushu Kyuuhai", "Suufon Renda", }:
            logging.debug("流局")
            status = 1
        else:
            raise Exception(f"未知结果: {result[0]}")

        for i in range(4):
            if status == 0 and result[1][i] > 0:
                user_result[names[i]].append(1)
            else:
                user_result[names[i]].append(0)

    return user_result, t.timestamp()
