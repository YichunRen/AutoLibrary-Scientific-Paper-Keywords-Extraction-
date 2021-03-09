mkdir -p ../data/raw 
cp autolibrary/documents_copy/mawiy966g65hskrdqeya0kgm5vld3nsd/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params_mawiy966g65hskrdqeya0kgm5vld3nsd.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python -u /home/yichunren/AutoLibrary/run.py data mawiy966g65hskrdqeya0kgm5vld3nsd 
