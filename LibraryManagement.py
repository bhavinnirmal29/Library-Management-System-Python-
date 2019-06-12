# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:53:21 2018

@author: Deesha
"""

#SIGNUP PAGE
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
   
class SignUp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand= True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames={}
        for F in (LoginPage,AdminPage,SignUpPage,AdminRightsPage,AddBookPage,RemoveBookPage,RemoveUserPage,Display_Books_Page,AfterUserLoginPage,ReturnBookPage,UserProfilePage):
            frame=F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(LoginPage)
    
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        l1=tk.Label(self,text="Online Library Management System",bg="light blue",compound=tk.CENTER)
        l1.config(font=("Times New Roman",24))
        
        login_header=tk.Label(self,text="LOGIN",bg="light blue",fg="red",font=("Times New Roman",38))
        login_header.grid(row=1,column=1,pady=30,ipadx=10)
        
        admin_btn=tk.Button(self,text="Admin",fg="blue",bg="grey",font=("times new roman",16),width=10,command=lambda:controller.show_frame(AdminPage))
        admin_btn.grid(row=1,column=2,padx=30)
        
        login_label=tk.Label(self,text="Login Id: ",bg="light blue",font=("Times New Roman",18))
        login_label.grid(row=2,column=0,sticky='w')
        
        self.uname=tk.StringVar()
        self.login_field=tk.Entry(self,bd=5,width=20,font=("Times New Roman",18),textvariable=self.uname)
        self.login_field.focus()
        self.login_field.delete(0,'end')
        self.login_field.grid(row=2,column=1)
        #login_field.pack(side=tk.RIGHT)
        
        pwd_label=tk.Label(self,text="Password: ",bg="light blue",font=("Times New Roman",18))
        pwd_label.grid(row=3,column=0,sticky='w',pady=20)
        #pwd_label.pack()
        
        self.pwd1=tk.StringVar()
        self.pwd_field=tk.Entry(self,bd=5,width=20,show="*",font=("Times New Roman",18),textvariable=self.pwd1)
        self.pwd_field.grid(row=3,column=1)
        
        login_btn=tk.Button(self,text="Login",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda:self.validate_Login_Page(controller))
        login_btn.grid(row=4,column=0,padx=10)
        
        signup_btn=tk.Button(self,text="Register",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: controller.show_frame(SignUpPage))
        signup_btn.grid(row=4,column=1)
        
        quit_btn=tk.Button(self,text="QUIT",fg="black",bg="light green",font=("Times New Roman",16),width=10,command=lambda:self.exitFunc(controller))
        quit_btn.grid(row=4,column=2)
        tk.Frame.configure(self,background="light blue")
    def exitFunc(self,cont):
        cont.destroy()
        '''
        b1=tk.Button(self,text="Back To Home",command=lambda: controller.show_frame(StartPage))
        b1.grid(row=5,column=1)
        '''
        
    def validate_Login_Page(self,cont):
            self.uname2=self.uname.get()
            self.pwd2=self.pwd1.get()
            conn=sqlite3.connect("users1.db")
            c=conn.cursor()
            c.execute("select username,pwd from signup")
            rows=c.fetchall()
            flag=0
            for row in rows:
                if(self.uname2==row[0] and self.pwd2==row[1]):
                    flag=1
                    break
                else:
                    flag=0
            if flag==1:
                tk.messagebox.showinfo("Login","Login Successful")
                conn1=sqlite3.connect("users1.db")
                c1=conn1.cursor()
                c1.execute("CREATE TABLE IF NOT EXISTS LoginDetail(username text)")
                c1.execute("INSERT INTO LoginDetail VALUES('"+self.uname2+"')")
                conn1.commit()
                conn1.close()
                self.login_field.delete(0,'end')
                self.pwd_field.delete(0,'end')
                self.login_field.focus()
                cont.show_frame(AfterUserLoginPage)
            else:
                tk.messagebox.showinfo("Error","Invalid Credentials")
                self.login_field.delete(0,'end')
                self.pwd_field.delete(0,'end')
                self.login_field.focus()


class AfterUserLoginPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        user_logout_btn=tk.Button(self,text="LOGOUT",fg="light green",bg="black",font=("Times New Roman",18),width=10,compound="left",command=lambda: self.logout_Button(controller))
        user_logout_btn.grid(row=0,columnspan=2,pady=20,padx=10)        
        
        user_detail_label=tk.Label(self,text="User Details",fg="red",bg="light blue",font=("Times New Roman",38))
        user_detail_label.grid(row=0,column=2,padx=40)
        
        self.profile_btn=tk.Button(self,text="My Profile",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: controller.show_frame(UserProfilePage))
        self.profile_btn.grid(row=1,column=2,pady=25)
        
        issue_btn=tk.Button(self,text="Issue Book",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda:controller.show_frame(Display_Books_Page))
        issue_btn.grid(row=2,column=2,pady=25)
        
        return_btn=tk.Button(self,text="Return Book",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda:controller.show_frame(ReturnBookPage))
        return_btn.grid(row=3,column=2,pady=25)
        
        tk.Frame.configure(self,background="light blue")
        
    def logout_Button(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("SELECT * FROM LoginDetail")
        rows=c.fetchall()
        uname=rows[0]
        c.execute("DELETE FROM LoginDetail WHERE username='%s'"%uname)
        conn.commit()
        conn.close()
        tk.messagebox.showinfo("Logout","You have been Logged Out")
        cont.show_frame(LoginPage)
    

class UserProfilePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        user_detail_label=tk.Label(self,text="MyProfile",fg="red",bg="light blue",font=("Times New Roman",38))
        user_detail_label.grid(row=0,column=2,padx=20)
        
        self.user_logout_btn=tk.Button(self,text="LOGOUT",fg="light green",bg="black",font=("Times New Roman",18),width=10,compound="left",command=lambda: self.logout_Button(controller))
        self.user_logout_btn.grid(row=0,columnspan=2,pady=20,padx=10)   
        
        self.get_profile_btn=tk.Button(self,text="Get Profile",fg="light green",bg="black",font=("Times New Roman",18),width=10,compound="left",command=lambda: self.get_Profile_Button(controller))
        self.get_profile_btn.grid(row=0,column=3,pady=20,padx=10)
        
        fname_label=tk.Label(self,text="First Name: ",bg="light blue",fg="black",font=("Times New Roman",18))
        fname_label.grid(row=1,column=0,padx=15,pady=10,sticky="w")
        
        self.fname_data=tk.Label(self,text="",bg="light blue",fg="black",font=("Times New Roman",18))
        self.fname_data.grid(row=1,column=2,padx=15,pady=10)
        
        lname_label=tk.Label(self,text="Last Name: ",bg="light blue",fg="black",font=("Times New Roman",18))
        lname_label.grid(row=2,column=0,padx=15,pady=10,sticky="w")
        
        self.lname_data=tk.Label(self,text="",bg="light blue",fg="black",font=("Times New Roman",18))
        self.lname_data.grid(row=2,column=2,padx=15,pady=10)
        
        username_label=tk.Label(self,text="UserName:",bg="light blue",fg="black",font=("Times New Roman",18))
        username_label.grid(row=3,column=0,padx=15,sticky='w',pady=10)
        
        self.user_data=tk.Label(self,bg="light blue",text="",fg="black",font=("Times New Roman",18))
        self.user_data.grid(row=3,column=2,padx=15,sticky='SENW',pady=10)
        
        book_label=tk.Label(self,text="Books Issued",bg="light blue",fg="black",font=("Times New Roman",18))
        book_label.grid(row=4,column=0,padx=15,sticky='w',pady=10)        
        
        self.Lb1 = tk.Listbox(self, width=30, height=3,font=("times",16),bg="light green",selectbackground="black")
        self.Lb1.grid(row=5, columnspan=3,padx=10,sticky="w")
        # create a vertical scrollbar to the right of the listbox
        self.yscroll = tk.Scrollbar(self,command=self.Lb1.yview, orient=tk.VERTICAL)
        self.yscroll.grid(row=5, column=3,sticky="e")
        self.Lb1.configure(yscrollcommand=self.yscroll.set)
        tk.Frame.configure(self,background="light blue")
        
    def get_Profile_Button(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        p_uname=""
        c.execute("Select * from LoginDetail")
        rows=c.fetchall()
        for i in rows:
            p_uname=i[0]
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("Select * from Signup where username = '"+p_uname+"'")
        rows=c.fetchall()
        for row in rows:
            self.fname_data.config(text=""+row[0])
            self.lname_data.config(text=""+row[1])
            self.user_data.config(text=""+p_uname)
        conn=sqlite3.connect("Books.db")
        c=conn.cursor()
        c.execute("Select book_name from Issued_Books where username = '"+p_uname+"'")
        rows=c.fetchall()
        for i in rows:
            self.Lb1.insert(1,i[0])
        #print(p_uname)
    def logout_Button(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("SELECT * FROM LoginDetail")
        rows=c.fetchall()
        uname=rows[0]
        c.execute("DELETE FROM LoginDetail WHERE username='%s'"%uname)
        conn.commit()
        conn.close()
        tk.messagebox.showinfo("Logout","You have been Logged Out")
        self.fname_data.config(text="")
        self.lname_data.config(text="")
        self.user_data.config(text="")
        cont.show_frame(LoginPage)

class AdminPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        admin_header=tk.Label(self,text="ADMIN",bg="light blue",fg="red",compound=tk.CENTER,font=("Times New Roman",38))
        admin_header.grid(row=0,column=1,sticky='N',pady=30)
        
        admin_login=tk.Label(self,text="Login Id: ",bg="light blue",fg="black",font=("Times New Roman",18))
        admin_login.grid(row=2,column=0,padx=15,sticky='SENW')
        
        self.admin_uname=tk.StringVar()
        self.admin_login_field=tk.Entry(self,bd=5,width=20,font=("Times New Roman",18),textvariable=self.admin_uname)
        self.admin_login_field.grid(row=2,column=1)
        
        admin_pwd_label=tk.Label(self,text="Password: ",bg="light blue",fg="black",font=("Times New Roman",18))
        admin_pwd_label.grid(row=3,column=0)
        #pwd_label.pack()
        
        self.admin_pwd=tk.StringVar()
        self.admin_pwd_field=tk.Entry(self,bd=5,width=20,show="*",font=("Times New Roman",18),textvariable=self.admin_pwd)
        self.admin_pwd_field.grid(row=3,column=1,pady=10)
        
        admin_login_btn=tk.Button(self,text="LOGIN",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: self.validate_Admin_Login(controller))
        admin_login_btn.grid(row=4,column=0,padx=25)

        back_btn=tk.Button(self,text="BACK",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda:controller.show_frame(LoginPage))
        back_btn.grid(row=4,column=1,padx=10,sticky="e")
        tk.Frame.configure(self,background="light blue")    
    def validate_Admin_Login(self,cont):
        admin_uname1=self.admin_uname.get()
        admin_pwd1=self.admin_pwd.get()
        
        if admin_uname1=="admin" and admin_pwd1=="password1234":
            tk.messagebox.showinfo("Admin","Login Successful")
            self.admin_login_field.delete(0,'end')
            self.admin_pwd_field.delete(0,'end')
            cont.show_frame(AdminRightsPage)
        else:
            tk.messagebox.showinfo("Admin","Invalid Credentials")
            self.admin_login_field.delete(0,'end')
            self.admin_pwd_field.delete(0,'end')

class AdminRightsPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        ad_label=tk.Label(self,text="ADMIN",fg="red",bg="light blue",font=("Times New Roman",38),width=20)
        #ad_label.grid(row=0,column=1,sticky='w')
        ad_label.pack(pady=30)
        
        rm_user_btn=tk.Button(self,text="Remove User",fg="black",bg="light green",font=("Times New Roman",18),width=20,command=lambda:controller.show_frame(RemoveUserPage))
        #rm_user_btn.grid(row=1,column=1)
        rm_user_btn.pack()
        
        add_book_btn=tk.Button(self,text="Add Book",fg="black",bg="light green",font=("Times New Roman",18),width=20,command=lambda:controller.show_frame(AddBookPage))
        #add_book_btn.grid(row=2,column=1)
        add_book_btn.pack(pady=30)
        
        rm_book_btn=tk.Button(self,text="Remove Book",fg="black",bg="light green",font=("Times New Roman",18),width=20,command=lambda:controller.show_frame(RemoveBookPage))
        #rm_book_btn.grid(row=3,column=1)
        rm_book_btn.pack()
        
        
        logout_btn=tk.Button(self,text="LOGOUT",fg="light green",bg="black",font=("Times New Roman",16),width=10,command=lambda:self.logout_Button(controller))
        logout_btn.pack(side=tk.RIGHT,pady=10)
        tk.Frame.configure(self,background="light blue")
         
    def logout_Button(self,cont):
        tk.messagebox.showinfo("Logout","You have been Logged Out")
        cont.show_frame(LoginPage)       
       
        
class SignUpPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        signup_header=tk.Label(self,text="SIGNUP",bg="light blue",fg="red",compound=tk.CENTER,font=("Times New Roman",38))
        signup_header.grid(row=0,column=1,sticky="w")  
        
        f_label=tk.Label(self,text="First Name:",bg="light blue",fg="black",font=("Times new Roman",18))
        f_label.grid(row=1,column=0,padx=40,pady=10,sticky="nw")
        
        self.fn=tk.StringVar()
        
        self.f_entry=tk.Entry(self,bd=5,textvariable=self.fn,width=20,font=("times",18))
        self.f_entry.grid(row=1,column=1)
        
        l_label=tk.Label(self,text="Last Name:",bg="light blue",fg="black",font=("Times new Roman",18))
        l_label.grid(row=2,column=0,pady=10)
        
        self.ln=tk.StringVar()
        self.l_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.ln)
        self.l_entry.grid(row=2,column=1)
        
        s_label=tk.Label(self,text="UserName:",bg="light blue",fg="black",font=("Times new Roman",18))
        s_label.grid(row=3,column=0,pady=10,sticky='n')
        
        self.ss=tk.StringVar()
        self.s_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.ss)
        self.s_entry.grid(row=3,column=1)
        
        spwd_label=tk.Label(self,text="Password:",bg="light blue",fg="black",font=("Times new Roman",18))
        spwd_label.grid(row=4,column=0,pady=10,sticky="n")
        
        self.sp=tk.StringVar()
        self.p_entry=tk.Entry(self,bd=5,width=20,font=("times",18),show="*",textvariable=self.sp)
        self.p_entry.grid(row=4,column=1)
        
        s_login_btn=tk.Button(self,text="SignUp",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: self.validate_Sign_Up(controller))
        s_login_btn.grid(row=5,column=0,pady=5,sticky='e')
        
        back_btn=tk.Button(self,text="Back",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: controller.show_frame(LoginPage))
        back_btn.grid(row=5,column=1,padx=10,pady=10,sticky="e")
        tk.Frame.configure(self,background="light blue")
    def validate_Sign_Up(self,cont):
        fn1=self.fn.get()
        ln1=self.ln.get()
        s1=self.ss.get()
        p1=self.sp.get()
        #print(fn1)
        #print(ln1)
        #print(s1)
        #print(p1)
        if len(fn1)==0 or len(ln1)==0 or len(s1)==0 or len(p1)==0: 
            tk.messagebox.showinfo("Alert","Enter valid Values")
            self.f_entry.delete(0,'end')
            self.l_entry.delete(0,'end')
            self.s_entry.delete(0,'end')
            self.p_entry.delete(0,'end')
            
        else:    
            conn=sqlite3.connect("users1.db")
            c=conn.cursor()
            c.execute('''CREATE TABLE if not exists signup 
                 (fname text,lname text,username text,pwd text)''')
            # Insert a row of data
            c.execute("INSERT INTO signup VALUES ('"+fn1+"','"+ln1+"','"+s1+"','"+p1+"')")
            #print("1 Row Inserted ")
            tk.messagebox.showinfo("Register","Succesfull")
            conn.commit()
            conn.close()
            self.f_entry.delete(0,'end')
            self.l_entry.delete(0,'end')
            self.s_entry.delete(0,'end')
            self.p_entry.delete(0,'end')
            cont.show_frame(LoginPage)
            
'''if fn1.isalpha() == False and len(fn1)<=3 and len(fn1)!=0:
    tk.messagebox.showinfo("Alert","Enter valid FirstName")
if ln1.isalpha() ==False and len(ln1)<=3 and len(ln1)!=0:
    tk.messagebox.showinfo("Alert","Enter valid LastName")
if s1.isalnum() == False and len(s1)<=4 and len(s1)!=0:
    self.messagebox.showinfo("Alert","Enter valid Username")
if p1.isalnum() == False and len(p1)<=6 and len(p1)!=0:
    self.messagebox.showinfo("Alert","Enter valid Password")
'''

class Issued_Book_Page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
class Display_Books_Page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        book_label=tk.Label(self,text="Books Available",fg="red",bg="light blue",font=("Times New Roman",38))
        book_label.grid(row=0,columnspan=5,ipadx=10,pady=5,sticky="nsew")
        
        Lb1 = tk.Listbox(self, width=50, height=10,font=("times",16),bg="light green",selectbackground="black")
        Lb1.grid(row=1, columnspan=4,padx=10,sticky="e")
        # create a vertical scrollbar to the right of the listbox
        yscroll = tk.Scrollbar(self,command=Lb1.yview, orient=tk.VERTICAL)
        yscroll.grid(row=1, column=4, sticky="NSWE")
        Lb1.configure(yscrollcommand=yscroll.set)
        self.temp=""
        def on_select(event):
            self.temp=event.widget.get(event.widget.curselection())
            print(self.temp)
        conn=sqlite3.connect("Books.db")
        c=conn.cursor()
        c.execute("select bk_title,bk_author,bk_isbn from BooksData")
        rows = c.fetchall()
        conn.commit()
        Lb1.bind('<<ListboxSelect>>', on_select)
        Lb1.insert(0,"TITLE")
        for i in rows:
            Lb1.insert(1,i[0])

        self.logout_btn=tk.Button(self,text="LOGOUT",fg="light green",bg="black",font=("Times New Roman",14),width=10,command=lambda:self.logout_Button(controller))
        self.logout_btn.grid(row=0,column=0,padx=10,pady=10,sticky="w")
        
        issue_bk_btn=tk.Button(self,text="Issue Book",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: self.book_Issued(controller))
        issue_bk_btn.grid(row=2,columnspan=1,sticky="n",pady=10)
        
        back_bk_btn=tk.Button(self,text="Back",fg="black",bg="light green",font=("times",18),width=10,command=lambda:controller.show_frame(AfterUserLoginPage))
        back_bk_btn.grid(row=2,column=3,sticky="n",pady=10)
        
        tk.Frame.configure(self,background="light blue")
    def logout_Button(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("SELECT * FROM LoginDetail")
        rows=c.fetchall()
        conn.commit()
        uname=""
        for i in rows:
            uname=i[0]
        c.execute("DELETE FROM LoginDetail WHERE username='%s'"%uname)
        conn.commit()
        conn.close()
        tk.messagebox.showinfo("Logout","You have been Logged Out")
        cont.show_frame(LoginPage)       
       
    def book_Issued(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("SELECT * FROM LoginDetail")
        rows=c.fetchall()
        conn.commit()
        uname1=""
        for i in rows:
            uname1=i[0]
        print(uname1)    
        uname=uname1
        self.bk_name=str(self.temp)
        bk1_name=str(self.bk_name)
        if(len(bk1_name)==0):
            tk.messagebox.showinfo("Error","You have not selected any Book")
        else:
            conn=sqlite3.connect("Books.db")
            c=conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Issued_Books(username text,book_name text)")
            conn.commit()
            c.execute("INSERT INTO Issued_Books VALUES ('"+uname+"','"+bk1_name+"')")
            tk.messagebox.showinfo("Success","books Issued")
            conn.commit()
        
class AddBookPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        book_label=tk.Label(self,text="Book Details",fg="red",bg="light blue",font=("Times New Roman",38))
        book_label.grid(row=0,columnspan=2,pady=5,padx=10,sticky="e")
        
        bk_title = tk.Label(self,text="Book Name: ",bg="light blue",fg="black",font=("Times new Roman",18))
        bk_title.grid(row=1,column=0,padx=10,sticky="w",ipadx=30)
        
        self.bkt=tk.StringVar()
        self.bk_title_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.bkt)
        self.bk_title_entry.grid(row=1,column=1,pady=10)
        
        bk_author = tk.Label(self,text="Author Name:",bg="light blue",fg="black",font=("Times new Roman",18))
        bk_author.grid(row=2,column=0)
        
        self.b_a=tk.StringVar()
        self.bk_author_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.b_a)
        self.bk_author_entry.grid(row=2,column=1,pady=10)
        
        bk_isbn_label = tk.Label(self,text="ISBN: ",bg="light blue",fg="black",font=("Times new Roman",18))
        bk_isbn_label.grid(row=3,column=0,sticky="NSEW")
        
        self.isbn=tk.StringVar()
        self.bk_isbn_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.isbn)
        self.bk_isbn_entry.grid(row=3,column=1,pady=10)
        
        bk_publish_date= tk.Label(self,text="Publish Date: ",bg="light blue",fg="black",font=("Times new Roman",18))
        bk_publish_date.grid(row=4,column=0)
        
        self.bpd=tk.StringVar()
        self.bk_publish_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.bpd)
        self.bk_publish_entry.grid(row=4,column=1,pady=10)
        
        done_btn=tk.Button(self,text="Done",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: self.add_New_Book(controller))
        done_btn.grid(row=5,column=0,ipadx=10,sticky='e')
        
        back_btn=tk.Button(self,text="BACK",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda:controller.show_frame(AdminRightsPage))
        back_btn.grid(row=5,column=1,padx=10,sticky="e")
        
        logout_btn=tk.Button(self,text="LOGOUT",fg="light green",bg="black",font=("Times New Roman",16),width=10)
        logout_btn.grid(row=0,column=0,padx=10,sticky="w")
        self.bk_title_entry.delete(0,'end')
        self.bk_author_entry.delete(0,'end')
        self.bk_isbn_entry.delete(0,'end')
        self.bk_publish_entry.delete(0,'end')
        tk.Frame.configure(self,background="light blue")
        
    def add_New_Book(self,cont):
        bktitle1=self.bkt.get()
        bkauthor1=self.b_a.get()
        bkisbn1=self.isbn.get()
        bkdate1=self.bpd.get()
        if (len(bktitle1)==0 or len(bkauthor1)==0 or len(bkisbn1)==0 or len(bkdate1)==0):
            tk.messagebox.showinfo("Error","Enter valid Values")
            self.bk_title_entry.delete(0,'end')
            self.bk_author_entry.delete(0,'end')
            self.bk_isbn_entry.delete(0,'end')
            self.bk_publish_entry.delete(0,'end')
        else:  
            conn=sqlite3.connect("Books.db")
            c=conn.cursor()
            c.execute("INSERT INTO BooksData VALUES ('"+bktitle1+"','"+bkauthor1+"','"+bkisbn1+"','"+bkdate1+"')")
            conn.commit()
            conn.close()
            tk.messagebox.showinfo("Success","Book Added Successfully")
            self.bk_title_entry.delete(0,'end')
            self.bk_author_entry.delete(0,'end')
            self.bk_isbn_entry.delete(0,'end')
            self.bk_publish_entry.delete(0,'end')
            cont.show_frame(AdminRightsPage)

class RemoveUserPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        rm_user_label=tk.Label(self,text="Remove User",fg="red",bg="light blue",font=("Times New Roman",38))
        rm_user_label.grid(row=0,columnspan=2,sticky="nsew",ipadx=30,pady=30)
        
        rm_uname_label=tk.Label(self,text="Username : ",bg="light blue",fg="black",font=("Times new Roman",18))
        rm_uname_label.grid(row=1,column=0,ipadx=20,sticky='w')
        
        self.rm_uname=tk.StringVar()
        self.rm_user_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.rm_uname)
        self.rm_user_entry.grid(row=1,column=1,padx=20,pady=10)
        
        rm_pwd_label=tk.Label(self,text="Admin Password : ",bg="light blue",fg="black",font=("Times new Roman",18))
        rm_pwd_label.grid(row=2,column=0,ipadx=20,sticky='w')
        
        self.rm_pwd=tk.StringVar()
        self.rm_pwd_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.rm_pwd,show="*")
        self.rm_pwd_entry.grid(row=2,column=1,padx=20,pady=10)
        
        rm_btn=tk.Button(self,text="Remove",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda : self.remove_User(controller))
        rm_btn.grid(row=3,column=0,padx=10,pady=20,sticky='e')
        
        rm_userback_btn=tk.Button(self,text="Back",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: controller.show_frame(AdminRightsPage))
        rm_userback_btn.grid(row=3,column=1,padx=10,pady=20,sticky='e')
        
        tk.Frame.configure(self,background="light blue")
    
    def remove_User(self,cont):
        flag=0
        self.rm_uname1=self.rm_uname.get()
        self.rm_pwd1=self.rm_pwd.get()
        if(len(self.rm_uname1)==0 and len(self.rm_pwd1)==0):
            tk.messagebox.showinfo("Error","Empty Fields")
        else:
            conn=sqlite3.connect("users1.db")
            c=conn.cursor()
            c.execute("SELECT username FROM signup")
            rows=c.fetchall()
            for row in rows:
                if(self.rm_uname1==row[0] and self.rm_pwd1=="password1234"):
                    flag=1
                    break
                else:
                    flag=0
            
            if (flag==1):
                sql="DELETE FROM Signup WHERE username = '%s'"%self.rm_uname1
                c.execute(sql)
                conn.commit()
                c.close()
                conn.close()
                tk.messagebox.showinfo("Success","User Found And Removed")
                self.rm_user_entry.delete(0,'end')
                self.rm_pwd_entry.delete(0,'end')
            else:
                tk.messagebox.showinfo("Error","Username/Password is Invalid")
                self.rm_user_entry.delete(0,'end')
                self.rm_pwd_entry.delete(0,'end')
    
class RemoveBookPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        book_label=tk.Label(self,text="Remove Book",fg="red",bg="light blue",font=("Times New Roman",38))
        book_label.grid(row=0,column=1,sticky="e",pady=30)
        
        rmbk_isbn_label = tk.Label(self,text="ISBN: ",bg="light blue",fg="black",font=("Times new Roman",18))
        rmbk_isbn_label.grid(row=1,column=0,padx=50)
        self.rm_isbn=tk.StringVar()
        self.rmbk_isbn_entry=tk.Entry(self,bd=5,width=20,font=("times",18),textvariable=self.rm_isbn)
        self.rmbk_isbn_entry.delete(0,'end')
        self.rmbk_isbn_entry.grid(row=1,column=1,padx=20,pady=10)
        
        rm_btn=tk.Button(self,text="Remove",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda:self.remove_book(controller))
        rm_btn.grid(row=2,columnspan=2,ipadx=10,pady=20,sticky='N')
        
        rm_back_btn=tk.Button(self,text="Back",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: self.back_Redirect(controller))
        rm_back_btn.grid(row=2,column=1,padx=10,pady=20,sticky='e')
        
        tk.Frame.configure(self,background="light blue")
    
    def back_Redirect(self,cont):
        self.rmbk_isbn_entry.delete(0,'end')
        cont.show_frame(AdminRightsPage)
    def remove_book(self,cont):
        flag=0
        self.bk_isbn=self.rm_isbn.get()
        print(self.bk_isbn)
        if(len(self.bk_isbn)==0):
            tk.messagebox.showinfo("Error","ISBN EMPTY")
        else:
            conn=sqlite3.connect("Books.db")
            c=conn.cursor()
            c.execute("SELECT bk_isbn FROM BooksData")
            rows=c.fetchall()
            for row in rows:
                if (row[0]==self.bk_isbn):
                    flag=1
                    break
                else:
                    flag=0
            if (flag==1):
                c.execute("DELETE FROM BooksData WHERE bk_isbn='"+self.bk_isbn+"'")
                conn.commit()
                tk.messagebox.showinfo("Success","Book Removed")
                self.rmbk_isbn_entry.delete(0,'end')
            else:
                tk.messagebox.showinfo("Error","Invalid ISBN")
                self.rmbk_isbn_entry.delete(0,'end')
                
        
class ReturnBookPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        book_label=tk.Label(self,text="Return Book",fg="red",bg="light blue",font=("Times New Roman",34))
        book_label.grid(row=0,column=1,ipadx=5,pady=5,sticky="nsew")
        
        self.Lb1 = tk.Listbox(self, width=50, height=10,font=("times",16),bg="light green",selectbackground="black")
        self.Lb1.grid(row=1, columnspan=4,padx=10,sticky="w")
        # create a vertical scrollbar to the right of the listbox
        yscroll = tk.Scrollbar(self,command=self.Lb1.yview, orient=tk.VERTICAL)
        yscroll.grid(row=1, column=4, sticky="NSWE")
        self.Lb1.configure(yscrollcommand=yscroll.set)
        
        self.temp=""
        def on_select(event):
            self.temp=event.widget.get(event.widget.curselection())
            print(self.temp)
        self.Lb1.bind('<<ListboxSelect>>', on_select)
        
        self.logout_btn=tk.Button(self,text="LOGOUT",fg="light green",bg="black",font=("Times New Roman",16),width=10,command=lambda:self.logout_Button(controller))
        self.logout_btn.grid(row=0,column=0,padx=10,pady=10,sticky="w")
        
        self.show_btn=tk.Button(self,text="Show Books",fg="light green",bg="black",font=("Times New Roman",16),width=10,command=lambda:self.show_Books(controller))
        self.show_btn.grid(row=0,column=2,padx=5,pady=10,sticky="w")
        
        rtn_bk_btn=tk.Button(self,text="Return Book",fg="black",bg="light green",font=("Times New Roman",18),width=10,command=lambda: self.return_Book(controller))
        rtn_bk_btn.grid(row=2,columnspan=1,sticky="n",pady=10)
        
        back_bk_btn=tk.Button(self,text="Back",fg="black",bg="light green",font=("times",18),width=10,command=lambda:controller.show_frame(AfterUserLoginPage))
        back_bk_btn.grid(row=2,column=2,sticky="w",pady=10)
        
        tk.Frame.configure(self,background="light blue")
    def logout_Button(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("SELECT * FROM LoginDetail")
        rows=c.fetchall()
        conn.commit()
        uname=""
        for i in rows:
            uname=i[0]
        c.execute("DELETE FROM LoginDetail WHERE username='%s'"%uname)
        conn.commit()
        conn.close()
        tk.messagebox.showinfo("Logout","You have been Logged Out")
        cont.show_frame(LoginPage)       
       
    def return_Book(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("Select * from LoginDetail")
        rows=c.fetchall()
        uname=""
        for i in rows:
            uname=i[0]
        bk1_name=self.temp
        if(len(bk1_name)==0):
            tk.messagebox.showinfo("Error","You have not selected any Book")
        else:
            conn=sqlite3.connect("Books.db")
            c=conn.cursor()
            c.execute("Delete from Issued_books where book_name = '"+bk1_name+"' and username = '"+uname+"'")
            tk.messagebox.showinfo("Success","Book Returned")
            conn.commit()
    def show_Books(self,cont):
        conn=sqlite3.connect("users1.db")
        c=conn.cursor()
        c.execute("Select * from LoginDetail")
        rows=c.fetchall()
        uname=""
        for i in rows:
            uname=i[0]
        conn.commit()
        conn=sqlite3.connect("Books.db")
        c=conn.cursor()
        c.execute("Select book_name from Issued_Books where username = '%s'"%uname)
        rows=c.fetchall()
        for i in rows:
            self.Lb1.insert(1,i[0])        
app=SignUp()
app.title("Online Library Management System")
app.geometry("605x400")
app.resizable(0,0)
app.mainloop()