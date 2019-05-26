from django.contrib import admin

from .models import *

# После создания модели в models.py, сюда ссылку, чтобы можно было администрировать в http://127.0.0.1:8000/admin/

admin.site.register(Product)
#admin.site.register(Portion)
admin.site.register(Diet)
