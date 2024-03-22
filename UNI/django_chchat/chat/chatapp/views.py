from django.shortcuts import render

# Create your views here.


def chatpage(request):
    return render(request, "chatapp/chatpage.html", context={"msg":"ChatPage Room!"})


def chatroom(request, room):
    return render(request, "chatapp/chatpage2.html", context={"msg":room})