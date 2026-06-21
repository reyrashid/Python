from utils import *
from datetime import datetime

xml_path = "../Data/ted-talks/FILTERED_xml/ted_en.xml"

def load_talks(path=xml_path):
    """Load talks from XML, excluding empty talks."""
    root = load_root(path)
    talks = get_talks(root)
    talks_with_text = []
    for talk in talks:
        if get_word_count(talk) > 0:
            talks_with_text.append(talk)
    return talks_with_text

def find_wc(talks, length="longest"):
    """Find the longest or shortest talk and mean word count."""
    
    if len(talks) == 0:
        titles = None
        ids = None
        extreme_wc = None
        mean_wc = None
        return titles, ids, extreme_wc, mean_wc

    total_words = 0
    extreme_wc = get_word_count(talks[0])

    for t in talks:
        wc = get_word_count(t)
        total_words += wc
        
        if length == "shortest":
            if wc < extreme_wc:
                extreme_wc = wc
        else:  
            if wc > extreme_wc:
                extreme_wc = wc

    titles = []
    ids = []
    for t in talks:
        if get_word_count(t) == extreme_wc:
            titles.append(get_talk_title(t))
            ids.append(get_talk_id(t))

    mean_wc = total_words / len(talks)

    return titles, ids, extreme_wc, mean_wc


def find_date(talks, time="newest"):
    """Find the oldest or newest talk by date."""
    
    if len(talks) == 0:
        titles = None
        ids = None
        return titles, ids

    selected_talk = None

    for t in talks:
        t_date = get_talk_date(t)
        if t_date is None:
            continue  

        if selected_talk is None:
            selected_talk = t
        else:
            selected_date = get_talk_date(selected_talk)
            if time == "oldest":
                if t_date < selected_date:
                    selected_talk = t
            else:  
                if t_date > selected_date:
                    selected_talk = t

    if selected_talk is None:
        titles = None
        ids = None
        return titles, ids
    else:
        titles = [get_talk_title(selected_talk)]
        ids = [get_talk_id(selected_talk)]
        dates = [get_talk_date(selected_talk).strftime("%Y-%m-%d")]   #found on the web
        return titles, ids, dates

def find_speaker(talks):
    """Return speakers with more than one talk in form of a dictionary."""
    speaker_dict = {}
    for t in talks:
        speaker = get_talk_speaker(t)
        if speaker is not None:
            if speaker not in speaker_dict:
                speaker_dict[speaker] = []
            speaker_dict[speaker].append((get_talk_title(t), get_talk_id(t)))

    multi = {}
    for sp in speaker_dict:
        if len(speaker_dict[sp]) > 1:
            multi[sp] = speaker_dict[sp]

    return multi

talks = load_talks()
print(f"The total number of English talks: {len(talks)}\n")

long_titles, long_ids, long_wc, mean_wc = find_wc(talks, "longest")
short_titles, short_ids, short_wc, _ = find_wc(talks, "shortest")
print(f"Longest talk: {long_titles} (id: {long_ids}) — {long_wc} words")
print(f"Shortest talk: {short_titles} (id: {short_ids}) — {short_wc} words")
print(f"Mean word count: {mean_wc}\n")

old_titles, old_ids, old_dates = find_date(talks, "oldest")
new_titles, new_ids, new_dates = find_date(talks, "newest")
print(f"Oldest talk: {old_titles} (id: {old_ids}) — Date: {old_dates}")
print(f"Newest talk: {new_titles} (id: {new_ids}) — Date: {new_dates}\n")

multi_speakers = find_speaker(talks)
print("Speakers with multiple talks:")
if multi_speakers:
    for sp in multi_speakers:
        print(f"{sp}: {multi_speakers[sp]}")
else:
    print("None found.")
