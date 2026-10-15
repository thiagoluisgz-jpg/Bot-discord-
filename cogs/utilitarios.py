from discord.ext import commands

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):

        await ctx.send("Pong!")

    @commands.command()
    async def ola(self, ctx):

        await ctx.send(f'Olá {ctx.author.mention}!')

async def setup(bot):

    await bot.add_cog(Utility(bot))