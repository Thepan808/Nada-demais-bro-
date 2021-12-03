from asyncio import QueueEmpty
from pyrogram import Client, filters
from pyrogram.types import Message, Audio, Voice
from Music import app
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.decorate import authorized_users_only
from Music.MusicUtilities.helpers.filters import command, other_filters
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
import os
import yt_dlp
from youtubesearchpython import VideosSearch
from os import path
import random
import asyncio
import shutil
from time import time
import time as sedtime
from Music import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME, ASSMENTION
from Music.MusicUtilities.tgcallsrun import (music, convert, download, clear, get, is_empty, put, task_done, smexy)
from Music.MusicUtilities.helpers.gets import (get_url, themes, random_assistant)
from pyrogram.types import Message
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup, audio_markup)
from Music.MusicUtilities.tgcallsrun import (convert, download)
from pyrogram import filters
from typing import Union
from youtubesearchpython import VideosSearch
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant

flex = {}

async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = await app.get_chat_member(chat_id, user_id)
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms
from Music.MusicUtilities.helpers.administrator import adminsOnly

@app.on_message(filters.command("cleandb"))
async def stop_cmd(_, message): 
    chat_id = message.chat.id
    try:
        clear(chat_id)
    except QueueEmpty:
        pass                        
    await remove_active_chat(chat_id)
    try:
        await music.pytgcalls.leave_group_call(chat_id)
    except:
        pass   
    await message.reply_text("Database apagado, filas, registros, arquivos inúteis, e downloads.")
    
@app.on_message(filters.command("pause"))
async def pause_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("Você é um: __Anonymous Admin__!\nReverta para sua conta normalmente sem essa bosta de de Admin Anônimo beleza :).") 
    permission = "can_manage_voice_chats"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text("Eu não acho que tenha algo, que está tocando no bate-papo de voz")
    elif not await is_music_playing(message.chat.id):
        return await message.reply_text("Eu não acho que tenha-se algo, que está tocando no bate-papo de voz")   
    await music_off(chat_id)
    await music.pytgcalls.pause_stream(chat_id)
    await message.reply_text(f"♦️✔️ Transmissão pausada pelo {checking}!")
    
@app.on_message(filters.command("resume"))
async def stop_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("Ei fiato, tá usando a permissão de __Admin Anônimo__!\nReverta essa sua merda de conta pra usar o bot.") 
    permission = "can_manage_voice_chats"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text("Eu não acho que tem algo, que está tocando no bate-papo de voz")
    elif await is_music_playing(chat_id):
        return await message.reply_text("Eu não acho que, algo está tocando no bate-papo de voz") 
    else:
        await music_on(chat_id)
        await music.pytgcalls.resume_stream(chat_id)
        await message.reply_text(f"♦️🧐 Transmissão sendo resumida novamente pelo {checking}!")

@app.on_message(filters.command(["stop", "end"]))
async def stop_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("Ei fdp, tá usando a opção __Anonymous Admin__!\nReverta sua conta fi.") 
    permission = "can_manage_voice_chats"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass                        
        await remove_active_chat(chat_id)
        await music.pytgcalls.leave_group_call(chat_id)
        await message.reply_text(f"😒 Transmissão encerrada pelo {checking}!") 
    else:
        return await message.reply_text("Eu não acho que tenha algo, que está tocando no bate-papo de voz")
    
