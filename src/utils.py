import os
import nbformat
from nbconvert import HTMLExporter
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_recall_curve

def convert_report(report_in_path, report_out_path, **kwargs):
    curdir = os.path.abspath(os.getcwd())
    indir, _ = os.path.split(report_in_path)
    outdir, _ = os.path.split(report_out_path)
    os.makedirs(outdir, exist_ok=True)

    config = {
        "ExecutePreprocessor": {"enabled": True},
        "TemplateExporter": {"exclude_output_prompt": True, "exclude_input": True, "exclude_input_prompt": True},
    }

    nb = nbformat.read(open(report_in_path), as_version=4)
    html_exporter = HTMLExporter(config=config)

    # change dir to notebook dir, to execute notebook
    os.chdir(indir)
    body, resources = (
        html_exporter
        .from_notebook_node(nb)
    )

    # change back to original directory
    os.chdir(curdir)

    with open(report_out_path, 'w') as fh:
        fh.write(body)

def min_max_scale(phrases):
    '''
    For notebooks/Experiment: Webtools
    '''
    fre_min = min(phrases.values())
    fre_max = max(phrases.values())
    for key in phrases:
        cur = phrases[key]
        phrases[key] = (cur - fre_min) / (fre_max - fre_min)
    return phrases

def graph_precision_recall(*args):
    '''
    For notebooks/Experiment: precision recall curve
    '''
    autophrase_cs_labels, autophrase_cs_df, jstor_cs_labels, jstor_cs_phrases, webtools_cs_labels, webtools_cs_phrases, monkeylearn_cs_labels, monkeylearn_cs_phrases, domain = args
    plt.figure(figsize=(10, 8))
    # autophrase
    precision, recall, thresholds = precision_recall_curve(
            y_true=autophrase_cs_labels,
            probas_pred=autophrase_cs_df.score)
    plt.plot(recall, precision, scalex=False, scaley=False, label = "AutoPhrase")
    # jstor
    precision, recall, thresholds = precision_recall_curve(
            y_true=jstor_cs_labels,
            probas_pred=list(jstor_cs_phrases.values()))
    plt.plot(recall, precision, scalex=False, scaley=False, label = "Jstor")
    # webtools
    precision, recall, thresholds = precision_recall_curve(
            y_true=webtools_cs_labels,
            probas_pred=list(webtools_cs_phrases.values()))
    plt.plot(recall, precision, scalex=False, scaley=False, label = "Webtools")
    # monkeylearn
    precision, recall, thresholds = precision_recall_curve(
            y_true=monkeylearn_cs_labels,
            probas_pred=list(monkeylearn_cs_phrases.values()))
    plt.plot(recall, precision, scalex=False, scaley=False, label = "monkeylearn")
    plt.title('Precision-Recall Curve: {}'.format(domain), fontsize=25)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend(loc="best")
    plt.show()