import unittest

from multiscript.bible.reference import BibleBook, BibleVerse, BibleRange, BibleRangeList

class TestBibleReference(unittest.TestCase):
    def test_range_list(self):
        range_list = BibleRangeList()
        range_list.append_group([BibleRange(BibleBook.Gen, 1, 3, 2, 3)])
        range_list.append_group([BibleRange(BibleBook.Exod, 3, 4, 4, 5), 
                                 BibleRange(BibleBook.Exod, 4, 10, 4, 20),
                                 BibleRange(BibleBook.Matt, 5, 8, 6, 9),
                                 BibleRange(BibleBook.Matt, 2, 4, 3, 7)])
        range_list.append_group([BibleRange(BibleBook.Lev, 6, 12, 7, 2)])
        self.assertEqual(range_list.string(), "Genesis 1:3-2:3; Exodus 3:4-4:5, 4:10-20, Matthew 5:8-6:9, 2:4-3:7; Leviticus 6:12-7:2")

    def test_range_list_from_text(self):
        range_list = BibleRangeList.new_from_text("Matt 5:6-8; Mark 1:1-12, Mark 1:15-18; Luke 3:1-5, Luke 4:10-12, John 10:1-8")
        self.assertEqual(str(range_list), "Matthew 5:6-8; Mark 1:1-12, 1:15-18; Luke 3:1-5, 4:10-12, John 10:1-8")

    def test_verse_arithmetic(self):
        self.assertTrue(BibleVerse(BibleBook.John, 1, 50).add(11) == BibleVerse(BibleBook.John, 2, 10))
        self.assertTrue(BibleVerse(BibleBook.John, 2, 10).subtract(12) == BibleVerse(BibleBook.John, 1, 49))
    
    def test_range_contains(self):
        self.assertFalse(BibleRange(BibleBook.Matt, 2, 20, 3, 7).contains(BibleVerse(BibleBook.Matt, 2, 19)))
        self.assertTrue(BibleRange(BibleBook.Matt, 2, 20, 3, 7).contains(BibleVerse(BibleBook.Matt, 2, 20)))
        self.assertTrue(BibleRange(BibleBook.Matt, 2, 20, 3, 7).contains(BibleVerse(BibleBook.Matt, 3, 7)))
        self.assertFalse(BibleRange(BibleBook.Matt, 2, 20, 3, 7).contains(BibleVerse(BibleBook.Matt, 3, 8)))

    def test_verse_comparison(self):
        self.assertTrue(BibleVerse(BibleBook.Gen, 2, 10) < BibleVerse(BibleBook.Gen, 3, 1))
        self.assertTrue(BibleVerse(BibleBook.Gen, 3, 1) <= BibleVerse(BibleBook.Gen, 3, 1))
        self.assertTrue(BibleVerse(BibleBook.Gen, 3, 1) >= BibleVerse(BibleBook.Gen, 3, 1))
        self.assertTrue(BibleVerse(BibleBook.Gen, 4, 2) > BibleVerse(BibleBook.Gen, 2, 15))
    
    def test_range_split(self):
        ref = BibleRange(BibleBook.John, 1, 11, 10, 5)
        split = ref.split(by_chap=False, num_verses=100)
        # print([r.string() for r in split])
        expected = [BibleRange(BibleBook.John, 1, 11, 3, 34),
                    BibleRange(BibleBook.John, 3, 35, 5, 44),
                    BibleRange(BibleBook.John, 5, 45, 7, 26),
                    BibleRange(BibleBook.John, 7, 27, 9, 14),
                    BibleRange(BibleBook.John, 9, 15, 10, 5)]
        self.assertTrue(split == expected)

    def test_book_validation(self):
        # Ensure that each Bible book passes basic verse validation
        for book in BibleBook:
            bible_verse = BibleVerse(book, 1, 1, True)
            self.assertIsNotNone(bible_verse)

    def test_string_roundtrip(self):
        # For each Bible book, test that we can convert a range to a string and back again
        for book in BibleBook:
            orig_range = BibleRange(book, 1, 1, 1, 2)

            # Test abbreviated strings
            string = orig_range.string(abbrev=True)
            range_list = BibleRangeList.new_from_text(string)
            self.assertNotEqual(len(range_list), 0)
            final_range = range_list[0]
            self.assertEqual(orig_range, final_range)

            # Test full strings
            string = orig_range.string(abbrev=False)
            range_list = BibleRangeList.new_from_text(string)
            self.assertNotEqual(len(range_list), 0)
            final_range = range_list[0]
            self.assertEqual(orig_range, final_range)