@app.on_message(filters.command("skip"))
async def stop_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("Você tá com admin com essa permissão __Anonymous Admin__!\nReverta tua conta.") 
    permission = "can_manage_voice_chats"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not await is_active_chat(chat_id):
        await message.reply_text("Nada está tocando na call")
    else:
        task_done(chat_id)
        if is_empty(chat_id):
            await remove_active_chat(chat_id)
            await message.reply_text("Não há mais música em __Fila__ \n\nSaindo da call")
            await music.pytgcalls.leave_group_call(chat_id)
            return  
        else:
            afk = get(chat_id)['file']
            f1 = (afk[0])
            f2 = (afk[1])
            f3 = (afk[2])
            finxx = (f"{f1}{f2}{f3}")
            if str(finxx) != "raw":   
                mystic = await message.reply_text("Música está atualmente tocando na Playlist...\n\nBaixando a próxima música da lista de reprodução....")
                url = (f"https://www.youtube.com/watch?v={afk}")
                try:
                    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                        x = ytdl.extract_info(url, download=False)
                except Exception as e:
                    return await mystic.edit(f"Falha ao baixar este vídeo.\n\n**Razão por isso**:{e}") 
                title = (x["title"])
                videoid = afk
                def my_hook(d):
                    if d['status'] == 'downloading':
                        percentage = d['_percent_str']
                        per = (str(percentage)).replace(".","", 1).replace("%","", 1)
                        per = int(per)
                        eta = d['eta']
                        speed = d['_speed_str']
                        size = d['_total_bytes_str']
                        bytesx = d['total_bytes']
                        if str(bytesx) in flex:
                            pass
                        else:
                            flex[str(bytesx)] = 1
                        if flex[str(bytesx)] == 1:
                            flex[str(bytesx)] += 1
                            sedtime.sleep(1)
                            mystic.edit(f"Baixando {title[:50]}\n\n**Arquivo Size:** {size}\n**Baixando:** {percentage}\n**Rapidamente em:** {speed}\n**ETA:** {eta} sec")
                        if per > 500:    
                            if flex[str(bytesx)] == 2:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Baixando {title[:50]}...\n\n**Arquivo Size:** {size}\n**Baixando:** {percentage}\n**Rapidamente em:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Baixando {percentage} a uma velocidade de {speed} em {chat_title} | ETA: {eta} seconds")
                        if per > 800:    
                            if flex[str(bytesx)] == 3:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Baixando {title[:50]}....\n\n**Arquivo Size:** {size}\n**Baixando:** {percentage}\n**Rapidamente em:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Baixando {percentage} a uma velocidade de {speed} em {chat_title} | ETA: {eta} seconds")
                        if per == 1000:    
                            if flex[str(bytesx)] == 4:
                                flex[str(bytesx)] = 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Baixando {title[:50]}.....\n\n**Arquivo Size:** {size}\n**Baixando:** {percentage}\n**Velocidade de:** {speed}\n**ETA:** {eta} sec") 
                                print(f"[{videoid}] Baixando {percentage} a uma velocidade de {speed} em {chat_title} | ETA: {eta} seconds")
                loop = asyncio.get_event_loop()
                xxx = await loop.run_in_executor(None, download, url, my_hook)
                file = await convert(xxx)
                await music.pytgcalls.change_stream(
                    chat_id, 
                    InputStream(
                        InputAudioStream(
                            file,
                        ),
                    ),
                )
                thumbnail = (x["thumbnail"])
                duration = (x["duration"])
                duration = round(x["duration"] / 60)
                theme = random.choice(themes)
                ctitle = (await app.get_chat(chat_id)).title
                ctitle = await CHAT_TITLE(ctitle)
                f2 = open(f'search/{afk}id.txt', 'r')        
                userid =(f2.read())
                thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                user_id = userid
                buttons = play_markup(videoid, user_id)
                await mystic.delete()
                semx = await app.get_users(userid)
                await message.reply_photo(
                photo= thumb,
                reply_markup=InlineKeyboardMarkup(buttons),    
                caption=(f"<b>__Pulou a faixa__</b>\n\n♦️ <b>__Transmissão iniciada, tocando:__ </b>[{title[:25]}]({url}) \n♦️ <b>__Duração:__</b> {duration} Mins\n🧐 **__Pedido pelo:__** {semx.mention}")
            )   
                os.remove(thumb)
            else:      
                await music.pytgcalls.change_stream(
                    chat_id, 
                    InputStream(
                        InputAudioStream(
                            afk,
                        ),
                    ),
                )
                _chat_ = ((str(afk)).replace("_","", 1).replace("/","", 1).replace(".","", 1))
                f2 = open(f'search/{_chat_}title.txt', 'r')        
                title =(f2.read())
                f3 = open(f'search/{_chat_}duration.txt', 'r')        
                duration =(f3.read())
                f4 = open(f'search/{_chat_}username.txt', 'r')        
                username =(f4.read())
                f4 = open(f'search/{_chat_}videoid.txt', 'r')        
                videoid =(f4.read())
                user_id = 1
                videoid = str(videoid)
                if videoid == "smex1":
                    buttons = audio_markup(videoid, user_id)
                else:
                    buttons = play_markup(videoid, user_id)
                await message.reply_photo(
                photo=f"downloads/{_chat_}final.png",
                reply_markup=InlineKeyboardMarkup(buttons),
                caption=f"<b>__Próxima faixa__</b>\n\n♦️ <b>__Transmissão iniciada, tocando:__</b> {title} \n♦️ <b>__Duração:__</b> {duration} \n🧐 <b>__Pedido pelo:__ </b> {username}",
                )
                return
