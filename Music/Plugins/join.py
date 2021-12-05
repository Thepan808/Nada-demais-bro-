from pyrogram import filters, Client
from pyrogram.types import Message
from Music.MusicUtilities.tgcallsrun import ASS_ACC as USER

@Client.on_message(filters.private & filters.incoming & filters.command("join"))
async def userbotjoin(_, message: Message):
    lol = await message.reply_text("**Processando...**")
    print("join request")
    if len(message.command) == 1:
        try:
           await lol.edit("**Dê um link de convite também!**")
        except:
          return
    elif len(message.command) == 2:      
        try:
           await lol.edit("Verificando o link de convite...")
           await asyncio.sleep(2)
           query = message.text.split(None, 1)[1]
           query = str(query)
           
           if query.startswith("http://t.me/+"):
              query = query.replace("http://t.me/+","https://t.me/joinchat/")
              pass
           elif query.startswith("https://t.me/+"):
              query = query.replace("https://t.me/+","https://t.me/joinchat/")
              pass
           elif query.startswith("t.me/+"):
              query = query.replace("t.me/+","https://t.me/joinchat/")
              pass
           elif query.startswith("telegram.me/+"):
              query = query.replace("telegram.me/+","https://t.me/joinchat/")
              pass
           elif query.startswith("-1"):
              return await lol.edit(f"Use /play comando no chat para convidar userbot para bate-papos públicos")
           elif query.startswith("http://t.me/"):
              query = query.replace("http://t.me/","https://t.me/joinchat/")
              return await lol.edit(f"Use /play comando no chat para convidar userbot para bate-papos públicos")
           elif query.startswith("https://"):
              query = query.replace("https://t.me/","https://t.me/joinchat/")
              return await lol.edit(f"Use /play comando no chat para convidar userbot para bate-papos públicos")
           elif query.startswith("t.me/"):
              query = query.replace("t.me/","https://t.me/joinchat/")
              return await lol.edit(f"Use /play comando no chat para convidar userbot para bate-papos públicos")
           elif query.startswith("telegram.me/"):
              query = query.replace("telegram.me/","https://t.me/joinchat/")
              return await lol.edit(f"Use /play comando no chat para convidar userbot para bate-papos públicos")            
           elif query.startswith("@"): 
              return await lol.edit(f"Use /play comando no chat para convidar userbot para bate-papos públicos")
           else:
              return await lol.edit(f"O link `{query}` é inválido..! Verifique novamente.")
           try:
              await lol.edit("Assiatant se juntando ao seu bate-papo...")
           except:
              pass
           try:
              await USER.join_chat(query)
              await USER.send_message(query, "Eu me juntei aqui como seu pedido")
              await lol.edit("Assistente juntou-se com sucesso ao seu bate-papo")
           except UserAlreadyParticipant:
              await lol.edit("Assistente já em seu bate-papo")
              pass   
           except Exception as e:
              return await lol.edit(f"Um erro ocorreu ao participar do seu bate-papo.\n\nRazão: {e}")
           except:
              return await lol.edit(f"Um erro ocorreu ao participar do seu bate-papo")   
                    
           return await lol.edit("Ocorreu erro desconhecido")
        except:
          return
    else:
       return
