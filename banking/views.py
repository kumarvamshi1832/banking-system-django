from django.shortcuts import render
from django.db import transaction
from django.template.context_processors import request
from django.db.models import Q
from django.shortcuts import redirect


from .models import Bank,Transaction

# Create your views here.
def home(request):
    return render(request, 'home.html')
def user_login(request):
    if request.method == "POST":
        a = request.POST.get("cid")
        b = request.POST.get("pwd")
        user = Bank.objects.filter(cid=a).first()
        if user and user.password == b:
            request.session['user'] = a
            return redirect('welcome')
        else:
            return render(request, 'user_login.html', {'msg': "Wrong password or ID"})
    return render(request, 'user_login.html')
def accountcreate(request):
    if request.method=='POST':
        a=request.POST.get('cid')
        b=request.POST.get('cname')
        c=request.POST.get('cacc')
        d=request.POST.get('cemail')
        e=request.POST.get('cphone')
        f=(request.POST.get('pwd'))
        g=request.POST.get('cadd')
        h=request.POST.get('cdob')
        i=request.POST.get('cbal')

        if Bank.objects.filter(accountnumber=c).exists():
            return render(request, 'accountcreate.html',{'msg':"account already exist"})
        if Bank.objects.filter(email=d).exists():
            return render(request, 'accountcreate.html',{'msg':"email already exist"})

        res=Bank(cid=a,cname=b,accountnumber=c,email=d,phoneno=e,password=f,address=g,dob=h,balance=i)
        res.save()
        return render(request,'accountcreate.html',{'msg':"account created successfully"})
    return render(request, 'accountcreate.html')

def welcome(request):
    cid = request.session.get('user')

    if not cid:
        return redirect('login')

    u = Bank.objects.get(cid=cid)

    return render(request, 'welcome.html', {
        'uname': u.cname
    })
def depositamount(request):
        if request.method == 'POST':
            cid = request.POST.get('cid')
            res=Bank.objects.filter(cid=cid).first()
            if res:
                amount=int(request.POST.get('amount'))
                if int(amount)>0:
                    res.balance=res.balance+amount
                    res.save()
                    Transaction.objects.create(from_account=res,to_account=res,amount=amount,transaction_type='deposit')
                    return render(request,'depositamount.html',{'e1': res,
                                                           'msg':'amount deposited sucessfully'})
                else:
                    return render(request,'depositamount.html',{'msg':'transaction failed check amount you entered'})
            else:
                return render(request,'depositamount.html',{'msg':'no such account'})

        return render(request, 'depositamount.html')

def withdrawamount(request):
    if request.method == 'POST':
        a=request.POST.get('cid')
        res=Bank.objects.filter(cid=a).first()
        if res:
            amount=request.POST.get('amount')
            amount=int(amount)
            if amount>0 and res.balance>=amount:
                res.balance=res.balance-amount
                res.save()
                Transaction.objects.create(from_account=res,to_account=res,amount=amount,transaction_type='withdraw')
                return render(request,'withdrawamount.html',{'e1': res,
                                                             'msg':'amount withdrawn sucessfully'})
            else:
                return render(request,'withdrawamount.html',{'msg':'Insufficient balance or invalid amount'})
        else:
            return render(request,'withdrawamount.html',{'msg':'no such account found'})
    return render(request, 'withdrawamount.html')
def transferamount(request):
    if request.method == 'POST':
        a=request.POST.get('cacc')
        b = request.POST.get('rac')
        sender=Bank.objects.filter(accountnumber=a).first()
        if sender:
            if a == b:
                return render(request, 'transferamount.html', {'msg': 'Cannot transfer to same account'})
            receiver=Bank.objects.filter(accountnumber=b).first()
            if receiver:
                amount=request.POST.get('amount')
                amount=int(amount)
                if amount>0 and sender.balance>=amount:
                    with transaction.atomic():
                        sender.balance -= amount
                        receiver.balance += amount
                        sender.save()
                        receiver.save()
                        Transaction.objects.create(from_account=sender,to_account=receiver,amount=amount,transaction_type='debit')
                        Transaction.objects.create(from_account=receiver,to_account=sender ,amount=amount,transaction_type='credit')

                        return render(request,'transferamount.html',
                                                     {'e1': sender,
                                                             'e2': receiver,
                                                          'msg':'amount transfered sucessfully'})
                else:
                    return render(request,'transferamount.html',{'msg':'check the number you entered'})
            else:
                return render(request,'transferamount.html',{'msg':'no such account found(r)'})
        else:
            return render(request,'transferamount.html',{'msg':'no such account found(s)'})
    else:
        return render(request,'transferamount.html')




    return render(request, 'transferamount.html')
def balancecheck(request):
    if request.method == 'POST':
        a=request.POST.get('cid')
        res=Bank.objects.filter(cid=a).first()
        return render(request,'balancecheck.html',{'e1': res})
    return render(request,'balancecheck.html')

def transactionhistory(request):
        if request.method == 'POST':
            a = request.POST.get('cid')
            res = Bank.objects.filter(cid=a).first()
            if res:
                transactions = Transaction.objects.filter(
                    from_account=res
                ).order_by('-created_at')
                return render(request, 'transactionhistory.html', {
                    'e1': res,
                    'data': transactions
                })
            else:
                return render(request, 'transactionhistory.html', {'msg': 'no such account'})
        return render(request, 'transactionhistory.html')
def deleteaccount(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        res = Bank.objects.filter(cid=cid).first()
        if res:
            res.delete()
            return render(request, 'deleteaccount.html', {
                'msg': 'Account deleted successfully'
            })
        else:
            return render(request, 'deleteaccount.html', {
                'msg': 'No such account'
            })
    return render(request, 'deleteaccount.html')