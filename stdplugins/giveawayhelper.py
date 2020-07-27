import asyncio
import datetime
from telethon import events
from uniborg.util import admin_cmd
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputMediaUploadedDocument,
    InputMediaUploadedPhoto,
    InputPeerNotifySettings,
    InputStickerSetID,
    InputStickerSetShortName,
    MessageMediaPhoto
)
from sql_helpers.ghdb_sql import in_channels, add_channel, rm_channel, get_all_channels

logs_id = Config.LOG_ID



@borg.on(admin_cmd("forward ?(.*)"))

async def forw(event): 
  if event.fwd_from:
    return
  channels = get_all_channels()
  await event.edit("Sending...")
  error_count = 0
  sent_count = 0 
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    message = previous_message.message
    raw_text = previous_message.raw_text
  error_count = 0
  for channel in channels:
    try:
      await borg.forward_messages(int(channel.chat_id), previous_message)
      sent_count += 1
      await event.edit(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
    except Exception as error:
      try:
        await borg.send_message(logs_id, f"Error in sending at {channel.chat_id}.")
        await borg.send_message(logs_id, "Error! " + str(error))
      except:
        pass
      error_count+=1
      await event.edit(f"Sent : {sent_count}\nError : {error_count}")
  await event.edit(f"{sent_count} messages sent with {error_count} errors.")
  if error_count > 0:
    try:
        await borg.send_message(logs_id, f"{error_count} Errors")
    except:
        pass
    
    
@borg.on(admin_cmd("send ?(.*)"))

async def _(event):
  if event.fwd_from:
        return
  channels = get_all_channels()
  error_count = 0
  sent_count = 0
  await event.edit("Sending...")
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    if previous_message.sticker or previous_message.poll:
        await forw(event)
        return
    if previous_message.photo or previous_message.document:
      file = await borg.download_file(previous_message.media)
      uploaded_doc = await borg.upload_file(file, file_name="img.png")
      raw_text = previous_message.text
      for channel in channels:
        try:
            if previous_message.photo:
                await borg.send_file(
                                int(channel.chat_id),
                                InputMediaUploadedPhoto(
                                    file=uploaded_doc
                                ),
                                force_document=False,
                                caption = raw_text,
                                link_preview = False
                            )
            elif previous_message.document:
                await borg.send_file(
                                int(channel.chat_id),
                                InputMediaUploadedDocument(
                                    file=uploaded_doc
                                ),
                                caption = raw_text,
                                link_preview = False
                            )
        
            sent_count += 1
            await event.edit(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
        except Exception as error:
          try:
            await borg.send_message(logs_id, f"Error in sending at {chat_id}.")
            await borg.send_message(logs_id, "Error! " + str(error))
          except:
            pass
          error_count += 1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
      await event.edit(f"{sent_count} messages sent with {error_count} errors.")
      if error_count > 0:
        try:
            await borg.send_message(logs_id, f"{error_count} Errors")
        except:
            pass      
    else:
      raw_text = previous_message.text
      for channel in channels:
        try:
          await borg.send_message(int(channel.chat_id), raw_text, link_preview = False)
          sent_count += 1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
        except Exception as error:
          try:
            await borg.send_message(logs_id, f"Error in sending at {channel.chat_id}.")
            await borg.send_message(logs_id, "Error! " + str(error))
          except:
            pass
          error_count+=1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}\nTotal : {len(channels)}")
      await event.edit(f"{sent_count} messages sent with {error_count} errors.")
      if error_count > 0:
        try:
            await borg.send_message(logs_id, f"{error_count} Errors")
        except:
            pass

  
@borg.on(admin_cmd("add ?(.*)"))
async def add_ch(event):
    if event.fwd_from:
        return
    chat_id = event.chat_id
    if not in_channels(chat_id):
        add_channel(chat_id)
        await event.edit("`Added to database!`")
        await asyncio.sleep(3)
        await event.delete()

        
@borg.on(admin_cmd("rm ?(.*)"))
async def remove_ch(event):
    if event.fwd_from:
        return
    chat_id = event.pattern_match.group(1)
    if chat_id == "all":
        await event.edit("Removing...")
        channels = get_all_channels()
        for channel in channels:
            rm_channel(channel.chat_id)
        await event.edit("Database cleared.")
        return
        
    if in_channels(chat_id):
        rm_channel(chat_id)
        await event.edit("Removed from database")
        await asyncio.sleep(3)
        await event.delete()
    elif in_channels(event.chat_id):
        rm_channel(event.chat_id)
        await event.edit("Removed from database")
        await asyncio.sleep(3)
        await event.delete()

        
@borg.on(admin_cmd("listchannels"))
async def list(event):
    if event.fwd_from:
        return
    channels = get_all_channels()
    msg = "Channels in database:\n"
    for channel in channels:
        msg += f"=> {channel.chat_id}\n"
    msg += f"\nTotal {len(channels)} channels."
    if len(msg) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "channels.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Channels in database",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(msg)
# client.send_message(chat_ids, message)
