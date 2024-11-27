from django.shortcuts import render


# type your views here
def home(request):
    print("[logger: HTTP] \"Get request| <home.html>\"")
    return render(request, 'index.html')


def enterGame(request):
    print("[Logger: Http] \"Get Request| < entrance.html\"")
    return render(request, 'entrance.html')
