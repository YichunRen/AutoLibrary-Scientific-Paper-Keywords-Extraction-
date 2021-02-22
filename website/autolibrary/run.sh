mkdir -p ../data/raw 
cp autolibrary/documents_copy/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py autophrase 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py weight 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape 
mkdir test_run3 
