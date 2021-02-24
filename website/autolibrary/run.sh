mkdir -p ../data/raw 
cp autolibrary/documents_copy/AutoNER.pdf ../data/raw 
cp autolibrary/data-params.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py autophrase 
mkdir test_weight 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py weight uvb5n84mxjwwendeixakun115klkixkw 
mkdir test_webscrape 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape uvb5n84mxjwwendeixakun115klkixkw 
cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json 
mkdir test_end 
