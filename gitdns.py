'''
Title: 快速获Github网站的IP地址
Author: JackieZheng
Date: 2022-01-20 19:37:35
LastEditTime: 2022-01-22 09:14:49
LastEditors: Please set LastEditors
Description:
FilePath: \\vsTemp\\gitdns.py
'''
import os
import sys
import re
import shutil
import requests


hosts_datas=[]
git_ip = []





def getip(website:str):
    """
    # 获取IP地址
    """
    request = requests.get('https://ipaddress.com/website/'+website)
    if request.status_code == 200:
        ips=re.findall(r"<strong>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}?)</strong>",request.text)
        for ip_item in ips:
            git_ip.append(ip_item+' '+website)

getip('github.com')
getip('assets-cdn.github.com')
getip('github.global.ssl.fastly.net')


hosts_dir=r'C:\Windows\System32\drivers\etc'
orign_hosts=os.path.join(hosts_dir,'hosts')
temp_hosts=os.path.join(sys.path[0],'hosts')

# 读取原来hosts内容
with open(orign_hosts,'r',encoding='utf-8') as orign_file:
    datas = orign_file.readlines()

# 复制hosts内容
hosts_datas=datas.copy()

# 删除原来github相关内容
for data in datas:
    if 'github' in data or data=='\n':
        hosts_datas.remove(data)

# 合并生成新hosts内容
hosts_datas.extend(git_ip)

# 生成临时hosts文件
with open(temp_hosts,'w') as temp_file:
    for host in hosts_datas:
        temp_file.writelines(host+'\n')

# 打开系统hosts目录
os.system("explorer.exe %s" % hosts_dir)

try:
    # 备份 覆盖 系统hosts文件
    shutil.move(orign_hosts,orign_hosts+'.bak')
    shutil.copy(temp_hosts,orign_hosts)
    INFOR_0="hosts文件已更新成功"
    print(INFOR_0)
except:
    INFOR_1="已经生成新hosts文件："+temp_hosts
    INFOR_2="请手工复制覆盖原系统hosts文件"
    print(INFOR_1,INFOR_2,sep = '\n')

INFOR_3="修改完后继续 执行 清理DNS缓存（ipconfig/flushdns） "
print(INFOR_3)

os.system('pause')

# 刷新dns缓存
os.system('ipconfig/flushdns')

os.system('pause')
