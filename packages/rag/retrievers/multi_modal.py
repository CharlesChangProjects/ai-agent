class MultiModalRetriever:
    def __init__(self, text_retriever, image_retriever):
        self.text_retriever = text_retriever
        self.image_retriever = image_retriever