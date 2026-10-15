import discord
from discord.ext import commands


class BoasVindas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # USUÁRIO ENTROU
    # =========================

    @commands.Cog.listener()
    async def on_member_join(self, member):

        print(
            f"[BOAS-VINDAS] Novo usuário: {member}"
        )

        # =========================
        # PROCURAR CANAL
        # =========================

        canal = discord.utils.get(
            member.guild.text_channels,
            name="entrada-saida"
        )

        if canal is None:

            print(
                "[BOAS-VINDAS] Canal 'boas-vindas' não encontrado."
            )

            return

        # =========================
        # EMBED DE ENTRADA
        # =========================

        embed = discord.Embed(
            title="🎉 Bem-vindo!",
            description=(
                f"Olá {member.mention}!\n\n"
                f"Seja muito bem-vindo ao "
                f"**{member.guild.name}**!\n\n"
                f"Esperamos que você aproveite "
                f"o servidor. ❤️"
            ),
            color=discord.Color.green()
        )

        # Avatar
        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        # Informações
        embed.add_field(
            name="👤 Usuário",
            value=member.mention,
            inline=True
        )

        embed.add_field(
            name="🆔 ID",
            value=str(member.id),
            inline=True
        )

        embed.add_field(
            name="👥 Membros",
            value=str(member.guild.member_count),
            inline=True
        )

        embed.set_footer(
            text=f"Seja o membro #{member.guild.member_count}"
        )

        embed.timestamp = discord.utils.utcnow()

        # Enviar
        await canal.send(
            embed=embed
        )

    # =========================
    # USUÁRIO SAIU
    # =========================

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        print(
            f"[SAÍDA] Usuário saiu: {member}"
        )

        # =========================
        # PROCURAR CANAL
        # =========================

        canal = discord.utils.get(
            member.guild.text_channels,
            name="entrada-saida"
        )

        if canal is None:

            print(
                "[SAÍDA] Canal 'saida' não encontrado."
            )

            return

        # =========================
        # EMBED DE SAÍDA
        # =========================

        embed = discord.Embed(
            title="👋 Até mais!",
            description=(
                f"**{member}** saiu do servidor.\n\n"
                f"Esperamos vê-lo novamente! ❤️"
            ),
            color=discord.Color.orange()
        )

        # Avatar
        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        # Informações
        embed.add_field(
            name="👤 Usuário",
            value=f"`{member}`",
            inline=True
        )

        embed.add_field(
            name="🆔 ID",
            value=str(member.id),
            inline=True
        )

        embed.add_field(
            name="👥 Membros restantes",
            value=str(member.guild.member_count),
            inline=True
        )

        embed.set_footer(
            text="Usuário deixou o servidor"
        )

        embed.timestamp = discord.utils.utcnow()

        # Enviar
        await canal.send(
            embed=embed
        )


# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(
        BoasVindas(bot)
    )