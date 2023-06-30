from django.db import models
import uuid

def UUIDrand():
    return str(uuid.uuid4())

class LOGIN(models.Model):
    FKcheck = models.CharField(max_length=36,default=UUIDrand)
    Rstate = models.CharField(max_length=42)
    Raccesscode = models.CharField(max_length=43)

class member(models.Model):
    account = models.CharField(primary_key=True, max_length=43, null=False)
    name = models.CharField(max_length=10, null=True)
    GPOINT = models.IntegerField()
    AC_CODE = models.CharField(max_length=43, null=True)
    def __str__(self):
        return self.account

class question(models.Model):
    account = models.CharField(max_length=100)
    question = models.CharField(max_length=500)
    def __str__(self):
        return self.account

class transaction(models.Model):
    ORDID = models.AutoField(primary_key=True, null=False)
    PROID = models.CharField(max_length=20, null=True)
    PRONAME = models.CharField(max_length=20, null=True)
    MEMO = models.CharField(max_length=20, null=True)
    MEMID = models.CharField(max_length=43, null=False)
    CDATE = models.CharField(max_length=43, null=True)
    GPOINT = models.IntegerField()
    BALANCE = models.IntegerField() # 此欄位要記得從member的GPOINT做更新
    AMOUNT = models.IntegerField(null=True)
    TIME = models.IntegerField(null=True)
    APPID = models.IntegerField() # 智慧喜組別
    state = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.MEMID
'''
class Countdown(models.Model):
    ORD = models.CharField(max_length=20)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    time_elapsed = models.IntegerField(null=True)
    overtime = models.IntegerField(null=True)
    def __str__(self):
        return self.ORD
'''
class product(models.Model):
    productID = models.AutoField(primary_key=True)
    productname = models.CharField(max_length=20, null=False)
    productimage1 = models.CharField(max_length=50, null=False)
    productpoint = models.IntegerField()
    productlimit = models.IntegerField()
    productkind = models.CharField(max_length=20)
    def __str__(self):
        return self.productname

class rankinfo(models.Model):
    rankname = models.CharField(max_length=20, null=False)
    rankengname = models.CharField(max_length=30, null=False)
    rankimg = models.CharField(max_length=20, null=False)
    rankpoint = models.IntegerField()
    def __str__(self):
        return self.rankname

class AIwash(models.Model):
    ORDID = models.CharField(max_length=20)
    MEM = models.CharField(max_length=100)
    APPID = models.CharField(max_length=20)
    TAX = models.IntegerField(null=True)
    GPOINT = models.IntegerField(null=False)
    TOTALMONEY = models.IntegerField()
    CDATE = models.CharField(max_length=40)
    def __str__(self):
        return self.MEM
    def save(self, *args, **kwargs):
        info = member.objects.get(account=self.MEM)
        info.GPOINT = info.GPOINT + self.GPOINT
        info.save()
        super().save(*args, **kwargs)
        print(self.MEM)

        transaction.objects.create(
            MEMID=self.MEM, GPOINT=self.GPOINT, CDATE=self.CDATE,
            BALANCE=info.GPOINT, APPID=self.APPID,
            MEMO="第"+self.APPID+"組智慧喜")
        
    class Meta:
        db_table = "AIwash"