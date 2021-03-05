# AutoLibrary - A Personal Digital Library to Find Related Works via Text Analyzer
- Website: https://yichunren.pythonanywhere.com/autolibrary/
- DSC180B - Capstone Project (Winter 2021)
- Section A04 Group03: Yichun Ren, Jiayi Fan, Bingqi Zhou
- Note: This is an application of [AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase) by Jingbo Shang.

## Docker
- The docker repository is `jfan1998/dsc180a-docker`.
- Note: The docker uses dsmlp base container. Please login to a dsmlp jumpbox before entering the command below.
- For local run, please refer to `requirements.txt` to check if all the packages and libraries needed are installed.
```
launch-scipy-ml.sh -i jfan1998/dsc180a-docker:latest
```
Use port-forwarding on dsmlp to open the website:
  - Instruction: https://docs.google.com/document/d/15ehCaVIKSXwgh2jvH3034l5uSPNLrZRgkczwl-xWNEU/edit?usp=sharing

### For Local Run
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
### Target 4: Webscrape the search results on Semantic Scholar with keywords and domains
```
python run.py webscrape
```
### Target 5: Test all previous targets on test data
Note: For the test run, raw test data and domain for search is in test/testdata directory.
```
python run.py test
```
### Target 6: Activating the website
```
python run.py website
```
### Target 7: Convert jupyter notebooks to html
```
python run.py report
```
#### Note for local run:
Since AutoLibary does not have access right to your local documents, if you would like to try other papers, please put the papers in ```~/AutoLibrary/website/autolibrary/documents``` and refresh the website.

### Responsbilities: 
- Yichun Ren: Dataset, Weight, Website Development
- Jiayi Fan: Data, Website Development
- Bingqi Zhou: Dataset, Webscrap
