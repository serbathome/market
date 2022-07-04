from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from .models import Profile, ProductCategory, Product
from django.contrib.auth.models import User
from django.core import serializers
from django.conf import settings
from decimal import Decimal
from .forms import CartAddProductForm
from django.views.decorators.http import require_POST

# Create your views here


def index(request):
    if request.user.is_authenticated == True:
        user = User.objects.filter(username__exact=request.user).first()
        profile = Profile.objects.filter(user__exact=user).first()
        print(profile)
        return render(request, "web/index.html", {'profile': profile})
    else:
        return render(request, "web/index.html")


def register(request):
    if request.method == "GET":
        return render(request, "web/register.html")
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        zip = request.POST.get('zip')
        # todo: check if such user exists
        user = User.objects.filter(username__iexact=email).first()
        if user is not None:
            return render(request, 'web/error.html', {'reason': 'Such user exists'})
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile = Profile.objects.create(user=user)
        profile.city = city
        profile.zip = zip
        profile.address = address
        profile.province = province
        profile.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'web/error.html', {'reason': 'Unsupported method call'})


def login(request):
    if request.method == "GET":
        return render(request, "web/login.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"{username} {password}")
        if username != "" and password != "":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                do_login(request, user)
                return HttpResponseRedirect("/")
            else:
                return render(request, 'web/error.html', {'reason': 'Authentication failed'})
    else:
        return render(request, 'web/error.html', {'reason': 'Unsupported method call'})


def logout(request):
    if request.user.is_authenticated:
        do_logout(request)
    return HttpResponseRedirect("/")


def profile_update(profile_dict, user, profile):
    print(profile_dict)
    if "first_name" in profile_dict:
        user.first_name = profile_dict['first_name']
    if "last_name" in profile_dict:
        user.last_name = profile_dict['last_name']
    if "address" in profile_dict:
        profile.address = profile_dict['address']
    if "city" in profile_dict:
        profile.city = profile_dict['city']
    if "zip" in profile_dict:
        profile.zip = profile_dict['zip']
    if "isFarmer" in profile_dict:
        profile.isFarmer = profile_dict['isFarmer']
    if "wantMarketingEmails" in profile_dict:
        profile.wantMarketingEmails = profile_dict['wantMarketingEmails']
    if "wantPromoEmails" in profile_dict:
        profile.wantPromoEmails = profile_dict['wantPromoEmails']
    user.save()
    profile.save()


def profile(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("/login")
    else:
        user = User.objects.filter(username__exact=request.user).first()
        profile = Profile.objects.filter(user__exact=user).first()
        if request.method == 'GET':
            return render(request, "web/profile.html", {"user": user, "profile": profile})
        elif request.method == 'POST':
            profile_update(request.POST, user, profile)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'web/error.html', {'reason': 'Unsupported method call'})


# API function calls
def get_categories(request):
    categories = []
    for category in ProductCategory.objects.all():
        categories.append(category.CategoryName)
    return JsonResponse(categories, safe=False)


def get_products(request):
    products = []
    for product in Product.objects.all():
        products.append({
            'CategoryID': product.CategoryID.CategoryName,
            'ProductName': product.ProductName,
            'Measure': product.Measure,
            'Price': product.Price
        })
    return JsonResponse(products, safe=False)

#СОздание класса Корзина
class Cart(object):

    def __init__(self, request):
        #Инициализируем корзину
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        #Добавить продукт в корзину или обновить его количество.
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(product.Price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True    

    def remove(self, product):
        #Удаление товара из корзины.
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        #Перебор элементов в корзине и получение продуктов из базы данных.
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        #Подсчет всех товаров в корзине.
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        #Подсчет стоимости товаров в корзине.
        return sum(Decimal(item['price']) * item['quantity'] for item in
                self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

def product_list(request, category_id=None):
    print(request)
    print(category_id)
    print('112')
    category = None
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    print(request)
    print('products') 
    print (products)      
    print('category') 
    print (category)
    print('categories') 
    print (categories)  
    print('212')
    if category_id:
      category = get_object_or_404(ProductCategory, id = category_id)
      products = products.filter(CategoryID=category)
      print('313')
    print(request)
    print('products') 
    print (products)      
    print('category') 
    print (category)
    print('categories') 
    print (categories)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product,id=id)
    cart_product_form = CartAddProductForm()
    print(cart_product_form)
    print("cart_product_form - end")
    return render(request,
                  'shop/product/detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})




@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    print('CART_add')
    print(product)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('shoping-cart')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shoping-cart')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/shoping-cart.html', {'cart': cart})