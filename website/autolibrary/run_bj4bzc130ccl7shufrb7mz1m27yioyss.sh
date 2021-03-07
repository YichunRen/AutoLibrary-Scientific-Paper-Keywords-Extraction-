mkdir -p ../data/raw 
cp autolibrary/documents_copy/bj4bzc130ccl7shufrb7mz1m27yioyss/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params_bj4bzc130ccl7shufrb7mz1m27yioyss.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data bj4bzc130ccl7shufrb7mz1m27yioyss 
