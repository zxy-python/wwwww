from django.shortcuts import render,HttpResponse
from repository import models
# Create your views here.
def curd(request):

    return render(request,'curd.html')
def get_data_list(request,modele_cls,table_config):
    values_list = []

    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    from django.db.models import Q

    condition = request.GET.get('condition')  # 获取前端发送过来的搜索条件
    condition_dict = json.loads(condition)
    con = Q()
    for name, values in condition_dict.items():
        ele = Q()
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name, item))
        con.add(ele, 'AND')

    server_list = modele_cls.objects.filter(con).values(*values_list)
    return server_list

#json扩展，让他支持序列化时间类型
import json
from datetime import date
from datetime import datetime
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)

from django.core import serializers
def curd_json(request):
    # v=models.Server.objects.all()
    # #序列化操作
    # data=serializers.serialize("json",v) #序列化对象

    # v = models.Server.objects.values("id", "hostname")
    # data=json.dumps(list(v))  #json不可以序列化时间

    #序列化时间
    # v = models.Server.objects.values("id","hostname",'create_at')
    # data = json.dumps(list(v),cls=JsonCustomEncoder)
    # return HttpResponse(data)
    if request.method=='DELETE':
        id_list=json.loads(str(request.body,encoding='utf-8'))
        #删除主机数据。。
        print(id_list)
        return HttpResponse("...")
    elif request.method == "PUT":
        all_list = json.loads(str(request.body, encoding='utf-8'))
        print(all_list)
        return HttpResponse('...')
    elif request.method=="POST":
        pass
    elif request.method=="GET":
        from backend.page_config import curd as curdConfig
        server_list=get_data_list(request,models.Server,curdConfig.table_config)
        ret={
            'server_list':list(server_list),
            'table_config':curdConfig.table_config,
            'search_config':curdConfig.search_config,
            'global_dict': {
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices,
                'idc_choices': list(models.IDC.objects.values_list('id', 'name')),
            }
             }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))

def asset(request):
    return render(request,'asset.html')

def asset_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body, encoding='utf-8'))
        # 删除主机数据。。。
        print(id_list)
        return HttpResponse("...")
    elif request.method == "PUT":
        all_list = json.loads(str(request.body, encoding='utf-8'))
        for row in all_list:
            nid=row.pop('id')
            models.Asset.objects.filter(id=nid).update(**row)
        return HttpResponse('...')
    elif request.method == "POST":
        pass
    elif request.method == "GET":
        from backend.page_config import asset as  assetConfig
        server_list = get_data_list(request,models.Asset,assetConfig.table_config)

        ret = {
            'server_list': list(server_list),
            'table_config': assetConfig.table_config,
            'search_config': assetConfig.search_config,
            'global_dict':{
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices,
                'idc_choices': list(models.IDC.objects.values_list('id','name')),
            },
        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))

def idc(request):
    return render(request, 'idc.html')

def idc_json(request):
    if request.method=='DELETE': #删除
        id_list=json.loads(str(request.body,encoding='utf-8'))
        #删除主机数据。。。
        print(id_list)
        return HttpResponse("...")
    elif request.method == "PUT": #更新
        all_list = json.loads(str(request.body, encoding='utf-8'))
        print(all_list)
        return HttpResponse('...')
    elif request.method=="POST":
        pass
    elif request.method=="GET":
        from backend.page_config import idc

        values_list = []
        for row in idc.table_config:
            if not row['q']:
                continue
            values_list.append(row['q'])

        server_list = models.IDC.objects.values(*values_list)

        ret = {
            'server_list': list(server_list),
            'table_config': idc.table_config,
            'global_dict': {}

        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def chart(request):
    return render(request,'chart.html')