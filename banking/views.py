from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
from django.http import HttpResponse
import random
from django.core.mail import send_mail
import time

from .models import Bank,Transaction

# Create your views here.
def test_email(request):
    send_mail(
        'Test Email',
        'Hello from Django project!',
        'kumarvamshi1832@gmail.com',
        ['your_other_email@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent")

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        data = request.session.get('user_data')

        if not data:
            return render(request, 'verify_otp.html', {
                'error': "Session expired. Please register again."
            })

        otp_time = request.session.get('otp_time')
        if not otp_time or time.time() - otp_time > 300:
            return render(request, 'verify_otp.html', {
                'error': "OTP expired. Please register again."
            })

        if entered_otp == session_otp:
            Bank.objects.create(
                cid=data['cid'],
                cname=data['cname'],
                accountnumber=data['accountnumber'],
                email=data['email'],
                phoneno=data['phoneno'],
                password=make_password(data['password']),
                address=data['address'],
                dob=data['dob'],
                balance=data['balance']
            )
            request.session.flush()
            return render(request, 'accountcreate.html', {
                'msg': "Account created successfully"
            })
        else:
            return render(request, 'verify_otp.html', {
                'error': "Invalid OTP"
            })
    return render(request, 'verify_otp.html')

def home(request):
    return render(request, 'home.html')
def user_login(request):
    if request.method == "POST":
        a = request.POST.get("cid")
        b = request.POST.get("pwd")
        user = Bank.objects.filter(cid=a).first()
        if user and check_password(b, user.password):
            request.session['user'] = a
            return redirect('welcome')
        else:
            return render(request, 'user_login.html', {'msg': "Wrong password or ID"})
    return render(request, 'user_login.html')

def generate_otp():
    return str(random.randint(100000, 999999))

def accountcreate(request):
    if request.method == 'POST':
        a = request.POST.get('cid')
        b = request.POST.get('cname')
        c = request.POST.get('cacc')
        d = request.POST.get('cemail')
        e = request.POST.get('cphone')
        f = request.POST.get('pwd')
        g = request.POST.get('cadd')
        h = request.POST.get('cdob')
        i = request.POST.get('cbal')
        if Bank.objects.filter(accountnumber=c).exists():
            return render(request, 'accountcreate.html', {'msg': "account already exist"})

        otp = generate_otp()

        request.session['otp'] = otp
        request.session['otp_time'] = time.time()
        request.session['user_data'] = {
            'cid': a,
            'cname': b,
            'accountnumber': c,
            'email': d,
            'phoneno': e,
            'password': f,
            'address': g,
            'dob': h,
            'balance': i
        }

        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            'kumarvamshi1832@gmail.com',
            [d],
            fail_silently=False,
        )

        return redirect('verify_otp')

    return render(request, 'accountcreate.html')

def welcome(request):
    a = request.session.get('user')

    if not a:
        return redirect('login')

    res = Bank.objects.get(cid=a)

    return render(request, 'welcome.html', {
        'uname': res.cname
    })
def depositamount(request):
        if request.method == 'POST':
            a = request.session.get('user')
            if not a:
                return redirect('login')
            res=Bank.objects.filter(cid=a).first()
            if res:
                amount=int(request.POST.get('amount'))
                if (amount)>0:
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
        a=request.session.get('user')
        if not a:
            return redirect('login')
        res = Bank.objects.filter(cid=a).first()
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
        a = request.session.get('user')
        if not a:
            return redirect('login')
        sender=Bank.objects.filter(cid=a).first()
        b = request.POST.get('rac')
        if sender:
            if sender.accountnumber == b:
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

def balancecheck(request):
        a = request.session.get('user')
        if not a:
            return redirect('login')
        res=Bank.objects.filter(cid=a).first()
        return render(request,'balancecheck.html',{'e1': res})

def transactionhistory(request):
            a = request.session.get('user')

            if not a:
                return redirect('login')

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

def deleteaccount(request):
    if request.method == 'POST':
        cid = request.session.get('user')
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