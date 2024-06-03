from django.http import HttpResponse
from django.shortcuts import render
from django.views import View



class GenerateReportView(View):
    def post(self, request):
        print("recieved post request")
        print(request)
        return HttpResponse("Result")


class RetrieveReportView(View):
    def get(self, request):
        print("recieved get request")
        print(request.body)
        return HttpResponse("Result")