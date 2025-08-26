from core import Project, Bot
import time, os
from dotenv import load_dotenv

load_dotenv()

# Init Telegram BOT
BOT_TOKEN = os.getenv("BOT_TOKEN")
Bot.init(token=BOT_TOKEN)


# Function to manage issue length
def pack_issue(project_name, issues):
    opened = []
    all_str = ""
    for issue in issues:
        if issue["state"] == "opened":
            msg = f"#{issue['iid']} - {issue['title']}\n"

            if len(all_str) + len(msg) < 350:  
                all_str += msg
            else:
                opened.append(all_str)   
                all_str = msg            

    if all_str:
        opened.append(all_str)

    Bot.broadcast(f"📌 **{project_name}** ")
    for msg in opened:
        Bot.broadcast(msg)
        time.sleep(0.1)
        
    print('Completed')


GIT_URL = os.getenv("GIT_URL")
POSOUT_TOKEN = os.getenv("POSOUT_TOKEN")
pos_project = Project(url=GIT_URL, token=POSOUT_TOKEN, fetch_issue=True)
pack_issue('POS_PYQT', pos_project.get_all_issue())

