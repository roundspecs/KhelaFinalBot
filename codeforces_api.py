import requests
from datetime import datetime


def leaderboard(handles, ratings, date=datetime.today().date()):
    res = [(solved_count(h, r, date=date), h) for h, r in zip(handles, ratings)]
    res = [item for item in res if item[0]]
    res.sort(reverse=True)
    return res


def solved_count(handle, rating, count=20, date=datetime.today().date()):
    def _is_submission_accepted(submission):
        return submission["verdict"] == "OK"

    def _is_submitted_today(submission):
        timestamp = submission["creationTimeSeconds"]
        submission_date = datetime.fromtimestamp(timestamp).date()
        return date == submission_date

    def _is_rating_more(submission):
        r = submission["problem"].get("rating", float('inf'))
        return r >= int(rating)

    def _is_ok(submission):
        return (
            _is_submission_accepted(submission)
            and _is_submitted_today(submission)
            and _is_rating_more(submission)
        )

    def _get_problem_id(submission):
        return str(submission["contestId"]) + str(submission["problem"]["index"])

    params = {"handle": handle, "count": count}
    submissions = _query_api("user.status", params=params)
    subs = set()
    for submission in submissions:
        if _is_ok(submission):
            subs.add(_get_problem_id(submission))
    return len(subs)


def get_rating_from_cf(handles):
    h = ";".join(handles)
    res = _query_api("user.info", {"handles": h})
    res = [r.get("rating", 0) for r in res]
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

if __name__=="__main__":
    solved_count("CHY_YASIR", 1450)