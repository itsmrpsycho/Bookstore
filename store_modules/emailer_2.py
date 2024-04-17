import smtplib
from email.message import EmailMessage


def buyer_mail(user_name, user_email_id, b_quan_name, price):
    message = EmailMessage()
    message['subject'] = 'Thank you for choosing our products'
    message['from'] = 'letbooks.swap@gmail.com'
    message['to'] = user_email_id
    message.set_content(f'{user_name}, your transaction has been registered.\nYou have bought {b_quan_name} composing a sum of INR {price}.\nThank you for choosing us.')
    html_message = open('buyer_mail.html').read()
    html_message = html_message.replace("$(name)", user_name)
    html_message = html_message.replace("$(b_dat)", b_quan_name)
    html_message = html_message.replace("$(price)", str(price))

    message.add_alternative(html_message, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('letbooks.swap@gmail.com', 'okboomer2003')
        smtp.send_message(message)


def seller_mail(user_name, user_email_id, b_quan_name):
    message = EmailMessage()
    message['subject'] = 'Thank you for trusting us'
    message['from'] = 'letbooks.swap@gmail.com'
    message['to'] = user_email_id
    message.set_content(f'{user_name}, your request has been registered.\nYou have put up {b_quan_name}. \nThank you for trusting us.')
    html_message = open('seller_mail.html').read()
    html_message = html_message.replace("$(name)", user_name)
    html_message = html_message.replace("$(b_dat)", b_quan_name)

    message.add_alternative(html_message, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('letbooks.swap@gmail.com', 'okboomer2003')
        smtp.send_message(message)
