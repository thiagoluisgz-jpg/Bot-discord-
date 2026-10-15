from discord.ext import commands
import discord
import asyncio

class Logs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # CANAL DE LOG
    # =========================

    async def pegar_canal_log(self, guild):

        return discord.utils.get(
            guild.text_channels,
            name="logs"
        )

    # =========================
    # PEGAR AUTOR DA AÇÃO
    # =========================

    async def pegar_autor(
        self,
        guild,
        action,
        target_id=None
    ):

        await asyncio.sleep(1)

        try:

            async for entry in guild.audit_logs(
                limit=10,
                action=action
            ):

                if (
                    target_id is None
                    or entry.target.id == target_id
                ):

                    return (
                        entry.user.mention,
                        entry.reason
                    )

        except Exception as erro:

            print(
                f"Erro audit log: {erro}"
            )

        return (
            "Desconhecido",
            "Sem motivo"
        )

    # =========================
    # CRIAR EMBED PADRÃO
    # =========================

    def criar_embed(
        self,
        titulo,
        cor,
        usuario=None
    ):

        embed = discord.Embed(
            title=titulo,
            color=cor
        )

        embed.timestamp = (
            discord.utils.utcnow()
        )

        if usuario:

            embed.set_thumbnail(
                url=usuario.display_avatar.url
            )

            embed.set_footer(
                text=f"ID: {usuario.id}"
            )

        return embed

    # =========================
    # MENSAGEM APAGADA
    # =========================

    @commands.Cog.listener()
    async def on_message_delete(
        self,
        message
    ):

        if message.author.bot:
            return

        canal = await self.pegar_canal_log(
            message.guild
        )

        if canal is None:
            return

        embed = self.criar_embed(
            "Mensagem apagada",
            discord.Color.red(),
            message.author
        )

        embed.add_field(
            name="Usuário",
            value=(
                f"{message.author.mention}\n"
                f"`{message.author}`"
            ),
            inline=False
        )

        embed.add_field(
            name="Mensagem",
            value=message.content or "Sem texto",
            inline=False
        )

        embed.add_field(
            name="Canal",
            value=message.channel.mention,
            inline=False
        )

        await canal.send(embed=embed)

    # =========================
    # USUÁRIO ENTROU
    # =========================

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member
    ):

        canal = await self.pegar_canal_log(
            member.guild
        )

        if canal is None:
            return

        embed = self.criar_embed(
            "Usuário entrou",
            discord.Color.green(),
            member
        )

        embed.add_field(
            name="Usuário",
            value=(
                f"{member.mention}\n"
                f"`{member}`"
            ),
            inline=False
        )

        await canal.send(embed=embed)

    # =========================
    # USUÁRIO SAIU / KICK
    # =========================

    @commands.Cog.listener()
    async def on_member_remove(
        self,
        member
    ):

        canal = await self.pegar_canal_log(
            member.guild
        )

        if canal is None:
            return

        try:

            async for entry in member.guild.audit_logs(
                limit=5,
                action=discord.AuditLogAction.kick
            ):

                if entry.target.id == member.id:

                    embed = self.criar_embed(
                        "Usuário expulso",
                        discord.Color.red(),
                        member
                    )

                    embed.add_field(
                        name="Usuário",
                        value=(
                            f"{member.mention}\n"
                            f"`{member}`"
                        ),
                        inline=False
                    )

                    embed.add_field(
                        name="Moderador",
                        value=entry.user.mention,
                        inline=False
                    )

                    embed.add_field(
                        name="Motivo",
                        value=(
                            entry.reason
                            or "Sem motivo"
                        ),
                        inline=False
                    )

                    await canal.send(embed=embed)

                    return

        except Exception as erro:

            print(
                f"Erro ao verificar kick: {erro}"
            )

        embed = self.criar_embed(
            "Usuário saiu",
            discord.Color.orange(),
            member
        )

        embed.add_field(
            name="Usuário",
            value=(
                f"{member.mention}\n"
                f"`{member}`"
            ),
            inline=False
        )

        await canal.send(embed=embed)

    # =========================
    # BAN
    # =========================

    @commands.Cog.listener()
    async def on_member_ban(
        self,
        guild,
        user
    ):

        canal = await self.pegar_canal_log(
            guild
        )

        if canal is None:
            return

        autor, motivo = await self.pegar_autor(
            guild,
            discord.AuditLogAction.ban,
            user.id
        )

        embed = self.criar_embed(
            "Usuário banido",
            discord.Color.dark_red(),
            user
        )

        embed.add_field(
            name="Usuário",
            value=(
                f"{user.mention}\n"
                f"`{user}`"
            ),
            inline=False
        )

        embed.add_field(
            name="Moderador",
            value=autor,
            inline=False
        )

        embed.add_field(
            name="Motivo",
            value=motivo or "Sem motivo",
            inline=False
        )

        await canal.send(embed=embed)

    # =========================
    # CARGO ALTERADO
    # =========================

    @commands.Cog.listener()
    async def on_member_update(
        self,
        before,
        after
    ):

        canal = await self.pegar_canal_log(
            after.guild
        )

        if canal is None:
            return

        cargos_antes = set(before.roles)
        cargos_depois = set(after.roles)

        cargo_add = cargos_depois - cargos_antes
        cargo_remove = cargos_antes - cargos_depois

        autor, motivo = await self.pegar_autor(
            after.guild,
            discord.AuditLogAction.member_role_update,
            after.id
        )

        # =========================
        # CARGO ADICIONADO
        # =========================

        for cargo in cargo_add:

            embed = self.criar_embed(
                "Cargo adicionado",
                discord.Color.blue(),
                after
            )

            embed.add_field(
                name="Usuário",
                value=(
                    f"{after.mention}\n"
                    f"`{after}`"
                ),
                inline=False
            )

            embed.add_field(
                name="Cargo",
                value=cargo.mention,
                inline=False
            )

            embed.add_field(
                name="Autor",
                value=autor,
                inline=False
            )

            await canal.send(embed=embed)

        # =========================
        # CARGO REMOVIDO
        # =========================

        for cargo in cargo_remove:

            embed = self.criar_embed(
                "Cargo removido",
                discord.Color.orange(),
                after
            )

            embed.add_field(
                name="Usuário",
                value=(
                    f"{after.mention}\n"
                    f"`{after}`"
                ),
                inline=False
            )

            embed.add_field(
                name="Cargo",
                value=cargo.name,
                inline=False
            )

            embed.add_field(
                name="Autor",
                value=autor,
                inline=False
            )

            await canal.send(embed=embed)

    # =========================
    # CANAL CRIADO
    # =========================

    @commands.Cog.listener()
    async def on_guild_channel_create(
        self,
        channel
    ):

        canal_logs = await self.pegar_canal_log(
            channel.guild
        )

        if canal_logs is None:
            return

        autor, motivo = await self.pegar_autor(
            channel.guild,
            discord.AuditLogAction.channel_create,
            channel.id
        )

        embed = self.criar_embed(
            "Canal criado",
            discord.Color.green()
        )

        embed.add_field(
            name="Canal",
            value=channel.mention,
            inline=False
        )

        embed.add_field(
            name="Autor",
            value=autor,
            inline=False
        )

        await canal_logs.send(embed=embed)

    # =========================
    # CANAL DELETADO
    # =========================

    @commands.Cog.listener()
    async def on_guild_channel_delete(
        self,
        channel
    ):

        canal_logs = await self.pegar_canal_log(
            channel.guild
        )

        if canal_logs is None:
            return

        autor, motivo = await self.pegar_autor(
            channel.guild,
            discord.AuditLogAction.channel_delete
        )

        embed = self.criar_embed(
            "Canal deletado",
            discord.Color.red()
        )

        embed.add_field(
            name="Canal",
            value=channel.name,
            inline=False
        )

        embed.add_field(
            name="Autor",
            value=autor,
            inline=False
        )

        await canal_logs.send(embed=embed)

    # =========================
    # CANAL ALTERADO
    # =========================

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self,
        before,
        after
    ):

        canal_logs = await self.pegar_canal_log(
            after.guild
        )

        if canal_logs is None:
            return

        if before.name != after.name:

            autor, motivo = await self.pegar_autor(
                after.guild,
                discord.AuditLogAction.channel_update,
                after.id
            )

            embed = self.criar_embed(
                "Canal alterado",
                discord.Color.blue()
            )

            embed.add_field(
                name="Antes",
                value=before.name,
                inline=False
            )

            embed.add_field(
                name="Depois",
                value=after.name,
                inline=False
            )

            embed.add_field(
                name="Autor",
                value=autor,
                inline=False
            )

            await canal_logs.send(embed=embed)

# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(
        Logs(bot)
    )