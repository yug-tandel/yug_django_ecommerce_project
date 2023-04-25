from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import random
from . models import *
from django.core.exceptions import ObjectDoesNotExist
from seller.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.


def index(request):
    if request.method == 'POST':
        a = request.POST['num-product']
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'index.html', {'buyer_data': buyer_obj})
    except:
        return render(request, 'index.html')



def about(request):
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'about.html', {'buyer_data': buyer_obj})
    except:
        return render(request, 'about.html')


def contact(request):
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'contact.html', {'buyer_data': buyer_obj})
    except:
        return render(request, 'contact.html')


def product_detail(request):
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'product-detail.html', {'buyer_data': buyer_obj})
    except:
        return render(request, 'product-detail.html')


def blog(request):
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'blog.html', {'buyer_data': buyer_obj})
    except:
        return render(request, 'blog.html')


def blog_detail(request):
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        return render(request, 'blog-detail.html', {'buyer_data': buyer_obj})
    except:
        return render(request, 'blog-detail.html')


# ----------------------Emaill Verification-----------------------------------

def register(request):
    if request.method == 'POST':
        try:
            buyer_obj = Buyer.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {'msg': 'email already registered'})
        except:
            if request.POST['password'] == request.POST['repassword']:
                global user_info
                user_info = {
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name'),
                    'mobile_num': request.POST.get('mobile'),
                    'email': request.POST.get('email'),
                    'password': request.POST.get('password')
                }
                global generated_otp
                generated_otp = random.randint(1000, 9999)
                subject = 'Registration!'
                message = f'Hello {user_info.get("first_name")},\nYour otp is {generated_otp}'
                from_mail = settings.EMAIL_HOST_USER
                recipient_list = [user_info.get('email')]
                send_mail(subject, message, from_mail, recipient_list)
                return render(request, 'otp.html', {'msg': 'check your mail box to verify otp'})
            else:
                return render(request, 'register.html', {'msg': 'both passwords do not match'})
    else:
        return render(request, 'register.html')


def otp(request):
    if request.method == 'POST':
        if int(generated_otp) == int(request.POST.get('otp')):
            Buyer.objects.create(
                first_name=user_info.get('first_name'),
                last_name=user_info.get('last_name'),
                mobile=user_info.get('mobile_num'),
                email=user_info.get('email'),
                password=user_info.get('password')
            )
            return render(request, 'login.html', {'msg': 'account created successfully'})
        else:
            return render(request, 'otp.html', {'msg': 'otp does not matched'})
    else:
        return render(request, 'otp.html')


def login(request):
    if request.method == 'POST':
        try:
            buyer_obj = Buyer.objects.get(email=request.POST['email'])
            if buyer_obj.password == request.POST.get('password'):
                request.session['email'] = buyer_obj.email
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': 'wrong password'})
        except:
            return render(request, 'login.html', {'msg': 'Email is not registered'})
    else:
        return render(request, 'login.html')


def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return redirect('index')
    except:
        return redirect('index')

# ________________________Email Verification Ended____________________________________________

def forgot_password(request):
    if request.method == 'POST':
        try:
            buyer_obj = Buyer.objects.get(email=request.POST['email'])
            subject = 'Get Password!!'
            message = f'hello{buyer_obj.first_name},\nYour password is {buyer_obj.password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            send_mail(subject, message, from_email, recipient_list)
            return render(request, 'forgot_password.html', {'buyer_data': buyer_obj, 'msg': 'check your mail box'})
        except:
            return render(request, 'forgot_password.html', {'msg': f'{request.POST["email"]} is not registered'})
    else:
        return render(request, 'forgot_password.html')


def edit_profile(request):
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        if request.method == 'GET':
            return render(request, 'edit_profile.html', {'buyer_data': buyer_obj})
        else:    # POST
            buyer_obj.first_name = request.POST.get('first_name')
            buyer_obj.last_name = request.POST.get('last_name')
            buyer_obj.mobile = request.POST.get('mobile')
            buyer_obj.address = request.POST.get('address')
            try:
                buyer_obj.pic = request.FILES['pic']
                buyer_obj.save()
                return render(request, 'edit_profile.html', {'buyer_data': buyer_obj, 'msg': 'Changes Applied !!'})
            except:
                buyer_obj.save()
                return render(request, 'edit_profile.html', {'buyer_data': buyer_obj, 'msg': 'Changes Applied !!'})
    except ObjectDoesNotExist:
        return render(request, 'login.html')


def reset_password(request):
    flag = False
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        if request.method == 'GET':
            return render(request, 'reset_password.html', {'buyer_data': buyer_obj, })
        else:
            if buyer_obj.password == request.POST['old_password']:
                if request.POST['new_password'] == request.POST['re_new_password']:
                    buyer_obj.password = request.POST['new_password']
                    flag = True
                    buyer_obj.save()
                    return render(request, 'reset_password.html', {'buyer_data': buyer_obj, 'msg': 'Password reset Successfully!!', 'flag': flag})
                else:
                    return render(request, 'reset_password.html', {'buyer_data': buyer_obj, 'msg': 'Both password does not match'})
            else:
                return render(request, 'reset_password.html', {'buyer_data': buyer_obj, 'msg': 'Old password is wrong'})
    except:
        return render(request, 'login.html')


wishlist_products = []
cartlist_products = []


