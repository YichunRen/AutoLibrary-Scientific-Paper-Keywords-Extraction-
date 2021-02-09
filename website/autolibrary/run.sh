mkdir -p ../data/raw 
cp autolibrary/documents_copy/[SIGMOD15]Mining_Quality_Phrases_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params.json  ../config 
cd .. 
python3 run.py data 
python3 run.py autophrase 
python3 run.py weight 
python3 run.py webscrape 
cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json