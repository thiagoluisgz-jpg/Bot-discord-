from discord.ext import commands

class Mensagens(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # =========================
        # PALAVRAS PROIBIDAS
        # =========================

        self.palavras_proibidas = [
            "teste",
            "aaa",
            "seila"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignora bots
        if message.author.bot:
            return

        texto = message.content.lower().strip()

        # =========================
        # PALAVRAS PROIBIDAS
        # =========================

        palavras = texto.split()

        for palavra in self.palavras_proibidas:

            if palavra in palavras:

                await message.delete()

                await message.channel.send(
                    f"{message.author.mention} essa palavra é proibida.",
                    delete_after=5
                )

                return

        # =========================
        # RESPOSTAS AUTOMÁTICAS
        # =========================

        # OI
        if texto == "oi":

            await message.channel.send(
                "Olá!"
            )

        # BOM DIA
        elif texto == "bom dia":

            await message.channel.send(
                "Bom dia!"
            )

        # TCHAU
        elif texto == "tchau":

            await message.channel.send(
                "Até mais!"
            )


# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(
        Mensagens(bot)
    )