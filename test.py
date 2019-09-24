import unittest
import unsplash
import logging
import os
# logging.basicConfig(level=logging.INFO)

class TestUnsplash(unittest.TestCase):

    def setUp(self):
        self.a = unsplash.Unsplash('love')

    def tearDown(self):
        # clean up resource after test
        del self.a
        os.removedirs('love')

    def test_listPhotos(self):
        self.assertEqual(self.a.listPhotos(per_page=10),(200,10))
    
    def test_randomPhotos(self):
        self.assertEqual(self.a.randomPhotos(10),(200,10))

    def test_randomPhotos_overCount(self):
        self.assertEqual(self.a.randomPhotos(500),(200,30))

    def test_searchPhotos(self):
        r = self.a.searchPhotos('love') # return (200, a number greater than 0)
        self.assertTrue(r[1]>0)

    def test_searchPhotos_NoneTotal(self):
        self.assertEqual(self.a.searchPhotos('cnfuhwn'),(200,0))


class TestGraphicRiver(unittest.TestCase):

    def setUp(self):
        self.a = unsplash.GraphicRiver('love')
    
    def tearDown(self):
        del self.a
        os.removedirs('love')

    def test_getUrl(self):
        self.assertEqual(self.a.getUrls('https://graphicriver.net/item/massive-x-presentation-template/21482501'), 951)

    def test_download(self):
        self.assertEqual(self.a.download(10),10)

if __name__ == '__main__':
    unittest.main()