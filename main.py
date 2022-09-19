from operator import imod
from fastapi import FastAPI
from fastapi import Body, status


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
    return user

