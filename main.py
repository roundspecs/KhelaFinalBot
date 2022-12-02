import os

import discord
from discord import Color, Embed, Interaction, Member
from discord.ext import commands

from cf import get_duel_url, handle_exists, who_solved_first
from handle import get_all_uid_handle, handleset, uid2handle, uid_exists
from keep_alive import keep_alive

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready():
    synced = await client.tree.sync()
    print(
        f"{client.user.name} is now running!\n"
        f"Number of slash commands synced: {len(synced)}"
    )


@client.tree.command(name="help", description="Shows all commands")
async def help(itr: Interaction):
    embed = Embed(title="Help")
    embed.add_field(
        name="/sethandle",
        value="`/sethandle <handle> <member>` to set the CF handle of a member",
        inline=False,
    )
    embed.add_field(
        name="/whois",
        value="`/whois <member>` shows the CF handle of the member (incognito)",
        inline=False,
    )
    embed.add_field(
        name="/list",
        value="`/list` lists all the CF handles of this server (incognito)",
        inline=False,
    )
    embed.add_field(
        name="/challenge",
        value="`/challenge <rating> <opponent(optional)>` to challenge others",
        inline=False,
    )
    embed.add_field(
        name="/help",
        value="`/help` shows this help text (incognito)",
        inline=False,
    )
    await itr.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="sethandle", description="Set or update handle")
async def set_handle(itr: Interaction, handle: str, member: Member):
    """
    Used to set(or update) handle of user

    - if no such handle is present in CF, sends an error message
    - otherwise, sets(or updates) the handle
    """
    embed: Embed
    if not handle_exists(handle):
        embed = Embed(
            description=f"Could not find handle, {handle} in CF", color=Color.red()
        )
    else:
        handleset(handle, member.id)
        embed = Embed(
            description=f"Handle of {member.mention} set to {handle}",
            color=Color.green(),
        )
    await itr.response.send_message(embed=embed)


@client.tree.command(
    name="whois",
    description="Shows CF handle of user (don't worry, s/he wouldn't know)",
)
async def whois(itr: Interaction, member: Member):
    """
    - if user already set his handle, it show the handle
    - otherwise, show that that handle is not set yet
    """
    embed = Embed(title=f"Who is {member.display_name}?")
    handle = uid2handle(member.id)
    if handle == None:
        handle = "Not set"
    embed.add_field(name="CF Handle", value=f"{handle}")
    embed.set_thumbnail(url=member.avatar)
    await itr.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name="list", description="List all handles")
async def list(itr: Interaction):
    uids, _handles = get_all_uid_handle()
    users = []
    handles = []
    for uid, handle in zip(uids, _handles):
        user = itr.guild.get_member(uid)
        if user != None:
            users.append(user)
            handles.append(handle)
    if users:
        embed = Embed(title="List of all handles")
        embed.add_field(
            name="Username", value="\n".join([user.mention for user in users])
        )
        embed.add_field(name="Handle", value="\n".join(handles))
        await itr.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = Embed(
            description="No handle found. User `/sethandle` to set handle",
            color=Color.red(),
        )
        await itr.response.send_message(embed=embed, ephemeral=True)


class EndDuelButtons(discord.ui.View):
    def __init__(self, p1: Member, p2: Member, url: str, rating: int, timeout=None):
        self.p1 = p1
        self.p2 = p2
        self.url = url
        self.rating = rating
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Complete", style=discord.ButtonStyle.success)
    async def complete(self, itr: Interaction, btn: discord.ui.Button):
        if itr.user.id != self.p1.id and itr.user.id != self.p2.id:
            embed = Embed(description="The challenge is not for you", color=Color.red())
            await itr.response.send_message(embed=embed, ephemeral=True)
        else:
            # embed = Embed(description="Checking if you completed the challenge", color=Color.purple())
            # await itr.response.send_message(embed=embed, ephemeral=True)
            winner_id = who_solved_first(self.p1.id, self.p2.id, self.url)
            if winner_id == None:
                embed = Embed(
                    description="None of you have completed the challenge yet",
                    color=Color.red(),
                )
                await itr.response.send_message(embed=embed, ephemeral=True)
            else:
                await itr.response.defer()
                loser = self.p1 if winner_id == self.p2.id else self.p2
                winner = client.get_user(winner_id)
                embed = Embed(
                    description=f"{winner.mention} won against {loser.mention}!",
                    color=Color.green(),
                )
                await itr.message.edit(embed=embed, view=None)


