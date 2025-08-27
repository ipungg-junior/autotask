import requests
    
    
class Project:
    
    def __init__(self, url, token, fetch_issue=False):
        self.__url = url
        self.__token = token
        self.__project_id = self.__get_self_id()
        self.__issues = []
        if fetch_issue:
            self.__fetch_issue()
    
    
    def __get_self_id(self):
        """
            Function to get project id by token API
        """
        projects = requests.get(f"{self.__url}/projects?membership=true", headers={"PRIVATE-TOKEN": self.__token}).json()
        return projects[0]['id']
    
        
    def __fetch_issue(self, state='all'):
        url = f"{self.__url}/projects/{self.__project_id}/issues?state={state}"
        resp = requests.get(url, headers={"PRIVATE-TOKEN": self.__token}).json()
        idx = 1
        for issue in resp:
            self.add_issue({'id':idx, 'iid':issue['iid'], 'title':issue['title'], 'state': issue['state'], 'author':issue['author']['username']})
            idx += 1
    
        
    def add_issue(self, issue):
        """
            Function to add issue to list issue (self.__issues)
        """
        self.__issues.append(issue)
        
        
    def get_all_issue(self):
        """
            function to get all issue (open/closed) in self project
        """
        return self.__issues
        


class Bot:
    
    __token = None
    __chat_room = {}
    
    @staticmethod
    def init(token):
        Bot.__token = token
        Bot.fetch_subscriber()
        
    
    @staticmethod
    def fetch_subscriber():
        url = f"https://api.telegram.org/bot{Bot.__token}/getUpdates"
        resp = requests.get(url).json()
        
        
        if (resp['ok']):
            for i in resp['result']:
                
                try:
                    Bot.__chat_room[i['message']['chat']['id']] = i['message']['chat']['username']      # set id and username
                except:
                    if (i['message']['chat']['type'] == 'supergroup'):
                        Bot.__chat_room[i['message']['chat']['id']] = i['message']['chat']['title']      # set id by group name                        
                    else:
                        try:
                            Bot.__chat_room[i['message']['chat']['id']] = i['message']['chat']['first_name']
                        except Exception as has_delete:
                            try:
                                if (i['my_chat_member']['new_chat_member']['status'] == 'kicked'):
                                    del Bot.__chat_room[i['my_chat_member']['chat']['id']]
                                else:
                                    Bot.__chat_room[i['my_chat_member']['chat']['id']] = Bot.__chat_room[i['my_chat_member']['chat']['first_name']]
                            except:
                                pass
            
                    
                
    @staticmethod
    def send(chat_id, text):
        url = f"https://api.telegram.org/bot{Bot.__token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
        }
        resp = requests.post(url, data=data)
        return resp.json()
        
        
    @staticmethod
    def broadcast(message):
        for uid, username in Bot.__chat_room.items():
            Bot.send(uid, message)
            
    
    
