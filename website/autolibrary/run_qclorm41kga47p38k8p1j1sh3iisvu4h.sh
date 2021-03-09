mkdir -p ../data/raw 
cp autolibrary/documents_copy/qclorm41kga47p38k8p1j1sh3iisvu4h/SetExpan.pdf ../data/raw 
cp autolibrary/params/data-params_qclorm41kga47p38k8p1j1sh3iisvu4h.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python -u /home/yichunren/AutoLibrary/run.py data qclorm41kga47p38k8p1j1sh3iisvu4h 
