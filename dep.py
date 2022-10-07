from pydantic import BaseModel, Field
import json

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

    def __init__(self) -> None:
        self.dic = {}
    
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

hist = Historial()

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
                    print("2",self.hist.get_count(self.user))
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
        print("debug",self.hist.get_count(self.user))
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

xiomara.message = "menu"

print({"id":xiomara.user_id,
"message":xiomara.message})

sendText = SendText(xiomara,hist)
print(sendText.tree_desicion())

xiomara.message = "1"

print({"id":xiomara.user_id,
"message":xiomara.message})
print(hist.get_count(xiomara))

sendText = SendText(xiomara,hist)
print(sendText.tree_desicion())

xiomara.message = "1"

print({"id":xiomara.user_id,
"message":xiomara.message})

sendText = SendText(xiomara,hist)
print(sendText.tree_desicion())