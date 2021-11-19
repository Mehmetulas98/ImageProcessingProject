from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
# Create your views here.


def index(request):
    Context = {}
    if(request.method == 'POST'):
        OperationType = request.POST.get("document", "")
        return render(request, "main.html")
        if(OperationType == "Görüntü İyileştirme Yöntemleri"):

            return render(request, "main.html")
        elif(OperationType == "Histogram Görüntüleme ve Eşikleme"):
            Context['values'] = ["yöntem 3", "yöntem 4"]
            return render(request, "main.html", Context)

    return render(request, "index.html")


def main(request, operationtype):
    Context = {}
    # print(request.method)
    # if(operationtype == "Görüntü İyileştirme Yöntemleri"):
    #     print("kontrol 1")
    #     Context['values'] = ["yöntem 1", "yöntem 2", "yarrak"]
    #     Context['controller'] = True

    #     return render(request, "main.html", Context)
    # elif(request.method == 'POST'):
    #     print("kontrol 2")
    # print("kontrol 3")

    # return render(request, "main.html")
    if(request.method == "POST"):
        if(operationtype == "Görüntü İyileştirme Yöntemleri"):
            Context['values'] = ["yöntem 1", "yöntem 2", "yarrak"]
            Context['controller'] = True
            return render(request, "main.html", Context)
        if(operationtype == "Histogram Görüntüleme ve Eşikleme"):
            Context['values'] = ["yöntem 4", "yöntem 5", "yarraksdsd"]
            Context['controller'] = True
            return render(request, "main.html", Context)
    else:
        print("op type")
        print(operationtype)
        # Burada ilgili işlerler
        return render(request, "main.html", status=None)
