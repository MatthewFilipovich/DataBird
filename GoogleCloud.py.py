import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six
import pandas as pd
import sys
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="authentication.json"

#********************************************
def sample_analyze_sentiment(content):
    client = language_v1.LanguageServiceClient()
    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')
    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}
    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    return sentiment.score, sentiment.magnitude

# #****************************************************

# def entity_sentiment_text(text):
#     """Detects entity sentiment in the provided text."""
#     client = language.LanguageServiceClient()
#     if isinstance(text, six.binary_type):
#         text = text.decode('utf-8')
#     document = types.Document(
#         content=text.encode('utf-8'),
#         type=enums.Document.Type.PLAIN_TEXT)
#     encoding = enums.EncodingType.UTF32
#     if sys.maxunicode == 65535:
#         encoding = enums.EncodingType.UTF16

#     result = client.analyze_entity_sentiment(document, encoding)

#     for entity in result.entities:
#         print('Mentions: ')
#         print(u'Name: "{}"'.format(entity.name))
#         for mention in entity.mentions:
#             print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
#             print(u'  Content : {}'.format(mention.text.content))
#             print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
#             print(u'  Sentiment : {}'.format(mention.sentiment.score))
#             print(u'  Type : {}'.format(mention.type))
#         print(u'Salience: {}'.format(entity.salience))
#         print(u'Sentiment: {}\n'.format(entity.sentiment))

def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16
    result = client.analyze_entity_sentiment(document, encoding)
    return(result.entities[0].name)

#*************************

message = pd.read_csv('mes.csv')
print(len(message))

score = list()
mag = list()
wordlist = list()
timelist = list()
for i in range(1000):
    print(i)
    try:
        if(len(message.iloc[i]['content']) < 25):
            continue
        t_score, t_magnitude = sample_analyze_sentiment(message.iloc[i]['content'])
        score.append(t_score)
        mag.append(t_magnitude) 
        timelist.append(message.iloc[i]['timestamp_ms'])
        t_word = entity_sentiment_text(message.iloc[i]['content'])
        wordlist.append(t_word)
    except:
        continue
pd.DataFrame({'Word' : wordlist}).to_csv('WordList.csv')
pd.DataFrame({'Time' : timelist, 'Score' : score, 'Magnitude' : mag}).to_csv('Emotions.csv')
