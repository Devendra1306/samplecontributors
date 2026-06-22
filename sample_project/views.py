from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb+srv://devendrasagar0988_db_user:DVEx2Q7zBwHMFy2L@cluster0.zlt1etx.mongodb.net/"
try:
    client = MongoClient(MONGO_URI)
    db = client['sample_contributions']
    collection = db['contributors']
except Exception as e:
    print("Could not connect to MongoDB:", e)
    collection = None

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
