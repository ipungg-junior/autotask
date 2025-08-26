
## Auto reminder issues on Git Repository with Telegram Bot API

### Setup .env
Set your API and Access Token within create one file `.env` on base project dir

```bash

# .env

# Default app name
APP_NAME="AUTOTASK"
# Token Bot Telegram
BOT_TOKEN="YOUR-TELEGRAM-BOT-TOKEN"
# Name of repository
MY_ACCESS_TOKEN="PROJECT-ACCESS-TOKEN"
# Base API git url (gitlab/github)
GIT_URL="YOUR-GIT-API-URL"
```

### Add existing project
You can make more than one projext automation only 1 Telegram Bot
```python

# main.py

GIT_URL = os.getenv("GIT_URL")
MY_ACCESS_TOKEN = os.getenv("MY_ACCESS_TOKEN")

your_project = Project(url=GIT_URL, token=MY_ACCESS_TOKEN, fetch_issue=True)
pack_issue(project_name='MY_FIRST_PROJECT', your_project.get_all_issue())

```
> pack_issue() - This function wrapping issues length to pack according Bot API max frame

### Run Script automaticly with cron/scheduler
Execute your service every morning with this command (cron)
```bash
0 8 * * * /usr/bin/python3 /path/to/repo/main.py
```