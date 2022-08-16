#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf
class BaseModel():
    def __init__(self, name, path):
        self._name = name
        self._path_to_model = path
        self._graph = tf.Graph()
        self.sess = tf.compat.v1.Session(graph=self._graph)

    def __del__(self):
        try:
            self.sess.close()
            del self.sess
        finally:
            print("Model closed..")

    def build_model(self):
        raise NotImplementedError
    def init_saver(self):
        raise NotImplementedError
    def save(self):
        raise NotImplementedError
    def load(self):
        raise NotImplementedError


# In[ ]:




