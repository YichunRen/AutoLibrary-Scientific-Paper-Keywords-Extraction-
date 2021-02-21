mkdir -p ../data/raw 
cp autolibrary/documents_copy/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params.json  ../config 
cd .. 
python run.py data 
python run.py autophrase 
python run.py weight 
python run.py webscrape 
cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json 
