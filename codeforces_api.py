from typing import List
import requests
from datetime import datetime


def leaderboard(handles, date=datetime.today().date()):
    res = [(solved_count(handle, date=date), handle) for handle in handles]
    res = [item for item in res if item[0]]
    res.sort(reverse=True)
    return res


def solved_count(handle, count=30, date=datetime.today().date()):
    def _is_submission_accepted(submission):
        return submission["verdict"] == "OK"

    def _is_submitted_today(submission):
        timestamp = submission["creationTimeSeconds"]
        submission_date = datetime.fromtimestamp(timestamp).date()
        return date == submission_date

    params = {"handle": handle, "count": count}
    submissions = _query_api("user.status", params=params)
    count = 0
    for submission in submissions:
        if _is_submission_accepted(submission) and _is_submitted_today(submission):
            count += 1
    return count


def get_rating(handles):
    h = ";".join(handles)
    res = _query_api("user.info", {"handles": h})
    res = [r["rating"] for r in res]
    return res


def _query_api(path, params):
    API_BASE_URL = "https://codeforces.com/api/"
    url = API_BASE_URL + "/" + path
    res = requests.get(url=url, params=params)
    if res.status_code == 200:
        res_json = res.json()
        if res_json["status"] == "OK":
            return res_json["result"]
        else:
            raise CfFailedException(res_json["comment"])
    else:
        raise requests.RequestException(res)


class CfFailedException(Exception):
    pass


if __name__ == "__main__":
    print(get_rating(["sakib.safwan", "ovi_xar", "roundspecs"]))
