from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def seller_index(request):
    # try:
    if(1):
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        ordered_products_objs = OrderedProducts.objects.all()
        seller_ordered_products_list = []
        purchased_date = []
        buyers = []
        total_sales = 0
        account_balance = 0
        purchased_product_quantity = []
        for i in ordered_products_objs:
            if i.product.seller == seller_obj:
                seller_ordered_products_list.append(i)
                buyers.append(i.my_order.buyer)
                purchased_date.append(i.my_order.purchased_date)
                print(int(i.total_amount/float(i.product.price)))
                purchased_product_quantity.append(int(i.total_amount/float(i.product.price)))
                total_sales = total_sales + int(i.total_amount/float(i.product.price))
                account_balance = account_balance + i.total_amount
                

        my_list = list(zip(seller_ordered_products_list,buyers,purchased_date,purchased_product_quantity))

        print(my_list)


        return render(request, 'seller-index.html',{'seller_obj':seller_obj,'my_list':my_list,'total_sales':total_sales,'account_balance':account_balance,'total_clients':len(set(buyers))})
    # except:
    else:
        return render(request, 'seller-login.html',{'msg':'please login to your account'})
    

def buttons(request):
    try:
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'buttons.html',{'seller_obj':seller_obj})
    except:
        return render(request, 'seller-login.html',{'msg':'please login to your account'})


def forms(request):
    try:
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'forms.html',{'seller_obj':seller_obj})
    except:
        return render(request, 'seller-login.html',{'msg':'please login to your account'})







# ------------------------------Seller Registration------------------------------------------

def seller_register(request):
    if request.method == 'POST':
        try:
            seller_obj = Seller.objects.get(email = request.POST['email'])
            return render(request, 'create-account.html',{'msg':'account already registered!'})
        except:
            if request.POST['password'] == request.POST['repassword']:
                global seller_data_dict
                seller_data_dict = {
                    'user_name' : request.POST['user_name'],
                    'mobile':request.POST['mobile'],
                    'email': request.POST['email'],
                    'password' : request.POST['password']
                }
                global seller_gotp
                seller_gotp = random.randint(1000,9999)
                subject = 'OTP verification by Coza Store'
                message = f'hello {seller_data_dict["user_name"]},\nYour otp is {seller_gotp}'
                from_email = settings.EMAIL_HOST_USER
                r_list = [seller_data_dict['email']]
                send_mail(subject,message,from_email,r_list)
                return render(request, 'seller-otp.html',{'msg':'check you mail box'})
            else:
                return render(request, 'create-account.html',{'msg':'Both password does not match'})
    else:
        return render(request,'create-account.html')
    
    
def seller_otp(request):
    if request.method == 'POST':
        try:
            seller_data_dict
            if int(seller_gotp) == int(request.POST['s_otp']):
                Seller.objects.create(
                    user_name = seller_data_dict['user_name'],
                    email = seller_data_dict['email'],
                    mobile = seller_data_dict['mobile'],
                    password = seller_data_dict['password']
                )
                return render(request, 'seller-login.html',{'msg':'account created Successfully'})
            else:
                return render(request,'seller-otp.html',{'msg':'password does not match'})
        except:
            return render(request, 'create-account.html',{'msg':'You need to register first'})
    else:
        return render(request,'seller-otp.html')
    

def seller_login(request):
    if request.method == 'GET':
        return render(request, 'seller-login.html')
    else:
        try:
            seller_obj = Seller.objects.get(email = request.POST['email'])
            if seller_obj.password == request.POST['password']:
                request.session['seller_email'] = seller_obj.email
                return redirect('seller_index')
            else:
                return render(request, 'seller-login.html',{'msg':'Wrong password'})
        except:
            return render(request, 'seller-login.html',{'msg':f'{request.POST["email"]} does not exist'})
        

def seller_logout(request):
    try:
        request.session['email']
        del request.session['seller_email']
        return redirect('seller_index')
    except:
        return redirect('seller_index')
    

def seller_edit_profile(request):
    changes_applied = False
    try:
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        if request.method == 'POST':
            seller_obj.user_name = request.POST['user_name']
            seller_obj.mobile = request.POST['mobile']
            seller_obj.address = request.POST['address']
            try:
                seller_obj.pic = request.FILES['pic']
                seller_obj.save()
                changes_applied = True
                return render(request,'seller-edit-profile.html',{'msg':'profile successfully updated','seller_data':seller_obj,'changes_applied':changes_applied})
            except:
                seller_obj.save()
                changes_applied = True
                return render(request,'seller-edit-profile.html',{'msg':'profile successfully updated','seller_data':seller_obj,'changes_applied':changes_applied})
        else:
            return render(request, 'seller-edit-profile.html',{'seller_data':seller_obj})
    except:
        return render(request, 'seller-login.html',{'msg':'login to your account'})
    



