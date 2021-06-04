from django.forms import ModelChoiceField
from django.contrib import admin

from .models import *


admin.site.register(Review)
admin.site.register(Genre)