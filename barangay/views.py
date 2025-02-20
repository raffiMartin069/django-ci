from django.shortcuts import render, redirect

def access_page(request):
    return render(request, "access.html")

def logout(request):
    request.session.flush()
    return redirect('login')