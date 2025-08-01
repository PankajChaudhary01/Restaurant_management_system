from src.Authentication.SignUp import SignUp_Menu
from src.Authentication.SignIn import SignIn
class ManageMenu:
    
    def MenuManagement(self):
        print("--* Pankaj's Restaurant *--")
        print("1. Sign in")
        print("2. Sign up")
        print("3. Exit")
        
        choice=int(input("Enter your choice :"))
        
        if(choice==1):
            login=SignIn()
            login.sign_in_menu()
        elif(choice==2):
            signup=SignUp_Menu()
            signup.SignUp_management()
        else:
            print("Thank you for visiting us")
            exit()