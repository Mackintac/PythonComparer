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
  # url = 'https://ecampusontario.pressbooks.pub/commbusprofcdn/chapter/the-evolution-of-digital-media/'
  # url2 = 'https://ecampusontario.pressbooks.pub/llsadvcomm/chapter/7-1-the-evolution-of-digital-media/'
  # url = 'https://openstax.org/books/calculus-volume-1/pages/1-introduction'
  # url = 'http://example.com'

  first_version_list = []
  second_version_list = []
  first_whole_page_text =[]
  second_whole_page_text =[]
  version_difference_ratio = []



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
        
    if 'pressbooks' in url:
      soup = parse_html(html_content_1)
      soupC = soup.find(id='content')
      soupP = soupC.find('section')
      first_whole_page_text = [soupP.get_text(), 'a']

      # print("CHILDREN: ", soupP)
      # print(soup.prettify())

      for para in soupP:
        p = para.get_text()
        p = clean_text(p)
        if p == "":
          continue
        first_version_list.append(p)

  html_content_2 = fetch_page(url2)
  if html_content_2:
    soup = parse_html(html_content_2)
    soupC = soup.find(id='content')
    soupP = soupC.find('section')
    second_whole_page_text = [soupP.get_text(), 'a']
    # print(soup.prettify())

    for para in soupP:
      p = para.get_text()
      p = clean_text(p)
      # print(p,"\n")
      if p == "":
        continue
      second_version_list.append(p)
    
    # print("First list: \t", first_version_list[0])

    # print("Second list: \t", second_version_list[0])

  # Provides a float ratio value ( 0 - 1 ) based on the percentage of similarity
  


  # first_version_list = [clean_text(line) for line in first_version_list]
  # second_version_list = [clean_text(line) for line in second_version_list]
  print(first_whole_page_text)
  print(second_whole_page_text)



  i = 0
  j = 0
  # for item in first_version_list:
  #   i+= 1
  #   print(i, item)
  # for item in second_version_list:
  #   j+= 1
  #   print(j, item)


  for item in first_version_list:

    if i >= len(first_version_list ) or j >= len(second_version_list):
      break
    item_seq_match = difflib.SequenceMatcher(None, first_version_list[i], second_version_list[j])
    ratio = item_seq_match.ratio()
    # if ratio < 0.30:
    #   second_version_list.insert(i, "NOT A CLOSE MATCH")
    # item_seq_match = difflib.SequenceMatcher(None, first_version_list[i], second_version_list[j])
    # ratio = item_seq_match.ratio()

    version_difference_ratio.insert(i, ratio)
    print("line: " ,i + 1, " similarity ratio: ", version_difference_ratio[i] * 100 ,"%")

    i+=1
    j+=1


  first_whole_page_text = '\n'.join(first_version_list)
  second_whole_page_text = '\n'.join(second_version_list)

  # Split the sections into sentences
  first_sentences = split_into_sentences(first_whole_page_text)
  second_sentences = split_into_sentences(second_whole_page_text)

  # Check if sentences in the first section are included in the second section
  for sentence in second_sentences:
      if sentence in first_whole_page_text:
          print(f"Sentence from first section found in second section: {sentence}")

  # for possibility in 


  seq_match = difflib.SequenceMatcher(None, '\n'.join(first_sentences), '\n'.join(second_sentences))
  ratio = seq_match.ratio()
  ratio = trunc(ratio * 100)
  print(ratio,"%")
  line_count_difference_amount = abs(len(first_version_list) - len(second_version_list))
  print(sum(version_difference_ratio) / (len(version_difference_ratio) + line_count_difference_amount))

    

  d = difflib.HtmlDiff(wrapcolumn=80)
  # html_diff =  d.make_file( first_version_list, second_version_list)
  html_diff =  d.make_file( first_sentences, second_sentences)
  with open("diff.html", "w", encoding="utf-8") as f:
    f.write(html_diff)



  return first_version_list, second_version_list, ratio, html_diff


if __name__ == "__main__":
  main()