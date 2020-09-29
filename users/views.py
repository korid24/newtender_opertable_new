from django.contrib.auth.views import LoginView, LogoutView
from .forms import PrettyAuthenticationForm


class LoginView(LoginView):
    '''
    Default login veiw with custom authentication form
    '''
    authentication_form = PrettyAuthenticationForm


class LogoutView(LogoutView):
    '''
    Default logout veiw with custom template
    '''
    template_name = 'registration/logout.html'
