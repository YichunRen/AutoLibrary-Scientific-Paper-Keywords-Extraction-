mkdir -p ../data/raw 
cp autolibrary/documents_copy/yv8i388om0whngchrw6hezpxg5z5wy65/2103.01926.pdf ../data/raw 
cp autolibrary/data-params.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py autophrase 
mkdir test_weight 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py weight yv8i388om0whngchrw6hezpxg5z5wy65 
mkdir test_webscrape 
/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape yv8i388om0whngchrw6hezpxg5z5wy65 
cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json 
mkdir test_end 
