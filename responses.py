from codeforces_api import leaderboard


def get_response(message: str) -> str | None:
    p_message = message.lower()

    if p_message == "hello":
        return "hi"

    if p_message == "leaderboard":
        handles = ["sakib.safwan", "ovi_xar", "roundspecs"]
        toppers = leaderboard(handles)
        res = "Number of problems solved today```yaml\nNo : CF handle\n"
        return (
            res
            + "\n".join([f"{count:02d} : {handle}" for count, handle in toppers])
            + "```"
            + "Congratutaions your majesty, "
            + toppers[0][1]
        )