class ApprovalButtons(discord.ui.View):
    def __init__(self, by: Member, rating: int, opponent: Member, timeout=60):
        self.by = by
        self.rating = rating
        self.opponent = opponent
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, itr: Interaction, btn: discord.ui.Button):
        """
        - if same user show error
        - if user didnt set handle, show error
        - else start duel
        """
        if self.by.id == itr.user.id:
            embed = Embed(
                description="You can't accept your own challenge", color=Color.red()
            )
            await itr.response.send_message(embed=embed, ephemeral=True)
        elif not uid_exists(itr.user.id):
            embed = Embed(
                description=(
                    "Can't find you handle in the database\n"
                    "Use the `/sethandle` to set your handle"
                ),
                color=Color.red(),
            )
            await itr.response.send_message(embed=embed, ephemeral=True)
        elif self.opponent != None and self.opponent.id != itr.user.id:
            embed = Embed(
                description="This challenge is not for you", color=Color.red()
            )
            await itr.response.send_message(embed=embed, ephemeral=True)
        else:
            await itr.response.defer()
            embed = Embed(
                title="Starting challenge",
                description="This may tak a while...",
                color=Color.purple(),
            )
            await itr.message.edit(embed=embed, view=None)
            embed = Embed(
                title="Challenge started",
                description=f"{self.by.mention} :crossed_swords: {itr.user.mention}",
                color=Color.purple(),
            )
            embed.add_field(name="Rating", value=self.rating, inline=False)
            url = get_duel_url(uid1=itr.user.id, uid2=self.by.id, rating=self.rating)
            view = EndDuelButtons(p1=self.by, p2=itr.user, url=url, rating=self.rating)
            view.add_item(
                discord.ui.Button(
                    label="Problem",
                    style=discord.ButtonStyle.link,
                    url=url,
                )
            )
            await itr.message.edit(embed=embed, view=view)


@client.tree.command(
    name="challenge",
    description="Challenge someone with a CF problem (automatically withdrawn in 60s)",
)
async def challenge(itr: Interaction, rating: int, opponent: Member = None):
    """
    - if the user didn't set handle asks him to set handle
    - if rating is not valid send error message
    """
    if rating not in range(800, 3600, 100):
        embed = Embed(description=f"{rating} is not a valid rating", color=Color.red())
        await itr.response.send_message(embed=embed, ephemeral=True)
    elif not uid_exists(itr.user.id):
        embed = Embed(
            description=(
                "Can't find your handle in the database\n"
                "Use the `/sethandle` to set your handle"
            ),
            color=Color.red(),
        )
        await itr.response.send_message(embed=embed, ephemeral=True)
    elif opponent != None and not uid_exists(opponent.id):
        embed = Embed(
            description=(
                f"Can't find {opponent.mention}'s handle in the database\n"
                "Use the `/sethandle` to set his handle"
            ),
            color=Color.red(),
        )
        await itr.response.send_message(embed=embed)
    else:
        title = (
            "Anyone" if opponent == None else f"{opponent.display_name},"
        ) + " up for a duel?"
        embed = Embed(title=title, color=Color.purple())
        embed.add_field(name="Opponent", value=f"{itr.user.mention}", inline=False)
        embed.add_field(name="Rating", value=rating, inline=False)
        embed.set_footer(text=f"This challenge will be automatically withdrawn in 120s")
        content = None if opponent == None else opponent.mention
        await itr.response.send_message(
            content=content,
            embed=embed,
            view=ApprovalButtons(itr.user, rating, opponent, timeout=120),
        )


keep_alive()
TOKEN = os.environ["TOKEN"]
try:
    client.run(TOKEN)
except discord.errors.HTTPException:
    os.system("kill 1")
    os.system("python restarter.py")
