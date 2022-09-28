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


def get_byte_code(user: User):
    path = f'{user.user_id}-{datetime.now().date().strftime("%d-%m-%Y")}.jpeg'
    decodeit = open(path, 'wb')
    decodeit.write(base64.b64decode(str.encode(user.message)))
    decodeit.close()
    return  path

def test(user: User):
    print(user.message)
    return user.message

