from codeforces_api import leaderboard
from utils import get_handles


async def get_response(message, user_message: str) -> str | None:
    p_message = user_message.lower()

    if p_message == "hello":
        return "hi"

    if p_message == "leaderboard":
        await message.channel.send("Digging deep into the codeforces database. This may take a while...")
        handles = get_handles()
        toppers = leaderboard(handles)
        res = "Number of problems solved today```yaml\nNo : CF handle\n"
        return (
            res
            + "\n".join([f"{count:02d} : {handle}" for count, handle in toppers])
            + "```"
            + "Congratutaions your majesty, "
            + toppers[0][1]
        )
