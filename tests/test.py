import re
import uuid
import base64

def uuid_url64():
    """Returns a unique, 16 byte, URL safe ID by combining UUID and Base64
    """
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


from aiogram.utils.deep_linking import get_start_link
import asyncio
asyncio.get_event_loop()
loop = asyncio.get_event_loop()
async def make():
    link = await get_start_link('foo', encode=True)
    print(link)
task = loop.create_task(make())
loop.run_until_complete(asyncio.wait(task))