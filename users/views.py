from users.models import TraderDocumentForm, User, Trader, TraderDocument
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from .validators import TraderValidator, UserValidator
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from efoodbasket.emails import send_verify_code

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request,*args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            next = request.GET.get('next', '/')
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Logged in successfully.", 'success')
            return redirect(next)
        else:
            messages.add_message(request, messages.ERROR, "Incorrect email or password.", 'fail')
        return render(request, 'login.html')

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
            send_verify_code(user)
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
            send_verify_code(user)
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
            send_verify_code(User.objects.get(pk=user_id))
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
                user.is_active = True
                user.save()
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Account verified successfully.", 'success')
        else:
            return 'Code is already expired'

