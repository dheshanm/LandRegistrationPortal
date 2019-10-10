from django.shortcuts import render
from django.http import HttpResponse
from .forms import LandDetailsForm, ZeroForm
from .models import Transaction
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime

import requests
import json

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"

# Create your views here.
data = []

def fetch_data():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global data
        data = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

def populateDB():
	global data
	fetch_data()

	queryset = Transaction.objects.all().order_by('-timestamp')

	for block in data:
		new_t_id = block['transaction_id']
		try:
			transact = Transaction.objects.get(transaction_id=new_t_id)
		except Transaction.DoesNotExist:
			t = Transaction(
				transaction_id=block["transaction_id"], 
				LandHolder_aadhaar=block["LandHolder_aadhaar"], 
				Land_state=block["Land_state"], 
				Land_district=block["Land_district"], 
				Land_taluk=block["Land_taluk"], 
				Land_village=block["Land_village"], 
				Land_survey_number=block["Land_survey_number"],
				Land_subdivision_number=block["Land_subdivision_number"], 
				block_timestamp=datetime.fromtimestamp(block["timestamp"]), 
				block_index=block["index"], block_hash=block["hash"])
			t.save()


def home(request):
	return render(request=request, template_name="main/index.html")

def about(request):
	return render(request=request, template_name="main/about.html")

def services(request):
	return render(request=request, template_name="main/services.html")

def contact(request):
	return render(request=request, template_name="main/contact.html")

def lookup(request):
	if request.method == "POST":
		form = ZeroForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)

			# Things to do before save
			

			# Submit a transaction
			new_tx_address = "{}/mine".format(CONNECTED_NODE_ADDRESS)
			msg = requests.get(new_tx_address,
                 	headers={'Content-type': 'application/json'})

			# messages.info(request, msg)
			# data.save()
			populateDB()
			return redirect(to='main:lookup')
	else:
		form = ZeroForm()
	return render(request=request, template_name="main/lookup.html", context={'form': form})

def register(request):
	if request.method == "POST":
		form = LandDetailsForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)

			# Things to do before save
			data_object = {
				'transaction_id': str(data.transaction_id),
				'LandHolder_aadhaar': data.LandHolder_aadhaar,

				'Land_state': data.Land_state,
				'Land_district': data.Land_district,
				'Land_taluk': data.Land_taluk,
				'Land_village': data.Land_village,
				'Land_survey_number': data.Land_survey_number,
				'Land_subdivision_number': data.Land_subdivision_number,
			}

			# Submit a transaction
			new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
			msg = requests.post(new_tx_address,
                  	json=data_object,
                 	headers={'Content-type': 'application/json'})

			messages.info(request, msg)
			# data.save()
			return redirect(to='main:home')
	else:
		form = LandDetailsForm()
	return render(request=request, template_name="main/register.html", context={'form': form})