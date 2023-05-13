# Novo Ensino Médio VSM

Aqui você encontra um modelo vetorial pré-treinado nos dados de 19 currículos de Ensino Médio no Brasil, um Corpus de 15.000 páginas. Também disponibilizei a base de dados com currículos de Ensino Médio de 19 estados brasileiros em PDF e .txt. 

Este modelo utiliza a TOP2VEC por Angelov. Artigo original: https://github.com/ddangelov/Top2Vec

`$ pip install top2vec`


####Implementação　
Load the model. 
```Python
model = Top2Vec.load("curricula_pretrained")
```
Pass a anchor word dictionary: What are you interested in finding in the corpus? 
```Python
anchor_dic = {} 

anchor_dic['Literatura'] = {'poesia', 'jornal', 'camoes'}

anchor_dic['Matemática'] = {'multiplicacao', 'soma', 'algebra'}
```
 Run these two functions: You can change the values: 
 This will get the 20 most similar topics to those words, and then take 20 most similar paragraphs in the document.
 The output is a CSV file with the topics, paragraphs and cosine similarity and where it came from
 
 ```Python
t_words, w_scores, t_scores, t_nums = utils.get_topic_data(model, anchor_dic, 20, negative_keywords=None)

utils.extract_topic_documents(model, anchor_dic, t_nums, 20, OUTPUT_DIR)
```



