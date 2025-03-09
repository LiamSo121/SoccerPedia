from django.shortcuts import redirect

def redirect_to_map(request):
    return redirect("http://localhost:3000/stadiumsmap/")