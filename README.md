# مشروع Backend لملحقات اللابتوب (Django REST Framework) - مُحسَّن لـ Python 3.13

هذا المشروع مُعد للعمل مع **Python 3.13** وPyCharm. يشمل API جاهزة لمطوّر الفرونت، مع إعدادات لتسهيل التشغيل (ملف هجرات ابتدائية لتجنّب أخطاء 'no such table').

### ملاحظات مهمة
- اعتمدت في `requirements.txt` نسخ حقيقية تدعم Python 3.13 (Django 5.2+, DRF 3.16+, SimpleJWT 5.5+).
- يوجد ملف هجرات ابتدائية (`store/migrations/0001_initial.py`) بحيث بعد تشغيل `migrate` ستُنشأ جداول `store` بدون الحاجة إلى `makemigrations` المحلي.
- يجب تثبيت المتطلبات عبر الإنترنت (pip) عند تشغيل المشروع للمرة الأولى على جهازك.

---

## تشغيل المشروع في PyCharm (Windows) مع Python 3.13

1. فكّ الضغط وضع المجلد في مكان مناسب.

2. افتح PyCharm → File → Open... واختر مجلد المشروع (المجلد الذي يحتوي `manage.py`).

3. إعداد Interpreter (مهم جداً):
   - File → Settings → Project: <اسم المشروع> → Python Interpreter → ⚙️ → Add...
   - اختر `Virtualenv Environment` → New environment داخل المجلد (مثلاً `<project>/venv`).
   - في خانة Base interpreter: اختر مسار Python 3.13 المثبت عندك (`python.exe` الخاص بالنسخة 3.13).
   - اضغط Create.

4. تثبيت الحزم:
   - افتح Terminal المدمج في PyCharm (سيستخدم الـ venv الذي أنشأته تلقائياً) ثم نفّذ:
     ```powershell
     python -m pip install --upgrade pip setuptools wheel
     pip install -r requirements.txt
     ```

5. شغّل الهجرات وأنشئ حساب أدمِن وبيانات العيّنة:
   ```powershell
   python manage.py migrate
   python manage.py seed_sample_data
   python manage.py createsuperuser
   ```

6. تشغيل الخادم (RunConfiguration أو عبر Terminal):
   ```powershell
   python manage.py runserver
   ```

7. افتح المتصفح: http://127.0.0.1:8000/admin/ أو http://127.0.0.1:8000/api/accessories/

---

## ملاحظات عن الأخطاء السابقة التي صُحِّحت
- تم إصلاح مشكلة `include('store.urls.auth')` وتحويلها إلى تضمين واحد `include('store.urls')` في `mysite/urls.py`.
- إضافة ملف هجرات ابتدائية لتجنّب خطأ `no such table: store_accessory` عند تشغيل الواجهة للمرة الأولى.
- توضيح وإرشاد كامل للعمل مع PyCharm وPython 3.13.

---


## إضافة صورة للمنتج وعمليات CRUD كاملة
- الحقل `image` أُضيف إلى نموذج `Accessory` ويمكن رفع صورة كجزء من POST/PUT باستخدام `multipart/form-data`.
- لاختبار عبر Postman: اختر Body -> form-data، أضف الحقول النصية مثل `name`, `price`, الخ، وأضف حقل `image` من النوع File.
- نقاط النهاية المدعومة الآن: `GET, POST, PUT, PATCH, DELETE` على `/api/accessories/` و`/api/accessories/{id}/`.
- تأكد من أن طلبات POST/PUT التي تحتاج مصادقة تستخدم `Authorization: Bearer <access_token>`.
