import discord
from discord.ext import commands


class AutoRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # NOVO USUÁRIO
    # =========================

    @commands.Cog.listener()
    async def on_member_join(self, member):

        print(
            f"[AUTOROLE] Novo usuário: {member}"
        )

        # =========================
        # PROCURAR CARGO
        # =========================

        cargo = discord.utils.get(
            member.guild.roles,
            name="Membro"
        )

        if cargo is None:

            print(
                f"[AUTOROLE] Cargo 'Membro' não encontrado."
            )

            return

        # =========================
        # VERIFICAR HIERARQUIA
        # =========================

        if cargo >= member.guild.me.top_role:

            print(
                "[AUTOROLE] Não posso adicionar esse cargo."
            )

            return

        # =========================
        # ADICIONAR CARGO
        # =========================

        try:

            await member.add_roles(
                cargo,
                reason="AutoRole - novo membro"
            )

            print(
                f"[AUTOROLE] Cargo '{cargo.name}' "
                f"adicionado para {member}."
            )

        except discord.Forbidden:

            print(
                "[AUTOROLE] Sem permissão para adicionar o cargo."
            )

        except Exception as erro:

            print(
                f"[AUTOROLE] Erro: {erro}"
            )


# =========================
# SETUP
# =========================

async def setup(bot):

    await bot.add_cog(
        AutoRole(bot)
    )