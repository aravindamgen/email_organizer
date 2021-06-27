import sqlite3
import re
import smtplib,ssl
from email.mime.text import MIMEText
import fire as fire


class sending_email:

    default_post_TLS = 587
    default_post_SSL = 465
    provider = {
        "gmail": {"server_name": "smtp.gmail.com", "port": 587},
        "outlook": {"server_name": "smtp.mail.outlook.com", "port": 587},
        "yahoo": {"server_name": "smtp.mail.yahoo.com", "port": 587},
    }

    def __init__(self, name="", email="", password=""):
        self.name = name
        self.email = email
        self.password = password

    def starting_SSL_connection(self):
        try:
            print("sadsad")
            self.smtp_obj = smtplib.SMTP_SSL(self.provider["gmail"], self.default_post_SSL)
            print("sadsad")

            self.smtp_obj.starttls()
            print("hello")
            # self.smtp_obj.login(self.email,self.password)
            return [True, "No error"]
        except Exception as msg:
            return [False, msg]

    def pushing_emails_simple(self, receiver_email_list, title, body):
        try:
            data = MIMEText("""body""")
            data["Subject"] = title
            data["body"] = body
            data["From"] = self.email
            data["TO"] = ", ".join(receiver_email_list)
            # self.smtp_obj.sendmail(self.email,receiver_email_list,str(data))
            return [True, "Finished"]
        except Exception as msg:
            return [False, msg]


class Model:
    def __init__(self, name="", email="", passwd=""):
        self.user_email = email
        self.name = name
        self.passwd = passwd

    def checking_the_detail(self):
        return [True, "Msg"]

    def validate_email(self):
        if len(re.findall("[a-z0-9.]+@[a-z0-9.]+\.[a-z]{2,}", self.user_email)) != 1:
            return [False, "Invalid Email"]
        return [True, "valid"]

    def adding_master_user(self):
        v_b, v_m = self.validate_email()
        if not (v_b): return [v_b, v_m]
        check_ = self.checking_the_detail()
        if check_[0]:
            try:
                conn = sqlite3.connect("book.db")
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM master_users WHERE email='{self.user_email}'")
                data = cursor.fetchall()
                if len(data) != 0: return [False,
                                           "This email is already has a power of a 'SUDO', No need to add it, if you want to edit some content, just edit it."]
                cursor.execute(
                    f"INSERT INTO master_users (name,email,password) VALUES ('{self.name}','{self.user_email}','{self.passwd}')")
                conn.commit()
            except Exception as msg:
                return [False, msg]
            return [True, "Sudo superuser had been added successfully"]
        else:
            return check_

    def modifiy_master_user(self, mode):
        try:
            conn = sqlite3.connect("book.db")
            cursor = conn.cursor()
            if mode == "UPDATE":
                cursor.execute(
                    f"UPDATE master_users  SET name='{self.name}',password='{self.passwd}'   WHERE email='{self.user_email}'")
                conn.commit()
            elif mode == "DELETE":
                cursor.execute(f"DELETE FROM master_users where email='{self.user_email}'")
                conn.commit()
            else:
                pass
            return [True, f"{mode}: Done"]
        except Exception as msg:
            return [False, msg]

    def palette(self, mode, palette_name, palette_color, id=1):
        try:
            conn = sqlite3.connect("book.db")
            cursor = conn.cursor()
            print(mode)
            if mode == "ADD":
                cursor.execute(f"SELECT * FROM palette  WHERE palette_name='{palette_name}'")
                data = cursor.fetchall()
                if len(data) != 0: return [False, "Palette name is already taken"]
                cursor.execute(
                    f"INSERT INTO palette (palette_name,palette_color) VALUES ('{palette_name}','{palette_color}')")
                conn.commit()
            elif mode == "UPDATE":
                cursor.execute(
                    f"UPDATE palette  SET palette_name='{palette_name}',palette_color='{palette_color}' where palette_id ='{id}'")
                conn.commit()
            elif mode == "DELETE":
                cursor.execute(f"DELETE FROM palette where id='{id}'")

                """work have to done here"""

                conn.commit()
            return [True, "Success"]
        except Exception as msg:
            return [False, msg]

    def adding_other_email_to_palette(self, palette_id, email_list):
        try:
            finished_list = []
            conn = sqlite3.connect("book.db")
            cursor = conn.cursor()
            for email in email_list:
                cursor.execute(f"SELECT * FROM email_list WHERE email='{email}'")
                data = cursor.fetchall()
                if len(data) == 0:
                    v_b = len(re.findall("[a-z0-9.]+@[a-z0-9.]+\.[a-z]{2,}", email)) == 1
                    if v_b:
                        cursor.execute(f"INSERT INTO email_list (palette_fk,email) VALUES ('{palette_id}','{email}')")
                        conn.commit()
                        finished_list.append(email)
                    else:
                        print(f"{email} is Invalid email.")
                else:
                    print(f"{email} is already in this palette")
            print(f"successfully add {len(finished_list)} to the palette.")
            return [True, "Success"]
        except Exception as msg:
            return [False, msg]

    def modifing_email_in_palette(self, id, mode, email=""):
        try:
            conn = sqlite3.connect("book.db")
            cursor = conn.cursor()
            if mode == "UPDATE":
                cursor.execute(
                    f"UPDATE email_list SET email='{email}' where email_list_id = {id}")
                conn.commit()
            elif mode == "DELETE":
                cursor.execute(
                    f"DELETE FROM email_list where email_list_id = {id}")
                conn.commit()
            return [True, "success"]
        except Exception as msg:
            return [False, msg]

    def show_detail(self, things):
        try:
            conn = sqlite3.connect("book.db")
            cursor = conn.cursor()
            if things == "MASTER_USERS":
                cursor.execute(f"SELECT * FROM master_users")
                data = cursor.fetchall()
            elif things == "PALETTE":
                cursor.execute(f"SELECT * FROM palette")
                data = cursor.fetchall()
            elif things == "PALETTE_EMAIL_LIST":
                cursor.execute(f"SELECT * FROM email_list")
                data = cursor.fetchall()
            else:
                data = ["INVALID KEY"]
            return [True, "NO Error", data]
        except Exception as msg:
            return [False, msg]




