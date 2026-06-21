import xml.etree.ElementTree as et
from datetime import datetime

def load_root(path):
    """Load XML file and return the root element."""
    tree = et.parse(path)
    root = tree.getroot()
    return root

def get_talks(root):
    """Return a list of all <file> talk elements."""
    return root.findall('file')

def get_talk_id(talk):
    """Return the talk's ID as a string."""
    talkid_el = talk.find('head/talkid')
    if talkid_el is not None and talkid_el.text:
        return talkid_el.text
    else:
        return None

def get_talk_title(talk):
    """Return the talk's title, or None if not found."""
    title_el = talk.find('head/title')
    if title_el is not None and title_el.text:
        return title_el.text
    else:
        return None

def get_talk_speaker(talk):
    """Return the talk's speaker, or None if not found."""
    speaker_el = talk.find('head/speaker')
    if speaker_el is not None and speaker_el.text:
        return speaker_el.text
    else:
        return None

def get_talk_date(talk):
    """Return the talk's date as a datetime object, or None if not found."""
    date_el = talk.find('head/date')
    if date_el is not None and date_el.text:
        return datetime.strptime(date_el.text, "%Y/%m/%d")     #found with web search
    else:
        return None

def get_word_count(talk):
    """Return the word count of the talk, or 0 if not found."""
    wc_el = talk.find('head/wordnum')
    if wc_el is not None and wc_el.text:
        return int(wc_el.text)
    else:
        return 0
