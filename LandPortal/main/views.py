from django.shortcuts import render
from django.http import HttpResponse
from .forms import LandDetailsForm, ZeroForm, LandForm
from .models import Transaction, Block, T2B, Chain
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.views.generic import TemplateView, ListView

import requests
import json
from hashlib import sha256

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"
THIS_ADDRESS = "http://127.0.0.1"

# Create your views here.
t_data = []
b_data = []

def compute_hash(data):
    """
    A function that return the hash of the block contents.
    """
    block_string = json.dumps(data, sort_keys=True)
    return sha256(block_string.encode()).hexdigest()

def update():
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    this_chain_address = "{}/api/chain".format(THIS_ADDRESS)
    response = requests.get(get_chain_address)
    curr_chain = requests.get(this_chain_address)
    if response.status_code == 200:
        chain = json.loads(response.content)
        try:
            this_chain = json.loads(curr_chain.content)[0]
            print("* {} blocks in client {} blocks in origin".format(len(this_chain["chain"]), len(chain["chain"])))
            flag = len(chain["chain"]) >= len(this_chain["chain"])
        except:
            this_chain = []
            flag = True
        if flag:
            print("* Recreating Chain from Blockchain")
            Chain.objects.all().delete()
            c = Chain(
                length=len(chain["chain"])
            )
            c.save()
            for block in chain["chain"]:
                new_b_hash = block['hash']
                try:
                    transact = Block.objects.get(hash=new_b_hash)
                except Block.DoesNotExist:
                    b = Block(
                        index=block["index"],
                        timestamp=datetime.fromtimestamp(float(block["timestamp"])),
                        previous_hash=block["previous_hash"],
                        nonce=block["nonce"],
                        hash=block["hash"],

                        chain=c
                    )
                    b.save()
                for tran in block["transactions"]:
                    new_t_id = tran['transaction_id']
                    try:
                        transact = Transaction.objects.get(transaction_id=new_t_id)
                    except Transaction.DoesNotExist:
                        t = Transaction(
                            transaction_id=tran["transaction_id"], 

                            LandHolder_aadhaar=tran["LandHolder_aadhaar"], 

                            Land_state=tran["Land_state"], 
                            Land_district=tran["Land_district"], 
                            Land_taluk=tran["Land_taluk"], 
                            Land_village=tran["Land_village"], 
                            Land_survey_number=tran["Land_survey_number"],
                            Land_subdivision_number=tran["Land_subdivision_number"],
                            Land_hash=tran["Land_hash"],

                            timestamp=datetime.fromtimestamp(float(tran["timestamp"])),
                            block=b
                        )

                        t.save()

                        link1 = T2B(
                            transaction=t,
                            block=b
                        )
                        link1.save()
        else:
            print("* Syncing Blockchain")
            update_chain_address = "{}/update".format(CONNECTED_NODE_ADDRESS)
            requests.post(update_chain_address)

def home(request):
    return render(request=request, template_name="main/index.html")

def about(request):
    return render(request=request, template_name="main/about.html")

def services(request):
    return render(request=request, template_name="main/services.html")

def contact(request):
    return render(request=request, template_name="main/contact.html")

def search(request):
    if request.method == "POST":
        form = LandForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)

            # Things to do before save
            hash_object = {
                'Land_state': data.Land_state,
                'Land_district': data.Land_district,
                'Land_taluk': data.Land_taluk,
                'Land_village': data.Land_village,
                'Land_survey_number': data.Land_survey_number,
                'Land_subdivision_number': data.Land_subdivision_number
            }

            search_hash = compute_hash(hash_object)

            object_list = Transaction.objects.filter(
                Q(Land_hash__icontains=search_hash)
            )

            return render(request=request, template_name="main/results.html", context={'object_list': object_list, 'query': search_hash}  )
    else:
        form = LandForm()
    return render(request=request, template_name="main/search.html", context={'form': form})

class SearchResultsView(ListView):
    model = Transaction
    template_name="main/results.html"

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Transaction.objects.filter(
            Q(LandHolder_aadhaar__icontains=query)
        )
        return object_list

    def get_context_data(self,**kwargs):
        context = super(SearchResultsView,self).get_context_data(**kwargs)
        context["query"] = self.request.GET.get('q')
        return context

def manage(request):
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
            update()
            return redirect(to='main:manage')
    else:
        form = ZeroForm()
    return render(request=request, template_name="main/manage.html", context={'form': form})

def register(request):
    if request.method == "POST":
        form = LandDetailsForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)

            # Things to do before save
            hash_object = {
                'Land_state': data.Land_state,
                'Land_district': data.Land_district,
                'Land_taluk': data.Land_taluk,
                'Land_village': data.Land_village,
                'Land_survey_number': data.Land_survey_number,
                'Land_subdivision_number': data.Land_subdivision_number
            }

            my_hash = compute_hash(hash_object)

            data_object = {
                'transaction_id': str(data.transaction_id),

                'LandHolder_aadhaar': data.LandHolder_aadhaar,

                'Land_state': data.Land_state,
                'Land_district': data.Land_district,
                'Land_taluk': data.Land_taluk,
                'Land_village': data.Land_village,
                'Land_survey_number': data.Land_survey_number,
                'Land_subdivision_number': data.Land_subdivision_number,

                'Land_hash' : my_hash
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
        form.fields['LandHolder_aadhaar'].widget.attrs['maxlength'] = '20'
    return render(request=request, template_name="main/register.html", context={'form': form})
