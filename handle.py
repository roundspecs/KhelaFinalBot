import pandas as pd

HANLDES_DB = "handles.csv"


def handleset(handle: str, uid: int):
    df = pd.read_csv(HANLDES_DB)
    if (df["uid"] == uid).any():
        df.loc[df["uid"] == uid, "handle"] = handle
    else:
        df = pd.concat([df, pd.DataFrame([{"uid": uid, "handle": handle}])])
    df.to_csv(HANLDES_DB, index=False)


def uid_exists(uid: int) -> bool:
    df = pd.read_csv(HANLDES_DB)
    return (df["uid"] == uid).any()


def uid2handle(uid: int) -> str | None:
    df = pd.read_csv(HANLDES_DB)
    s = df.loc[df["uid"] == uid, "handle"].to_list()
    if len(s) != 0:
        return s[0]