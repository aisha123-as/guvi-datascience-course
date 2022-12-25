
#mock aadhar website using MongoDB. 1) Registration, 2)Update, 3)PDF Generation.
     

#guvi logo updation
#insert once at the creation of the website
'''
import pymongo
client = pymongo.MongoClient("mongodb+srv://<user name>:<password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
db = client.assignment
records =Aadhar
logo = {"_id" : 1}
from PIL import Image
import io
file_name = input()
img = Image.open(file_name)
image_bytes = io.BytesIO()
img.save(image_bytes, format = 'JPEG')
#img.show() 
logo["Logo"] = image_bytes.getvalue()
records.insert_one(logo)
'''
     
!pip install qrcode
!pip install fpdf
     

class Registration:
    #getting inputs from the user nad validation process
    
    def inputs():
        print("WELCOME TO GUVI AADHAR REGISTRATION PORTAL\nTHIS AADHAR IS UNIQUE FOR ALL INDIVIDUALS AND NEW USERS CAN ONLY DO REGISTRATION HERE\nTHIS AADHAR SERVICE PROVIDES AADHAR CARD FOR ALL CATOGRY PEOPLE OF ALL AGE GROUP\nFOR NEW BORN BABIES AADHAR WILL BE PROVIDED AFTER THE COMPLETION OF ONE YEAR.")
        wrng_details = [] #will finaly displays the incorrect inputs if any
        print("WARNING...!THIS IS AN OFFICIAL PROCESS\nENTER YOUR DETAILS PROPERLY AND READ THE DISCRIPTION GIVEN BEFORE FILLING IT")
        print("ONCE YOU ENTER THE WORNG DETAILS YOU CAN NOT GO BACK.\nYOU HAVE TO RE-ENTER THE DETAILS AGAIN TO CONTINUE")
        print("NAMES SHOULD CONTAILS ONLY ALPHABETS.\n NO NUMBERS AND SPECIAL CHARACTERS WERE ALLOWED.\nENTER YOUR NAME AS PER YOUR VOTER ID.")
        user_info = {} #will carry the user information
        Name = input("Enter your name properly: ")
        name = (Name).replace(" ", "")
        if (name).isalpha():
            print("***** Name vaild *****")
            Name = (Name).capitalize()
            user_info["Name"] = Name
        else:
            print("WARNING ! ***** Name invalid...!Please enter a valid name!!! *****")
            wrng_details.append("Name")
        #"********************************************************************************************"
        try:
            from PIL import Image
            import io
            print("***** Insert your image here *****\n***** The image size should be between the range of 20 to 100 kb *****\***ONLY JPG FORMAT IS SUPPERTED***\n")
            file_name = input("Enter your image file name : ")
            img = Image.open(file_name)
            image_bytes = io.BytesIO()
            img.save(image_bytes, format = 'JPEG')
            #img.show() 
            user_info["Photo"] = image_bytes.getvalue()
        except FileNotFoundError:
            print("Please enter a valid file name in your local PC")
            wrng_details.append("Photo")
        #"*********************************************************************************************"
        print("***** ENTER YOUR DATE OF BIRTH AS PER YOUR BIRTH CERTIFICATE *****\n***** ONLY NUMBERS WERE ALLOWED *****")
        import datetime
        cur = str(datetime.datetime.now())
        c_year = int(cur[0:4]) #current year
        max_yr = c_year-110 #max age of a person is set here as 110
        D = int(input("Enter your birth date : "))
        M = int(input("Enter your birth month : "))
        Y = int(input("Enter your birth year : "))
        DOB = ""# final formatted dob
        err = 0 #counter, will increase if invalid date or month or year is given as input
        lp_yr = 0 #counter to check for leap year
        l_m = [1, 3, 5, 7, 8, 10, 12]#months with 31 days
        s_m = [4, 6, 9, 11] #months with 30 days
        if Y==max_yr:
            if M <= 12:
                if M in l_m:
                    if D <= 31:
                        err+=0
                    elif D >31:
                        err+=1
                elif M in s_m:
                    if D<=30:
                         err+=0
                    elif D>=31:
                        err +=1
                elif M == 2:
                    if (Y % 400 == 0) and (Y % 100 == 0):
                        lp_yr +=1
                    elif (Y % 4 ==0) and (Y % 100 != 0):
                        lp_yr +=1
                    if lp_yr == 1:
                        if D <= 29:
                            err +=0
                        elif D > 29:
                            err+=1
                    elif lp_yr == 0:
                        if D <=28:
                            err +=0
                        elif D > 28:
                            err+=1
            elif M >12:
                err+=1
        elif Y>= c_year or Y< max_yr:
            err +=1
        if err == 0:
            print("***** validated *****")
            if M <10:
                m = str(0)+str(M)
            elif M >=10:
                m = M
            if D <10:
                d = str(0)+str(D)
            elif D >=10:
                d = D
            DOB = DOB+str(d)+"/"+str(m)+"/"+str(Y)
            user_info["DOB"] = DOB
        elif err >0:
            print("WARNING ! ***** Invalid input...! ***** ")
            wrng_details.append("DOB")
                                    
        #"************************************************************************************************"
        
        print("*****Enter your permanent address as per your voter ID*****\n*****No special characters were allowed*****\n*****Only , . and spaces were allowed*****")
        def v_char(x):
            count = 0
            for i in x:
                if i.isalpha():
                    count+=0
                elif i == " ":
                    count+=0
                else:
                    count+=1
            if count == 0:
                return 0
            elif count >0:
                return 1
        def v_pin(x):
            if x.isdigit() and len(x) == 6:
                return 0
            else:
                return 1
        d_no = input("Enter your door number")
        st_name = input("Enter your street name : ").capitalize()
        city = input("Enter your City : ").capitalize()
        state = input("Enter your State : ").title()
        pincode = input("Enter your pincode without space : ")
        a = v_char(st_name)
        b = v_char(city)
        c = v_char(state)
        d = v_pin(pincode)
        x = a+b+c+d
        if x == 0:
            Permanent_address = {"Door no":d_no, "Street name":st_name, "City":city, "State":state, "Pincode":pincode}
            user_info["Permanent address"] = Permanent_address
            res_add = input("Enter YES if your permanent address and present address are same else enter NO:").upper()
            if res_add == "YES":
                Present_address = Permanent_address.copy()
                user_info["Present address"] = Present_address
            elif res_add == "NO":
                d_no1 = input("Enter your door number:")
                st_name1 = input("Enter your street name : ")
                city1 = input("Enter your City : ")
                state1 = input("Enter your State : ")
                pincode1 = input("Enter your pincode without space : ")
                e = v_char(st_name1)
                f = v_char(city1)
                g = v_char(state1)
                h = v_pin(pincode1)
                y = e+f+g+h
                if y == 0:
                    Present_address = {"Door no":d_no1, "Street name":st_name1, "City":city1, "State":state1, "Pincode":pincode1}
                    user_info["Present address"] = Present_address
                elif y > 0:
                    print("WARNING !*****Address given were not valid*****\n*****Please use only alphabats and sapces only*****")
                    wrng_details.append("Present Address")
        elif x > 0:
            print("Address given were not valid.\nPlease use only alphabats and sapces only")
            wrng_details.append("Premanent Address")
            
        #"**********************************************************************************************"
        gen = ["MALE", "FEMALE", "TRANSGENDER"]
        gender = input("Enter your Gender\nMALE\ FEMALE\ TRANSGENDER : ").upper()
        if gender in gen:
            print("******Validated******")
            user_info["Gender"] = gender
        elif (gender).upper not in gen:
            print("WARNING ! ***** Invalid input....!! *****")
            wrng_details.append("Gender")   
        #"********************************************************************************************"
        edu_qua = input("Enter your educational qualification\nNA(For children below 15 and illitrates)\n10th\n12th\nDIPLOMA\nUNDER GRADUATE\nPOST GRADUATE\nDOCTRATE\n>>>")

        if len(edu_qua) <5:
          stream = "NA"
          edu = edu_qua
        elif len(edu_qua) >=5:
          edu_qua = (edu_qua).upper()
          if edu_qua == "DIPLOMA":
            stream = input("Enter your stream\nCIVIL\nMECHANICAL\nECE\nEEE\nOTHERS :")
            if stream == "OTHERS":
              stream = input("Enter your stream : \n>>>").title()
              edu = "Diploma"
            elif stream != "OTHERS":
              edu = "Diploma"
          elif edu_qua == "UNDER GRADUATE":    
            s = input("Enter your Degree\nARTS & SCIENCE\nB.E\B.TECH : \n>>>").upper()
            if s == "ARTS & SCIENCE":
              stream = input("Enter your stream\nENGLISH\nSCIENCE\nACCOUNTS\nECONOMICS\nOTHERS : \n>>>").upper()
              if stream == "OTHERS":
                stream = input("Enter your stream : \n>>>").title()
                edu = "Arts & Science"
              elif stream != "OTHERS":
                edu = "Arts & Science"
            elif s == "B.E" or "B.TECH":
              stream = input("Enter your stream\nMECHANICAL\nCIVIL\nCOMPUTER SCIENCE\IT\nBIO TECH\nOTHERS : \n>>>").upper()
              if stream == "OTHERS" :
                stream = input("Enter your stream : \n>>>").title()
                edu = s
              elif stream != "OTHERS":
                edu = s
          elif edu_qua == "POST GRADUATE" or "DOCTRATE":
            stream = input("Enter your stream : \n>>>").title()
            edu = (edu_qua).capitalize()
        Educational_qualification = {"Qualification": edu, "Stream": stream}
        user_info["Educational qualification"] = Educational_qualification
            
        #"***************************************************************************************************"
        phone_num = input("Enter your 10 digit Phone Number : ")
        if len(phone_num) == 10 and (phone_num).isdigit():
          print("******Number validated!******")
          user_info["Phone number"] = phone_num

        elif len(phone_num) != 10 or not((phone_num).isdigit()):
            print("WARNING ! **********Number invalid...!Please enter a valid number...!**********")
            wrng_details.append("Phone number")
            
        #"************************************************************************************************"
        c = 0 # counter for verifying email id
        email_id = input("Enter your email_id :")
        x = email_id.split("@")
        if email_id.endswith("@gmail.com") or email_id.endswith("@yahoo.in") or email_id.endswith("@hotmail.com") or email_id.endswith("@reddifmail.com"):
            c+=0
            if email_id[0].isalpha():
                c+=0
                for i in x[0]:
                    if i.isdigit():
                        continue
                    if i.isalpha():
                        continue 
                    elif i == "_" or i == ".":
                        continue
                    else:
                        c+=1               
            else:
                c+=1
        else:
            c+=1
        if c>0:
            print("Your mail_id is invalid")
            wrng_details.append("Email id")
        elif c == 0:
            print("Email id is validated")
            user_info["Email ID"] = email_id
        if len(wrng_details) == 0:
            print("**********Details entered are valid **********")
            '''user_info = {"Name":Name, "Photo":image_bytes, "DOB":DOB, "Address":
                        {"Permenent Address":Permanent_address, "Present address":Present_address}, "Gender":gender,
                        "Educational qualification":{"Qualification":edu_qua , "Stream":stream},
                        "Phone number":p_num, "Email ID":email_id}'''
            #"************************************************************************************************************"
            #aadhar number generation
            import random
            a = str(random.randint(100000000000, 999999999999))
            Aadhar_no = a[:4]+" "+a[4:8]+" "+a[8:]
            print(f"YOUR UNIQUE 12 DIGIT AADHAR NUMBER IS {Aadhar_no}\nNOTE DOWN YOUR AADHAR NUMBER FOR FURTHER PROCESS")
            user_info["Aadhar Number"] = Aadhar_no

            #"**********************************************************************************************************************"
            #remainder date generation
            from datetime import date
            from dateutil.relativedelta import relativedelta
            r_d = str(date.today() + relativedelta(years=+2))
            renewal_date = r_d[-2:]+"/"+r_d[-5:-3]+"/"+r_d[:4]
            user_info["Renewal date"] = renewal_date
            print("Your renewal date is "+renewal_date)

            #"************************************************************************************************************"
            #qr generation
            info=f'''       GUVI AADHAR CARD      \n
                    UNIQUE IDENTIFICATION  AUTHORITY OF GUVI\n
                    NAME : {Name}\n
                    PERMANENT ADDRESS : {Permanent_address["Door no"]}, {Permanent_address["Street name"]}\n
                                                      {Permanent_address["City"]},\n
                                                      {Permanent_address["State"]},\n
                                                      {Permanent_address["Pincode"]}\n
                    PRESENT ADDRESS : {Present_address["Door no"]}, {Present_address["Street name"]}\n
                                                  {Present_address["City"]},\n
                                                  {Present_address["State"]},\n
                                                  {Present_address["Pincode"]}\n
                    DOB : {DOB}\n
                    EDUCATIONAL QUALIFICATION : {edu_qua}\n
                    STREAM : {stream}\n
                    Renewal date : {renewal_date}
                    Phone number : ********+{p_num[-2:]}
                    Email ID : {email_id}
                        YOUR AADHAR NUMBER    \n
                        ***{Aadhar_no}***          '''
            #!pip install qrcode
            #if module not found error accured run the above command
            import qrcode
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=2,
                border=1,
            )
            qr.add_data(info)
            qr.make(fit=True)

            img_qr= qr.make_image(fill_color="black", back_color="white")
            img_qr = img_qr.save(f"{Name}_qr.png")
            
            img_qr = Image.open(f"{Name}_qr.png")
            image_bytes_qr = io.BytesIO()
            img_qr.save(image_bytes_qr, format = 'JPEG')
            user_info["QRcode"] = image_bytes_qr.getvalue()
            #"****************************************************************************************************************************************"
            #details updation
            import pymongo
            client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
            db = client.guviProof
            records = db.Aadhar
            records.insert_one(user_info)
            print("Details updated successfully...!!!")

            print(user_info)

        elif len(wrng_details) > 0:
            for i in wrng_details:
                print("**********You have entered invalid "+str(i)+"**********")
            print("WARNING !!!! Read the discription given and enter the valid details !!!!")
 
     

