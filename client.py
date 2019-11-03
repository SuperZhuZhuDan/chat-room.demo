#!/usr/bin/env python3
#coding=utf-8
from socket import *
import sys,os

#退出程序
def do_quit(s,SADDR,name):
    qname='Q%s'%name
    s.sendto(qname.encode(),SADDR)
#注册用户
def regist(s,SADDR):
    while True:
        #输入登录人信息
        name=input("请输入登录人姓名或输入回车退出：")
        #如果输入回车则退出
        if not name:
            os._exit(2)
            print('退出程序')
            break
        elif ' ' in list(name):
            print('用户名不能含有空格')
            continue
        #添加判断
        Lname='L'+name
        s.sendto(Lname.encode(),SADDR)
        data,addr=s.recvfrom(1024)
        if data.decode()=='OK':
            print('你已进入聊天室(输入##退出程序)')
            return name
        else:
            print(data.decode())
    return 0


#收消息
def do_recv(s):
    while True:
        data,addr=s.recvfrom(1024)
        if data=='Exit':
            sys.exit(0)
        print(addr,':\n',data.decode())


#发消息
def do_send(s,SADDR,name):
    while True:
        say=input()
        #判断退出
        if say == '##':
            do_quit(s,SADDR,name)
            sys.exit('退出程序')
        else:
            sayn='%s ：%s'%(name,say)
            csay='C'+sayn
            if len(csay.encode())>1024:
                print('请输入1024字节以内的消息')
                continue
            s.sendto(csay.encode(),SADDR)


def main():
    s=socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,\
        SO_REUSEADDR,1)
    #server address
    SADDR=('192.168.1.8',8888)
    try:
        name=regist(s,SADDR)
        if not name:
            s.close()
        #聊天
        pid=os.fork()
        if pid<0:
            print('创建进程失败')
        elif pid==0:
            do_recv(s)
        else:
            do_send(s,SADDR,name)
    except KeyboardInterrupt:
        if not name:
            s.close()
        else:
            do_quit(s,SADDR,name)
        sys.exit('退出程序')

        


if __name__ == '__main__':
    main()    