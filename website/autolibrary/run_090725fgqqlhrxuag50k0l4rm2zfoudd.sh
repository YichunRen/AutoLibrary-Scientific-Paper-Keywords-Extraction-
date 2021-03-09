mkdir -p ../data/raw 
cp autolibrary/documents_copy/090725fgqqlhrxuag50k0l4rm2zfoudd/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params_090725fgqqlhrxuag50k0l4rm2zfoudd.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python -u /home/yichunren/AutoLibrary/run.py data 090725fgqqlhrxuag50k0l4rm2zfoudd 
