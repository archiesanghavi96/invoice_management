from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, get_user_model, login as auth_login,authenticate,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime


User = get_user_model()

@login_required
def generate_invoice(request):
	login_user = request.user
	try:
		errors = ""
		if request.method == "POST":
			num = request.POST['invoice_number']
			v_name = request.POST['v_name']
			date = request.POST['invoice_date']
			file = request.FILES['invoice_file']
			items_id = request.POST.getlist('items', [])

			item_list = []
			for data in items_id:
				item_list.append(int(data))

			fs = FileSystemStorage()
			fs.save(file.name, file)

			obj = invoice.objects.create(invoice_no=num,vendor_name=v_name,invoice_date=date,pdf=file, user=login_user)
			obj.item.add(*item_list)

			subject = "Invoice by" + login_user.email + obj.invoice_date
			msg = "Invoice genearted"
			from_email = login_user.email
			to_mail = ["abc@gmail.com",]
			# send_mail(subject,msg,from_email,to_mail,fail_silently=False)

			return redirect('agent_invoice')
		else:
			item = items.objects.all()
			return render(request, "generate_invoice.html",{"items":item})
	except:
		errors = "Something went wrong"
		return render(request, "generate_invoice.html",{"errors":errors})


@login_required
def all_invoice(request):
	invoices = invoice.objects.all()
	return render(request, "all_invoice.html", {'invoices':invoices})

@login_required
def agent_invoice(request):
	login_user = request.user
	print("------",login_user,type(login_user),login_user.email,login_user.id)
	invoices = invoice.objects.filter(user=login_user)
	return render(request, "agent_invoice.html", {'invoices':invoices})



def login_view(request):
	error= ""
	if request.method == "POST":
		email    = request.POST['email']
		password = request.POST['password']
		
		user = authenticate(request, username=email, password=password)
		if user:
			auth_login(request,user)
						
			if user.is_manager:
				return redirect('all_invoice')
			else:
				return redirect('agent_invoice')

		else:
			error = "Email or password entered is incorrect"

	return render(request, 'login.html', {'errors':error})

def logout(request):
	auth_logout(request)
	return redirect('login_view')