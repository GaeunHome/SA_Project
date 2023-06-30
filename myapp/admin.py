from django.contrib import admin
from myapp.models import member, question, transaction, product, rankinfo, LOGIN, AIwash

class userAdmin(admin.ModelAdmin):
    list_display=('account', 'name', 'GPOINT','AC_CODE')
# Register your models here.
admin.site.register(member, userAdmin)

class questionAdmin(admin.ModelAdmin):
    list_display=('account','question')
admin.site.register(question, questionAdmin)

class transactionAdmin(admin.ModelAdmin):
    list_display=('ORDID','PROID','MEMO','MEMID','CDATE','GPOINT','AMOUNT','APPID')
admin.site.register(transaction, transactionAdmin)

class productAdmin(admin.ModelAdmin):
    list_display=('productID','productname','productimage1','productpoint','productlimit','productkind')
admin.site.register(product, productAdmin)

class rankAdmin(admin.ModelAdmin):
    list_display=('rankname','rankengname','rankimg','rankpoint')
admin.site.register(rankinfo, rankAdmin)

class loginAdmin(admin.ModelAdmin):
    list_display=('FKcheck', 'Rstate', 'Raccesscode')
admin.site.register(LOGIN, loginAdmin)

class AIwashAdmin(admin.ModelAdmin):
    list_display=('MEM', 'GPOINT')
admin.site.register(AIwash, AIwashAdmin)
'''
class CountdownAdmin(admin.ModelAdmin):
    list_display=('ORD', 'start_time','end_time','time_elapsed','overtime')
admin.site.register(Countdown, CountdownAdmin)
'''