from django.core.mail import send_mail, mail_admins
from efoodbasket.settings import WEBSITE_DOMAIN
from django.template.loader import render_to_string
from django.urls import reverse


def get_email_body(title, link_or_code_html, body_text):
    logo_url = 'https://raw.githubusercontent.com/lcbiplove/efoodbasket-logo/main/efoodbasket-logo.png'
    body = render_to_string('email_base.html', {
        'title': title,
        'website': WEBSITE_DOMAIN,
        'logo_url': logo_url,
        'body_text': body_text,
        'link_or_code_html': link_or_code_html
    })
    return body

def get_alt_body(code_or_link, body_text):
    alt_body = """
        ---------------------------
        |        efoodBasket      |     
        ---------------------------
        Hi, 
        %s
                            %s           
        Thanks 
        eFoodBasket
        -----------------------------------------------------------
        eFoodBasket - 98 Neville Street - Cleckhuderfax, UK - 56789
    """ % (body_text, code_or_link)
    return alt_body


def send_verify_code(user):
    email = user.email
    code = user.valid_otp
    title = "Email Verification Code"
    code_html = f"<span style='letter-spacing: 5px; font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #7FCB0A; display: inline-block;'>{code}</span>"
    body_text = """
    We're excited to have you get started. First, you need to confirm your account. 
    Below is the code to verify your account:
    """
    subject = "Your eFoodBasket verification code"
    body = get_email_body(title, code_html, body_text)
    alt_body = get_alt_body(code, body_text)

    send_mail(
        subject=subject, 
        message=alt_body, 
        from_email='no@reply.com', 
        recipient_list=[email],
        html_message=body
    )

def send_trader_request_to_admin(user):
    request_link = reverse('trader_request', args=[user.id])
    link = WEBSITE_DOMAIN + request_link
    title = "Review Trader Form"
    link_or_code_html = f"<a href='{link}' target='_blank' style='letter-spacing: 5px; font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #7FCB0A; display: inline-block;'>Link</a>"
    body_text = "A new trader is requesting to join our platform. They are waiting for your response to start working with us. Please review the user and make your decision:"
    subject = "Review trader request"
    body = get_email_body(title, link_or_code_html, body_text)
    alt_body = get_alt_body(link, body_text)

    mail_admins(
        subject=subject,
        message=alt_body,
        html_message=body,
    )

def send_trader_rejected(user):
    link = WEBSITE_DOMAIN + '/signup-trader/'
    title = "Request to become trader"
    email = user.email
    link_or_code_html = f"<a href='{link}' target='_blank' style='letter-spacing: 5px; font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #7FCB0A; display: inline-block;'>Signup</a>"
    body_text = "We are sorry that we could not accept your request of joining efoodbasket as trader. Please signup again with appropriate and real documents to work with us."

    subject = "Request to become trader"
    body = get_email_body(title, link_or_code_html, body_text)
    alt_body = get_alt_body(link, body_text) 
    send_mail(
        subject=subject, 
        message=alt_body, 
        from_email='no@reply.com', 
        recipient_list=[email],
        html_message=body
    )

def send_trader_accepted(user, token, uidb64):
    link = WEBSITE_DOMAIN + reverse('password_reset', kwargs={
        'uidb64': uidb64,
        'token': token
    })

    email = user.email
    title = "Request Accepted"

    link_or_code_html = f"<a href='{link}' target='_blank' style='letter-spacing: 5px; font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #7FCB0A; display: inline-block;'>Set Password</a>"

    body_text = "Welcome to efoodbasket for traders!!! We are so happy to inform you that you can now use our trader features. You can now login to efoodbasket as trader once you have set your password:"

    subject = "Request Accepted"
    body = get_email_body(title, link_or_code_html, body_text)
    alt_body = get_alt_body(link, body_text)
    send_mail(
        subject=subject, 
        message=alt_body, 
        from_email='no@reply.com', 
        recipient_list=[email],
        html_message=body
    )

def send_password_reset(user, token, uidb64):
    link = WEBSITE_DOMAIN + reverse('password_reset', kwargs={
        'uidb64': uidb64,
        'token': token
    })
    title = "Password Reset Link"
    link_or_code_html = f"<a href='{link}' target='_blank' style='font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #7FCB0A; display: inline-block;'>Reset Password</a>"
    body_text = "We have recently received a request to reset forgotten password for your efoodbasket account. To change your efoodbasket account password, please click the link below:"
    subject = "Password Reset"
    body = get_email_body(title, link_or_code_html, body_text)
    alt_body = get_alt_body(link, body_text)
    send_mail(
        subject=subject, 
        message=alt_body, 
        from_email='no@reply.com', 
        recipient_list=[user.email],
        html_message=body
    )