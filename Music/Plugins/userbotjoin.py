import asyncio
from Music import client as USER
from Music import BOT_USERNAME
from Music.config import OWNER_ID
from Music import ASSNAME, ASSUSERNAME
from Music.MusicUtilities.helpers.decorate import authorized_users_only, sudo_users_only, errors
from Music.MusicUtilities.helpers.filters import command
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"userbotjoin"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "• **Eu não tenho permissão:**\n\n» ❌ __Adicionar usuários__",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Assistant_Grave_Sad_Official"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 Erro de espera por inundação 🛑 \n\n** ❌ {ASSNAME}(@{ASSUSERNAME}) não poderia se juntar ao seu grupo devido a pedidos pesados de adesão para userbot**"
            "\n\n**Você deve adicionar o assistente manualmente ao seu Grupo e tentar novamente**",
        )
        return
    await message.reply_text(
        f"✅ **Userbot entrou ao chat**",
    )


@Client.on_message(
    command(["leave", f"userbotleave"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def leave_group(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ userbot deixou o chat com sucesso")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "❌ **Userbot não poderia deixar o seu grupo, pode ser floodwaits.**\n\n**» ou dê kick ou ban e depois tira ~ manualmente o userbot do seu grupo**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in OWNER_ID:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **Userbot** deixando todos os bate-papos !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Userbot deixando todo os grupos...\n\nSaiu em: {left} chats.\nFalhou em: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Userbot saindo...\n\nSaiu em: {left} chats.\nFalhou em: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ Saiu de: {left} chats.\n❌ Falhou em: {failed} chats."
    )
