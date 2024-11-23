from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

# Create your views here.


def home(request):
    context = {'title': "Welcome Home"}
    return render(request, 'home/index.html', context)


def about_us(request):
    context = {'title': "About us"}
    return render(request, 'home/about-us.html', context)


def service(request):
    context = {'title': "Our Services"}
    return render(request, 'home/services.html', context)


def loan(request):
    context = {'title': "Our Loans"}
    return render(request, 'home/loan.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your message has been sent successfully!')
            form = ContactForm()  # Reinitialize form to clear it after successful submission
        else:
            messages.error(request, 'Cannot send your message!')
    else:
        form = ContactForm()

    context = {'title': "Contact Us", 'form': form}
    return render(request, 'home/contact.html', context)


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)


def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)


def handler400(request, exception):
    return render(request, 'errors/400.html', status=400)
