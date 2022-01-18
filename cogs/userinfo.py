from discord.commands.commands import Option
from discord.ext import commands
from discord import Member, Embed
from discord.commands import slash_command

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[919085238427201567], name="userprofile")
    async def userprofile(self, ctx, user: Option(Member, "Enter a user", required=False)):
        """Get information of a user"""
        user = ctx.user if user is None else user
        embed = Embed(color=user.top_role.color, title="User Profile", type='rich')
        roles = "No roles."
        if len(user.roles) != 0:
            roles = ""
            reversed_roles = user.roles
            reversed_roles.reverse()

            for role in reversed_roles[:-1]:
                roles += role.mention + " "

        embed.set_author(name=user)
        embed.set_thumbnail(url=user.display_avatar.url)

        embed.add_field(name="Username", value=f"{user} ({user.mention})", inline=True)
        embed.add_field(name="Level", value="Placeholder", inline=True)
        embed.add_field(name="XP", value="Placeholder", inline=True)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.add_field(name="Joined at", value=f"<t:{int(user.joined_at.timestamp())}:F> (<t:{int(user.joined_at.timestamp())}:R>)", inline=False)
        embed.add_field(name="Acount created at", value=f"<t:{int(user.created_at.timestamp())}:F> (<t:{int(user.created_at.timestamp())}:R>)", inline=False)

        await ctx.respond(embed=embed)