def product(request):
    wishlist_products.clear()
    cartlist_products.clear()
    all_product_objs = Product.objects.all()
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        wishlist_objs = Wishlist.objects.filter(buyer=buyer_obj)
        cart_objs = Cart.objects.filter(buyer=buyer_obj)
        wish_len = len(wishlist_objs)
        cart_len = len(cart_objs)
        for i in range(0, wish_len+cart_len):
            if i >= wish_len and i >= cart_len:
                break
            else:
                # cart maate
                if i >= cart_len:
                    pass
                else:
                    try:
                        buyer_cart_obj = Cart.objects.filter(
                            buyer=buyer_obj).get(product=cart_objs[i].product)
                        cartlist_products.append(buyer_cart_obj.product)
                    except:
                        try:
                            cartlist_products.remove(cart_objs[i].product)
                        except:
                            pass

                # wishlist maate
                if i >= wish_len:
                    pass
                else:
                    try:
                        buyer_wishlist_obj = Wishlist.objects.filter(
                            buyer=buyer_obj).get(product=wishlist_objs[i].product)
                        # Wishlist.objects.
                        wishlist_products.append(buyer_wishlist_obj.product)
                    except:
                        try:
                            wishlist_products.remove(wishlist_objs[i].product)
                        except:
                            pass
        return render(request, 'product.html', {'buyer_data': buyer_obj, 'all_product_objs': all_product_objs,
                                                'all_product_objs_len': len(all_product_objs), 'cartlist_products': cartlist_products, 'wishlist_products': wishlist_products})
    except:
        return render(request, 'login.html', {'msg': 'please login first', 'all_product_objs': all_product_objs})


def my_wishlist(request):
    try:
        cart_pro_list = []
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        buyer_wishlist_objs = Wishlist.objects.filter(buyer=buyer_obj)
        buyer_cartlist_objs = Cart.objects.filter(buyer=buyer_obj)

        for i in buyer_cartlist_objs:
            if i.product not in cart_pro_list:
                cart_pro_list.append(i.product)
            else:
                pass
        return render(request, 'wishlist.html', {'buyer_wishlist_objs': buyer_wishlist_objs, 'buyer_data': buyer_obj, 'cart_pro_list': cart_pro_list})
    except:
        return redirect('login')


def add_to_wishlist(request, pk):
    all_product_objs = Product.objects.all()
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        single_pro_obj = Product.objects.get(id=pk)
        try:
            buyer_wishlist_objs = Wishlist.objects.filter(
                buyer=buyer_obj).get(product=single_pro_obj)
            wishlist_products.append(single_pro_obj)
            return redirect('product')
        except:
            Wishlist.objects.create(
                buyer=buyer_obj,
                product=single_pro_obj
            )
            wishlist_products.append(single_pro_obj)
            return render(request, 'product.html', {'buyer_obj': buyer_obj, 'all_product_objs': all_product_objs, 'wishlist_products': wishlist_products})
    except:
        return redirect('login')


def remove_from_wishlist(request, pk, string):
    all_product_objs = Product.objects.all()
    buyer_obj = Buyer.objects.get(email=request.session['email'])
    if string == 'wishlist':
        single_wishlist_product = Wishlist.objects.filter(
            buyer=buyer_obj).get(id=pk)
        single_wishlist_product.delete()
        return redirect('my_wishlist')
    else:
        single_pro_obj = Product.objects.get(id=pk)
        single_wishlist_product = Wishlist.objects.filter(
            buyer=buyer_obj).get(product=single_pro_obj)
        single_wishlist_product.delete()
        return redirect('product')


def add_to_cart(request, pk, string):
    if request.method == 'POST':
        try:
            buyer_obj = Buyer.objects.get(email=request.session['email'])
            single_product_obj = Product.objects.get(id=pk)
            try:
                cart_object = Cart.objects.filter(buyer=buyer_obj).get(product=single_product_obj)
                
                return redirect('product')
            except:
                Cart.objects.create(
                    product=single_product_obj,
                    buyer=buyer_obj,
                    quantity=request.POST['quantity']
                )
                if string == 'product':
                    return redirect('product')
                else:
                    return redirect('my_wishlist')
        except:
            return redirect('login')
    else:
        return redirect('product')


def shoping_cart(request):
    try:
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        cart_objs = Cart.objects.filter(buyer=buyer_obj)
        if cart_objs:
            pass
        else:
            return render(request, 'shoping-cart.html',{'buyer_data':buyer_obj,'empty':True})
        cart_product_price_list = []
        count = 0
        global total_price
        total_price = 1
        for item in cart_objs:
            cart_product_price_list.append(
                float(item.product.price * item.quantity))
            total_price = total_price + (float(item.product.price) * item.quantity)
        my_list = list(zip(cart_objs, cart_product_price_list))
        currency = 'INR'
        amount = float(total_price*100)  - 1

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                           currency=currency,
                                                           payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'


        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context.update(
            {'buyer_data': buyer_obj, 'my_list': my_list, 'total_price': total_price-1})
        return render(request, 'shoping-cart.html', context=context)
    except:
        return redirect('login')


def remove_from_cart(request, pk):
    try:       
        buyer_obj = Buyer.objects.get(email=request.session['email'])
        single_product = Product.objects.get(id=pk)
        cart_obj = Cart.objects.filter(
            buyer=buyer_obj).get(product=single_product)
        cart_obj.delete()
        return redirect('shoping_cart')
    except:
        return redirect('login')



# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = float(total_price*100) - 1 # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # personal logic code
                    buyer_obj = Buyer.objects.get(email = request.session['email'])
                    cart_objs = Cart.objects.filter(buyer = buyer_obj)

                    my_order_obj = MyOrders.objects.create(
                        buyer = buyer_obj
                    )

                    for i in cart_objs:
                        product_obj = Product.objects.get(id = i.product.id)
                        product_obj.product_stock = product_obj.product_stock - i.quantity
                        product_obj.save()
                        OrderedProducts.objects.create(
                            my_order = my_order_obj,
                            product = product_obj,
                            total_amount = i.product.price * i.quantity
                        )

                        # i.product.product_stock = i.product.product_stock - i.quantity
                    cart_objs.delete()
                
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
