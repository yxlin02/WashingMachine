import smtplib
from email.mime.text import MIMEText


def send_email(to_email):
    try:
        mailserver = 'smtp.gmail.com'  # 邮箱服务器地址
        username_send = ''  # 邮箱用户名
        password = ''  # 邮箱密码：需要使用授权码
        username_recv = to_email  # '1565172273@qq.com'  # 收件人，多个收件人用逗号隔开
        mail = MIMEText('''{},you are receiving this email because of the following reason: 1) Your laundry is complete. Please take your clothes out and checkout the washing machine ASAP. 2) You have booked an appointment. It is the time to do your laundry!'''.format(to_email))
        mail['Subject'] = 'Washing Machine Needs Operation'
        mail['From'] = username_send  # 发件人
        mail['To'] = username_recv  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
        smtp = smtplib.SMTP(mailserver, port=587)  # 连接邮箱服务器，smtp的端口号是25
        # smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465) #QQ邮箱的服务器和端口号
        smtp.ehlo()
        smtp.starttls()
        smtp.login(username_send, password)  # 登录邮箱
        smtp.sendmail(username_send, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
        smtp.quit()  # 发送完毕后退出smtp
        print('success')
        return True
    except Exception as e:
        print(e.args)
        return False
