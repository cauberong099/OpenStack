from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from RegisterForm import RegisterForm
import requests, json
from django.core.mail import EmailMessage
from django.conf import settings
from config import *
from django.core.urlresolvers import reverse

def registration(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        if form.is_valid() :
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            fullname = form.cleaned_data["fullname"]
            email = form.cleaned_data["email"]

            # Call API to middleservice with user info.
            url = API_URL+"users"
            payload = {'username':username,'password':password,'email':email}
            headers = {'content-type':'application/json','Accept-Charset': 'UTF-8'}
            try:
                r = requests.post(url, data=json.dumps(payload), headers=headers)
            except Exception as e:
                return render(request, 'registration/register_wrong.html')

            # If create user success
            if r.status_code == 200 and 'id' in r.json():
                SITE_URL = getattr(settings, 'SITE_URL', 'http:127.0.0.1')
                PORT_BASE = getattr(settings, 'PORT_BASE', '9999')
                subject = "[OpenStack Mail]"
                body = "Thanks you for register, Please click the folowing link to confirm: " + SITE_URL+":"+PORT_BASE+reverse('registration:confirm', kwargs={'uid':str(r.json()["id"])})
                e = EmailMessage(subject, body, to=[email])
                res = e.send()
                if res == 0:
                    return render(request, 'registration/register_wrong.html')
                return render(request, 'registration/register_success.html', {'username': username,'fullname': fullname,'email': email})
            else:
                return render(request, 'registration/register_wrong.html')

        
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register_form.html', {'form': form})



def confirm(request, uid):

    # Call API to active user with uid
    r = requests.put(API_URL+'users/'+uid)
    if r.status_code == 200:
        return render(request, 'registration/register_confirm.html')
    return render(request, 'registration/register_wrong.html')