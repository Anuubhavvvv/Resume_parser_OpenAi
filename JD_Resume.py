from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from numpy.linalg import norm
import numpy as np
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')


def preprocess_text(text):
    text = text.lower()

    text = re.sub('[^a-z]', ' ', text)

    text = re.sub(r'\d+', '', text)

    text = ' '.join(text.split())

    return text


def Calculate_score(jd, cv_test):
    input_jd = preprocess_text(jd)
    input_cv = preprocess_text(cv_test)

    model = Doc2Vec.load("JD.model")
    v1 = model.infer_vector(input_cv.split())
    v2 = model.infer_vector(input_jd.split())

    similarity = 10 * (np.dot(np.array(v1), np.array(v2))) / (norm(np.array(v1))) * (norm(np.array(v2)))
    return (round(similarity, 2))
