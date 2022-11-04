from codeforces_api import leaderboard
from utils import get_handles


async def get_response(message, user_message):
    # Just a joke
    if str(message.author).startswith("chy_chy") and user_message == "<@693265856305692764>":
        return "<@693265856305692764>, yasir bhai dake"

    if user_message == 'help':
        return "- type `leaderboard` to see who solved how many problems today\n"\
        "- type `whats next` to see future plans\n"\
        "- you can also dm me with the same commands"

    if user_message in ["hello", "hi"]:
        return "ki obostha?"
    
    if user_message == "whats next":
        return "**Plans:**\n"\
        "- Make sure everyone solves problems with rating greater than their own rating\n"\
        "- If someone does not solve any problem for 30 consecutive days, remove his/her handle form database\n"\
        "- Automatically show leaderboard everyday at 11:59 PM"

    if user_message == "leaderboard":
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
            + "Congratutaions coder of the day, **"
            + toppers[0][1]
            + "** :crown:"
        )
