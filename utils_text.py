import requests
import re
import string
try:
  import emoji
except:
  print("Error importing emoji library: demojisation may not work")
class PreProcess:
  def __init__(self, remove_punct=False, sep_url=True, remove_url=True,
               remove_hashtag=False,remove_usertag=False,remove_no=True, lowercase=False,
               convert_emoji=True, solve_gaps=True, remove_newline=True):
    self.remove_punct = remove_punct
    self.sep_url = sep_url
    self.remove_url = remove_url
    self.remove_hashtag = remove_hashtag
    self.remove_usertag = remove_usertag
    self.remove_no = remove_no
    self.lowercase = lowercase
    self.remove_newline = remove_newline
    self.convert_emoji = convert_emoji
    self.solve_gaps = solve_gaps
    if(self.convert_emoji):
      import emoji

  def preprocess(self, text=""):
      try:
        processed_text = text[:]

        #separate the external url 
        if(self.sep_url):
          url = None
          processed_text, _, url = text.partition("…")
          if(url!=''):
              url = "".join(url.split())
              url = "https://t.co/" + url.rsplit('/', 1)[-1]
          else:
              url=None

        #remove urls in text
        if(self.remove_url):
          processed_text = re.sub("http\S+", "", processed_text, flags=re.MULTILINE)
        
        #remove all newlines
        if(self.remove_newline):
          processed_text = processed_text.replace("\n", " ")

        #handle hashtags and usernames
        if(self.remove_hashtag):
          processed_text = re.sub("#", "", processed_text)
        if(self.remove_usertag):
          processed_text = re.sub("@", "", processed_text)



        #remove repeated punctuations
        if(self.remove_punct):
            for punctuation in string.punctuation:
                while True:
                    replaced =  processed_text.replace(punctuation * 2, punctuation)
                    if replaced == processed_text:
                        break
                    processed_text = replaced



        #tokenize punctuations
        """
        for punctuation in string.punctuation:
            processed_text =  processed_text.replace(punctuation, " " + punctuation+ " ")
        """ 


        #remove numbers
        if(self.remove_no):
          processed_text = re.sub("\d+", "", processed_text)



        #convert emojis
        if(self.convert_emoji):
          processed_text = emoji.demojize(processed_text)



        #convert multiple whitespaces to single
        #detect newline and replace with random string
        #processed_text = processed_text.replace("\n", "QSDWDSrfefafawecsd")
        processed_text = re.sub("\s\s+", " ", processed_text)
        #replace again with newline
        #processed_text = processed_text.replace("QSDWDSrfefafawecsd", "\n")

        #Convert to lower case
        if(self.lowercase):   
          processed_text = processed_text.lower()

        if(processed_text == ""):
          processed_text = "blank"
        
        #breaks the lang labels:
        if(self.solve_gaps):
          processed_text = processed_text.replace("@ ", "@").replace(" _ ", "_")
        
        if self.sep_url:
          return (processed_text, url)
        else:
          return processed_text
      except Exception as e:
        print("Error at: ", text, "--",e)


def clean_for_transliterate(text):
  text = re.sub(r"[#~]", "", text)
  #add for !!!!!! -> !
  return text.replace(' ’ ', '\'').replace(' .', '.')


def transliterate(text):
  try:
    return (requests.get(f"https://www.google.com/inputtools/request?text={text}&ime=transliteration_en_hi")).json()[1][0][1][0]
  except:
    return text
