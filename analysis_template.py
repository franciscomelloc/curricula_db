from top2vec import Top2Vec
from utils import *

BASE_DIR = Path().absolute() # Document path
DATA_DIR = BASE_DIR / 'data' # Path to data
OUTPUT_DIR = BASE_DIR / 'output'

# Load the model. This would work for any TOP2VEC model. For training TOP2VEC models check: https://github.com/ddangelov/Top2Vec

model = Top2Vec.load("curricula_pretrained")

# Pass a anchor word dictionary: What are you interested in finding in the corpus? 

anchor_dic = {} # This is an example implementation, don't run the dictionary in the main code. 

anchor_dic['Literatura'] = {'poesia', 'jornal', 'camoes'}

anchor_dic['Matemática'] = {'multiplicacao', 'soma', 'algebra'}

# Run these two functions: You can change the values: 
# This will get the 20 most similar topics to those words, and then take 20 most similar paragraphs in the document.
# The output is a CSV file with the topics, paragraphs and cosine similarity and where it came from

t_words, w_scores, t_scores, t_nums = utils.get_topic_data(model, anchor_dic, 20, negative_keywords=None)

utils.extract_topic_documents(model, anchor_dic, t_nums, 20, OUTPUT_DIR)
