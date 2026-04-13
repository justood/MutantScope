import unittest
import binary_search

class TestBinarySearch(unittest.TestCase):

    def test_found_middle(self):
        self.assertTrue(binary_search.find([2,4,6,8,10], 6))

    def test_found_first(self):
        self.assertTrue(binary_search.find([2,4,6,8,10], 2))

    def test_found_last(self):
        self.assertTrue(binary_search.find([2,4,6,8,10], 10))

    def test_not_found(self):
        self.assertFalse(binary_search.find([2,4,6,8,10], 5))

    def test_empty_list(self):
        self.assertFalse(binary_search.find([], 5))

    def test_single_element(self):
        self.assertTrue(binary_search.find([3], 3))
        self.assertFalse(binary_search.find([3], 2))

if __name__ == "__main__":
    unittest.main()
