from django.shortcuts import render,HttpResponse,redirect
import json
from repository import models
from api.assets import disk
import hashlib
from autoserver import settings
import time
from django.http import JsonResponse
# Create your views here.
api_key_record={}
from Crypto.Cipher import AES
def decrypt(msg):
    key = settings.DATA_KEY
    cipher=AES.new(key,AES.MODE_CBC,key)
    result=cipher.decrypt(msg)
    data=result[0:-result[-1]]  #去除填充的数据
    return str(data,encoding='utf-8')

def asset(request):

    client_md5_time_key = request.META.get('HTTP_OPENKEY')
    print(client_md5_time_key)
    client_md5_key, client_ctime = client_md5_time_key.split('|')
    client_ctime = float(client_ctime)
    server_time = time.time()

    # 第一关
    if server_time - client_ctime > 10:
        return HttpResponse('【第一关】验证超时')
    # 第二关
    temp = "%s|%s" % (settings.AUTH_KEY, client_ctime,)
    m = hashlib.md5()
    m.update(bytes(temp, encoding='utf-8'))
    server_md5_key = m.hexdigest()
    if server_md5_key != client_md5_key:
        return HttpResponse('【第二关】验证失败')

    for k in list(api_key_record.keys()):
        v = api_key_record[k]
        if server_time > v:
            del api_key_record[k]

    # 第三关:
    if client_md5_time_key in api_key_record:
        return HttpResponse('【第三关】有人已经来过了...')
    else:
        api_key_record[client_md5_time_key] = client_ctime + 10

    if server_md5_key != client_md5_key:
        return HttpResponse('认证失败...')
    if request.method == 'GET':
        ys = '重要的不能被闲杂人等看的数据'
        return HttpResponse(ys)
    elif request.method=="POST":
        # server_info = json.loads(request.body.decode("utf-8"))
        server_info = json.loads(decrypt(request.body))
        print('start',server_info)
        disk_obj=disk.Disk_views(models,server_info)
        disk_obj.main_program()
    return HttpResponse("...")

def servers(request):
    if request.method=='GET':
        v=models.Server.objects.values('id','hostname')
        server_list=list(v)
        return JsonResponse(server_list,safe=False)  #默认传字典就不需要safe参数
    elif request.method=='POST':
        return JsonResponse(status=201)

def servers_detail(request,nid):
    if request.method=='GET':
        obj=models.Server.objects.filter(id=nid).first()
        return HttpResponse("...")
    elif request.method=='DELETE':
        models.Server.objects.filter(id=nid).delete()
        return HttpResponse()
    elif request.method=='PUT':
        print(request.body)
        models.Server.objects.filter(id=nid).update()

# from rest_framework import serializers
#
# class ServerSerialiter(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model=models.Server
#        fields=('id','asset_id','hostname','sn')
#        # exclude=('ug',)
#        depth=1  #大于等于0小于等于10。0代表自己
#
# from rest_framework import viewsets
# class ServerViewSet(viewsets.ModelViewSet):
#     queryset=models.Server.objects.all().order_by("-id")
#     serializer_class=ServerSerialiter
from rest_framework.views import APIView
from django.views import View
from django.core import serializers
from . import serializers
from rest_framework.parsers import JSONParser
class ServerView(APIView):
    def get(self,request,*args,**kwargs):
        """获取数据"""
        data_list=models.UserProfile.objects.all()
        # data=serializers.serialize("json",data_list)
        #序列化 + from验证
        serializer=serializers.MySerializer(instance=data_list,many=True) #many表示列表。数据很多的时候
        # return HttpResponse(json.dumps(serializer.data))
        return JsonResponse(serializer.data,safe=False)


    def post(self, request, *args, **kwargs):
        """创建数据"""
        # print(request.data) #request._request.body 也可以取到值
        # models.UserProfile.objects.create(**request.data)
        data = JSONParser().parse(request)
        serializer = serializers.MySerializer(data=data) #序列化form验证
        if serializer.is_valid():
            serializer.save()
        return HttpResponse("...")

class ServerDetail(APIView):
    def get(self, request,nid):
        """获取单条数据"""
        obj=models.UserProfile.objects.filter(id=nid).first()
        serializer = serializers.MySerializer(instance=obj)
        return JsonResponse(serializer.data)


    def delete(self, request,nid):
        """删除数据"""
        obj = models.UserProfile.objects.filter(id=nid).delete()
        return HttpResponse(status=204)

    def put(self, request, nid):
        """更新数据"""
        obj = models.UserProfile.objects.filter(id=nid).first()
        data = JSONParser().parse(request) #获取数据
        serializer = serializers.MySerializer(instance=obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=200)



