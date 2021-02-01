cd website/website 
echo "SECRET_KEY = 'wfu9-o-wre7ss%kl-4^e0iv(vb=5#loylpow66cb#r5orl0qlu'" >> settings.py 
cd .. 
open "http://127.0.0.1:8000/autolibrary" && python manage.py runserver 
