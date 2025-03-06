import requests
import difflib
import re
from math import trunc
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def clean_text(text):
    return " ".join(text.lower().strip().split())

def split_into_sentences(text):
    # Split text into sentences using a regular expression
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    return sentence_endings.split(text)

def compare_urls(url, url2):
    first_version_list = []
    second_version_list = []
    first_whole_page_text = []
    second_whole_page_text = []

    html_content_1 = fetch_page(url)
    if html_content_1:
        if 'openstax' in url:
            soup = parse_html(html_content_1)
            soupC = soup.find(id='main-content')
            soupP = soupC.find('div')
            first_whole_page_text = [soupP.get_text(), 'a']

            for para in soupP:
                p = para.get_text()
                p = clean_text(p)
                if p == "":
                    continue
                first_version_list.append(p)
                
        elif 'pressbooks' in url:
            soup = parse_html(html_content_1)
            soupC = soup.find(id='content')
            soupP = soupC.find('section')
            first_whole_page_text = [soupP.get_text(), 'a']

            for para in soupP:
                p = para.get_text()
                p = clean_text(p)
                if p == "":
                    continue
                first_version_list.append(p)

        else:  
            soup = parse_html(html_content_1)
            soupC = soup.find('body')
            first_whole_page_text = [soupC.get_text(), 'a']

            for para in soupC:
                p = para.get_text()
                p = clean_text(p)
                if p == "":
                    continue
                first_version_list.append(p)
    else:
        return ["Error fetching first URL"], ["Error fetching first URL"], 0, "<html><body>Error fetching first URL</body></html>"

    html_content_2 = fetch_page(url2)
    if html_content_2:
        if 'openstax' in url:
            soup = parse_html(html_content_2)
            soupC = soup.find('main')
            soupP = soupC.find('div')
            second_whole_page_text = [soupP.get_text(), 'a']

            for para in soupP:
                p = para.get_text()
                p = clean_text(p)
                if p == "":
                    continue
                second_version_list.append(p)
                
        elif 'pressbooks' in url:
            soup = parse_html(html_content_2)
            soupC = soup.find(id='content')
            soupP = soupC.find('section')
            second_whole_page_text = [soupP.get_text(), 'a']

            for para in soupP:
                p = para.get_text()
                p = clean_text(p)
                if p == "":
                    continue
                second_version_list.append(p)

        else:
            soup = parse_html(html_content_2)
            soupC = soup.find('body')
            second_whole_page_text = [soupC.get_text(), 'a']

            for para in soupC:
                p = para.get_text()
                p = clean_text(p)
                if p == "":
                    continue
                second_version_list.append(p)
    else:
        return ["Error fetching second URL"], ["Error fetching second URL"], 0, "<html><body>Error fetching second URL</body></html>"

    # Provides a float ratio value ( 0 - 1 ) based on the percentage of similarity

    first_whole_page_text = '\n'.join(first_version_list)
    second_whole_page_text = '\n'.join(second_version_list)

    # Split the sections into sentences
    first_sentences = split_into_sentences(first_whole_page_text)
    second_sentences = split_into_sentences(second_whole_page_text)

    # Check if sentences in the first section are included in the second section

    seq_match = difflib.SequenceMatcher(None, '\n'.join(first_sentences), '\n'.join(second_sentences))
    ratio = seq_match.ratio()
    ratio = trunc(ratio * 100)

    d = difflib.HtmlDiff(wrapcolumn=80)
    html_diff = d.make_file(first_sentences, second_sentences)
    with open("diff.html", "w", encoding="utf-8") as f:
        f.write(html_diff)

    return first_version_list, second_version_list, ratio, html_diff

if __name__ == "__main__":
    main()