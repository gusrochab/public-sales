from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Immobile, Automobile, Like_Immobile

from .celery_tasks import sleepy


def home(request):
    immobiles = Immobile.objects.order_by('date_auction')
    return render(request, 'sales/home.html', {'auctions': immobiles})


def home2(request):
    return render(request, 'sales/home2.html')


def about(request):
    return render(request, 'sales/about.html')


@login_required
def sales_list(request, id):
    user = User.objects.get(id=id)
    immobiles = Immobile.objects.all()
    liked_auctions = []
    for immobile in immobiles:
        if user in immobile.liked.all():
            liked_auctions.append(immobile)
    context = {'title': 'Leilões Marcados', 'liked_auctions': liked_auctions}
    return render(request, 'sales/sales_list.html', context)


@login_required
def liked(request):
    user = request.user
    if request.method == 'POST':
        immobile_id = request.POST.get('immobile_id')
        immobile = Immobile.objects.get(id=immobile_id)
        if user in immobile.liked.all():
            immobile.liked.remove(user)
        else:
            immobile.liked.add(user)

        like, created = Like_Immobile.objects.get_or_create(
            user=user, immobile_id=immobile_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    if request.POST.get('user_list'):
        return redirect('sales_list', id=user.id)
    else:
        return redirect('home')


def celery(request):
    sleepy(10)
    return HttpResponse('Done!')
