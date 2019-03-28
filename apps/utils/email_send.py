# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/3/28 15:38'

import random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from rapzhang_online.settings import EMAIL_FROM


'''生成一个随机字符串,当做邮箱激活链接当中的字符串'''
def create_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str


'''后台发送邮件'''
def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code = create_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == 'register':
        email_title = '奔哥哥在线动作教育平台激活链接'
        email_body = '亲,请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            print('激活邮件已发送至邮箱')
            pass

    elif send_type == 'forget':
        email_title = '奔哥哥在线动作教育平台密码重置链接'
        email_body = '亲,请点击下面的链接重置账号的密码:http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('激活邮件已发送至邮箱')
            pass
