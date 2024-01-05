from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views import View  
class Detail(View):  
    def get(self, request):  
        # View logic will place here  
        return HttpResponse('Helloworld')  