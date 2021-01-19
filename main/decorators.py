from django.shortcuts import redirect


def unauthenticated_user(view_func):

    """ If a user is logged in and tries to access the login
     or registration page this redirects them to the dashboard """

    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

