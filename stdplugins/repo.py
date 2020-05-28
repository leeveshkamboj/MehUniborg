from telethon import events
from uniborg.util import admin_cmd

@borg.on(admin_cmd("repo"))
async def handler(event):
    await event.edit("[Click here](https://github.com/IG-Ricky/MehUniborg) to open this lit repo!")
    
@borg.on(admin_cmd("mrepo"))
async def handler(event):
    await event.edit("[Click here](https://github.com/leeveshkamboj/MehUniborg) to open this lit repo!")    
