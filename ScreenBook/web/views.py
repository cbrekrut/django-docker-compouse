from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .models import App
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import AppCategory, OSCategory, ScreenType, UIElement
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from aiogram import Bot
import asyncio
from aiogram.client.default import DefaultBotProperties
from yookassa import Configuration, Payment
from yookassa.domain.common import PaymentMethodType
from django.utils import timezone
import uuid

BOT_TOKEN = '7825512220:AAHk-zRbFxjAD-ZSYSnBWgNnAfSKznnynpQ'
CHAT_ID = -4877002860
YOOKASSA_SHOP_ID = "1100145"
YOOKASSA_SECRET_KEY = "test_PAax1WP-2Izhe18vostgxtL9Jl89ALD3S6Tjqc62NGg"

Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY

@csrf_exempt
@login_required
def start_payment(request):
    user = request.user
    payment = Payment.create({
        "amount": {
            "value": "1000.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri('/')
        },
        "capture": True,
        "description": f"Подписка для {user.email}",
        "metadata": {
            "user_id": user.id
        },
        "receipt": {
            "customer": {
                "email": user.email
            },
            "items": [
                {
                    "description": "Подписка на 6 месяцев",
                    "quantity": 1.0,
                    "amount": {
                        "value": "1000.00",
                        "currency": "RUB"
                    },
                    "vat_code": 1 
                }
            ]
        }
    }, uuid.uuid4())

    return redirect(payment.confirmation.confirmation_url)

@csrf_exempt
def payment_webhook(request):
    import json
    from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotification

    event_json = json.loads(request.body)
    notification = WebhookNotification(event_json)
    
    if notification.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
        payment_object = notification.object
        user_id = payment_object.metadata.get("user_id")
        print(">>> payment metadata:", payment_object.metadata)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)

        now = timezone.now()
        if user.subscription_end and user.subscription_end > now:
            user.subscription_end += timezone.timedelta(days=180)
        else:
            user.subscription_start = now
            user.subscription_end = now + timezone.timedelta(days=180)

        user.is_subscribed = True
        user.save()

    return JsonResponse({'ok': True})

@csrf_exempt
def submit_review(request):
    if request.method == 'POST':
        positive = request.POST.get('positive', '').strip()
        negative = request.POST.get('negative', '').strip()
        contact = request.POST.get('contact', '').strip()

        message = f"""
<b>Новый отзыв из ScreenBook</b>
❤️ <b>Что нравится:</b> {positive or '—'}
🔧 <b>Что улучшить:</b> {negative or '—'}
👤 <b>Контакт:</b> {contact or '—'}
        """.strip()

        async def send_message():
            bot = Bot(
                token=BOT_TOKEN,
                default=DefaultBotProperties(parse_mode="HTML")
            )
            await bot.send_message(chat_id=CHAT_ID, text=message)
            await bot.session.close()

        asyncio.run(send_message())
    return redirect('home')

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        issue = request.POST.get('issue', '').strip()
        contact = request.POST.get('contact', '').strip()

        message = f"""
<b>Обратная связь по скриншоту</b>
🛠 <b>Проблема:</b> {issue or '—'}
👤 <b>Контакт:</b> {contact or '—'}
        """.strip()

        async def send_message():
            bot = Bot(
                token=BOT_TOKEN,
                default=DefaultBotProperties(parse_mode="HTML")
            )
            await bot.send_message(chat_id=CHAT_ID, text=message)
            await bot.session.close()

        asyncio.run(send_message())

    return redirect('home')

