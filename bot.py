import discord
from discord.ext import commands
import asyncio
import os

# =========================
# CONFIG
# =========================

from configs.config import (
    TOKEN,
    PREFIX,
    STATUS
)

# =========================
# INTENTS
# =========================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

# =========================
# BOT
# =========================

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents
)

# =========================
# CARREGAR COGS E EVENTOS
# =========================

async def load():

    print("LOAD EXECUTADO")

    # =========================
    # COGS
    # =========================

    for arquivo in os.listdir("./cogs"):

        if (
            arquivo.endswith(".py")
            and arquivo != "__init__.py"
        ):

            try:

                await bot.load_extension(
                    f"cogs.{arquivo[:-3]}"
                )

                print(
                    f'Cog carregada: {arquivo}'
                )

            except Exception as erro:

                print(
                    f'Erro ao carregar cog {arquivo}'
                )

                print(erro)

    # =========================
    # EVENTOS
    # =========================

    for arquivo in os.listdir("./eventos"):

        if (
            arquivo.endswith(".py")
            and arquivo != "__init__.py"
        ):

            try:

                await bot.load_extension(
                    f"eventos.{arquivo[:-3]}"
                )

                print(
                    f'Evento carregado: {arquivo}'
                )

            except Exception as erro:

                print(
                    f'Erro ao carregar evento {arquivo}'
                )

                print(erro)

# =========================
# READY
# =========================

@bot.event
async def on_ready():

    print("=" * 40)
    print(f'Bot online como {bot.user}')
    print("=" * 40)

    # STATUS
    await bot.change_presence(
        activity=discord.Game(STATUS)
    )

# =========================
# MAIN
# =========================

async def main():

    async with bot:

        await load()

        await bot.start(TOKEN)

# =========================
# INICIAR BOT
# =========================

asyncio.run(main())