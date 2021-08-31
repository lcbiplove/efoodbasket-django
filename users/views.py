from users.models import TraderDocumentForm, User, Trader, TraderDocument
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from .validators import TraderValidator, UserValidator
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from efoodbasket import emails
from django.views.generic import DetailView
from .permissions import AdminPermission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.middleware.csrf import get_token
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request,*args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user:
            if self.handle_not_activated(request, user):
                return redirect('login')
                
            next = request.GET.get('next', '/')
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Logged in successfully.", 'success')
            return redirect(next)
        else:
            messages.add_message(request, messages.ERROR, "Incorrect email or password.", 'fail')
        return render(request, 'login.html')
    
    def handle_not_activated(self, request, user):
        if not user.can_login:
            csrf_token = get_token(request)
            csrf_token_html = f"<input type='hidden' name='csrfmiddlewaretoken' value='{csrf_token}' />"
            verify_link = reverse('verify_email', kwargs={'id': user.id})
            mssg = f"Your email is not verified. You need to verify your email to login.<form class='otp-inline-form' method='POST' action='{verify_link}'>{csrf_token_html}<input type='hidden' name='email' value='{user.email}' /><input type='hidden' name='resend' value='resend' /><button class='submit'>VERIFY</button></form>"

            messages.add_message(request, messages.INFO, mssg, 'info')
            return True

class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.SUCCESS, "Logged out successfully.", 'success')
        return response

class SignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')

    def post(self, request, *args, **kwargs):
        valid_data = {}

        keys = ['fullname', 'contact', 'address', 'email', 'password', 'confpass', 'terms']

        validator = UserValidator(request.POST, keys)
        errors = validator.get_errors()

        for key in request.POST:
            if key in keys:
                valid_data[key] = request.POST.get(key)

        if len(errors) == 0:
            user = User.objects.create_user(
                email=request.POST.get('email'), 
                password=request.POST.get('password'),
                fullname=request.POST.get('fullname'),
                contact=request.POST.get('contact'),
                user_role=User.USER_IS_CUSTOMER,
                address=request.POST.get('address'),
            )
            emails.send_verify_code(user)
            messages.add_message(request, messages.INFO, "Please check your email to verify your account.", 'info')
            return redirect('verify_email', id=user.id)

        return render(request, 'signup.html', {
            'errors': errors,
            'valid_data': valid_data,
        })


class SignupTraderView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup-trader.html')

    def post(self, request, *args, **kwargs):
        valid_data = {}

        keys = ['fullname', 'contact', 'address', 'email', 'terms', 'pan', 'type', 'details']

        validator = TraderValidator(request.POST, keys)
        errors = validator.get_errors()

        for key in request.POST:
            if key in keys:
                valid_data[key] = request.POST.get(key)

        document_form = TraderDocumentForm(request.POST, request.FILES)

        if not document_form.is_valid():
            errors['documents'] = document_form['document'].errors.as_text()[2:]

        if len(request.FILES.getlist('documents')) > 5:
            errors['documents'] = 'You can only add maximum 5 documents.'

        if len(errors) == 0:
            user = User.objects.create_user(
                email=request.POST.get('email'), 
                password=None,
                fullname=request.POST.get('fullname'),
                contact=request.POST.get('contact'),
                address=request.POST.get('address'),
                user_role=User.USER_IS_TRADER
            )
            emails.send_verify_code(user)
            trader = Trader.objects.create(
                pan=request.POST.get('pan'),
                product_type=request.POST.get('type'),
                product_details=request.POST.get('details'),
                user=user
            )
            for photo in request.FILES.getlist('document'):
                TraderDocument.objects.create(document=photo, trader=trader)
            messages.add_message(request, messages.INFO, "Please check your email to verify your account.", 'info')
            return redirect('verify_email', id=user.id)

        return render(request, 'signup-trader.html', {
            'errors': errors,
            'valid_data': valid_data,
        })

