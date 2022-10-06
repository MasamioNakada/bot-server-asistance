from pydantic import BaseModel, Field
import json

dic= {}

class User(BaseModel):
    user_id : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='51952841852@.se'
    )
    message : str = Field(
        ...,
        example='/proceso de seleccion'
    )

xiomara =User
xiomara.user_id = "51934935843@c.us"

class Historial:
    dic= {}

    def add_user(self,user:User) -> dict:
        dic[user.user_id] = [0,""]
        return dic[user.user_id]

    def count(self,user:User,direccion:str = "" ,count=True,reset:bool =False) -> dict: 
        if count:
            dic[user.user_id][0] += 1
        dic[user.user_id][1] += direccion
        if reset:
            dic[user.user_id][0] = 0
            dic[user.user_id][1] = ""
        return dic
    
    def get_count(self, user:User) -> dict:
        return dic[user.user_id]
    
hist = Historial()
hist.add_user(xiomara)
    
class SendText:

    def __init__(self,user:User) -> None:
        self.user = user

    def __add_direccion(self) -> None:
        direccion_dict = {
        "r" : ("1","si"),
        "l" : ("2","no")
        }
        for key in direccion_dict.keys():
            if self.user.message != "0":
                if self.user.message in direccion_dict[key]:
                    hist.count(self.user,key)
                    print(1,hist.get_count(self.user))
                    return None
                else:
                    hist.count(self.user)
                    print(2,hist.get_count(self.user))
                    return None
            else:
                hist.count(self.user,reset=True)
                print(3,hist.get_count(self.user))
                return None

    def tree_desicion(self) -> str:
        data = json.loads(open('./respuesta.json',mode="r",encoding="utf-8").read())
        
        for cat in data.keys():
            category = data[cat]
            if str(hist.get_count(self.user)[0]) == category["layer"]:
                if str(hist.get_count(self.user)[1] == category["direccion"]):
                    if self.user.message in category["value"]:
                        self.__add_direccion()
                        return category["message"]

xiomara.message = "0"

print({"id":xiomara.user_id,
"message":xiomara.message})
   
sendText = SendText(xiomara)
print(sendText.tree_desicion())