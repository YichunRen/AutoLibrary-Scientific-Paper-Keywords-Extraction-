mkdir -p ../data/raw 
cp autolibrary/documents_copy/[SIGMOD15]Mining_Quality_Phrases_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py autophrase 
mkdir test_weight 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py weight 
mkdir test_webscrape 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape 
cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json 
mkdir test_end 
