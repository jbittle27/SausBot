from discord.ext import commands


class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f'{ctx.command.name} was invoked incorrectly.')
        print(error)


def setup(bot):
    bot.add_cog(CommandEvents(bot))
