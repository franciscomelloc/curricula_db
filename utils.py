from top2vec import Top2Vec
from pathlib import Path
import pandas as pd
import fileinput


class utils:

    def get_topic_data(model, anchor_dic, n_topics, negative_keywords=None):
        
        """
        Given a trained Top2Vec model and a dictionary of anchor groups and keywords, this function retrieves 
        the topic words, word scores, topic scores, and topic numbers for each group, excluding certain keywords.
        
        Parameters
        ----------
        model : Top2Vec
            A trained Top2Vec model.
            
        anchor_dic : dict
            A dictionary where each key is an anchor group and each value is a list of keywords associated with that group.
            
        n_topics : int
            The number of topics to search for each anchor group.
            
        negative_keywords : list, optional
            A list of keywords to exclude from the search. If None, no keywords are excluded.
        
        Returns
        -------
        tuple
            A tuple containing four lists: topic words, word scores, topic scores, and topic numbers.
        """

        if negative_keywords is None:
            negative_keywords = []
        
        t_nums = []
        t_words = []
        t_scores = []
        w_scores = []

        for anchor_group, anchors in anchor_dic.items():
            t_nums += [[]]
            topic_words, word_scores, topic_scores, topic_nums = model.search_topics(
                keywords=list(anchors), keywords_neg=negative_keywords, num_topics=n_topics)
            t_words += topic_words
            t_scores += list(topic_scores)
            w_scores += word_scores
            t_nums[-1] += [list(topic_nums)]
        
        return t_words, w_scores, t_scores, t_nums
    

    def extract_topic_documents(model, anchor_dic, t_nums, n_paragraphs, outputfolder):
        
        """
        Extracts the documents associated with the topics in a trained Top2Vec model.

        Parameters
        ----------
        model : Top2Vec
            A trained Top2Vec model.
        anchor_dic : dict
            A dictionary with groups of anchor words.
        t_nums : list
            A list of lists, where each list contains the topic numbers for a particular group.
        n_paragraphs : int
            Number of paragraphs to extract from each document.
        outputfolder : str
            Path to the output folder.

        Returns
        -------
        None
        """

        t_nums = [item for items in t_nums for item in items]

        doc_names = []
        for anchor_group, anchors in anchor_dic.items():
            doc_names.append(anchor_group)

        gambiarra = []  
        z_all = []
        a_all = []
        b_all = []
        c_all = []

        for topic_list in t_nums:
            gambiarra.append(topic_list)
            names = [names for names in doc_names]
            export = [] 

            for topic in topic_list:
                documents, document_scores, document_ids = model.search_documents_by_topic(topic_num = topic, num_docs = n_paragraphs)

                for doc, score, doc_id in zip(documents, document_scores, document_ids):
                    z_all.append(topic)
                    a_all.append(doc_id)
                    b_all.append(score)
                    c_all.append(doc) 
            
            # numero = len(gambiarra) - 1
            # data_folder = Path(outputfolder)
            # export_file = data_folder / f"{names[numero]}.txt"

            # with open(export_file, "w", encoding = 'utf-8') as text_file:
            #     text_file.write("\n".join(map(str, export)))

        all_latin = []
        for i in c_all:
            latin1 = i.encode('latin-1', 'replace').decode('latin-1')
            all_latin.append(latin1)

        dic = {'Topic' : z_all, 'Document ID': a_all, 'Similarity Score': b_all, 'Paragraph': all_latin}
        Sample_Paragraphs = pd.DataFrame(dic)
        output_file = Path(outputfolder) / "Sample_Paragraphs.csv"
        Sample_Paragraphs.to_csv(output_file, encoding='latin-1', index=False)


    def read_docs_paragraph(textfolder):
    
        """
        
        Reads in all text files in a folder and returns a dataframe with the text and the filename.
        
        Parameters
        ----------
        textfolder : str
            The path to the folder containing the text files.
        
        Returns
        -------
        pandas.DataFrame
            A dataframe with the text and the filename.
        
        """
        
        ### Subfunction for cleaning pathnames
        
        def get_docname(path):

            """
            This function takes a path to a file and returns the name of the file.

            Parameters
            ----------
            path : str
                The path to the file.

            Returns
            -------
            doc_name : str
                The name of the file.
            """

            from pathlib import Path
            p = Path(path)
            doc_name = p.name

            return doc_name.replace(".txt", "")
        
        ### Actual Function:
            
        with fileinput.input(Path(textfolder).glob("*.txt"), openhook=fileinput.hook_encoded("utf-8")) as files:
            df = pd.DataFrame(
                ([line, files.filename()] for line in files),
                columns = ["Corpus", "Document"]
            )
        
        df['Document'] = df['Document'].apply(get_docname)
        
        return df