@csrf_exempt
def filter_apps_ajax(request):
    tab = request.GET.get('tab', 'apps')
    viewmode = request.GET.get('viewmode', '')  # ← новое
    os_filter = request.GET.get('os', 'iOS')
    screen_type = request.GET.get('screen_type')
    app_category = request.GET.get('app_category')
    ui_element = request.GET.get('ui_element')
    term = request.GET.get('q', '').strip()

    apps = App.objects.all()

    # Прежняя фильтрация
    if tab == 'screen':
        apps = apps.filter(screen=True)
    elif tab == 'animation':
        apps = apps.filter(animation=True)

    # Новая фильтрация по viewmode
    if viewmode == 'screens':
        apps = apps.filter(screen=True)
    elif viewmode == 'animations':
        apps = apps.filter(animation=True)

    if os_filter:
        apps = apps.filter(os_category__name__iexact=os_filter)

    if screen_type:
        apps = apps.filter(screen_type__id=screen_type)
    if app_category:
        apps = apps.filter(app_category__id=app_category)
    if ui_element:
        apps = apps.filter(ui_element__id=ui_element)

    if term:
        apps = apps.filter(
            Q(title__icontains=term) |
            Q(screen_type__name__icontains=term) |
            Q(app_category__name__icontains=term) |
            Q(ui_element__name__icontains=term) |
            Q(os_category__name__icontains=term)
        ).distinct()

    html = render_to_string('partials/app_list.html', {'apps': apps}, request=request)

    return JsonResponse({'html': html})

@csrf_exempt
def index(request):
    query = request.GET.get('q', '')
    os_filter = request.GET.get('os', 'iOS')
    tab = request.GET.get('tab', 'apps')
    active_tab = request.GET.get('tab', 'login')

    login_form = LoginForm(request)
    register_form = RegistrationForm()

    if request.method == 'POST':
        if 'login' in request.POST.get('form_type', ''):
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')
            active_tab = 'login'
        elif 'register' in request.POST.get('form_type', ''):
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('home')
            active_tab = 'register'

    apps = App.objects.all()

    if tab == 'screen':
        apps = apps.filter(screen=True)
    elif tab == 'animation':
        apps = apps.filter(animation=True)

    if query:
        apps = apps.filter(title__icontains=query)

    if os_filter:
        apps = apps.filter(os_category__name__iexact=os_filter)

    context = {
        "apps": apps,
        "search_query": query,
        "selected_os": os_filter,
        "selected_tab": tab,
        'now': timezone.now(),
        "login_form": login_form,
        "register_form": register_form,
        "active_tab": active_tab,
        "filter_screen_types": ScreenType.objects.all(),
        "filter_app_categories": AppCategory.objects.all(),
        "filter_ui_elements": UIElement.objects.all(),
    }
    return render(request, "index.html", context)

@csrf_exempt
def login_view(request):
    login_form = LoginForm(request, data=request.POST or None)
    register_form = RegistrationForm()
    apps = App.objects.all()
    os_filter = request.GET.get('os', 'iOS')
    tab = request.GET.get('tab', 'apps')

    if request.method == 'POST' and login_form.is_valid():
        user = login_form.get_user()
        login(request, user)
        return redirect('home')

    context = {
        "apps": apps,
        "selected_os": os_filter,
        "selected_tab": tab,
        "login_form": login_form,
        "register_form": register_form,
        "active_tab": 'login',
        "filter_screen_types": ScreenType.objects.all(),
        "filter_app_categories": AppCategory.objects.all(),
        "filter_ui_elements": UIElement.objects.all(),
    }
    return render(request, "index.html", context)

@csrf_exempt
def register_view(request):
    login_form = LoginForm(request)
    register_form = RegistrationForm(request.POST or None)
    apps = App.objects.all()
    os_filter = request.GET.get('os', 'iOS')
    tab = request.GET.get('tab', 'apps')

    if request.method == 'POST' and register_form.is_valid():
        user = register_form.save()
        login(request, user)
        return redirect('home')

    context = {
        "apps": apps,
        "selected_os": os_filter,
        "selected_tab": tab,
        "login_form": login_form,
        "register_form": register_form,
        "active_tab": 'register',
        "filter_screen_types": ScreenType.objects.all(),
        "filter_app_categories": AppCategory.objects.all(),
        "filter_ui_elements": UIElement.objects.all(),
    }
    return render(request, "index.html", context)

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('home')

@csrf_exempt
@login_required
def account_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)  
        return redirect('account')
    return render(request, 'account.html', {'form': CustomPasswordChangeForm(request.user), 'now': timezone.now()})

@csrf_exempt
def app_detail(request, slug):
    app = get_object_or_404(App, slug=slug)
    viewmode = request.GET.get('viewmode', 'screens')
    images = app.images.all()
    videos = app.videos.all()

    context = {
        'app': app,
        'images': images,
        'videos': videos,
        'selected_tab': viewmode,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/gallery_block.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'app_detail.html', context)