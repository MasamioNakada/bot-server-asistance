import requests
from bs4 import BeautifulSoup
import json
from model import User
import base64




from datetime import datetime

data = json.loads(open('./01_mvp.json',mode="r",encoding="utf-8").read())

def diagnostico_cat():
    url_diagnostico = "https://cpal.edu.pe/diagnostico-y-tratamiento/diagnostico/"
    cpal_diagnostico = requests.get(url_diagnostico)   
    s_cpal = BeautifulSoup(cpal_diagnostico.text, 'lxml') 
    secciones = s_cpal.find_all('a', attrs={'class':'b37-linkcategoria'})
    a = []
    for seccion in secciones:
        a.append(seccion.text)
    return a


dict_func = {
    "diagnostico":diagnostico_cat()
}

def json_scan(message:str) -> str:
    for i in data['intents']:
        if message in i['patterns']:
            return {'response': i['responses'],
                    'tag': i['tag']}


def val_message(message:str):
    r = json_scan(message)
    if r['response'] != "function":
        return r['response']
    else:
        return str(dict_func[r['tag']]) 

 

def byte_code_to_image(path:str) -> str:
    with open(path, "rb") as imageFile:
        data = base64.b64encode(imageFile.read())
    return data


def get_byte_code(user: User):
    path = f'{user.user_id}-{datetime.now().date().strftime("%d-%m-%y")}.jpeg'
    decodeit = open(path, 'wb')
    data = base64.b64decode(str.encode(user.message))
    decodeit.write(data)
    decodeit.close()
    return  path

def test(user: User):
    print(user.message)
    return user.message

# Second MVP

class Historial:

    def __init__(self, dic:dict) -> None:
        self.dic = dic
    
    def add_user(self,user:User) -> dict:
        self.dic[user.user_id] = [0,""]
        return self.dic[user.user_id]

    def count(self,user:User,direccion:str = "" ,count=True,reset:bool =False) -> dict: 
        if count:
            self.dic[user.user_id][0] += 1
        self.dic[user.user_id][1] += direccion
        if reset:
            self.dic[user.user_id][0] = 0
            self.dic[user.user_id][1] = ""
        return self.dic
    
    def get_count(self, user:User) -> dict:
        return self.dic[user.user_id]


class SendText:

    def __init__(self,user:User,hist:Historial) -> None:
        self.user = user
        self.hist = hist
        hist.add_user(self.user)


    def __add_direccion(self) -> None:
        direccion_dict = {
        "l" : ("1","si"),
        "r" : ("2","no")
        }
        for key in direccion_dict.keys():
            if self.user.message != "0":
                if self.user.message in direccion_dict[key]:
                    self.hist.count(self.user,key)
                    return None
                else:
                    self.hist.count(self.user)
                    return None
            else:
                self.hist.count(self.user,reset=True)
                self.hist.count(self.user)
                return None

    def tree_desicion(self) -> str:
        data = json.loads(open('./respuesta.json',mode="r",encoding="utf-8").read())
        self.__add_direccion()
        for cat in data.keys():
            category = data[cat]
            if self.user.message == "0":
                self.hist.count(self.user,reset = True)
                self.hist.count(self.user)

            if str(self.hist.get_count(self.user)[0]) == category["layer"]:
                if str(self.hist.get_count(self.user)[1] == category["direccion"]):
                    if self.user.message in category["value"]:
                        print(self.hist.get_count(self.user))
                        return category["message"]