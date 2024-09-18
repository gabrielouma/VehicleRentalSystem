from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth import logout
from django.db.models import Q
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.
def clear_messages(request):
    # Clear any previous messages
    storage = messages.get_messages(request)
    for _ in storage:
        pass

def index(request):
    clear_messages(request)
    all_vehicles = Vehicles.objects.filter(is_available=True)
    vehicles = []
    for vehicle in all_vehicles:
        dealer = Users.objects.get(user_id=vehicle.dealer_id)
        vehicles.append({'vehicle': vehicle, 'dealer': dealer})
    return render(request, "index.html", {'vehicles':vehicles})

def aboutpage(request):
    return render(request,'about.html')

def contactus(request):
    clear_messages(request)
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phoneno = request.POST['phoneno']
        emailid = request.POST['emailid']
        message = request.POST['messages']

        contact_us = Contactus(firstname=firstname, lastname=lastname, phoneno=phoneno, emailid=emailid, message=message)
        contact_us.save()
        messages.success(request, 'Successfully Sent')
        return redirect('/contactus')
    return render(request, 'contactus.html')

def user_register(request):
    clear_messages(request)
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST['gender']
        phoneno = request.POST['phoneno']
        emailid = request.POST['emailid']
        password = request.POST['password']
        secure_question = request.POST['secure_question']
        answer = request.POST['answer']

        # Check if the phone number or email is already registered
        user_data = Users.objects.filter(Q(phoneno=phoneno) | Q(emailid=emailid)).first()

        
        if user_data:
            messages.error(request, 'This phone number or emailid has already registered')
            
        else:
            add_user = Users(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                phoneno=phoneno,
                emailid=emailid,
                password=password,
                secure_question=secure_question,
                answer=answer
            )
            add_user.save()
            
            messages.success(request, 'You are successfully registered')
            return redirect('/user_register')
    return render(request, 'register.html')

def password_recovery(request):
    clear_messages(request)
    
    user_pw = None
    if request.method == 'POST':
        phone_email = request.POST.get('phone_email')
        question = request.POST.get('secure_question')
        answer = request.POST.get('answer')
        
        if phone_email.isnumeric():
            # Handle phone number case
            lookup = Q(phoneno=phone_email)
        else:
            # Handle email case
            lookup = Q(emailid=phone_email)
        
        try:
            # Fetch user data based on the lookup criteria
            user_data = Users.objects.get(lookup)
            
            if user_data.secure_question == question and user_data.answer == answer:
                user_pw = user_data.password
                messages.success(request, 'Password recovery successful. Check below 👇')
                # Render the template instead of redirecting to preserve user_pw
                return render(request, 'recovery.html', {'user_pw': user_pw})
            else:
                messages.error(request, 'Invalid secure question or answer. Please try again.')
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist')
    return render(request, 'recovery.html',{'user_pw':user_pw})

def customer_login(request):
    clear_messages(request)
    
    if request.method == 'POST':
        uphoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        
        try:
            user_data = Users.objects.get(phoneno=uphoneno)
            if user_data and user_data.password == password:
                user_data.status = 'Active now'
                user_data.save()
                request.session['user_id'] = user_data.user_id
                request.session['login_type'] = "customer"
                messages.success(request, 'Login successfully as customer')
                return redirect('/select_vehicle')
            else:
                messages.error(request, 'Invalid password')
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist')
    return render(request, 'customer_login.html')

