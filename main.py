
from fastapi import FastAPI
from fastapi import Body, status
from fastapi.responses import FileResponse

import io
from starlette.responses import StreamingResponse

#from chatbot import wikibot
from respuesta import val_message, get_byte_code, Historial, SendText

from model import User 

app = FastAPI()

@app.get(
    path = '/',
    status_code=status.HTTP_200_OK,
    tags=['Home']
)
def home():
    return {'response':'Cpal - Bot Service'}

@app.post(
    path = '/text',
    status_code=status.HTTP_202_ACCEPTED,
    tags=['text_message'],
    summary="Send a text message"
)
def text(user : User = Body(...)):
    '''
    Text message

    Recibe una sólo strings

    Parameters:
    -----------

     
    '''

    dic= {}
    hist = Historial(dic)
    hist.add_user(user)
    
    return {'reply':SendText(user,hist).tree_desicion()}

@app.post(
    path = '/image',
    status_code=status.HTTP_202_ACCEPTED,
    tags=['image_message'],
    summary="Send Image"
)
def image(user: User = Body(...)):
    path  = get_byte_code(user)
    return {"reply":path}

@app.get(
    path='/image/{path}'
)
def ex(path:str):
    return FileResponse(path) 

