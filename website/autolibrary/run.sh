cd ..
cp -a /home/yichunren/AutoLibrary/AutoPhrase2/. /home/yichunren/AutoLibrary/AutoPhrase_qclorm41kga47p38k8p1j1sh3iisvu4h/
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py autophrase qclorm41kga47p38k8p1j1sh3iisvu4h
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py weight qclorm41kga47p38k8p1j1sh3iisvu4h
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape qclorm41kga47p38k8p1j1sh3iisvu4h
cp data/out_qclorm41kga47p38k8p1j1sh3iisvu4h/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase_qclorm41kga47p38k8p1j1sh3iisvu4h.json
