import re

import bs4          # Beautiful Soup library
import requests
import urllib

from multiscript.sources.base import BibleSource
from multiscript.bible.version import BibleVersion
from multiscript.bible.reference import BibleBook, BibleRange, BibleVerse



class GetBibleDotNetSource(BibleSource):
    def __init__(self, plugin):
        super().__init__(plugin)
        self.id = "getbible.net"
        self.name = "GetBible.net"

    def new_bible_version(self, version_id=None, name=None, lang=None, abbrev=None):
        '''Overridden from BibleVersion.
        
        Constructs a new GetBibleDotNetVersion for this BibleSource.
        '''
        return GetBibleDotNetVersion(self, version_id, name, lang, abbrev)

    def new_source_app_config(self):
        '''Overridden from BibleVersion.
        
        If this source stores app config, this method must return an instance
        of a subclass of SourceAppConfig. Returns None if the source stores no 
        app config.
        '''
        return None

    def new_source_plan_config(self):
        '''Overridden from BibleVersion.
        
        If this source stores plan config, this method must return an instance
        of a subclass of SourcePlanConfig. Returns None if the source stores no 
        plan config.
        '''
        return None

    def get_all_versions(self):
        '''Overridden from BibleVersion.
        
        Return all of the BibleVersions available for this BibleSource.
        '''
        response = requests.get('https://getbible.net/v2/translations.json')
        resp_dict = response.json()
        versions = []
        for key, vers_dict in resp_dict.items():
            id = key
            version = self.new_bible_version(id)
            version.user_labels.name = vers_dict['translation']
            version.user_labels.abbrev = vers_dict['abbreviation'].upper()
            version.user_labels.lang = vers_dict['language']
            version.copyright_text = vers_dict['distribution_license']
            versions.append(version)
        return versions

    def bible_content_loading(self, runner):
        '''Overridden from BibleVersion.
        
        When a plan contains versions from this Bible source, this method is called when the plan
        run is beginning to load Bible content.

        Subclasses may override to load any resources that may need to be shared amongst versions
        from this source during the plan run.
        '''
        pass

    def bible_content_loaded(self, runner):
        '''Overridden from BibleVersion.
        
        Called when a plan run has finished loading content from all its Bible versions.

        Subclasses may override to clean up any resources that were allocated during bible_content_loading().
        '''
        pass


class GetBibleDotNetVersion(BibleVersion):
    book_codes = {BibleBook.Gen:        "1",
                  BibleBook.Exod:       "2",
                  BibleBook.Lev:        "3",
                  BibleBook.Num:        "4",
                  BibleBook.Deut:       "5",
                  BibleBook.Josh:       "6",
                  BibleBook.Judg:       "7",
                  BibleBook.Ruth:       "8",
                  BibleBook._1Sam:      "9",
                  BibleBook._2Sam:      "10",
                  BibleBook._1Kgs:      "11",
                  BibleBook._2Kgs:      "12",
                  BibleBook._1Chr:      "13",
                  BibleBook._2Chr:      "14",
                  BibleBook.Ezra:       "15",
                  BibleBook.Neh:        "16",
                  BibleBook.Esth:       "17",
                  BibleBook.Job:        "18",
                  BibleBook.Psa:        "19",
                  BibleBook.Prov:       "20",
                  BibleBook.Eccl:       "21",
                  BibleBook.Song:       "22",
                  BibleBook.Isa:        "23",
                  BibleBook.Jer:        "24",
                  BibleBook.Lam:        "25",
                  BibleBook.Ezek:       "26",
                  BibleBook.Dan:        "27",
                  BibleBook.Hos:        "28",
                  BibleBook.Joel:       "29",
                  BibleBook.Amos:       "30",
                  BibleBook.Obad:       "31",
                  BibleBook.Jonah:      "32",
                  BibleBook.Mic:        "33",
                  BibleBook.Nah:        "34",
                  BibleBook.Hab:        "35",
                  BibleBook.Zeph:       "36",
                  BibleBook.Hag:        "37",
                  BibleBook.Zech:       "38",
                  BibleBook.Mal:        "39",
                  BibleBook.Matt:       "40",
                  BibleBook.Mark:       "41",
                  BibleBook.Luke:       "42",
                  BibleBook.John:       "43",
                  BibleBook.Acts:       "44",
                  BibleBook.Rom:        "45",
                  BibleBook._1Cor:      "46",
                  BibleBook._2Cor:      "47",
                  BibleBook.Gal:        "48",
                  BibleBook.Eph:        "49",
                  BibleBook.Phil:       "50",
                  BibleBook.Col:        "51",
                  BibleBook._1Thess:    "52",
                  BibleBook._2Thess:    "53",
                  BibleBook._1Tim:      "54",
                  BibleBook._2Tim:      "55",
                  BibleBook.Titus:      "56",
                  BibleBook.Phlm:       "57",
                  BibleBook.Heb:        "58",
                  BibleBook.James:      "59",
                  BibleBook._1Pet:      "60",
                  BibleBook._2Pet:      "61",
                  BibleBook._1Jn:       "62",
                  BibleBook._2Jn:       "63",
                  BibleBook._3Jn:       "64",
                  BibleBook.Jude:       "65",
                  BibleBook.Rev:        "66"
                  }

    def __init__(self, source=None, id=None, name=None, lang=None, abbrev=None):
        super().__init__(source, id, name, lang, abbrev)

    def load_content(self, bible_range, bible_content):
        book_code = GetBibleDotNetVersion.book_codes[bible_range.book]
        bible_content.copyright_text = self.copyright_text
        content_body = bible_content.body
        content_body.strip_text = True
        content_body.insert_missing_whitespace = True
        content_body.insert_missing_chap_num = True

        bible_ranges = bible_range.split(by_chap=True, num_verses=None)
        for indiv_range in bible_ranges:
            url = f'https://getbible.net/v2/{self.id}/{book_code}/{indiv_range.start.chap}.json'
            response = requests.get(url)
            resp_dict = response.json()
            
            for verse_dict in resp_dict['verses']:
                verse_num = int(verse_dict['verse'])
                verse_ref = BibleVerse(indiv_range.book, indiv_range.start.chap, verse_num)
                if bible_range.contains(verse_ref):
                    content_body.current_verse = verse_ref
                    content_body.add_start_verse_num()
                    content_body.add_text(str(verse_num))
                    content_body.add_end_verse_num()
                    content_body.add_text(verse_dict['text'])