def seller_forgot_password(request):
    if request.method == 'POST':
        try:
            seller_obj = Seller.objects.get(email=request.POST['email'])
            subject = 'Get Password!!'
            message = f'hello{seller_obj.user_name},\nYour password is {seller_obj.password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            send_mail(subject, message, from_email, recipient_list)
            return render(request, 'seller_forgot_password.html', {'seller_data': seller_obj, 'msg': 'check your mail box'})
        except:
            return render(request, 'seller_forgot_password.html', {'msg': f'{request.POST["email"]} is not registered'})
    else:
        return render(request, 'seller_forgot_password.html')






def seller_reset_password(request):
    flag = False
    try:
        seller_obj = Seller.objects.get(email=request.session['seller_email'])
        if request.method == 'GET':
            return render(request, 'seller_reset_password.html', {'seller_data': seller_obj, })
        else:
            if seller_obj.password == request.POST['old_password']:
                if request.POST['new_password'] == request.POST['re_new_password']:
                    seller_obj.password = request.POST['new_password']
                    flag = True
                    seller_obj.save()
                    return render(request, 'seller_reset_password.html', {'seller_data': seller_obj, 'msg': 'Password reset Successfully!!', 'flag': flag})
                else:
                    return render(request, 'seller_reset_password.html', {'seller_data': seller_obj, 'msg': 'Both password does not match'})
            else:
                return render(request, 'seller_reset_password.html', {'seller_data': seller_obj, 'msg': 'Old password is wrong'})
    except:
        return render(request, 'seller_login.html')





def add_product(request):
    try:
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        if request.method == 'POST':
            Product.objects.create(
                product_name = request.POST['product_name'],
                price = request.POST['price'],
                des = request.POST['des'],
                product_stock = request.POST['stock'],
                category = request.POST['field'],
                product_pic = request.FILES['product_pic'],
                seller = seller_obj
            )
            return render(request, 'add-product.html',{'msg':'product added successfully','seller_obj':seller_obj})
        else:
            p1 = Product()
            choices =  p1.product_choice
            return render(request, 'add-product.html',{'seller_obj':seller_obj,'choices':choices})
    except:
        return render(request, 'seller-login.html',{'msg':'please login to your account'})
    


def show_product(request):
    try:
    # if(1):
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        product_obj = Product.objects.filter(seller = seller_obj)
        print(product_obj)
        return render(request, 'show-product.html',{'seller_obj':seller_obj,'product_obj':product_obj})
    except:
    # else:
        return render(request, 'seller-login.html',{'msg':'please login to your account'})
    


def edit_product(request,pk):
    try:
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        product_obj =  Product.objects.get(id=pk)
        if request.method == 'POST':
            product_obj.product_name = request.POST['product_name']
            product_obj.product_stock = request.POST['product_stock']
            product_obj.price = request.POST['price']
            product_obj.des = request.POST['des']
            product_obj.category = request.POST['field']
            try:
                product_obj.product_pic = request.FILES['product_pic']
                product_obj.save()
                return render(request, 'edit-product.html',{'msg':'Changes Applied Successfully','product_obj':product_obj})
            except:
                product_obj.save()
                return render(request, 'edit-product.html',{'msg':'Changes Applied Successfully','product_obj':product_obj})
        else:
            return render(request, 'edit-product.html', {'seller_obj':seller_obj,'product_obj':product_obj})
    except:
        return render(request, 'seller-login.html',{'msg':'please login first'})

def delete_product(request,pk):
    try:
    # if(1):
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        product_obj = Product.objects.get(id=pk)
        product_obj.delete()
        return redirect('show_product')
    # else:
    except:
        return render(request, 'seller-login.html',{'msg':'please login first'})
    



def ordered_products(request):
    # try:
    if(1):
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        ordered_products_objs = OrderedProducts.objects.all()
        seller_ordered_products_list = []
        purchased_date = []
        buyers = []
        total_sales = 0
        account_balance = 0
        purchased_product_quantity = []
        for i in ordered_products_objs:
            if i.product.seller == seller_obj:
                seller_ordered_products_list.append(i)
                buyers.append(i.my_order.buyer)
                purchased_date.append(i.my_order.purchased_date)
                print(int(i.total_amount/float(i.product.price)))
                purchased_product_quantity.append(int(i.total_amount/float(i.product.price)))
                total_sales = total_sales + int(i.total_amount/float(i.product.price))
                account_balance = account_balance + i.total_amount
                

        my_list = list(zip(seller_ordered_products_list,buyers,purchased_date,purchased_product_quantity))

        print(my_list)


        return render(request, 'ordered-products.html',{'seller_obj':seller_obj,'my_list':my_list,'total_sales':total_sales,'account_balance':account_balance,'total_clients':len(set(buyers))})
    # except:
    else:
        return render(request, 'ordered-products.html',{'msg':'please login to your account'})