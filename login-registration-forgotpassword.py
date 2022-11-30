import re
regex = r'\b[A-Za-z]+[A-Za-z0-9._%+-]+@[A-Za-z0-9]+\.[A-Z|a-z]{2,}\b'
# To run the program on your machine uncomment the below line which is used for file creation
#file10 = open("USER_DATA.txt", "w")
def choices():
  print("Please choose what you would like to do.")
  choice = int(input("\n Login == 1, Registration == 2, Forgot Password == 3:"))
  if choice == 1:
    return Login()
  elif choice == 2:
    return Registration()
  elif choice == 3:
     return ForgotPassword()
  else:
    print("You have entered a wrong input")

def Login():
  print("Please Provide")
  username = str(input("Username/email: "))
  Password = str(input("Password: "))
  f = open("USER_DATA.txt",'r')
  info = f.read()
  info = info.split()
  if username in info:
    index = info.index(username) + 1
    usr_Password = info[index]
    if usr_Password == Password:
      return "Welcome Back, " + username
    else:
       return "Password entered is wrong"
  else:
        return "Username not found. Please Sign Up."

def Registration():
    print("\nEmail or user name should have @ followed by .   \n example : aishashaikh@gmail.com ")
    print("It should not be like this eg:- @gmail.com ")
    print("There should not be any . immediate next to @ \n example aisha@.com ")
    print("It should not start with special characters and numbers \n eg:- 123#@gmail.com")

    print("Please Provide")
    username = str(input("username\email: "))
    password = str(input("Password: "))
    check(username)
    checkPassword(password)
    f = open("USER_DATA.txt",'r')
    info = f.read()
    if username in info:
       return "Username Unavailable. Please Try Again"
    f.close()
    f = open("USER_DATA.txt",'w')
    info = info + " " +username + " " + password
    f.write(info)

def ForgotPassword():
  print("Please enter your username")
  p=input()
  file10=open("USER_DATA.txt", "r")
  a =  file10.read()
  if p in a:
    res = a.split(p,1)
    newlist = res[1].split()
    print("Your password is", newlist[0])
  else:
    print("Wrong username please signup ")

def check(email):
 

    # pass the regular expression

    # and the string into the fullmatch() method

    if(re.fullmatch(regex, email)):

        print("Valid Email")
 

    else:

        print("Invalid Email")

def checkPassword(password):
  l, u, p, d = 0, 0, 0, 0
  if (len(password) > 5 and len(password) < 16):
    for i in password:
 
        # counting lowercase alphabets
        if (i.islower()):
            l+=1           
 
        # counting uppercase alphabets
        if (i.isupper()):
            u+=1           
 
        # counting digits
        if (i.isdigit()):
            d+=1           
 
        # counting the mentioned special characters
        if(i=='@'or i=='$' or i=='_'or i=='#'or i=='%'or i=='^'or i=='*'):
            p+=1          
  if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password)):
    print("Valid Password")
  else:
    print("Invalid Password")
  
print(choices())
