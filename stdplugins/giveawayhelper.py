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

channel = {
            -1001191913647 : "Trash", -1001469149410 : "@WWMethLabs", 1289688851 : "@error69club",
            1461820250 : "@T3L3FAM", 1398471558 : "fsocietypremium", 1185965787 : "@jusicegiveaway",
            1295042400 : "@ninjahub007", 1275383207 : "@mivislink1", 1180330670 : "@joinforgiveaway",
            1212694660 : "Dark Giveaways", 1201395264 : "Abnormal bins", 1185741535 : "@BurnCracking",
            1206921330 : "The Ballad of jesse", 1370345200 : "@legendsassociation", 1336319764: "@dailyhotstargiveaway",
            1372489330 : "@giveawayjunction", 1210379638 : "@techysihag", 1458513856 : "Netflix's Giveaways",
            1230938290 : "Reborn Giveaways", 1481743754 : "@royalgiveaways", 1166459724 : "@marvelgiveawayhaker",
            1434905058 : "Netflix Accounts", 1484944621 : "@paulinasworld", 1311532625 : "@PremiumAccountGiveaway",
            1397629501 : "@thepremiumcracker", 1439458337 : "@TeampoionXD", 1446541060 : "@crackingarmy",
            1245370939 : "@giveawayaccountsAJ", 1372335147 : "@techymast", 1309721959 : "@giveaway_24hrs",
            1186776124 : "@netflixaccc", 1351220732 : "@crazyarmygames", 1336950662 : "@joinhereforgibaways",
            1263822220 : "@sam9086", 1456736802 : "@theoggyworld", 223462655 : "@mavericgiveaway",
            1432006231 :"Direct zone", 1404962771 : "@ppremium_giveaways", 1336950662 : "@joinhereforgibaways",
            1219885001 : "@freechannelsforall", 1409761529 : "@phoenixgang", 1302017626 : "@bulbagiveaways",
            1423183267 : "@androidapk_mod", 1437719131 : "@vmhack", 1236770095 : "@liveismylife",
            1364162634 : "@fir3club", -1001467728767 : "@PremiumGiweaway", 1424034733 : "@onlupremiumarmy"
          }
logs_id = -411442681



message = "test"
error_msg = "Error"


@borg.on(admin_cmd("send ?(.*)"))
async def _(event):
  if event.fwd_from:
    return
  error_count = 0
  sent_count = 0
  input_str = event.pattern_match.group(1)
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    if previous_message.photo:
      file = await borg.download_file(previous_message.media)
      uploaded_img = await borg.upload_file(file, file_name="img.png")
      for chat_id in channel.keys():
        try:
          await borg.send_file(
                                chat_id,
                                InputMediaUploadedPhoto(

                                    file=uploaded_img
                                ),
                                force_document=False
                            )
          sent_count += 1
        except Exception as error:
          await borg.send_message(logs_id, f"Error in sending at {channel[chat_id]} ({chat_id}).")
          await borg.send_message(logs_id, "Error! " + str(error))
          error_count += 1
    else:
      raw_text = previous_message.text
      for chat_id in channel.keys():
        try:
          await borg.send_message(chat_id, raw_text)
          sent_count += 1
        except Exception as error:
          await borg.send_message(logs_id, f"Error in sending at {channel[chat_id]} ({chat_id}).")
          await borg.send_message(logs_id, "Error! " + str(error))
          error_count+=1
      await event.edit(f"{sent_count} messages sent with {error_count} errors.")
      await borg.send_message(logs_id, f"{error_count} Errors")

  
@borg.on(admin_cmd("forward ?(.*)"))
async def _(event): 
  if event.fwd_from:
    return
  error_count = 0
  sent_count = 0 
  input_str = event.pattern_match.group(1)
  if event.reply_to_msg_id:
    previous_message = await event.get_reply_message()
    message = previous_message.message
    raw_text = previous_message.raw_text
  error_count = 0
  for chat_id in channel.keys():
    try:
      await borg.forward_messages(chat_id, previous_message)
      sent_count += 1
    except Exception as error:
      await borg.send_message(logs_id, f"Error in sending at {channel[chat_id]} ({chat_id}).")
      await borg.send_message(logs_id, "Error! " + str(error))
      error_count+=1
  await event.edit(f"{sent_count} messages sent with {error_count} errors.")
  await borg.send_message(logs_id, f"{error_count} Errors")


#client.send_message(chat_ids, message)
