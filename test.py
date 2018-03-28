# # #!/usr/bin/env python
# # #encoding:utf-8
# # import requests
# # requests.post(url='http://127.0.0.1:8000/api/servers/',json={'name':'alex','email':'alex@qq.com'})
# data=[3	,
# 18	,
# 17	,
# 16	,
# 8	,
# 9	,
# 8	,
# 11	,
# 17	,
# 9	,
# 16	,
# 6	,
# 7	,
# 7	,
# 8	,
# 7	,
# 6	,
# 4	,
# 4	,
# 5	,
# 10	,
# 10	,
# 12	,
# 15	,
# 1181,
# 754	,
# 672	,
# 985	,
# 888	,
# 993	,
# 693	,
# 969	,
# 807	,
# 481	,
# 788	,
# 646	,
# 894	,
# 856	,
# 1340,
# 765	,
# 617	,
# 840	,
# 617	,
# 993	,
# 628	,
# 124	,
# 94	,
# 95	,
# 90	,
# 88	,
# 150	,
# 191	,
# 960	,
# 660	,
# 761	,
# 830	,
# 711	,
# 1077,
# 662	,
# 988	,
# 686	,
# 673	,
# 1295,
# 918	,
# 1336,
# 956	,
# 1218,
# 1039,
# 701	,
# 1196,
# 929	,
# 1202,
# 781	,
# 1342,
# 870	,
# 754	,
# 1175,
# 2214,
# 1659,
# 1145,
# 1361,
# 1027,
# 781	,
# 1147,
#
# ]
# l=[]
# num=6
# index=0
# sun=0
# for i in data:
#     sun+=i
#     index+=1
#     if index>num:
#         l.append(sun)
#         index =0
#         sun=0
# print(l)
# #
#
#
#
# data=[1,1,4,1,2,23,2]
# nums=[1,1,4,1,2,23,2]
# class Solution:
#     def twoSum(self,nums,target):
#         l = []
#         count = len(nums)
#         for i in range(0, count):
#             for j in range(i + 1, count):
#                 if nums[i] + nums[j] == target:
#                     l.append(i)
#                     l.append(j)
#                     return l
#
#
# a=Solution()
# print(a.twoSum(nums,27))
# # #
# nums=[1,1,4,1,2,23,]
#
# target=2
# index=0
# l=[]
# count=len(nums)
# for i in range(0,count):
#     for j in range(i+1,count):
#         if nums[i]+nums[j]==target:
#             l.append(i)
#             l.append(j)
#             # l.append(i+1)
#             break

#
#
# print(l)
# #
# #
#
S = [-1,0,1,2,-1,-4]
class Solution:
    def threeSum(self, nums):
        d1 = {}
        count = len(nums)
        for i in range(0, count):
            for j in range(i + 1, count):
                for k in range(j + 1, count):
                    if nums[i] + nums[j] + nums[k] == 0:
                        l1 = (nums[i], nums[j], nums[k])
                        d1[tuple(sorted(l1))] = 1

        return [list(z) for z in d1]
a = Solution()
print(a.threeSum(S))
