mkdir -p ../data/raw 
cp autolibrary/documents_copy/uvb5n84mxjwwendeixakun115klkixkw/[TKDE18]Automated_Phrase_Mining_from_Massive_Text_Corpora.pdf ../data/raw 
cp autolibrary/data-params_uvb5n84mxjwwendeixakun115klkixkw.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python -u /home/yichunren/AutoLibrary/run.py data uvb5n84mxjwwendeixakun115klkixkw 
