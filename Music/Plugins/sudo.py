from Music import app, OWNER
import os
import subprocess
import shutil
import re
import sys
import traceback
from Music.MusicUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo, add_sudo)
from pyrogram import filters, Client
from pyrogram.types import Message

@app.on_message(filters.command("addmsudo") & filters.user(OWNER))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("❌ Responda à mensagem de um usuário ou dê nome de usuário/user_id.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user 
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("✅ Adicionado como Sudo User.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(f"✅ Adicionado **{user.mention}** como um Super Usuário para o Baianor")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await edit_or_reply(message, text="❌ Algo errado aconteceu, verifique os registros.")  
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("✅ Já é usuário do Sudo.")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"✅ Adicionado **{mention}** como um Super Usuário para Baianor")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await edit_or_reply(message, text="❌ Algo errado aconteceu, verifique os registros.")  
    return    
          
              
@app.on_message(filters.command("delmsudo") & filters.user(OWNER))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("❌ Responda à mensagem de um usuário ou dê nome de usuário/user_id.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user      
        if user.id not in await get_sudoers():
            return await message.reply_text(f"❌ Não faz parte do Sudo do Baianor..")        
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"✅ Removido **{user.mention}** Para Sudo Baianor.")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await message.reply_text(f"❌ Algo errado aconteceu..")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"❌ Não faz parte do Sudo de Panda..")        
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"✅ Removido **{mention}** para Pan Sudo.")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await message.reply_text(f"❌ Algo errado aconteceu..")
                
                          
@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "**__Lista de Usuários sudo do Baianor:-__**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:                     
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue                     
        text += f"➤ {user}\n"
    if not text:
        await message.reply_text("❌ Sem usuários sudo")  
    else:
        await message.reply_text(text) 
