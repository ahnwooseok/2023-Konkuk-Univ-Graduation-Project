import yaml
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

try:
    yaml._warnings_enabled["YAMLLoadWarning"] = False
except (KeyError, AttributeError, TypeError) as e:
    pass

import re
import math
import joblib
import inspect
import collections
import numpy as np
import pandas as pd
import scipy.sparse as sp

from tqdm import tqdm
from pathlib import Path
from packaging import version
from collections import defaultdict
from scipy.sparse import csr_matrix
from scipy.cluster import hierarchy as sch
from scipy.spatial.distance import squareform

# Typing
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
from typing import List, Tuple, Union, Mapping, Any, Callable, Iterable

# Models
import hdbscan
from umap import UMAP
from sklearn.preprocessing import normalize
from sklearn import __version__ as sklearn_version
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# BERTopic
from bertopic import plotting
from bertopic.cluster import BaseCluster
from bertopic.backend import BaseEmbedder
from bertopic.representation._mmr import mmr
from bertopic.backend._utils import select_backend
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import BaseRepresentation
from bertopic.dimensionality import BaseDimensionalityReduction
from bertopic.cluster._utils import hdbscan_delegator, is_supported_hdbscan
from bertopic._utils import (
    MyLogger, check_documents_type, check_embeddings_shape,
    check_is_fitted, validate_distance_matrix
)
import bertopic._save_utils as save_utils

# Visualization
import plotly.graph_objects as go
class Custom(BERTopic):
    def _extract_representative_docs(self,
                                     c_tf_idf,
                                     documents,
                                     topics,
                                     nr_samples: int = 500,
                                     nr_repr_docs: int = 5,
                                     diversity: float = None
                                     ):
        # Sample documents per topic
        documents_per_topic = (
            documents.drop("Image", axis=1, errors="ignore")
                     .groupby('Topic')
                     .sample(n=nr_samples, replace=True, random_state=42)
                     .drop_duplicates()
        )

        # Find and extract documents that are most similar to the topic
        repr_docs = []
        repr_docs_indices = []
        repr_docs_mappings = {}
        repr_docs_ids = []
        labels = sorted(list(topics.keys()))
        for index, topic in enumerate(labels):

            # Slice data
            selection = documents_per_topic.loc[documents_per_topic.Topic == topic, :]
            selected_docs = selection["Document"].values
            selected_docs_ids = selection.index.tolist()
            
            # Calculate similarity
            nr_docs = nr_repr_docs if len(selected_docs) > nr_repr_docs else len(selected_docs)
            bow = self.vectorizer_model.transform(selected_docs)
            ctfidf = self.ctfidf_model.transform(bow)
            sim_matrix = cosine_similarity(ctfidf, c_tf_idf[index])

            # Use MMR to find representative but diverse documents
            if diversity:
                docs = mmr(c_tf_idf[index], ctfidf, selected_docs, top_n=nr_docs, diversity=diversity)

            # Extract top n most representative documents
            else:
                indices = np.argpartition(sim_matrix.reshape(1, -1)[0], -nr_docs)[-nr_docs:]
                docs = [selected_docs[index] for index in indices]
                
            doc_ids = [selected_docs_ids[index] for index, doc in enumerate(selected_docs) if doc in docs]
            repr_docs_ids.append(doc_ids)
            repr_docs.extend(docs)
            repr_docs_indices.append([repr_docs_indices[-1][-1] + i + 1 if index != 0 else i for i in range(nr_docs)])
        repr_docs_mappings = {topic: repr_docs[i[0]:i[-1]+1] for topic, i in zip(topics.keys(), repr_docs_indices)}
        return repr_docs_mappings, repr_docs, repr_docs_indices, repr_docs_ids