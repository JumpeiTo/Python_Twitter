from django.shortcuts import render

def home(request):
  return render(
    request, 'boardapptest_app/home.html'
  )