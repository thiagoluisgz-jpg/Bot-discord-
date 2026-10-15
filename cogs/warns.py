from discord.ext import commands
import discord


class Warns(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # =========================
        # ARMAZENAR WARNS
        # =========================

        self.warns = {}

    # =========================
    # VERIFICAR PUNIÇÃO
    # =========================

    async def verificar_punicao(
        self,
        ctx,
        membro
    ):

        quantidade = len(
            self.warns.get(
                membro.id,
                []
            )
        )

        moderacao = self.bot.get_cog(
            "Moderacao"
        )

        if moderacao is None:

            print(
                "[WARNS] Cog Moderacao não encontrada."
            )

            return

        # =========================
        # 2 WARNS → MUTE
        # =========================

        if quantidade == 2:

            await moderacao.aplicar_mute(
                membro,
                "2 warns acumulados"
            )

            await ctx.send(
                f"🔇 {membro.mention} foi mutado "
                f"automaticamente por atingir "
                f"**2 warns**."
            )

        # =========================
        # 3 WARNS → KICK
        # =========================

        elif quantidade == 3:

            await moderacao.aplicar_kick(
                membro,
                "3 warns acumulados"
            )

            await ctx.send(
                f"👢 {membro.mention} foi expulso "
                f"automaticamente por atingir "
                f"**3 warns**."
            )

        # =========================
        # 4 WARNS → BAN
        # =========================

        elif quantidade >= 4:

            await moderacao.aplicar_ban(
                membro,
                "4 warns acumulados"
            )

            await ctx.send(
                f"🔨 {membro.mention} foi banido "
                f"automaticamente por atingir "
                f"**4 warns**."
            )

    # =========================
    # WARN
    # =========================

    @commands.command()
    @commands.has_permissions(
        manage_messages=True
    )
    async def warn(
        self,
        ctx,
        membro: discord.Member,
        *,
        motivo="Sem motivo"
    ):

        # =========================
        # CRIAR LISTA
        # =========================

        if membro.id not in self.warns:

            self.warns[membro.id] = []

        # =========================
        # ADICIONAR WARN
        # =========================

        self.warns[membro.id].append({

            "motivo": motivo,

            "moderador": ctx.author.id

        })

        quantidade = len(
            self.warns[membro.id]
        )

        # =========================
        # EMBED
        # =========================

        embed = discord.Embed(
            title="⚠️ Advertência",
            description=(
                f"{membro.mention} recebeu "
                f"uma advertência."
            ),
            color=discord.Color.orange()
        )

        # Avatar

        embed.set_thumbnail(
            url=membro.display_avatar.url
        )

        # Usuário

        embed.add_field(
            name="👤 Usuário",
            value=(
                f"{membro.mention}\n"
                f"`{membro}`"
            ),
            inline=False
        )

        # Motivo

        embed.add_field(
            name="📝 Motivo",
            value=motivo,
            inline=False
        )

        # Moderador

        embed.add_field(
            name="👮 Moderador",
            value=ctx.author.mention,
            inline=False
        )

        # Total

        embed.add_field(
            name="⚠️ Total de warns",
            value=str(quantidade),
            inline=False
        )

        embed.set_footer(
            text=f"ID do usuário: {membro.id}"
        )

        embed.timestamp = discord.utils.utcnow()

        await ctx.send(
            embed=embed
        )

        # =========================
        # VERIFICAR PUNIÇÃO
        # =========================

        await self.verificar_punicao(
            ctx,
            membro
        )

    # =========================
    # LISTAR WARNS
    # =========================

    @commands.command()
    @commands.has_permissions(
        manage_messages=True
    )
    async def warns(
        self,
        ctx,
        membro: discord.Member
    ):

        lista = self.warns.get(
            membro.id,
            []
        )

        if not lista:

            await ctx.send(
                f"{membro.mention} "
                f"não possui warns."
            )

            return

        embed = discord.Embed(
            title="⚠️ Histórico de advertências",
            color=discord.Color.orange()
        )

        embed.set_thumbnail(
            url=membro.display_avatar.url
        )

        for numero, warn in enumerate(
            lista,
            start=1
        ):

            moderador = ctx.guild.get_member(
                warn["moderador"]
            )

            if moderador:

                moderador_texto = (
                    moderador.mention
                )

            else:

                moderador_texto = (
                    f"`{warn['moderador']}`"
                )

            embed.add_field(
                name=f"Warn #{numero}",
                value=(
                    f"📝 **Motivo:** "
                    f"{warn['motivo']}\n"
                    f"👮 **Moderador:** "
                    f"{moderador_texto}"
                ),
                inline=False
            )

        embed.set_footer(
            text=(
                f"Total: {len(lista)} warns"
            )
        )

        await ctx.send(
            embed=embed
        )

    # =========================
    # LIMPAR WARNS
    # =========================

    @commands.command()
    @commands.has_permissions(
        manage_messages=True
    )
    async def clearwarns(
        self,
        ctx,
        membro: discord.Member
    ):

        if membro.id not in self.warns:

            await ctx.send(
                f"{membro.mention} "
                f"não possui warns."
            )

            return

        quantidade = len(
            self.warns[membro.id]
        )

        del self.warns[membro.id]

        await ctx.send(
            f"✅ Foram removidos "
            f"**{quantidade} warns** de "
            f"{membro.mention}."
        )


# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(
        Warns(bot)
    )