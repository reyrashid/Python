import glob
import os
from utils import *
from collections import defaultdict

def map_languages_to_paths(folder_path='../Data/ted-talks/FILTERED_xml'):
    """
    Returns a dictionary mapping languages to file paths.
    """
    xml_files = glob.glob(f"{folder_path}/ted_*.xml")

    lang_to_path = {}

    for path in xml_files:
        filename = os.path.basename(path)
        name_without_ext = filename.replace(".xml", "")  
        if '_' in name_without_ext:
            lang_code = name_without_ext.split('_')[-1] 
            lang_to_path[lang_code] = path

    return lang_to_path

def find_coverage(lang_to_paths, coverage="most"):
    """
    Returns a dictionary with the language(s)(keys) that have the most/least translations(values).

    """
    lang_counts = {}

    for lang, path in lang_to_paths.items():
        root = load_root(path)
        talks = get_talks(root)
        
        talks_with_text = []
        for talk in talks:
            if get_word_count(talk) > 0:
                talks_with_text.append(talk)

        lang_counts[lang] = len(talks_with_text)

    if len(lang_counts) == 0:
        return {}

    if coverage == "most":
        extreme_value = max(lang_counts.values())
    elif coverage == "least":
        extreme_value = min(lang_counts.values())
    else:
        return {}

    result = {}
    for lang, count in lang_counts.items():
        if count == extreme_value:
            result[lang] = count

    return result

def get_id_title_dict(path):
    """
    Returns a dictionary that maps talk ids to English titles, excluding empty talks.

    """
    root = load_root(path)
    talks = get_talks(root)

    id_title_dict = {}
    for talk in talks:
        if get_word_count(talk) > 0: 
            talk_id = get_talk_id(talk)
            title = get_talk_title(talk)
            id_title_dict[talk_id] = title

    return id_title_dict

def map_talks_to_languages(lang_to_paths):
    """
    A dictionary that maps talk IDs (keys) to the languages they have been translated into (values).

    """
    talk_langs = defaultdict(list)  # creates empty list automatically for new keys

    for lang, path in lang_to_paths.items():
        root = load_root(path)         
        talks = get_talks(root)      

        for t in talks:
            talk_id = get_talk_id(t)   
            if talk_id is not None and len(talk_id) > 0:                
                talk_langs[talk_id].append(lang)

    return dict(talk_langs) 
    
def map_nlang_to_talks(talk_langs):
    """
     A dictionary that maps the number of translations (keys) to the list of talk IDs (values).
    """
    nlang_to_talks = defaultdict(list)

    for talk_id, langs in talk_langs.items():
        n_translations = len(langs)
        nlang_to_talks[n_translations].append(talk_id)

    return dict(nlang_to_talks)

def find_top_coverage(lang_to_paths, coverage="most"):
    """
    Returns a dictionary that maps English talk titles (keys) with the most or least translations (values).
    """
    talk_langs = map_talks_to_languages(lang_to_paths)
    nlang_to_talks = map_nlang_to_talks(talk_langs)

    if coverage == "most":
        extreme_n = max(nlang_to_talks.keys())
    elif coverage == "least":
        extreme_n = min(nlang_to_talks.keys())
    else:
        return {}

    eng_path = lang_to_paths.get('en', '../Data/ted-talks/FILTERED_xml/ted_en.xml')
    id_title = get_id_title_dict(eng_path)

    result = {}
    for talk_id in nlang_to_talks[extreme_n]:
        if talk_id in id_title:
            result[id_title[talk_id]] = talk_langs[talk_id]

    return result

if __name__ == "__main__":          #found by web search
    lang_to_paths = map_languages_to_paths()

    print(f"Total number of available languages: {len(lang_to_paths)}\n")

    most_translated = find_top_coverage(lang_to_paths, "most")
    least_translated = find_top_coverage(lang_to_paths, "least")

    print("Talk(s) with the most translations:")
    print(most_translated) 

    print("\nTalk(s) with the least translations:")
    print(least_translated)  