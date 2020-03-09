import asyncio
import datetime
from telethon import events


chat_id = -1001191913647
logs_id = -411442681



message = "test"
error_msg = "Error"

@borg.on(events.NewMessage(pattern=r"^.test$", outgoing=True))
async def test(e):
  try:
    await borg.send_message(chat_id, message)
    await borg.send_message(logs_id, f"{message} sent at {chat_id}")
  except:
    await borg.send_message(logs_id, error_msg)

#client.send_message(chat_ids, message)