def dealer_login(request):
    clear_messages(request)
    
    if request.method == 'POST':
        uphoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        
        try:
            user_data = Users.objects.get(phoneno=uphoneno)
            if user_data and user_data.password == password:
                user_data.status = 'Active now'
                user_data.save()
                request.session['user_id'] = user_data.user_id
                request.session['login_type'] = "dealer"
                messages.success(request, 'Login successfully as dealer')
                return redirect('/dealer_home')
            else:
                messages.error(request, 'Invalid password')
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist')
    return render(request, 'dealer_login.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('/')

def customer_home(request):
    clear_messages(request)
    
    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="customer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/customer_login')
    
    user = Users.objects.get(user_id=user_id)

    all_vehicles = Vehicles.objects.filter(is_available=True).exclude(dealer_id=user_id)
    vehicles = []
    for vehicle in all_vehicles:
        dealer = Users.objects.get(user_id=vehicle.dealer_id)
        vehicles.append({'vehicle': vehicle, 'dealer': dealer})
    return render(request, 'customer_home.html', {'vehicles':vehicles, 'user':user})

def dealer_home(request):
    clear_messages(request)
    
    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="dealer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/dealer_login')
    
    user = Users.objects.get(user_id=user_id)
    vehicles = Vehicles.objects.filter(dealer_id=user_id)
    return render(request, 'dealer_home.html', {'vehicles':vehicles, 'user':user})

def add_vehicle(request):
    clear_messages(request)
    
    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="dealer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/dealer_login')
    
    logo_name = "logo.png"
    vehicle_dealer = Users.objects.get(user_id=user_id)
    if request.method == "POST":
        if 'name' in request.FILES:
            try:
                vehicle_name = request.POST['vehicle_name']
                capacity = request.POST['capacity']
                rent = request.POST['rent']
                city = request.POST['city']
                vehicle_type = request.POST['vehicle_type']

                image = request.FILES['name']
                root = settings.MEDIA_ROOT_2
                fs = FileSystemStorage(location=root)
                final_file_name = fs.save(image.name, image)
                dealer_id = vehicle_dealer.user_id

                vehicle = Vehicles(
                    name=vehicle_name,
                    image=final_file_name,
                    capacity=capacity,
                    rent=rent,
                    location=city,
                    vehicle_type=vehicle_type,
                    dealer_id=dealer_id
                )
                vehicle.save()

                messages.success(request, 'Vehicle Added')
                return redirect('/add_vehicle')
            except Exception as e:
                messages.error(request, 'Upload vehicle image')
        else:
            messages.error(request, "'name' not in FILES")
    return render(request, 'add_vehicle.html', {'logo_name': logo_name, 'user':vehicle_dealer})

def vehicle_rent(request):
    clear_messages(request)
    
    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="customer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/customer_login')
    
    id = request.POST['id']
    user = Users.objects.get(user_id=user_id)
    vehicle = Vehicles.objects.get(vehicle_id=id)
    dealer = Users.objects.get(user_id=vehicle.dealer_id)
    return render(request, 'customer_confirm_order.html', {'vehicle':vehicle, 'user':user, 'dealer':dealer})

def order_details(request):
    clear_messages(request)

    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="customer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/customer_login')
    
    vehicle_id = request.POST['id']
    days = request.POST['days']
    vehicle = Vehicles.objects.get(vehicle_id=vehicle_id)
    user = Users.objects.get(user_id=user_id)
    total_rent = (int(vehicle.rent))*(int(days))
    order_date = datetime.datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')

    vehicle.is_available = False
    vehicle.save()

    order = Orders(
        total_rent=total_rent,
        days=days,
        order_date=order_date,
        dealer_id=vehicle.dealer_id,
        customer_id=user.user_id,
        status="pending",
        location=vehicle.location,
        vehicle_image = vehicle.image,
        vehicle_name = vehicle.name,
        vehicle_type = vehicle.vehicle_type,
        vehicle_id = vehicle_id,
        capacity = vehicle.capacity
    )
    order.save()
    messages.success(request, 'Successfully placed order')
    return redirect('/request_vehicle')

def request_vehicle(request):
    clear_messages(request)

    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="customer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/customer_login')

    user = Users.objects.get(user_id=user_id)
    orders = Orders.objects.filter(
        Q(customer_id=user_id) & (Q(status='pending') | Q(status='accepted'))
    )
    request_vehicles_info = []

    for order in orders:
        dealer = Users.objects.get(user_id=order.dealer_id)
        request_vehicles_info.append({
            'order': order,
            'dealer': dealer
        })
    return render(request, 'vehicle_rent_request.html', {'user':user, 'request_vehicles_info': request_vehicles_info, 'login_type':login_type})

def customer_orders(request):
    clear_messages(request)

    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="customer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/customer_login')
    
    user = Users.objects.get(user_id=user_id)
    all_orders = Orders.objects.filter(customer_id=user.user_id).order_by('-order_id')
    orders = []
    for order in all_orders:
        dealer = Users.objects.get(user_id=order.dealer_id)
        orders.append({'order': order, 'dealer': dealer})
    return render(request, 'customer_orders.html', {'user':user, 'orders':orders})

def delete_order_history(request, ord_id):
    order = Orders.objects.filter(order_id=ord_id)
    # order.delete()
    return redirect("/customer_orders")

def edit_profile(request):
    clear_messages(request)
    
    user_id = request.session.get('user_id')
    login_type = request.session.get('login_type')

    # Check if the user is logged in
    if not user_id:
        messages.error(request, 'Please login first')
        if login_type == "dealer":
            return redirect('/dealer_login')
        else:
            return redirect('/customer_login')
    
    user = Users.objects.get(user_id=user_id)
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        emailid = request.POST.get('emailid')
        secure_option = request.POST.get('secure_option')
        answer = request.POST.get('answer')
        
        user.firstname=firstname
        user.lastname=lastname
        user.phoneno=phoneno
        user.emailid=emailid
        user.password = password
        user.secure_question=secure_option
        user.answer=answer

        if 'name' in request.FILES:
            image = request.FILES['name']
            root = settings.MEDIA_ROOT
            fs = FileSystemStorage(location=root)
            final_file_name = fs.save(image.name, image)
            user.images = final_file_name
        
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('/user_profile')
    return render(request, 'user_profile.html', {'user':user, 'login_type':login_type})

def delete_vehicle(request, v_id):
    vehicle = Vehicles.objects.filter(vehicle_id=v_id)
    vehicle.delete()
    return redirect("/dealer_home")

def edit_vehicle(request, v_id):
    clear_messages(request)

    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="dealer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/dealer_login')
    
    user = Users.objects.get(user_id=user_id)
    vehicle = Vehicles.objects.filter(vehicle_id=v_id)[0]
    if request.method == 'POST':
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_name = request.POST.get('vehicle_name')
        capacity = request.POST.get('capacity')
        rent = request.POST.get('rent')
        city = request.POST.get('city')

        vehicle.vehicle_type=vehicle_type
        vehicle.name=vehicle_name
        vehicle.capacity=capacity
        vehicle.rent=rent
        vehicle.location = city

        if 'name' in request.FILES:
            image = request.FILES['name']
            root = settings.MEDIA_ROOT_2
            fs = FileSystemStorage(location=root)
            final_file_name = fs.save(image.name, image)
            vehicle.image = final_file_name
        
        vehicle.save()
        messages.success(request, 'Vehicle updated successfully')
        return redirect('/dealer_home')
    return render(request, 'edit_vehicle.html', {'user':user, 'vehicle':vehicle})

def dealer_orders(request):
    clear_messages(request)

    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="dealer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/dealer_login')
    
    user = Users.objects.get(user_id=user_id)
    all_orders = Orders.objects.filter(dealer_id=user.user_id).order_by('-order_id')
    orders = []
    for order in all_orders:
        customer = Users.objects.get(user_id=order.customer_id)
        orders.append({'order': order, 'customer': customer})
    return render(request, 'dealer_orders.html', {'user':user, 'orders':orders})

def rented_vehicle(request):
    clear_messages(request)

    login_type = request.session.get('login_type')
    user_id = request.session.get('user_id')

    # Check if the user is logged in
    if not (user_id and login_type=="dealer"):
        logout(request)
        messages.error(request, 'Please login first')
        return redirect('/dealer_login')

    user = Users.objects.get(user_id=user_id)
    orders = Orders.objects.filter(
        Q(dealer_id=user_id) & (Q(status='pending') | Q(status='accepted'))
    )
    rented_vehicles_info = []

    for order in orders:
        customer = Users.objects.get(user_id=order.customer_id)
        rented_vehicles_info.append({
            'order': order,
            'customer': customer
        })
    return render(request, 'vehicle_rent_request.html', {'user':user, 'rented_vehicles_info': rented_vehicles_info})

def complete_rent_request(request):
    clear_messages(request)

    if request.method == 'POST':
        v_id = request.POST.get('v_id')

        try:
            vehicle = Vehicles.objects.get(vehicle_id=v_id)
            vehicle.is_available=True
            vehicle.save()
        except:
            pass

        order = Orders.objects.get(vehicle_id=v_id, status='accepted')
        order.status = "completed"
        order.save()

        dealer = Users.objects.get(user_id=order.dealer_id)
        dealer.earnings += int(order.total_rent)
        dealer.save()
        messages.success(request, 'Vehicle rent completed')
        return redirect('/request_vehicle')

def cancel_rent_request(request):
    clear_messages(request)
    login_type = request.session.get('login_type')

    if request.method == 'POST':
        v_id = request.POST.get('v_id')

        try:
            vehicle = Vehicles.objects.get(vehicle_id=v_id)
            vehicle.is_available=True
            vehicle.save()
        except:
            pass

        order = Orders.objects.get(vehicle_id=v_id, status='pending')
        order.status = "cancelled"
        order.save()

        if login_type == "customer":
            messages.success(request, 'Vehicle request cancelled')
            return redirect('/request_vehicle')
        else:
            messages.success(request, 'Vehicle rent cancelled')
            return redirect('/rented_vehicle')

def accept_rent_request(request):
    clear_messages(request)

    if request.method == 'POST':
        v_id = request.POST.get('v_id')

        order = Orders.objects.get(vehicle_id=v_id, status='pending')
        order.status = "accepted"
        order.save()

        messages.success(request, 'Vehicle rent accepted')
        return redirect('/rented_vehicle')
