#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2020/4/27 20:44
# @Author  :Coco
# @FileName: main.py

# @Software: PyCharm
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓ ┏┓
            ┏┛┻━┛┻━┓
            ┃   ☃  ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
               ┃     ┗━━┓
               ┃        ┣┓
               ┃　      ┏┛
               ┗┓┓━━┳┓━┛
                 ┃┫  ┃┫
                 ┗┛  ┗┛
"""

from mysql_jingdong import JD

if __name__ == '__main__':
    # 实例化京东对象
    jd = JD()
    while True:
        print('1: 查看所有商品')
        print('2: 购买商品')
        print('q: 退出系统')
        num = input('> : 请选择您想办理的业务\n')
        if num == '1':
            print('查看所有商品')
            jd.show_goods_info()
        elif num == '2':
            print('购买商品')
            customer_name = input('> : 请输入用户名')
            # 判断用户是否存在
            check_customer = jd.cursor.execute('''select * from customers where name = %s''', [customer_name])
            if check_customer == 1:
                passwd_name = input('> : 请输入')
                # 判断密码是否正确：
                while yyy not 'q':
                # 开始购物
                else:
                    passwd_name = input('> : 请输入')
        elif num == 'q':
            print('退出系统')
            break
