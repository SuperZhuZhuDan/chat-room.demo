#!/usr/bin/env python3
#coding=utf-8

'''
name:朱家豪
email:1269347182@qq.com
date:2019-10
Class:
introduce:chatroom server
env:python3
'''
from socket import *
import os,sys

#注册函数
def do_login(s,user,name,addr):
    #判断用户是否存在
    if (name in user) or (name=='管理员'):
        s.sendto('姓名已存在'.encode(),addr)
        return
    #添加用户
    user[name]=addr
    s.sendto('OK'.encode(),addr)
    #通知所有人
    msg='%s进入聊天室'%name
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
    return

#收发聊天消息
def do_talk(s,user,data,addr):
    for i in user:
        if user[i] != addr:
            s.sendto(data.encode(),user[i])

#用户退出
def do_quit(s,user,name):
    msg='%s退出了聊天室'%name
    for i in user:
        if i==name:
            s.sendto('Exit'.encode(),user[i])
        else:
            s.sendto(msg.encode(),user[i])
    del user[name]




#接收客户端请求
def do_parent(s):
    #成员目录（名字key=地址）
    user={}
    while True:
        data,addr=s.recvfrom(4096)
        #判断字符
        datah=data.decode()[0]
        #具体内容
        datal=data.decode()[1:]
        #运行注册检测
        if datah=='L':
            do_login(s,user,datal,addr)
        #聊天内容收发
        elif datah=='C':
            do_talk(s,user,datal,addr)
        elif datah=='Q':
            print(data.decode())
            print(addr)
            do_quit(s,user,datal)

#管理员喊话函数
def do_child(s,ADDR):
    while True:
        msg=input('管理员消息:')
        msgs='C管理员-->%s'%msg
        s.sendto(msgs.encode(),ADDR)
    

#创建网络，创建进程，调用功能函数
def main():
    #server address
    ADDR=('0.0.0.0',8888)

    #创建数据报套接字
    s=socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,\
        SO_REUSEADDR,1)
    s.bind(ADDR)

    #创建一个新的进程，进行管理员喊话功能
    pid=os.fork()
    if pid<0:
        sys.exit('程序启动失败')
    elif pid==0:
        do_child(s,ADDR)
    else:
        do_parent(s)

if __name__ == '__main__':
    main()