# fire config
def sendemail():
    model_ = Model()
    data = model_.show_detail("MASTER_USERS")
    print("\nSelect the master email address")
    key_={}
    for i in data[2]:
        key_[i[0]]=i
        print(f"{i[0]}: {i[2]}")
    key=int(input("Enter the key: "))
    if key in key_.keys():
        data=key_[key]
        context = ssl.create_default_context()
        class_sending_email=smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        class_sending_email.login(data[2], data[3])
        title=input("Enter the title: ")
        body=input("Enter the body of content: ")
        data=show_data_palette()
        send=sending_email()
        send.pushing_emails_simple([],title=title,body=body)
        print("Email has been sended successfully")
    else:
        print("Invalid key")


def add_master_user():
    try:
        name = input("Enter the name: ")
        email = input("Enter the email: ")
        print("Note: Don't use your email password, it won't work.")
        print("App a new password in your account (secure app) for 'python', use that password.")
        print("Every thing will store locally, no one can access your data except you.")
        password = input("Enter the password: ")
        model_ = Model(name, email, password)
        model_.adding_master_user()
    except KeyboardInterrupt:
        print("Cancelling the registation process")
    except Exception as msg:
        print(f"Error: {msg}")


def show_data_master_user():
    model_ = Model()
    data = model_.show_detail("MASTER_USERS")
    return data[2]


def show_data_palette():
    model_ = Model()
    data = model_.show_detail("PALETTE")
    return data[2]


def show_data_email_list():
    model_ = Model()
    data = model_.show_detail("PALETTE_EMAIL_LIST")
    return data[2]


def palette_add():
    model_ = Model()
    palette_name = input("Enter the palette name: ")
    color = "#00FF00"
    model_.palette("ADD", palette_name, color)


def palette_update():
    model_ = Model()
    data = show_data_palette()
    palette_name = input("Enter the palette name: ")
    color = "#00FF00"
    model_.palette("ADD", palette_name, color)


def add_email_to_palette():
    data = show_data_palette()
    model_ = Model()
    keys = []
    if (len(data) != 0):
        for palette in range(len(data)):
            keys.append(palette + 1)
            print(f"{palette + 1}. {data[palette][1]}")
        key = int(input("Enter the key to add email: "))
        if key in keys:
            user_email = []
            e_n = input("Enter the number of email address you want to add: ")
            for i in range(int(e_n)):
                user_email.append(input(f"Enter the email address {i + 1}: "))
            model_ = Model()
            model_.adding_other_email_to_palette(key, user_email)
        else:
            print("Invalid key")


def update_master_users():
    model_ = Model()
    data = model_.show_detail("MASTER_USERS")
    print()
    key_ = {}
    for d_a in range(len(data[2])):
        key_[str(d_a + 1)] = data[2][d_a][2]
        print(f"{d_a + 1}: {data[2][d_a][2]}")
    key = input("Enter the key: ")
    if key in key_.keys():
        email = key_[key]
        name = input("Enter the name: ")
        print("Note: Don't use your email password, it won't work.")
        print("App a new password in your account (secure app) for 'python', use that password.")
        print("Every thing will store locally, no one can access your data except you.")
        password = input("Enter the password: ")
        model_ = Model(name, email, password)
        model_.modifiy_master_user("UPDATE")
    else:
        print("Invalid key")


def delete_master_user():
    model_ = Model()
    data = model_.show_detail("MASTER_USERS")
    print()
    key_ = {}
    for d_a in range(len(data[2])):
        key_[str(d_a + 1)] = data[2][d_a][2]
        print(f"{d_a + 1}: {data[2][d_a][2]}")
    key = input("Enter the key: ")
    if key in key_.keys():
        model_ = Model(email=key_[key])
        model_.modifiy_master_user("DELETE")
    else:
        print("Invalid key")




if __name__ == "__main__":
    fire.Fire({
        #send email
        "sendemail":sendemail,
        # add
        "add_master_user": add_master_user,
        "add_palette": palette_add,
        "add_email_to_palette": add_email_to_palette,
        # show
        "master_users": show_data_master_user,
        "palette": show_data_palette,
        "palette_email": show_data_email_list,
        # update
        "update_master_users": update_master_users,
        #delete
        "delete_master_users":delete_master_user,
    })
