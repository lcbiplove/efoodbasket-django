from django.core.mail import send_mail
from efoodbasket.settings import WEBSITE_DOMAIN
from django.template.loader import render_to_string

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

