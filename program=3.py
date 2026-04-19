import sqlite3 as sql
con = sql.connect("banks")
cur=con.cursor()
q="create table if not exists cus (cid int, cacc int primary key,cname text,password text, amount int)"
#q="drop table  cus"
cur.execute(q)
print("table created successfully")
q="""CREATE TABLE if not exists transactions(tid INTEGER PRIMARY KEY AUTOINCREMENT,cacc INTEGER,ttype TEXT,amount INTEGER,tdate DATETIME DEFAULT (datetime('now','localtime')))"""
#q="drop table  transactions"
cur.execute(q)
print("table created")
con.commit()

ch="y"
while ch=="y":
    list = ["1)Create Account", "2)Deposit Amount", "3)Withdraw Amount", "4)Transfer", "5)Balance Enquiry",
            "6)Transaction history", "7)Delete Account Details", "8)exit"]
    for i in list:
        print(i)
    choice = int(input("enter your choice:"))
    if choice >= 1 and choice <= 8:
        if choice==1:
            print("Create Account")
            q1="insert into cus values(?,?,?,?,?)"
            cid=int(input("enter customer id:"))
            cacc=int(input("enter customer account:"))
            cname=str(input("enter customer name:"))
            pwd=str(input("enter customer password:"))
            amount=int(input("enter amount:"))
            lenght=len(pwd)
            if lenght>=8 and lenght<=14:
                l,u,d,s=0,0,0,0
                for i in pwd:
                    if i.islower():
                        l+=1
                    elif i.isupper():
                        u+=1
                    elif i.isdigit():
                        d+=1
                    else:
                        s+=1
                if l>=1 and u>=1 and d>=1 and s>=1:
                    cur.execute(q1,(cid,cacc,cname,pwd,amount))
                    t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                    cur.execute(t, (cacc, "deposit", amount))
                    con.commit()
                    print("Account Created Successfully")
                else:
                    print("Password must have uppercase, lowercase, digit & special character")
            else:
                print("Password is too short,it should be between 8 and 14")
        elif choice==2:
            print("Deposit Amount")
            cacc=int(input("enter customer account:"))
            pwd=str(input("enter customer password:"))
            q3="select * from cus where cacc=? and password=?"
            cur.execute(q3, (cacc,pwd))
            data=cur.fetchone()
            if data:
                print("valid username and password")
                amount = int(input("enter amount:"))
                q4="update cus set amount=amount + ? where cacc=?"
                cur.execute(q4,(amount,cacc))
                t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                cur.execute(t, (cacc, "deposit", amount))
                con.commit()
                print("amount deposited successfully")
            else:
                print("invalid username or password")
        elif choice==3:
            print("Withdraw Amount")
            cacc=int(input("enter customer account:"))
            pwd=str(input("enter customer password:"))
            q5 = "select * from cus where cacc=? and password=?"
            cur.execute(q5, (cacc, pwd))
            data = cur.fetchone()
            if data:
                a,b,c,d,e=data
                print("valid username and password")
                amount = int(input("enter amount:"))
                if amount<=e:
                    q6="update cus set amount=amount - ? where cacc=?"
                    cur.execute(q6,(amount,cacc))
                    t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                    cur.execute(t, (cacc, "withdraw", amount))
                    con.commit()
                    print("amount withdrawn successfully")
                else:
                    print("sorry!... insufficent funds")
            else:
                print("invalid username or password")
        elif choice==4:
            print("Transfer Amount")
            q7="select * from cus where cacc=? and password=?"
            cacc=int(input("enter customer(s) account:"))
            pwd=str(input("enter customer(s) password:"))
            cur.execute(q7, (cacc, pwd))
            data = cur.fetchone()
            if data:
                print("valid username and password")
                print(data)
                amount = int(input("enter amount:"))
                a,b,c,d,e=data
                if amount<=e:
                    acc=int(input("enter customer(r) account:"))
                    if cacc!=acc:
                        q8="update cus set amount=amount - ? where cacc=? and password=?"
                        t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                        cur.execute(q8, (amount, cacc, pwd))
                        cur.execute(t, (cacc, "transfer", amount))
                        q9="select * from cus where cacc=?"
                        cur.execute(q9, (acc,))
                        data=cur.fetchone()
                    else:
                        print("sender and reciever account number are same")
                    if data:
                        a,b,c,d,e=data
                        q10 = "update cus set amount=amount + ? where cacc=?"
                        cur.execute(q10, (amount, acc))
                        t = "insert into transactions(cacc, ttype, amount) values(?,?,?)"
                        cur.execute(t, (acc, "received", amount))
                        print("transaction successfully completed")
                        con.commit()
                    else:
                            print("reciver data not found")
                else:
                    print("sorry!... insufficent funds")
            else:
                print("invalid username or password")
        elif choice==5:
            print("Balance Enquiry")
            q11="select * from cus where cacc=? and password=?"
            cacc=int(input("enter customer account:"))
            pwd=str(input("enter customer password:"))
            cur.execute(q11, (cacc, pwd))
            data = cur.fetchone()
            if data:
                a,b,c,d,e=data
                print("Your Current Balance is",e)
            else:
                print("invalid username or password")
        elif choice==6:
            print("Transaction History")
            q12 = "select * from transactions where cacc=?"
            cacc = int(input("enter customer account no:"))
            cur.execute(q12, (cacc,))
            data = cur.fetchall()
            if data:
                for i in data:
                    for j in i:
                        print(j, end="\t")
                    print()
        elif choice==7:
            print("Delete Account Details")
            q13="delete from cus where cacc=? and password=?"
            cacc=int(input("enter customer account no:"))
            pwd=str(input("enter customer password:"))
            cur.execute(q13, (cacc, pwd))
            con.commit()
        elif choice==8:
            exit()
    else:
        print("invalid choice")
    ch=input("Do you want to continue?(y/n):")
con.close()
