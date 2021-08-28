from users.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from .validators import UserValidator
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
                address=request.POST.get('address'),
            )
            send_verify_code(user)
            messages.add_message(request, messages.INFO, "Please check your email to verify your account.", 'info')
            return redirect('verify_email', id=user.id)

        return render(request, 'signup.html', {
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
            code = request.POST.get('code')
            user = get_object_or_404(User, pk=user_id)

            if not user.otp_expired:
                if str(user.otp) != str(code):
                    error = 'Please enter correct code'
                else:
                    user.is_active = True
                    user.save()
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Account verified successfully.", 'success')
                    return redirect('/')
            else:
                error = 'Code is already expired'
            
        return render(request, 'verify-notice.html', {
            'user_id': user_id,
            'error': error,
        })

