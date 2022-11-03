from codeforces_api import leaderboard
from utils import get_handles


async def get_response(message, user_message):
    # Just a joke
    if str(message.author).startswith("chy_chy") and user_message == "<@693265856305692764>":
        return "<@693265856305692764>, yasir bhai dake"

    p_message = user_message.lower()

    if p_message in ["hello", "hi"]:
        return "ki obostha?"

    if p_message == "leaderboard":
        await message.channel.send(
            "Digging deep into the codeforces database. This may take a while...\nPlease don't type `leaderboard` for the next 5 minutes.\nI'll mention you when I'm done (if nothing goes wrong)."
        )
        handles = get_handles()
        toppers = leaderboard(handles)
        res = "**Number of problems solved today**```yaml\nNo : CF handle\n--------------\n"
        return (
            res
            + "\n".join([f"{count:02d} : {handle}" for count, handle in toppers])
            + "```"
            + "Congratutaions Coder of the day, "
            + toppers[0][1]
            + " :crown:"
        )
