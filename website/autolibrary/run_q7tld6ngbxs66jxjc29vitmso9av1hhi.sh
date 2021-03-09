mkdir -p ../data/raw 
cp autolibrary/documents_copy/q7tld6ngbxs66jxjc29vitmso9av1hhi/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/params/data-params_q7tld6ngbxs66jxjc29vitmso9av1hhi.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python -u /home/yichunren/AutoLibrary/run.py data q7tld6ngbxs66jxjc29vitmso9av1hhi 
