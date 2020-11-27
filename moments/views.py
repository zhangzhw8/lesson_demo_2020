import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
from blueking.component.shortcuts import get_client_by_request
from moments.models import WeChatUser, Status, Reply
from moments.tasks import send_mail
from weixin.core.accounts import WeixinAccount


def home(request):
    # return render(request, "homepage.html")
    return render(request, "moments/homepage.html")


@login_required
def show_user(request):
    """
    po = {
        "username": "xiao po",
        "motto": "i love kungfu",
        "email": "xiaopo@disney.com",
        "region": "Shaanxi",
        "pic": "Po2.jgp",
    }
    #sqlit
    import pdb
    pdb.set_trace()
    """
    user, is_created = WeChatUser.objects.get_or_create(user=request.user)
    return render(request, "moments/user.html", {"user": user})


@login_required
def show_status(request):
    # statuses = Status.objects.all()
    """
    import pdb
    pdb.set_trace()
    """

    keyword = request.GET.get("keyword")
    page = request.GET.get("page", "1")
    if not keyword:
        statuses = Status.objects.all()
    else:
        statuses = Status.objects.filter(Q(text__contains=keyword) | Q(user__user__username__contains=keyword))
        # statuses = Status.objects.filter(text__contains=keyword)
        # statuses = Status.objects.filter(user__user__username__contains=keyword)
    p = Paginator(statuses, 2)
    statuses = p.get_page(page)
    for status in statuses:
        status.likes = Reply.objects.filter(status=status, type="0")
        status.comments = Reply.objects.filter(status=status, type="1")
    return render(request, "moments/status.html", {"statuses": statuses,
                                           "keyword": keyword,
                                           "page": int(page),
                                           "page_range": p.page_range})


@login_required
def submit_post(request):
    """
    import pdb
    pdb.set_trace()
    """
    user, is_created = WeChatUser.objects.get_or_create(user=request.user)
    text = request.POST.get("text")
    uploded_file = request.FILES.get("pics")
    if uploded_file:
        name = uploded_file.name
        with open("./moments/static/image/{}".format(name), "wb") as handler:
            for block in uploded_file.chunks():
                handler.write(block)
    else:
        name = ''
    if text:
        status = Status(user=user, text=text, pics=name)
        status.save()
        is_weixin_visit = WeixinAccount().is_weixin_visit(request)
        adapt_site_url = settings.WEIXIN_SITE_URL if is_weixin_visit else settings.SITE_URL
        return redirect("{}status".format(adapt_site_url))

    return render(request, "moments/my_post.html")


@login_required
def friend(request):
    return render(request, "moments/friends.html")


def register(request):
    try:
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = User(username=username,  email=email)
        user.set_password(password)
        user.save()
        WeChatUser.objects.create(user=user)
    except Exception as err:
        result = False
        message = str(err)
    else:
        result = True
        message = "Register success!"

    return JsonResponse({"result": result, "message": message})


@login_required
def update_user(request):
    try:
        motto = request.POST.get("motto")
        if motto:
            WeChatUser.objects.filter(user=request.user).update(motto=motto)
        region = request.POST.get("region")
        if region:
            WeChatUser.objects.filter(user=request.user).update(region=region)
        pic = request.POST.get("pic")
        if region:
            WeChatUser.objects.filter(user=request.user).update(pic=pic)
        email = request.POST.get("email")
        if email:
            WeChatUser.objects.filter(user=request.user).update(email=email)
    except Exception as err:
        result = False
        message = str(err)
    else:
        result = True
        message = "Update success!"

    return JsonResponse({"result": result, "message": message})


from moments.tasks import send_mail

@login_required
def like(request):
    user = request.user.username
    status_id = request.POST.get("status_id")

    liked = Reply.objects.filter(author=user, status=status_id, type="0")
    if liked:
        liked.delete()
    else:
        Reply.objects.create(author=user, status=Status.objects.get(id=status_id), type="0")

        # 发送朋友圈点赞通知邮件
        status = Status.objects.get(id=status_id)
        receiver = status.user.email
        title = f"{user} 点赞了你的朋友圈状态"
        content = f"<p style=\"color: red; background: green;\">{user} 点赞了你的朋友圈状态：<strong>【{status.text}】</strong></p>"

        client = get_client_by_request(request)
        send_mail.delay(client, receiver, title, content)

    return JsonResponse({"result": True})


@login_required
def comment(request):
    user = request.user.username
    status_id = request.POST.get("status_id")
    at_person = request.POST.get("at_person")
    text = request.POST.get("text")

    Reply.objects.create(author=user, status=Status.objects.get(id=status_id), type="1", at_person=at_person, text=text)
    return JsonResponse({"result": True})


@login_required
def delete_comment(request):
    comment_id = request.POST.get("comment_id")
    Reply.objects.filter(id=comment_id).delete()
    return JsonResponse({"result": True})



from rest_framework import viewsets

from moments.serializers import WeChatUserSerializer
from moments.models import WeChatUser


class WeChatUserViewSet(viewsets.ModelViewSet):

    # 指定查询集
    queryset = WeChatUser.objects.all()

    # 指定序列化器
    serializer_class = WeChatUserSerializer
