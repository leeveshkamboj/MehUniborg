import asyncio
import datetime
from telethon import events


chat_ids = {-1001191913647: "Trash"}
logs_id = -411442681



message = "test"
error_msg = "Error"


@borg.on(admin_cmd("send ?(.*)"))
async def _(event):
  if event.fwd_from:
    return
  input_str = event.pattern_match.group(1)
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    message = previous_message.message
  for chat_id in chat_ids.keys()
    try:
      await borg.send_message(chat_id, message)
      await borg.send_message(logs_id, f"{message} sent at {chatids[chat_id]}({chat_id}) successfully.")
    except:
      await borg.send_message(logs_id, error_msg)

#client.send_message(chat_ids, message)
