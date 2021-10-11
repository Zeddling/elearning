from courses import models
from django.shortcuts import render


# Create your views here.
def index(request):
    context_dict = {}
    context_dict["courses"] = models.Course.objects.all()
    return render(request, "courses/index.html", context_dict)
