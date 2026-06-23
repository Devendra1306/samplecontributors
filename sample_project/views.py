import os
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI')
try:
    client = MongoClient(MONGO_URI)
    db = client['sample_contributions']
    collection = db['contributors']
except Exception as e:
    print("Could not connect to MongoDB:", e)
    collection = None

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'sample@admin123')

@csrf_exempt
def index(request):
    success = False
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if collection is not None and name and phone and email and role:
            collection.insert_one({
                'name': name,
                'phone': phone,
                'email': email,
                'role': role
            })
            success = True

    return render(request, 'index.html', {'success': success})


@csrf_exempt
def admin_panel(request):
    error = None

    # Handle login
    if request.method == "POST" and 'password' in request.POST:
        if request.POST.get('password') == ADMIN_PASSWORD:
            request.session['admin_auth'] = True
        else:
            error = "Incorrect password. Please try again."

    # Handle logout
    if request.GET.get('logout'):
        request.session.flush()
        return redirect('/admin-panel/')

    # Check auth
    if not request.session.get('admin_auth'):
        return render(request, 'admin_login.html', {'error': error})

    # Fetch contributors
    contributors = []
    total = 0
    search = request.GET.get('search', '').strip()

    if collection is not None:
        query = {}
        if search:
            query = {
                '$or': [
                    {'name': {'$regex': search, '$options': 'i'}},
                    {'email': {'$regex': search, '$options': 'i'}},
                    {'role': {'$regex': search, '$options': 'i'}},
                ]
            }
        docs = list(collection.find(query).sort('_id', -1))
        total = collection.count_documents({})
        for doc in docs:
            doc['id'] = str(doc['_id'])
            contributors.append(doc)

    return render(request, 'admin_panel.html', {
        'contributors': contributors,
        'total': total,
        'search': search,
        'count': len(contributors),
    })
