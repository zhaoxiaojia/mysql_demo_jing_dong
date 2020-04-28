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
import time


def update_orders(customer_id):
    '''
    +-----------------+--------------+------+-----+---------+----------------+
    | id              | int unsigned | NO   | PRI | NULL    | auto_increment |
    | order_date_time | varchar(40)  | YES  |     | NULL    |                |
    | customer_id     | int          | NO   |     | NULL    |                |
    +-----------------+--------------+------+-----+---------+----------------+
    更新orders订单表
    :param customer_id:
    :return:order_id
    '''
    # 获得当前日期时间
    order_date_time = time.localtime(time.time())
    # 插入数据
    jd.cursor.execute('''insert into orders value(0,%s,%s)''', [order_date_time, customer_id])
    # 获得刚插入的id
    jd.cursor.execute('''select id from orders where order_date_time = %s''', [order_date_time])
    order_id = jd.cursor.fetchall()[0][0]
    jd.conn.commit()
    return order_id


def update_order_detial(order_id, good_id, quantity):
    '''
    +----------+--------------+------+-----+---------+----------------+
    | id       | int unsigned | NO   | PRI | NULL    | auto_increment |
    | order_id | int          | NO   |     | NULL    |                |
    | good_id  | int          | NO   |     | NULL    |                |
    | quantity | int          | NO   |     | NULL    |                |
    +----------+--------------+------+-----+---------+----------------+
    更新order_detial
    :param order_id:
    :param good_id:
    :param quantity:
    :return:
    '''
    # 插入数据
    jd.cursor.execute('''insert into order_detial value(0,%s,%s,%s)''', [order_id, good_id, quantity])
    jd.conn.commit()


def check_good_exist(goods):
    if goods.isdigit():
        exist = jd.cursor.execute('''select * from goods where id = %s''', [goods])
    else:
        exist = jd.cursor.execute('''select * from goods where name = %s''', [goods])
    if exist != 1:
        return False
    else:
        return True


def shop(goods):
    '''
    模拟选购物品 选后完成后添加到对应的表单中
    :return:
    '''
    print('正在查询该商品是否存在')
    while not check_good_exist(goods):
        goods = input('> : ！没有该商品，请重新输入\n')
    else:
        # 获得商品id
        if not goods.isdigit():
            jd.cursor.execute('''select id from goods where name = %s''', [goods])
            good_id = jd.cursor.fetchall()[0][0]
        else:
            good_id = goods
        quantity = input('> : 请输入想购买的个数\n')
        while not quantity.isdigit():
            quantity = input('> : !输入有误，请重新输入\n')
            # Todo 判断仓库是否还有足够数量发货
        # jd.cursor.execute('''数量-1''')
        print('已完成购买')
        return good_id, quantity


def check_customer():
    '''
    检测用户是否存在 不存在则重新创建并记录到数据库
    :return:
    '''
    good_id, quantity = '', ''
    customer_name = input('> : 请输入用户名\n')
    # 判断用户是否存在
    check_customer = jd.cursor.execute('''select * from customers where name = %s''', [customer_name])
    if check_customer == 1:
        jd.cursor.execute('''select passwd from customers where name = %s''', [customer_name])
        customer_passwd = jd.cursor.fetchall()[0][0]
        # print(customer_passwd)
        # print('customer_passwd', type(customer_passwd))
        input_passwd = input('> : 请输入密码\n')
        # 判断密码是否正确：
        while input_passwd != 'q':
            if input_passwd == customer_passwd:
                # 开始购物
                print('开始购物')
                wanted_good = input('> : 请输入请选择想购买的物品名称或者id\n')
                if wanted_good == 'q':
                    break
                good_id, quantity = shop(wanted_good)
            else:
                input_passwd = input('> : 密码错误，请重新输入\n')
    elif check_customer == 0:
        # 输入的用户名不存在
        create_boole = input('！ 该用户名不存在，是否使用该用户名创建(y/n)\n')
        if create_boole == 'y' or create_boole == 'yes':
            # 用户需要重新创建
            # 收集信息
            '''
            +---------+--------------+------+-----+---------+----------------+
            | id      | int unsigned | NO   | PRI | NULL    | auto_increment |
            | name    | varchar(150) | NO   |     | NULL    |                |
            | address | varchar(150) | NO   |     | NULL    |                |
            | tel     | varchar(11)  | NO   |     | NULL    |                |
            | passwd  | varchar(40)  | NO   |     | NULL    |                |
            +---------+--------------+------+-----+---------+----------------+
            '''
            name = customer_name
            address = input('> : 请输入收货地址\n')
            tel = input('> : 请输入收货人手机\n')
            passwd = input('> : 请输入密码\n')
            try:
                jd.cursor.execute('''insert into customers value(0,%s,%s,%s,%s)''', [name, address, tel, passwd])
                jd.conn.commit()
                print('已创建成功')
                wanted_good = input('> : 请输入请选择想购买的物品名称或者id\n')
                good_id, quantity = shop(wanted_good)
            except Exception as e:
                print('输入的数据有误,已退出当前业务')
                print(e)
        elif create_boole == 'n' or create_boole == 'no':
            print('正在退出当前业务...')
            return
    jd.cursor.execute('''select id from customers where name = %s''', [customer_name])
    customer_id = jd.cursor.fetchall()[0][0]
    # 更新orders订单表
    order_id = update_orders(customer_id)
    # 更新order_detial
    update_order_detial(order_id, good_id, quantity)


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
            check_customer()
        elif num == 'q':
            print('退出系统')
            break
