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
channel = [-1001191913647, -447105382]
logs_id = -411442681



message = "test"
error_msg = "Error"


@borg.on(admin_cmd("send ?(.*)"))
async def _(event):
  if event.fwd_from:
    return
  error_count = 0
  sent_count = 0
  await event.edit("Sending...")
  input_str = event.pattern_match.group(1)
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    if previous_message.photo:
      file = await borg.download_file(previous_message.media)
      uploaded_img = await borg.upload_file(file, file_name="img.png")
      raw_text = previous_message.text
      for chat_id in channel:
        try:
          await borg.send_file(
                                chat_id,
                                InputMediaUploadedPhoto(

                                    file=uploaded_img
                                ),
                                force_document=False,
                                caption = raw_text
                            )
          sent_count += 1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}")
        except Exception as error:
          await borg.send_message(logs_id, f"Error in sending at {chat_id}.")
          await borg.send_message(logs_id, "Error! " + str(error))
          error_count += 1
          await event.edit("fSent : {sent_count}\nError : {error_count}")
      await event.edit(f"{sent_count} messages sent with {error_count} errors.")
      await borg.send_message(logs_id, f"{error_count} Errors")        
    else:
      raw_text = previous_message.text
      for chat_id in channel:
        try:
          await borg.send_message(chat_id, raw_text)
          sent_count += 1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}")
        except Exception as error:
          await borg.send_message(logs_id, f"Error in sending at {chat_id}.")
          await borg.send_message(logs_id, "Error! " + str(error))
          error_count+=1
          await event.edit(f"Sent : {sent_count}\nError : {error_count}")
      await event.edit(f"{sent_count} messages sent with {error_count} errors.")
      await borg.send_message(logs_id, f"{error_count} Errors")

  
@borg.on(admin_cmd("forward ?(.*)"))
async def _(event): 
  if event.fwd_from:
    return
  await event.edit("Sending...")
  error_count = 0
  sent_count = 0 
  input_str = event.pattern_match.group(1)
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    message = previous_message.message
    raw_text = previous_message.raw_text
  error_count = 0
  for chat_id in channel:
    try:
      await borg.forward_messages(chat_id, previous_message)
      sent_count += 1
      await event.edit(f"Sent : {sent_count}\nError : {error_count}")
    except Exception as error:
      await borg.send_message(logs_id, f"Error in sending at {chat_id}.")
      await borg.send_message(logs_id, "Error! " + str(error))
      error_count+=1
      await event.edit(f"Sent : {sent_count}\nError : {error_count}")
  await event.edit(f"{sent_count} messages sent with {error_count} errors.")
  await borg.send_message(logs_id, f"{error_count} Errors")


# client.send_message(chat_ids, message)
