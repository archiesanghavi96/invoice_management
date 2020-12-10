from invoice_management.models import *
from datetime import datetime,date,timedelta

def my_scheduled_job():
	yesterday = date.today()-timedelta(days=1)
	obj_list = invoice.objects.filter(invoice_date=yesterday)
	
	total_amt = 0
	total_invoice = len(obj_list)
	for rec in obj_list:
		for amt in rec.item:
			total_amt += amt.rate

	subject = "Yesterday's Invoice List"
	from_email = "archiesanghavi96@gmail.com"
	to_mail = "archiesanghavi96@gmail.com"
	msg = """
		Dear <Manager_Name>,

		Here is a summary for  <%s>.
		No. of invoices:  <%s>
		Total amount:  <%s>

		Here, the total amount is equal to the sum of the item rate of all items of all invoices for that particular day.
	"""%(yesterday.strftime("%m-%d-%Y"),total_invoice,total_amt)

	send_mail(subject,msg,from_email,to_mail,fail_silently=False)