import requests
import handle
import random


def handle_exists(handle: str):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    return requests.get(url).json()["status"] == "OK"


def get_duel_url(uid1: int, uid2: int, rating: int):
    handle1 = handle.uid2handle(uid1)
    handle2 = handle.uid2handle(uid2)
    subs1 = _get_all_subs(handle1)
    subs2 = _get_all_subs(handle2)
    u_subs = subs1.union(subs2)
    problems = _query_api(path="problemset.problems")["problems"]
    random.shuffle(problems)
    for prob in problems:
        pID = _problemDict2pID(prob)
        if pID in u_subs:
            continue
        if rating == pID[2]:
            return f"https://codeforces.com/problemset/problem/{pID[0]}/{pID[1]}"


def is_prob_ac(url: str, rating: int, uid: int):
    pID = _url2pID(url, rating)
    h = handle.uid2handle(uid)
    return pID in _get_all_ac_subs(h)

def _get_all_subs(handle: str):
    params = {"handle": handle}
    submissions = _query_api("user.status", params=params)
    subs = set()
    for submission in submissions:
        subs.add(_submission2pID(submission))
    return subs

def _get_all_ac_subs(handle: str):
    params = {"handle": handle}
    submissions = _query_api("user.status", params=params)
    subs = set()
    for submission in submissions:
        if _is_sub_ac(submission):
            subs.add(_submission2pID(submission))
    return subs


def _is_sub_ac(submisssion: dict) -> bool:
    return submisssion.get("verdict") == "OK"


def _submission2pID(submission: dict):
    return _problemDict2pID(submission["problem"])


def _problemDict2pID(problem: dict):
    return (problem.get("contestId"), problem.get("index"), problem.get("rating"))


def _url2pID(url: str, rating: int):
    splitter = url.strip('/').split('/')
    contestID, index = splitter[-2:]
    return (int(contestID), index, rating)


def _query_api(path: str, params=None) -> list:
    API_BASE_URL = "https://codeforces.com/api/"
    res = requests.get(url=API_BASE_URL + path, params=params)
    return res.json()["result"]
