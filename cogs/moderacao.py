from discord.ext import commands
import discord


class Moderacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # MUTE INTERNO
    # =========================

    async def aplicar_mute(
        self,
        membro,
        motivo="Sem motivo"
    ):

        cargo = discord.utils.get(
            membro.guild.roles,
            name="Mutado"
        )

        # Se o cargo não existir
        if cargo is None:

            cargo = await membro.guild.create_role(
                name="Mutado",
                reason="Criação automática do cargo de mute"
            )

        # Adicionar cargo
        await membro.add_roles(
            cargo,
            reason=motivo
        )

        return cargo

    # =========================
    # KICK INTERNO
    # =========================

    async def aplicar_kick(
        self,
        membro,
        motivo="Sem motivo"
    ):

        await membro.kick(
            reason=motivo
        )

    # =========================
    # BAN INTERNO
    # =========================

    async def aplicar_ban(
        self,
        membro,
        motivo="Sem motivo"
    ):

        await membro.ban(
            reason=motivo
        )

    # =========================
    # LIMPAR
    # =========================

    @commands.command()
    @commands.has_permissions(
        manage_messages=True
    )
    async def limpar(
        self,
        ctx,
        quantidade: int
    ):

        apagadas = await ctx.channel.purge(
            limit=quantidade + 1
        )

        await ctx.send(
            f"{len(apagadas) - 1} mensagens apagadas."
        )

    # =========================
    # KICK
    # =========================

    @commands.command()
    @commands.has_permissions(
        kick_members=True
    )
    async def kick(
        self,
        ctx,
        membro: discord.Member,
        *,
        motivo="Sem motivo"
    ):

        await self.aplicar_kick(
            membro,
            motivo
        )

        await ctx.send(
            f"{membro.mention} foi expulso."
        )

    # =========================
    # BAN
    # =========================

    @commands.command()
    @commands.has_permissions(
        ban_members=True
    )
    async def ban(
        self,
        ctx,
        membro: discord.Member,
        *,
        motivo="Sem motivo"
    ):

        await self.aplicar_ban(
            membro,
            motivo
        )

        await ctx.send(
            f"{membro.mention} foi banido."
        )

    # =========================
    # MUTAR
    # =========================

    @commands.command()
    @commands.has_permissions(
        manage_roles=True
    )
    async def mutar(
        self,
        ctx,
        membro: discord.Member,
        *,
        motivo="Sem motivo"
    ):

        await self.aplicar_mute(
            membro,
            motivo
        )

        await ctx.send(
            f"{membro.mention} foi mutado."
        )


# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(
        Moderacao(bot)
    )