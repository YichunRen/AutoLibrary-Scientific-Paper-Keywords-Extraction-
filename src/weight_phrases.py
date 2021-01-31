import pandas as pd
from operator import itemgetter

def change_weight(paper_ap_path, domain_ap_path, out_path):
    print("\n")
    print(">>>>>>>>>>>>>>>>>>>>>>>> Weighting quality scores <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("  => Altering quality scores of phrases in the input document according to domain...")
    data = pd.read_csv(paper_ap_path, sep="\t", header = None, names=["score", "phrase"])
    data_domain = pd.read_csv(domain_ap_path, sep="\t", header = None, names=["score", "phrase"])
    domain_dict = data_domain.set_index('phrase').T.to_dict()
    phrases_dict = dict()

    domain_phrases = list(data_domain['phrase'])
    for i in range(data.shape[0]):
        phrase = data.loc[i, 'phrase']
        score = data.loc[i, 'score']
        if phrase in domain_phrases:
            phrases_dict[phrase] = score * domain_dict[phrase]['score']
            
    print("  => Saving results...")
    sorted_weight = sorted(phrases_dict.items(), key=itemgetter(1), reverse=True)
    pd.DataFrame(sorted_weight, columns= ['phrase', 'score']).to_csv(out_path)
    print(" => Done! Weighted result is saved as '" + out_path + "'")
    print("\n")
    return