class VerifyEmailView(View):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')

        return render(request, 'verify-notice.html', {
            'user_id': user_id
        })

    def post(self, request, *args, **kwargs):
        resend = request.POST.get('resend', None)
        user_id = self.kwargs.get('id')
        error = ''
        if resend:
            emails.send_verify_code(User.objects.get(pk=user_id))
            messages.add_message(request, messages.INFO, "Please check your email to verify your account.", 'info')
        else:
            error = self.check_verify_code(request=request, user_id=user_id)

            if not error:
                return redirect('/')
            
        return render(request, 'verify-notice.html', {
            'user_id': user_id,
            'error': error,
        })

    def check_verify_code(self, request, user_id):
        code = request.POST.get('code')
        user = get_object_or_404(User, pk=user_id)

        if not user.otp_expired:
            if str(user.otp) != str(code):
                return 'Please enter correct code'
            else:
                self.handle_correct_code(request=request, user=user)
        else:
            return 'Code is already expired'

    def handle_correct_code(self, request, user):
        user.is_active = True
        user.save()
        if user.is_trader:
            messages.add_message(request, messages.INFO, 'Your email is verified successfully. You will be notified once your documents are reviewed.', 'info')
            emails.send_trader_request_to_admin(user)
        else:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Account verified successfully.', 'success')

class TraderRequestsDetailView(AdminPermission, DetailView):
    model = User
    template_name = "trader-request.html"
    context_object_name = 'trader'
    queryset = User.objects.filter(user_role=User.USER_IS_TRADER)

    def post(self, request, *args, **kwargs):
        accept = request.POST.get('accept')
        reject = request.POST.get('reject')
        user = self.get_object()
        if reject:
            emails.send_trader_rejected(user)
            user.delete()
            
        if accept:
            user.trader.status = Trader.APPROVAL_IS_SUCCESS
            user.trader.save()
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            emails.send_trader_accepted(user, token, uidb64)
        
        return redirect('/admin/')


class PasswordResetView(View):

    def dispatch(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64')
        uid = force_text(urlsafe_base64_decode(uidb64))
        self.user = get_object_or_404(User, pk=uid)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token_generator = PasswordResetTokenGenerator()
        token = self.kwargs.get('token')
        if not token_generator.check_token(self.user, token):
            messages.add_message(request, messages.ERROR, 'Invalid link!!! Try resetting password again.', 'fail')
            return redirect('login')

        return render(request, 'password-reset.html')

    def post(self, request, *args, **kwargs):
        keys = ['password', 'confpass']

        validator = UserValidator(request.POST, keys, validate_terms=False)
        errors = validator.get_errors()

        if len(errors) == 0:
            self.user.set_password(request.POST.get('password'))
            self.user.is_active = True
            self.user.save()
            login(request, self.user)
            messages.add_message(request, messages.SUCCESS, "Password saved and logged in successfully.", 'success')
            return redirect('/')

        return render(request, 'password-reset.html', {
            'errors': errors,
        })

class ForgotPasswordView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'forgot-password.html')
    
    def post(self, request, *args, **kwargs):
        errors = {}
        email = request.POST.get('email')

        user = User.objects.filter(email=email)

        if not user.exists():
            errors['email'] = "Email you entered does not exist"

        if len(errors) == 0:
            user = user.first()
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            emails.send_password_reset(user, token, uidb64)
            messages.add_message(request, messages.INFO, 'Password reset link is send to your email.', 'info')
        
        return render(request, 'forgot-password.html', {
            'errors': errors
        })


class ManageAccountView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'manage-account.html')

    def post(self, request, *args, **kwargs):
        errors = {}

        keys = ['fullname', 'address', 'contact']

        validator = UserValidator(request.POST, keys, validate_terms=False)
        errors = validator.get_errors()

        preserved = {key:request.POST[key] for key in keys}

        if len(errors) == 0:
            for key in keys:
                setattr(request.user, key, request.POST.get(key))
            request.user.save()
            messages.add_message(request, messages.SUCCESS, 'Profile updated successfully.', 'success')
            return redirect('manage_account')

        return render(request, 'manage-account.html', {
            'preserved': preserved,
            'errors': errors,
        })

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'change-password.html')

    def post(self, request, *args, **kwargs):
        errors = {}
        keys = ['password', 'confpass']

        validator = UserValidator(request.POST, keys, validate_terms=False)
        errors = validator.get_errors()

        if not request.user.check_password(request.POST.get('oldpass')):
            errors['oldpass'] = "Password you entered is not correct."

        if len(errors) == 0:
            request.user.set_password(request.POST.get('password'))
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.add_message(request, messages.SUCCESS, "Password updated successfully.", 'success')
            return redirect('manage_account')

        return render(request, 'change-password.html', {
            'errors': errors,
        })

    
    