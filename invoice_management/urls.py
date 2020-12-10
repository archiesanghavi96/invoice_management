from django.urls import path,re_path
from . import views

urlpatterns = [
	path('',views.login_view, name="login_view"),
	path('generate/',views.generate_invoice, name="generate_invoice"),
	path('all_invoice/',views.all_invoice, name="all_invoice"),
	path('agent_invoice/',views.agent_invoice, name="agent_invoice"),
	path('logout/', views.logout, name="logout")
]