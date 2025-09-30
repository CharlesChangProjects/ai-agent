import unittest
from unittest.mock import MagicMock
from packages.core.src.memory.manager import VectorMemory

class TestVectorMemory(unittest.TestCase):
    def test_retrieve(self):
        mock_store = MagicMock()
        mock_store.similarity_search.return_value = ["doc1", "doc2"]
        memory = VectorMemory(mock_store)
        self.assertEqual(len(memory.retrieve("test")), 2)