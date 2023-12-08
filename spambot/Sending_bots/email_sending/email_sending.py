# # -*- coding: utf-8 -*-
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from spambot.core.models.seller import WholesaleCustomer
# import asyncio
#
#
# def login_server():
#     email_sender = u"noobiko262@gmail.com"
#     password = u"xqbr ridq klln jzkj"
#
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     try:
#         server.login(email_sender, password)
#     except Exception as exc:
#         return f"{exc} ошибка с логином"
#     return server, email_sender
#
#
# def send_message(message: str, server: smtplib.SMTP,
#                  email_sender: str, email_recipient: str) -> str | Exception:
#     try:
#         server.sendmail(email_sender, email_recipient, message)
#         return "Сообщение было отправлено"
#     except Exception as exc:
#         return f"{exc} ошибка с логином"
#
#
# def message_setting(article, theme, body):
#     message = MIMEText(body, "html")
#     message['Subject'] = theme
#     message['From'] = "Аренда мото 'звёздочка'"
#     message['To'] = ""
#     return message
#
#
# def html_template_for_sending_message():
#     with open("C:\PythonPrograms\SpamBot\spambot\Sending_bots\email_sending\send_message.html", "r",
#               encoding="utf-8") as file:
#         return file.read()
#
#
# def email_sender(customers_list: list[WholesaleCustomer],
#                  article, theme):
#     server, email_sender = login_server()
#     body = html_template_for_sending_message()
#     message = message_setting(article=article,
#                               theme=theme,
#                               body=body).as_string()
#     for customer in customers_list:
#         send_message(message=message,
#                      server=server,
#                      email_sender=email_sender,
#                      email_recipient=customer.social_network.email)
