#!/usr/bin/env python
#encoding:utf-8
from django.shortcuts import render,HttpResponse,redirect
class Disk_views():
    def __init__(self,models,server_info):
        self.models=models
        self.server_info=server_info
    def main_program(self):
        # 新资产信息

        # print(server_info)
        hostname = self.server_info['basic']['data']['hostname']

        # 找到服务器的基本信息(单条)，资产表中以前的信息
        server_obj = self.models.Server.objects.filter(hostname=hostname).first()

        if not server_obj:
            return HttpResponse("当前主机名在资产中未录入")

        # 处理硬盘信息
        if not self.server_info['disk']['status']:
            self.models.ErrorLog.objects.create(content=self.server_info['disk']['data'], asset_obj=server_obj.asset,
                                           title='[%s]硬盘采集错误信息' % hostname)
        new_disk_dict = self.server_info['disk']['data']

        # 硬盘信息
        # disk_list=server_obj.disk.all()
        # 或者
        old_disk_list =self.models.Disk.objects.filter(server_obj=server_obj)
        new_slot_list = list(new_disk_dict.keys())
        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        # 交集 更新
        record_list = []
        row_map = {'capacity': '容量', 'pd_type': '类型', 'model': '型号'}
        update_list = set(new_slot_list).intersection(old_slot_list)
        for slot in update_list:
            new_dist_row = new_disk_dict[slot]
            old_disk_row = self.models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()
            for k, v in new_dist_row.items():
                value = getattr(old_disk_row, k)
                if v != value:
                    record_list.append("槽位%s,%s由%s变更为%s" % (slot, row_map[k], value, v))
                    setattr(old_disk_row, k, v)
            old_disk_row.save()
        if record_list:
            content = ";".join(record_list)
            self.models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)  # 处理

        # 差集 创建
        create_list = set(new_slot_list).difference(old_slot_list)
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot]
            disk_dict['server_obj'] = server_obj
            self.models.Disk.objects.create(**disk_dict)
            temp = "新增硬盘:位置[slot],容量[capacity],型号[model],类型[pd_type]".format(**disk_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            self.models.AssetRecord.objects.filter(asset_obj=server_obj.asset, content=content)  # 处理

        # 差集 删除
        del_list = set(old_slot_list).difference(new_slot_list)
        if del_list:
            self.models.Disk.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
            self.models.AssetRecord.objects.create(asset_obj=server_obj.asset,
                                              content="移除硬盘:%s" % (",".join(del_list),))  # 处理


