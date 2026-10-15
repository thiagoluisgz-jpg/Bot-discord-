from discord.ext import commands
import random

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def moeda(self, ctx):

        print("COMANDO MOEDA EXECUTOU")

        resultado = random.choice(
            ["Cara", "Coroa"]
        )

        await ctx.send(resultado)

    @commands.command()
    async def dado(self, ctx):

        numero = random.randint(1, 6)

        await ctx.send(f'Dado: {numero}')

# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(Fun(bot))