class Update:
  def __init__(self, Aadhar_no):
    self.Aadhar_no = Aadhar_no
  def otp_verification(self):
    #otp verification for edit informations
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    import random
    otp = str(random.randint(1000, 9999))
    message = f"GUVI AADHAR IDENTIFICATION AUTHORITY\nTHIS OTP IS VALID FOR NEXT 5 MINUTES\nDO NOR SHARE THIS OTP WITH ANYONE\nYOUR OTP IS {otp}"

    emailid = input("Enter your email: ")
    s.login("oogify55@gmail.com", "hnnbegvvwtqyhcex")
    s.sendmail('"oogify55@gmail.com"',emailid,message)

    a = input("Enter your OTP >>: ")
    if a == otp:
      #print("Verified")
      return 1
    else:
      #print("Please Check your OTP again")
      return 0
  def qr_updation(self):
    #updating qr code after any edit in the information
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    b = records.find_one(myquery, {"_id":0, "Photo":0, "QRcode": 0})
    #qr generation
    info=f'''       GUVI AADHAR CARD      \n
            UNIQUE IDENTIFICATION  AUTHORITY OF GUVI\n
            NAME : {b["Name"]}\n
            PERMANENT ADDRESS : {b["Permanent address"]["Door no"]}, {b["Permanent address"]["Street name"]}\n
                                              {b["Permanent address"]["City"]},\n
                                              {b["Permanent address"]["State"]},\n
                                              {b["Permanent address"]["Pincode"]}\n
            PRESENT ADDRESS : {b["Present address"]["Door no"]}, {b["Present address"]["Street name"]}\n
                                          {b["Present address"]["City"]},\n
                                          {b["Present address"]["State"]},\n
                                          {b["Present address"]["Pincode"]}\n
            DOB : {b["DOB"]}\n
            EDUCATIONAL QUALIFICATION : {b["Educational qualification"]["Qualification"]}\n
            STREAM : {b["Educational qualification"]["Stream"]}\n
            Renewal date : {b["Renewal date"]}
            Phone number : {b["Phone number"]}
            Email ID : {b["Email ID"]}
                YOUR AADHAR NUMBER    \n
                ***{b["Aadhar Number"]}***          '''
    #!pip install qrcode
    #if module not found error come run the above code
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(info)
    qr.make(fit=True)

    img_qr= qr.make_image(fill_color="black", back_color="white")
    img_qr = img_qr.save(f"{b['Name']}_qr.png")

    from PIL import Image
    import io        
    img_qr = Image.open(f"{b['Name']}_qr.png")
    image_bytes_qr = io.BytesIO()
    img_qr.save(image_bytes_qr, format = 'JPEG')
    updated_qr = image_bytes_qr.getvalue()
    qr_update = {"$set":{"QRcode": updated_qr}}
    c = records.update_one(myquery,qr_update)
    if c !=0:
      print("QR updated successfully...!")
    else:
      print("QR updatetion failed....Try again!!!")
  #"****************************************************************************************************************************************************"
  def update_name(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    x = []#user to find weather the record is in the database or not
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) > 0:
      Name = input("Enter your name properly: ")
      name = (Name).replace(" ", "")
      if (name).isalpha():
          print("***** Name vaild *****")
          Name = (Name).capitalize()
          newvalue = {"$set" : {"Name" :Name}}
          verify = Edit.otp_verification(self)
          if verify == 1:
            print("OTP verified")
            a = records.update_one(myquery, newvalue)
            if a != 0:
              print("Name updated successfully")
              Update.qr_updation(self)
            else:
              print("Something went wrong... Try again later..!!!")
          elif verify == 0:
            print("Invalid OTP ...!Try again!!!")         
      else:
        print("WARNING ! ***** Name invalid...!Please enter a valid name!!! *****")

        #"****************************************************************************************************************************************"
  def update_photo(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      try:
        from PIL import Image
        import io
        print("***** Insert your image here *****\n***** The image size should be between the range of 20 to 100 kb *****")
        file_name = input("Enter your image file name : ")
        img = Image.open(file_name)
        image_bytes = io.BytesIO()
        img.save(image_bytes, format = 'JPEG')
        updated_image = image_bytes.getvalue()
        newvalue = {"$set":{"Photo": updated_image}}
        verify = Update.otp_verification(self)
        if verify == 1:
          print("OTP verified")
          a = records.update_one(myquery, newvalue)
          if a != 0:
            print("Photo updated successfully")
            Update.qr_updation(self)
          else:
            print("Something went wrong... Try again later..!!!")
        elif verify == 0:
          print("Invalid OTP ...!Try again!!!")      
      except FileNotFoundError:
        print("Please enter a valid file name in your local PC")

  #"*******************************************************************************************************************"
  #edit permanent address
  def update_per_add(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      def v_char(x):
            count = 0
            for i in x:
                if i.isalpha():
                    count+=0
                elif i == " ":
                    count+=0
                else:
                    count+=1
            if count == 0:
                return 0
            elif count >0:
                return 1
      def v_pin(x):
          if x.isdigit() and len(x) == 6:
              return 0
          else:
              return 1
      door_no = input("Enter your door number : ")
      st_name = input("Enter your street name : ").capitalize()
      city = input("Enter your city name : ").capitalize()
      state = input("Enter your state name : ").title()
      pincode = input("Enter your pincode : ")
      #validating the given inputs
      p = v_char(st_name)
      q = v_char(city)
      r = v_char(state)
      s = v_pin(pincode)
      t = p+q+r+s
      if t == 0:
        print("*********** Address validated **********")
        per_add = {"Door no" :door_no, "Street name" :st_name, "City": city, "State": state, "Pincode":pincode}
        newvalue = {"$set": {"Permanent_address":per_add}}
        verify = Update.otp_verification(self)
        if verify == 1:
          print("OTP verified")
          a = records.update_one(myquery, newvalue)
          if a != 0:
            print("Address updated successfully")
            Update.qr_updation(self)
          else:
            print("Something went wrong... Try again later..!!!")
        elif verify == 0:
          print("Invalid OTP ...!Try again!!!")     
      elif t >0:
        print("Address given were not valid.\nPlease use only alphabats and sapces only")

        #"******************************************************************************************************"
  #edit present address
  def update_pre_add(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      def v_char(x):
            count = 0
            for i in x:
                if i.isalpha():
                    count+=0
                elif i == " ":
                    count+=0
                else:
                    count+=1
            if count == 0:
                return 0
            elif count >0:
                return 1
      def v_pin(x):
          if x.isdigit() and len(x) == 6:
              return 0
          else:
              return 1
      door_no = input("Enter your door number : ")
      st_name = input("Enter your street name : ").capitalize()
      city = input("Enter your city name : ").capitalize()
      state = input("Enter your state name : ").title()
      pincode = input("Enter your pincode : ")
      #validating the given inputs
      p = v_char(st_name)
      q = v_char(city)
      r = v_char(state)
      s = v_pin(pincode)
      t = p+q+r+s
      if t == 0:
        print("*********** Address validated **********")
        pre_add = {"Door no" :door_no, "Street name" :st_name, "City": city, "State": state, "Pincode":pincode}
        newvalue = {"$set": {"Present_address":pre_add}}
        verify = Update.otp_verification(self)
        if verify == 1:
          print("OTP verified")
          a = records.update_one(myquery, newvalue)
          if a != 0:
            print("Address updated successfully")
            Update.qr_updation(self)
          else:
            print("Something went wrong... Try again later..!!!")
        elif verify == 0:
          print("Invalid OTP ...!Try again!!!")     
      elif t >0:
        print("Address given were not valid.\nPlease use only alphabats and sapces only")

      #"********************************************************************************************************************************************"
  def update_gender(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      gen = ["MALE", "FEMALE", "TRANSGENDER"]
      gender = input("Enter your Gender\nMALE\ FEMALE\ TRANSGENDER : ").upper()
      if gender in gen:
          print("******Validated******")
          newvalue = {"$set":{"Gender" : gender}}
          verify = Update.otp_verification(self)
          if verify == 1:
            print("OTP verified")
            a = records.update_one(myquery, newvalue)
            if a != 0:
              print("Gender updated successfully")
              Update.qr_updation(self)
            else:
              print("Something went wrong... Try again later ..!!!")
          elif verify == 0:
            print("Invalid OTP ...!Try again!!!")     
      elif (gender).upper not in gen:
          print("WARNING ! ***** Invalid input....!! *****")


      #"*********************************************************************************************************************************************"

  def update_phone_no(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      p_num = input("Enter your 10 digit Phone Number : ")
      if len(p_num) == 10 and (p_num).isdigit():
        print("******Number validated!******")
        newvalue = {"$set":{"Phone number": p_num}}
        verify = Update.otp_verification(self)
        if verify == 1:
          print("OTP verified")
          a = records.update_one(myquery, newvalue)
          if a != 0:
            print("Phone Number updated successfully")
            Update.qr_updation(self)
          else:
            print("Something went wrong... Try again later..!!!")
        elif verify == 0:
          print("Invalid OTP ...!Try again!!!")     
      elif len(p_num) != 10 or not((p_num).isdigit()):
          print("WARNING ! **********Number invalid...!Please enter a valid number...!**********")

          #"***************************************************************************************************************************************"

  def update_email(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      c = 0 # counter for verifying email id
      email_id = input("Enter your email_id :")
      x = email_id.split("@")
      if email_id.endswith("@gmail.com") or email_id.endswith("@yahoo.in") or email_id.endswith("@hotmail.com") or email_id.endswith("@reddifmail.com"):
          c+=0
          if email_id[0].isalpha():
              c+=0
              for i in x[0]:
                  if i.isdigit():
                      continue
                  if i.isalpha():
                      continue 
                  elif i == "_" or i == ".":
                      continue
                  else:
                      c+=1               
          else:
              c+=1
    else:
        c+=1
    if c>0:
        print("Your mail_id is invalid")
    elif c == 0:
        print("Email id is validated")
        newvalue = {"$set":{"Email ID": email_id}}
        verify = Update.otp_verification(self)
        if verify == 1:
          print("OTP verified")
          a = records.update_one(myquery, newvalue)
          if a != 0:
            print("Email ID  updated successfully")
            Update.qr_updation(self)
          else:
            print("Something went wrong... Try again later..!!!")
        elif verify == 0:
          print("Invalid OTP ...!Try again!!!")     

          #"******************************************************************************************************************************************"
  def update_qua(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      edu_qua = input("Enter your educational qualification\nNA(For children below 15 and illitrate)\n10th\n12th\nDIPLOMA\nUNDER GRADUATE\nPOST GRADUATE\nDOCTRATE\n")
      if len(edu_qua) <5:
        stream = "NA"
      elif len(edu_qua) >=5:
        edu_qua = (edu_qua).upper()
        if edu_qua == "DIPLOMA":
          stream = input("Enter your stream\nCIVIL\nMECHANICAL\nECE\nEEE\nOTHERS :").upper()
        elif edu_qua == "UNDER GRADUATE":
          s = input("Enter your stream\nARTS & SCIENCE\nB.E\B.TECH").upper()
          if s == "ARTS & SCIENCE":
            stream = input("Enter your stream\nENGLISH\nSCIENCE\nACCOUNTS\nECONOMICS\nOTHERS").upper()
          elif s == "B.E" or "B.TECH":
            stre = input("Enter your stream\nMECHANICAL\nCIVIL\nCOMPUTER SCIENCE\IT\nBIO TECH\nOTHERS").upper()
            stream = s+" "+stre
        elif edu_qua == "POST GRADUATE" or "DOCTRATE":
          stream = input("Enter your stream : ").upper()
      Educational_qualification = {"Qualification": edu_qua, "Stream": stream}
      #renewal date generation
      from datetime import date
      from dateutil.relativedelta import relativedelta
      r_d = str(date.today() + relativedelta(years=+2))
      renewal_date = r_d[-2:]+"/"+r_d[-5:-3]+"/"+r_d[:4]
      print("Your next renewal date is "+renewal_date)
      newvalue = {"$set":{"Educational qualification": Educational_qualification,"Renewal date" : renewal_date}}
      verify = Update.otp_verification(self)
      if verify == 1:
        print("OTP verified")
        a = records.update_one(myquery, newvalue)
        if a != 0:
          print("Educational Qualification updated successfully")
          Update.qr_updation(self)
        else:
          print("Something went wrong... Try again later..!!!")
      elif verify == 0:
        print("Invalid OTP ...!Try again!!!")    
     

class PDF_generation(Update):

  def pdf_generate(self):
    myquery = {"Aadhar Number":self.Aadhar_no}
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://<user Name>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
    db = client.guviProof
    records = db.Aadhar
    x = []#user to find weather the record is in the database or not
    for i in records.find(myquery):
      x.append(i)
    if len(x) == 0:
      print("NO RECORDS FOUND ON THIS AADHAR NUMBER..! ENTER A VALID AADHAR NUMBER")
    elif len(x) >0:
      verify = Update.otp_verification(self)
      if verify == 0:
        print("Invalid OTP...!!! Try again...!!!")
      elif verify == 1:
        b = records.find_one(myquery, {"_id" : 0})
        xyz = records.find_one({"_id" : 1}, {"_id" : 0})
        from PIL import Image
        import io #input output stream
        img = Image.open(io.BytesIO(xyz["Logo"]))
        img_name = "guvi.jpg"
        img.save(img_name)
        #pdf generation part
        #!pip install fpdf
        #if module not found error thrown run the above code
        from fpdf import FPDF
        pdf = FPDF("P","mm", (115, 230))
        pdf.add_page()
        pdf.image("guvi.jpg", 5, 3, 20)
        pdf.set_font("Arial", "B", 15)
        pdf.set_text_color(255,36, 0)
        pdf.cell(0, 10, "GUVI AADHAR CARD", ln = 1, align = "C")
        pdf.set_font("Arial", "BI", 10)
        pdf.set_text_color(0, 0, 128)
        pdf.cell(0, 10, "UNIQUE IDENTIFICATION AUTHORITY OF GUVI", ln = 1, align = "C")
        pdf.set_text_color(0, 0, 0)
        pdf.cell(150, 20, " ", ln = 1)
        #retriving image from database and saving locally for pdf generation
        img = Image.open(io.BytesIO(b["Photo"]))
        img_name = f"{b['Name']}.jpg"
        img.save(img_name)
        pdf.image(img_name, 7,50, 30, 40)
        user = [f"                                  Name:{b['Name']}",
               f"                                  Address : {b['Permanent address']['Door no']}, {b['Permanent address']['Street name']}",
                f"                                                    {b['Permanent address']['City']}",
                f"                                                    {b['Permanent address']['State']}",
                f"                                  Pincode: {b['Permanent address']['Pincode']}",
                f"                                  DOB :{b['DOB']}",
                f"                                  GENDER : {b['Gender']}",
                f"                                  Educational Qualification :{b['Educational qualification']['Qualification']}",
                f"                                  Stream : {b['Educational qualification']['Stream']}"]

        for i in user:
            pdf.set_font("Arial", "", 10)
            pdf.cell(30,5, f"{i}", ln = 1, align = "L")
        pdf.set_font("Arial", "BI", 14)
        pdf.set_text_color(35, 142, 35)
        pdf.cell(0, 25, "YOUR UNIQUE AADHAR NUMBER IS ", ln = 1,align = "C")
        pdf.set_text_color(238, 0, 0)
        pdf.set_font("Arial","B", 28)
        pdf.cell(0, 5, f"{self.Aadhar_no}", ln = 1, align = "C")
        pdf.set_text_color(0, 0, 0)
        #retriving qr code from database and saving locally for pdf generation
        from PIL import Image
        import io#input output stream
        qr = Image.open(io.BytesIO(b["QRcode"]))
        qr_name = f"{b['Name']}_qr.jpg"
        qr.save(qr_name)
        pdf.image(qr_name,36, 140, 40, 40)
        pdf.cell(0, 60, " ", ln = 1)
        h1 = "Customer Helpline No : 1234"
        h2 = "Customer helpline Mali ID :guviaadhar@gmail.com"
        h3 = "Customer helpline website : www.aadharguvi.com"
        pdf.set_font("Arial", "I", 10)
        pdf.cell(100, 5, f"{h1}", ln = 1, align = "C")
        pdf.cell(100, 5, f"{h2}", ln = 1, align = "C")
        pdf.cell(100, 5, f"{h3}", ln = 1, align = "C")

        pdf.output(f"{b['Name']}.pdf")
        print("PDF generated successfully.\nTHIS IS A DIGITALLY GENERATED AADHAR CARD.\nYOU CAN USE THIS A IDENTITY PROOF.")
  
     

def Guvi_Aadhar_Portal():
  inp = input("For new registration enter >>R<<\nFor edit informations enter >>E<<\nTo generate your aadhar card as PDF enter >>F<<\n      ").upper()
  if inp == "R":
    reg = Registration
    reg.inputs()
  if inp == "E":
    a_no = input("Enter your 12 digit aadhar number here. No special characters allowed only numbers : ")
    a_no = a_no.replace(" ", "")
    if (a_no).isdigit():
      ad_no = a_no[:4]+" "+a_no[4:8]+" "+a_no[8:]
      ed = Update(ad_no)
      edt = input("Select your edit option...\n>>>FOR NAME ENTER N<<<\n>>>FOR PHOTO ENTER I<<<\n>>>FOR PERMANENT ADDRESS ENTER P<<<\n>>>FOR PRESENT ADDRESS ENTER T<<<\n>>>FOR GENDER ENTER G<<<\n>>>FOR EDUCATIONAL QUALIFICATION ENTER E<<<\n>>>FOR PHONE NUMBER C<<<\n>>>FOR EMAIL ID ENTER E<<<").upper()
      if edt == "N":
        ed.edit_name()
      elif edt == "I":
        ed.edit_photo()
      elif edt == "P":
        ed.edit_per_add()
      elif edt == "T":
        ed.edit_pre_add()
      elif edt == "G":
        ed.edit_gender()
      elif edt == "E":
        ed.edit_qua()
      elif edt == "C":
        ed.edit_p_no()
      elif edt == "E":
        ed.edit_email()
      elif edt != "N" or "I" or "P" or "T" or "G" or "E" or "C" or "E":
        print("Enter a valid key...!!!")
    else:
      print("Enter a valid aadhar number...!!!")
  elif inp == "F":
    print("***** WELCOME TO GUVI AADHAR PORTAL *****")
    a_no = input("Enter your 12 digit aadhar number here. No special characters allowed only numbers : ")
    a_no = a_no.replace(" ","")
    if (a_no).isdigit():
      ad_no = a_no[:4]+" "+a_no[4:8]+" "+a_no[8:]
      p = PDF_generation(ad_no)
      p.pdf_generate()
    else:
      print("Enter a valid aadhar number...!!!")
  elif inp != "R" or "E" or "F":
    print("Enter a valid key...!!!")
     

Guvi_Aadhar_Portal()
