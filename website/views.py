from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import SignUpForm, AddRecordForm
from django.http import JsonResponse
from .models import Record

def home(request):
    # Grab all records in the Records Table
    records = Record.objects.all()

    # Check to see if Logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully Logged In!")
            return redirect('home')
        else:
            messages.success(request, "Error Logging in, Please try again!")
            return redirect('home')

    return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
	if request.user.is_authenticated:
		#look up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})

	else:
		messages.success(request, "You Must Be Logged In To View That Page..")
		return redirect('home')



def delete_records(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids[]')
        Record.objects.filter(id__in=ids).delete()
        return JsonResponse({"message": "Selected records deleted successfully."})
    return JsonResponse({"message": "Invalid request"}, status=400)


def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Records Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Delete!")
		return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')

		return render(request, 'add_record.html', {'form': form})
	else:
		messages.success(request, "You must be logged in...")
		return redirect('home')


def clean(self):
    if self.marital_status == "Single" and self.fullname_spouse not in [None, "", "N/A"]:
        raise ValidationError("A single person cannot have a spouse name.")


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form': form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

