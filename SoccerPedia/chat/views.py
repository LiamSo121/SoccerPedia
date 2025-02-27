from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def redirect_to_chat(request):
    return redirect("http://localhost:3000/")

@login_required()
def get_authenticated_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"username": request.user.username})
    return JsonResponse({"error": "Not authenticated"}, status=401)

@login_required
def get_messages(request, room_name):
    try:
        messages = Message.objects.filter(room=room).order_by("timestamp")
        return JsonResponse({"messages": [
            {"sender": msg.sender.username, "content": msg.content, "timestamp": msg.timestamp} for msg in messages
        ]}, safe=False)
    except Exception as e:
        return JsonResponse({"error": "Room not found"}, status=404)