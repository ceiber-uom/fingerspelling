
import re
import random as rand
from math import floor

from dash.exceptions import PreventUpdate


def sort_list(filename="google-10000-english-no-swears.txt" ):

  print(filename)


  with open(filename,'rt') as f:
    doc = f.read().split()

  # change this to get different min, max length
  doc = [d for d in doc if len(d) > 3 and len(d) < 9]

  # change this to use a different REGEX filter
  vowels = re.compile(r"[aeiou][aeiou]")
  doc = [d for d in doc if re.search(vowels,d) is not None]

  # everything below is rearranging the input file to match the output file
  doc.sort(key=len)
  print("list has "+str(len(doc))+" elements")

  word_len = [len(s) for s in doc]

  counts = [word_len.count(a) for a in range(4,9)]

  with open("output-vowels.txt",'wt') as f:

    offset = 0

    for c in counts:
      f.write('{0:09d} {1:09d}\n'.format(0,c))

    offset = f.tell() 
    f.seek(0,0)

    for i in range(0,len(counts)):
      c = counts[i]
      f.write('{0:09d} {1:09d}\n'.format(offset,c))
      offset += c*(i+6)

    for s in doc:
      f.write(s+'\n')



def test_list(filename=""):

  n_letters = ['4','5','6']

  nl = [int(n) for n in n_letters]
  if len(nl) == 0:
    raise PreventUpdate

  nl = rand.choice(nl)
  print('Getting a '+str(nl)+"-letter word\n")

  with open("vowel-pair.txt","rt") as file:
    for u in range(0,nl-3): 
      header = file.readline()

    print("header: " + header)
    
    header = [int(s) for s in header.split()] # header values
    index = rand.randrange(header[1])   # get a random index
    file.seek(header[0] + (nl+2)*index) # jump to destination
    word = file.readline() # and read the word you found there

    print("word: " + word)



if __name__ == "__main__":
    # sort_list()
    test_list()