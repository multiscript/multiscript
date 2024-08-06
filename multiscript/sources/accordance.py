
import logging
from pathlib import Path
import platform
import plistlib

from bibleref import BibleBook, BibleRange, BibleVerse

from multiscript.sources.base import BibleSource, VersionProgressReporter
from multiscript.bible.version import BibleVersion
from multiscript.plan.runner import PlanRunner


_logger = logging.getLogger(__name__)

DEFAULT_ACCORDANCE_DATA_PATH = None
if platform.system() == "Darwin":
    DEFAULT_ACCORDANCE_DATA_PATH = "~/Library/Application Support/Accordance"


class AccordanceSource(BibleSource):
    def __init__(self, plugin):
        super().__init__(plugin)
        self.id = "accordancebible.com"
        self.name = "Accordance"

    def new_bible_version(self, version_id=None, name=None, lang=None, abbrev=None):
        '''Overridden from BibleVersion.
        
        Constructs a new AccordanceVersion for this BibleSource.
        '''
        return AccordanceVersion(self, version_id, name, lang, abbrev)

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

    def get_all_versions(self, progress_reporter: VersionProgressReporter):
        '''Overridden from BibleVersion.
        
        Return all of the BibleVersions available for this BibleSource.
        '''
        versions = []
        if DEFAULT_ACCORDANCE_DATA_PATH is not None:
            data_path = Path(DEFAULT_ACCORDANCE_DATA_PATH).expanduser().resolve()
            texts_path = data_path / "Modules" / "Texts"
            if texts_path.exists():
                for text_path in texts_path.glob('*.atext'):
                    if not text_path.is_dir():
                        continue
                    info_path = text_path / "Info.plist"
                    if not info_path.exists():
                        info_path = text_path / "ExtraInfo.plist"
                        if not info_path.exists():
                            _logger.warn(f"plist not found for {text_path}")
                            continue
                    with open(info_path, 'rb') as file:
                        info_dict = plistlib.load(file)
                    id = text_path.stem
                    version = self.new_bible_version(id)
                    
                    version.user_labels.abbrev = info_dict.get('com.oaktree.module.textabbr', id).strip()
                    version.user_labels.name = info_dict.get('com.oaktree.module.humanreadablename',
                                                             info_dict.get('com.oaktree.module.fullmodulename',
                                                                           version.user_labels.abbrev)).strip()
                    version.copyright = info_dict.get('com.oaktree.module.copyriteinfo', '').strip()
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


class AccordanceVersion(BibleVersion):
    book_codes = {BibleBook.Gen:        "Gen",
                  BibleBook.Exod:       "Ex",
                  BibleBook.Lev:        "Lev",
                  BibleBook.Num:        "Num",
                  BibleBook.Deut:       "Deut",
                  BibleBook.Josh:       "Josh",
                  BibleBook.Judg:       "Judg",
                  BibleBook.Ruth:       "Ruth",
                  BibleBook.ISam:       "1Sam",
                  BibleBook.IISam:      "2Sam",
                  BibleBook.IKgs:       "1Kings",
                  BibleBook.IIKgs:      "2Kings",
                  BibleBook.IChr:       "1Chr",
                  BibleBook.IIChr:      "2Chr",
                  BibleBook.Ezra:       "Ezra",
                  BibleBook.Neh:        "Neh",
                  BibleBook.Esth:       "Esth",
                  BibleBook.Job:        "Job",
                  BibleBook.Psa:        "Psa",
                  BibleBook.Prov:       "Prov",
                  BibleBook.Eccl:       "Eccl",
                  BibleBook.Song:       "Song",
                  BibleBook.Isa:        "Is",
                  BibleBook.Jer:        "Jer",
                  BibleBook.Lam:        "Lam",
                  BibleBook.Ezek:       "Ezek",
                  BibleBook.Dan:        "Dan",
                  BibleBook.Hos:        "Hos",
                  BibleBook.Joel:       "Joel",
                  BibleBook.Amos:       "Amos",
                  BibleBook.Obad:       "Obad",
                  BibleBook.Jonah:      "Jonah",
                  BibleBook.Mic:        "Mic",
                  BibleBook.Nah:        "Nah",
                  BibleBook.Hab:        "Hab",
                  BibleBook.Zeph:       "Zeph",
                  BibleBook.Hag:        "Hag",
                  BibleBook.Zech:       "Zech",
                  BibleBook.Mal:        "Mal",
                  BibleBook.Matt:       "Matt",
                  BibleBook.Mark:       "Mark",
                  BibleBook.Luke:       "Luke",
                  BibleBook.John:       "John",
                  BibleBook.Acts:       "Acts",
                  BibleBook.Rom:        "Rom",
                  BibleBook.ICor:       "1Cor",
                  BibleBook.IICor:      "2Cor",
                  BibleBook.Gal:        "Gal",
                  BibleBook.Eph:        "Eph",
                  BibleBook.Phil:       "Phil",
                  BibleBook.Col:        "Col",
                  BibleBook.ITh:        "1Th",
                  BibleBook.IITh:       "2Th",
                  BibleBook.ITim:       "1Tim",
                  BibleBook.IITim:      "2Tim",
                  BibleBook.Titus:      "Titus",
                  BibleBook.Phlm:       "Philem",
                  BibleBook.Heb:        "Heb",
                  BibleBook.Jam:        "James",
                  BibleBook.IPet:       "1Pet",
                  BibleBook.IIPet:      "2Pet",
                  BibleBook.IJn:        "1John",
                  BibleBook.IIJn:       "2John",
                  BibleBook.IIIJn:      "3John",
                  BibleBook.Jude:       "Jude",
                  BibleBook.Rev:        "Rev"
                  }

    def __init__(self, source=None, id=None, name=None, lang=None, abbrev=None):
        super().__init__(source, id, name, lang, abbrev)

    def load_content(self, bible_range: BibleRange, bible_content, plan_runner: PlanRunner):
        book_code = AccordanceVersion.book_codes[bible_range.start.book]
        content_body = bible_content.body
        content_body.strip_text = True
        content_body.insert_missing_whitespace = True
        # content_body.insert_missing_chap_num = True

        # bible_ranges = bible_range.split(by_chap=True, num_verses=None)
        # for indiv_range in bible_ranges:
        #     indiv_range: BibleRange = indiv_range
        #     url = f'https://api.getbible.net/v2/{self.id}/{book_code}/{indiv_range.start.chap_num}.json'
        #     response = requests.get(url, timeout=15)
        #     resp_dict = response.json()
        #     for verse_dict in resp_dict['verses']:
        #         verse_num = int(verse_dict['verse'])
        #         verse_ref = BibleVerse(indiv_range.start.book, indiv_range.start.chap_num, verse_num)
        #         if bible_range.contains(verse_ref):
        #             content_body.current_verse = verse_ref
        #             content_body.add_start_verse_num()
        #             content_body.add_text(str(verse_num))
        #             content_body.add_end_verse_num()
        #             content_body.add_text(verse_dict['text'])