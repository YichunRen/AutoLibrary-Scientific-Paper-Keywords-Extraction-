mkdir -p ../data/raw 
cp autolibrary/documents_copy/0yuywooah4759qzzuisamzgueozh1m8d/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/params/data-params_0yuywooah4759qzzuisamzgueozh1m8d.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python -u /home/yichunren/AutoLibrary/run.py data 0yuywooah4759qzzuisamzgueozh1m8d 
