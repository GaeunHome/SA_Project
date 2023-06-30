from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from myapp.models import member, question, transaction, product, rankinfo, LOGIN, AIwash
from django.core.exceptions import ObjectDoesNotExist
from myapp.serializers import myappSerializer
from rest_framework import viewsets
import requests
from django.utils import timezone
from datetime import datetime, timedelta

SACCngrok = 'https://10eb-1-34-54-152.jp.ngrok.io'
serverngrok = 'https://4035-114-140-152-136.jp.ngrok.io' # ngrok網址
# 登入介面
def login_view(request):
    sum = ""
    rand = LOGIN.objects.create()
    url = SACCngrok+'/RESTapiApp/Line_1/?Rbackurl='+serverngrok+'/api2/?fk='+rand.FKcheck
    req = requests.get(url, headers = {'Authorization': 'Token a875790e1ed1d791f7b8be1032ff321d3c8d1adf','ngrok-skip-browser-warning': '7414'})
    # print(req.json())
    req_read = req.json()
    # print(req_read["Rstate"])
    LOGIN.objects.filter(FKcheck=rand.FKcheck).update(Rstate=req_read["Rstate"])
    firstLogin = "https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1657781063&redirect_uri="+SACCngrok+"/LineLoginApp/callback&state="+req_read["Rstate"]+"&scope=profile%20openid%20email&promot=consent&ui_locales=zh-TW?http://example.com/?ngrok-skip-browser-warning=7414"
    return render(request, 'login.html', locals())
# 登入後得到LINEapi
def api2(request):
    if request.method == 'GET':
        fknum = request.GET.get('fk')
        nomatter = LOGIN.objects.filter(FKcheck=fknum)
        sum=''
        for i in nomatter:
            sum = i.Rstate
    url = SACCngrok+'/RESTapiApp/Line_2/?Rstate='+sum
    req = requests.get(url, headers = {'Authorization': 'Token a875790e1ed1d791f7b8be1032ff321d3c8d1adf','ngrok-skip-browser-warning': '7414'})
    req_read = req.json()
    # print(req_read)
    userUID = req_read["RuserID"]
    access_code = req_read["Raccess_code"]
    LOGIN.objects.filter(FKcheck=fknum).update(Raccesscode=req_read["Raccess_code"])
    # print(req_read["Raccess_code"])
    return login(request, userUID, access_code)
# 確定登入後會將資料匯入資料庫
def login(request, userUID, access_code):
    check = member.objects.filter(account=userUID)
    if check:
        check.update(AC_CODE=access_code)
    else:
        member.objects.create(account=userUID, name="使用者", GPOINT=100, AC_CODE=access_code)
    request.session['user'] = userUID
    return HttpResponseRedirect('/member/')
