mkdir -p ../data/raw 
cp autolibrary/documents_copy/uvb5n84mxjwwendeixakun115klkixkw/CrossWeigh.pdf ../data/raw 
cp autolibrary/params/data-params_uvb5n84mxjwwendeixakun115klkixkw.json  ../config 
cd .. 
/home/yichunren/AutoLibrary/myvenv/bin/python -u /home/yichunren/AutoLibrary/run.py data uvb5n84mxjwwendeixakun115klkixkw 
