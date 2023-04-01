import smtplib
import traceback
from email.mime.text import MIMEText
from config.auth import settings as AuthConfig

def send_email(receiver: str, post_id: int, post_name: str):
    """
    发送邮件
    :param receiver: 邮箱地址
    :param post_id:  文章ID
    :param post_name: 文章标题
    :return:
    """
    sender = AuthConfig.EMAIL_USER
    content = make_content(post_id, post_name)
    message = MIMEText(content, 'html', 'utf-8')
    message['FROM'] = sender
    message['TO'] = receiver
    message['Subject'] = '新回复'

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(AuthConfig.EMAIL_HOST, AuthConfig.EMAIL_SMTP_PORT)
        smtp_obj.login(AuthConfig.EMAIL_USER, AuthConfig.EMAIL_PWD)
        smtp_obj.sendmail(sender, receiver, message.as_string())
    except smtplib.SMTPException as e:
        traceback.print_exc()