# 會員介面
def vip(request):
    if 'user' in request.session:
        account = request.session['user']
        results = member.objects.filter(account=account)
        ac_code = ''
        for result in results:
            ac_code = result.AC_CODE
        url2 = SACCngrok+'/RESTapiApp/Access/?Raccess_code='+ac_code
        req2 = requests.get(url2, headers = {'Authorization': 'Token a875790e1ed1d791f7b8be1032ff321d3c8d1adf','ngrok-skip-browser-warning': '7414'})  
        req_read2 = req2.json()
        print(type(req2.status_code))
        request.session.set_expiry(60*30)
        if (req2.status_code!=200):
            messages.error(request, '存取權已過期，請重新登入')
            return signout(request)
        else:
            pic = req_read2["sPictureUrl"]
            name = req_read2["sName"]
        rank = rankinfo.objects.all()
        unit = member.objects.get(account=account)
        if unit.GPOINT >= 50000:
            present = rankinfo.objects.get(rankname="環保大師")
        elif unit.GPOINT >= 20000:
            present = rankinfo.objects.get(rankname="環保鑽石鬥士")
            total = 50000 - unit.GPOINT
        elif unit.GPOINT >= 10000:
            present = rankinfo.objects.get(rankname="環保白金鬥士")
            total = 20000 - unit.GPOINT
        else:
            present = rankinfo.objects.get(rankname="環保黃金鬥士")
            total = 10000 - unit.GPOINT
        return render(request, 'member.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 登出
def signout(request):
    del request.session['user']
    messages.success(request, "您已登出")
    return HttpResponseRedirect('/')
# 碳權存摺 # transations
def passbook(request):
    if 'user' in request.session:
        account = request.session['user']
        unit = member.objects.get(account=account)
        passbook = transaction.objects.filter(MEMID=account)
        return render(request, 'passbook.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 碳權點數商城
def productlist(request):
    if 'user' in request.session:
        account = request.session['user']
        products = product.objects.all()
        return render(request, 'shoppingmall.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 「食」頁面
def daily(request):
    if 'user' in request.session:
        account = request.session['user']
        pro = product.objects.filter(productkind="食")
        return render(request, 'dailylife.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 「行」頁面
def travel(request):
    if 'user' in request.session:
        account = request.session['user']
        pro = product.objects.filter(productkind="行")
        return render(request, 'travel.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 碳權點數商品
def products(request):
    if request.method == 'POST':
        if 'user' in request.session:
            account = request.session['user']
            mem = member.objects.get(account=account)
            productnum = request.POST.get('go')
            products = product.objects.get(productID=productnum)
            if mem.GPOINT < products.productlimit:
                messages.error(request, "您的段位未到達，請努力累積碳權點數")
                return redirect('/productlist/')
            else:
                return render(request, 'commodity.html', locals())
        else:
            messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 問題回報
def report(request):
    if 'user' in request.session:
        account = request.session['user']
        if request.method == 'GET':
            return render(request, 'question.html')
        elif request.method == 'POST':
            content = request.POST.get('content')
            question.objects.create(account=account, question=content)
            messages.success(request, "已將您的問題回報了！會儘速解決您的問題")
            return render(request, 'question.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 購買 # transation
def buy(request):
    if 'user' in request.session:
        account = request.session['user']
        if request.method == 'GET':
            return render(request, 'Redemption.html')
        elif request.method == 'POST':
            pro = product.objects.get(productID=request.POST.get('pro'))
            info = member.objects.get(account=account)
            number = int(request.POST.get('number'))
            if (info.GPOINT - pro.productpoint*number) < 0:
                messages.error(request, "對不起！您的碳權點數不夠買該商品")
                return HttpResponseRedirect('/productlist/')
            total = info.GPOINT - pro.productpoint*number
            member.objects.filter(account=account).update(GPOINT=total)
            transaction.objects.create(
                PROID=pro.productID, MEMO=pro.productname+"兌換", PRONAME=pro.productname,
                MEMID=account, CDATE=timezone.now().strftime("%Y-%m-%d% %H:%M"), GPOINT=pro.productpoint*number, 
                AMOUNT=0, TIME=number, BALANCE=total, APPID=10, state="可使用")
            messages.success(request, "兌換成功！！")
            return HttpResponseRedirect('/productlist/')
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 兌換條碼 
def qrcodes(request):
    if 'user' in request.session:
        account = request.session['user']
        qr = transaction.objects.filter(MEMID=account)
        pro = product.objects.all()
        return render(request, 'voucher.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
def change(request):
    if 'user' in request.session:
        account = request.session['user']
        if request.method == 'POST':
            change = request.POST.get('to')
            transaction.objects.filter(ORDID=change).update(state="使用中")
            return HttpResponseRedirect('/qrcode/')
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
def doing(request):
    if 'user' in request.session:
        account = request.session['user']
        if request.method == 'POST':
            change = request.POST.get('to2')
            transaction.objects.filter(ORDID=change).update(state="正在使用中")
            return HttpResponseRedirect('/qrcode/')
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
def end(request):
    if 'user' in request.session:
        account = request.session['user']
        if request.method == 'POST':
            change = request.POST.get('to3')
            transaction.objects.filter(ORDID=change).update(state="結束")
            return HttpResponseRedirect('/qrcode/')
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
def check(request):
    if 'user' in request.session:
        account = request.session['user']
        if request.method == 'POST':
            unit = transaction.objects.get(MEMID=account, ORDID=request.POST.get('to4'), state="正在使用中")
            time = 3600*unit.TIME
            hour, remainder = divmod(time, 3600)
            minute, second = divmod(remainder, 60)
            return render(request, 'test.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 修改會員資料介面
def memberset(request):
    if 'user' in request.session:
        account = request.session['user']
        mem = member.objects.get(account=account)
        return render(request, 'memberset.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 修改會員資料
def modify(request):
    if 'user' in request.session:
        account = request.session['user']
        mem = member.objects.filter(account=account)
        if request.method == 'POST':
            mem.update(name=request.POST.get('name'))
            messages.success(request, "修改成功")
        return HttpResponseRedirect('/memberset/')
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 排位詳細介面
def ranklist(request):
    if 'user' in request.session:
        account = request.session['user']
        mem = member.objects.get(account=account)
        results = member.objects.filter(account=account)
        ac_code = ''
        for result in results:
            ac_code = result.AC_CODE
        url2 = SACCngrok+'/RESTapiApp/Access/?Raccess_code='+ac_code
        req2 = requests.get(url2, headers = {'Authorization': 'Token a875790e1ed1d791f7b8be1032ff321d3c8d1adf','ngrok-skip-browser-warning': '7414'})  
        req_read2 = req2.json()
        print(type(req2.status_code))
        request.session.set_expiry(60*30) # 存在30分鐘
        if (req2.status_code!=200):
            messages.error(request, '存取權已過期，請重新登入')
            return signout(request)
        else:
            pic = req_read2["sPictureUrl"]
            name = req_read2["sName"]
        rank = rankinfo.objects.all()
        if mem.GPOINT >= 50000:
            present = rankinfo.objects.get(rankname="環保大師")
        elif mem.GPOINT >= 20000:
            present = rankinfo.objects.get(rankname="環保鑽石鬥士")
        elif mem.GPOINT >= 10000:
            present = rankinfo.objects.get(rankname="環保白金鬥士")
        else:
            present = rankinfo.objects.get(rankname="環保黃金鬥士")
        return render(request, 'leaderboard.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 對接頁面
def service(request):
    if 'user' in request.session:
        account = request.session['user']
        return render(request, 'service.html', locals())
    else:
        messages.error(request, "您還未登入！！")
        return HttpResponseRedirect('/')
# 對接測試(傳值)
class myappViewSet(viewsets.ModelViewSet):
    queryset = AIwash.objects.all()
    serializer_class = myappSerializer
'''
# 之前的登入註冊
def register(request):
    return render(request, 'register.html')
# 登入已完成優化
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    elif request.method == 'POST':
        account = request.POST.get('username')
        password = request.POST.get('password')
        try:
            unit = member.objects.get(account=account)
            if unit.password==password:
                request.session['account'] = unit.account
                return HttpResponseRedirect('/member/')
            else:
                messages.error(request, "密碼錯誤")
                return render(request, 'signin.html', locals())
        except ObjectDoesNotExist:
            messages.error(request, "帳號不存在")
            return render(request, 'signin.html', locals())
# 註冊已完成優化
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        uaccount = request.POST.get('account')
        check_account = member.objects.filter(account=uaccount).first()
        if check_account!= None:
            messages.error(request, "此帳號已被註冊過")
            return render(request, 'signup.html', locals())
        upassword = request.POST.get('password')
        upassword2 = request.POST.get('password2')
        uphone = request.POST.get('phone')
        uemail = request.POST.get('email')
        uname = request.POST.get('name')
        if upassword!=upassword2:
            messages.error(request, "兩次密碼不正確")
            return render(request, 'signup.html', locals())
        member.objects.create(account=uaccount, password=upassword, phone=uphone, email=uemail, name=uname, GPOINT=0)
        messages.success(request, "恭喜！註冊成功")
        return HttpResponseRedirect('/signin/')
# 索取個資
def access(request, pic):
    results = member.objects.filter(account=request.session['user'])
    ac_code = ''
    for result in results:
        ac_code = result.AC_CODE
    url2 = SACCngrok+'/RESTapiApp/Access/?Raccess_code='+ac_code
    req2 = requests.get(url2, headers = {'Authorization': 'Token a875790e1ed1d791f7b8be1032ff321d3c8d1adf','ngrok-skip-browser-warning': '7414'})  
    req_read2 = req2.json()
    print(type(req2.status_code))
    if (req2.status_code!=200):
        messages.error(request, '存取權已過期，請重新登入')
        return signout(request)
    else:
        pic = req_read2["sPictureUrl"]
        print(pic)
        return vip(request, pic)
# 手機驗證 # 未完成
def api3(request):
    rand = LOGIN.objects.create()
    url3 = SACCngrok+'/RESTapiApp/SMS_1/?Rphone='+request.POST.get('cellphone')
    req3 = requests.get(url3, headers = {'Authorization': 'Token a875790e1ed1d791f7b8be1032ff321d3c8d1adf','ngrok-skip-browser-warning': '7414'})
    print(req3.json())
    req3_read = req3.json()
    RSMSid = req3_read["RSMSid"]
    print(req3_read["RSMSid"])
    return login(RSMSid)
'''