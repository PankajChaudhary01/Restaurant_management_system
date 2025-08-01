import uuid
import json

path="D:\Restaurant_management_system\src\Database\Staff.json"

class SignUp_Menu:
    
    def SignUp_management(self):
        from src.Authentication.ManageMenu import ManageMenu
        staff_List=[]
       
        
        with open(path,"r") as file:
            staff_List=json.load(file)
        
            
        staff_Dict={}
        
        staff_id=str(uuid.uuid4())[:6]
        staff_Dict["id"]=staff_id
        staff_Dict["username"]=input("Enter your username :")
        staff_Dict["email"]=input("Enter your email :")
        staff_Dict["password"]=input("Enter your password :")
        
        staff_List.append(staff_Dict)
        
        with open(path,"w") as file:
            json.dump(staff_List,file,indent=4)
        
        
        manage_me=ManageMenu()
        manage_me.MenuManagement()
        
        
        
        
       
        
        