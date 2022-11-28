import pandas as pd
import pathlib
import math
from cf_api import get_duel_url, is_solved

from utils import uname2handle

BASE_DIR = pathlib.Path().resolve()
DUEL_DB = BASE_DIR / "duel.csv"


def challenge(uname_from: str, uname_to: str, rating: int):
    """
    if uname already exits return the df
    else add the challenge to duel.csv
    """
    df = pd.read_csv(DUEL_DB)
    uname_from_info = df.loc[(uname_from == df["from"]) | (uname_from == df["to"])]
    if len(uname_from_info) != 0:
        raise AlreadyInChallenge(uname_from_info.iloc[0])
    uname_to_info = df.loc[(uname_to == df["from"]) | (uname_to == df["to"])]
    if len(uname_to_info) != 0:
        raise AlreadyInChallenge(uname_to_info.iloc[0])

    new_challenge_dict = {"from": uname_from, "to": uname_to, "rating": rating}
    new_challenge_df = pd.DataFrame([new_challenge_dict])
    new_challenge_df.to_csv(DUEL_DB, mode="a", index=False, header=not DUEL_DB.exists())


def accept(uname_to: str, epoch: str):
    df = pd.read_csv(DUEL_DB)
    if df.loc[df["to"] == uname_to].empty:
        raise NoSuchUName()
    if not math.isnan(df.loc[df["to"] == uname_to, "start"]):
        raise DuelAlreadyAccepted()
    s = df.loc[df["to"] == uname_to].iloc[0]
    handle1 = uname2handle(s["from"])
    handle2 = uname2handle(s["to"])
    rating = s["rating"]
    url = get_duel_url(handle1, handle2, rating)
    splitted = url.split("/")
    contest, index = splitted[-2:]
    df.loc[df["to"] == uname_to, "start"] = epoch
    df.loc[df["to"] == uname_to, "contest"] = contest
    df.loc[df["to"] == uname_to, "index"] = index
    df.to_csv(DUEL_DB, index=False)
    return df.loc[df["to"] == uname_to].iloc[0]


def decline(uname_to: str):
    df = pd.read_csv(DUEL_DB)
    if df.loc[df["to"] == uname_to].empty:
        raise NoSuchUName()
    if df.loc[(df["to"] == uname_to) & (df["start"] != math.nan)].empty:
        raise DuelAlreadyAccepted()
    df = df.loc[df["to"] != uname_to]
    df.to_csv(DUEL_DB, index=False)


def withdraw(uname_from: str):
    df = pd.read_csv(DUEL_DB)
    if df.loc[df["from"] == uname_from].empty:
        raise NoSuchUName()
    if df.loc[(df["from"] == uname_from) & (df["start"] != math.nan)].empty:
        raise DuelAlreadyAccepted()
    df = df.loc[df["from"] != uname_from]
    df.to_csv(DUEL_DB, index=False)


def cancel(uname: str):
    df = pd.read_csv(DUEL_DB)
    if df.loc[(df["from"] == uname) | (df["to"] == uname)].empty:
        raise NoSuchUName()
    df = df.loc[(df["from"] != uname) & (df["to"] != uname)]
    df.to_csv(DUEL_DB, index=False)


def list():
    df = pd.read_csv(DUEL_DB)
    df["from"] = df["from"].map(uname2handle)
    df["to"] = df["to"].map(uname2handle)
    return df


def complete(uname: str):
    df = pd.read_csv(DUEL_DB)
    dff = df.loc[(df["from"] == uname) | (df["to"] == uname)]
    if dff.empty:
        raise NoSuchUName()
    s = dff.iloc[0]
    url = f"https://codeforces.com/problemset/problem/{s['contest']}/{s['index']}"
    handle = uname2handle(uname)
    if not is_solved(url, handle):
        raise NotSolved()
    return TODO


class NotSolved(Exception):
    ...


class NoSuchUName(Exception):
    ...


class DuelAlreadyAccepted(Exception):
    ...


class AlreadyInChallenge(Exception):
    ...


if __name__ == "__main__":
    x = pd.read_csv(DUEL_DB)
    y = x.loc[x["start"] == math.nan]
