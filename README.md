# AutoLibrary
- DSC180B - Capstone Project (Winter 2021)
- Section A04 Group03: Yichun Ren, Jiayi Fan, Bingqi Zhou
- Personal Digital Library to save the documents and find similar papers via text analyzer.
- Note: This is an application of [AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase) by Jingbo Shang.

## Docker
- The docker repository is `jfan1998/dsc180a-docker`.
- Note: The docker uses dsmlp base container. Please login to a dsmlp jumpbox before entering the command below.
- For local run, please refer to `requirements.txt` to check if all the packages and libraries needed are installed.
```
launch-scipy-ml.sh -i jfan1998/dsc180a-docker:latest
```

## Default Run: open AutoLibrary website
```
python run.py
```
- The home page of website: `http://127.0.0.1:8000/autolibrary/`
### Target 1: Convert the input .pdf file into .txt
```
python run.py data
```
### Target 2: Run AutoPhrase on the input file
```
python run.py autophrase
```
### Target 3: Apply weight to the quality scores of phrases according the corresponding quality score in its domain
```
python run.py weight
```
### Target 4: Web Scraping the search results on Semantic Scholar with keywords and domains
```
python run.py webscrape
```
### Target 5: Activating the website
```
python run.py website
```
### Target 6: Test All previous targets on test data
Note: For the test run, raw test data is in test/testdata directory.
```
python run.py test
```
- Note: To run the test target on DSMLP, need to do port-forwarding as follows:
```kubectl get pods```
NAME          READY   STATUS    RESTARTS   AGE
[ssh-name]-27897   1/1     Running   0          15s

```kubectl port-forward [ssh-name]-27897 :8000```
Forwarding from 127.0.0.1:44474 -> 8000
Forwarding from [::1]:44474 -> 8000

### Responsbilities: 
- Yichun Ren: Dataset, Weight, Website Development
- Jiayi Fan: Data, Website Development
- Bingqi Zhou: Dataset, Webscrap
