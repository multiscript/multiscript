
import logging
from pathlib import Path
import platform
import plistlib

from bibleref import BibleBook, BibleRange, BibleVerse
from bibleref.ref import BibleRefParsingError

from multiscript.sources.base import BibleSource, VersionProgressReporter
from multiscript.bible.version import BibleVersion
from multiscript.plan.runner import PlanRunner


_logger = logging.getLogger(__name__)


class AccordanceSource(BibleSource):
    def __init__(self, plugin):
        super().__init__(plugin)
        self.id = "accordancebible.com"
        self.name = "Accordance"

        if platform.system() == "Darwin":
            from multiscript.sources.accordance.mac import AccordanceMacPlatform
            self.platform = AccordanceMacPlatform(self)
        else:
            self.platform = None

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
        if self.platform is not None and self.platform.DEFAULT_ACCORDANCE_DATA_PATH is not None:
            data_path = Path(self.platform.DEFAULT_ACCORDANCE_DATA_PATH).expanduser().resolve()
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
                    
                    version.user_labels.abbrev = info_dict.get('com.oaktree.module.textabbr', '').strip()
                    if version.user_labels.abbrev == "":
                        version.user_labels.abbrev = id
                    
                    version.user_labels.name = info_dict.get('com.oaktree.module.fullmodulename', '').strip()
                    if version.user_labels.name == "":
                        version.user_labels.name = info_dict.get('com.oaktree.module.humanreadablename', '').strip()
                        if version.user_labels.name == "":
                            version.user_labels.name = version.user_labels.abbrev
                    
                    version.copyright = info_dict.get('com.oaktree.module.copyriteinfo', '').strip()
                    vers_lang_code = info_dict.get('com.oaktree.module.textlanguage', None)
                    
                    if vers_lang_code is None:
                        # Handle missing language codes.
                        version_user_labels_name_casefold = version.user_labels.name.casefold()
                        # First, try 'com.oaktree.module.language' key, which is an older Accordance
                        # numeric language code:
                        #   1 = Usually English, but not always
                        #   2 = Greek
                        #   3 = Hebrew
                        numeric_lang_code = info_dict.get('com.oaktree.module.language', 0)
                        if numeric_lang_code == 2:
                            vers_lang_code = 'el'
                        elif numeric_lang_code == 3:
                            vers_lang_code = 'he'
                        # If still no language code, look for languages in the module name.
                        # The languages searched for here are derived from the list of Accordance modules
                        # at https://www.accordancebible.com/wp-content/uploads/2021/06/CompModList21_05.pdf
                        elif 'Afrikaans'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'af'
                        elif 'Arabic'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'ar'
                        elif 'Chinese'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'zh'
                        elif 'Dutch'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'nl'
                        elif 'Finnish'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'fi'
                        elif 'French'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'fr'
                        elif 'German'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'de'
                        elif 'Italian'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'it'
                        elif 'Japanese'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'ja'
                        elif 'Korean'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'ko'
                        elif 'Latvian'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'lv'
                        elif 'Greek'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'el'
                        elif 'Bokmål'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'nb'
                        elif 'Nynorsk'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'nn'
                        elif 'Norwegian'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'no'
                        elif 'Polish'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'pl'
                        elif 'Portuguese'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'pt'
                        elif 'Romanian'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'ro'
                        elif 'Russian'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'ru'
                        elif 'Spanish'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'es'
                        elif 'Swedish'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'sv'
                        elif 'Tagalog'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'tl'
                        elif 'Thai'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'th'
                        elif 'Ethiopic (Ge'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'gez'
                        elif 'Coptic'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'cop'
                        elif 'Latin'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'la'
                        elif 'Aramaic'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'arc'
                        elif 'Samaritan Targum'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'sam'
                        elif 'Vetus Latina'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'la'
                        elif 'Peshitta'.casefold() in version_user_labels_name_casefold:
                            vers_lang_code = 'syc'
                        elif numeric_lang_code == 1:
                            # At this point it's likely to be English
                            vers_lang_code = 'en'

                    if vers_lang_code is not None:
                        version.set_lang_from_code(vers_lang_code)

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
        self.bible_source: AccordanceSource = self.bible_source
        data_path = Path(self.bible_source.platform.DEFAULT_ACCORDANCE_DATA_PATH).expanduser().resolve()
        text_path = data_path / "Modules" / "Texts" / f"{self.id}.atext"
        if not text_path.exists() or not text_path.is_dir():
            _logger.info(f"Accordance module {self.id} not found.")
            return

        book_code = AccordanceVersion.book_codes[bible_range.start.book]
        content_body = bible_content.body
        content_body.strip_text = True
        content_body.insert_missing_whitespace = True
        content_body.insert_missing_chap_num = True

        bible_ranges = bible_range.split(by_chap=True, num_verses=None)
        for indiv_range in bible_ranges:
            if self.bible_source.platform is not None:
                accordance_text = self.bible_source.platform.get_bible_text(self.id, str(indiv_range))
                linebreak_before_accord_lines = False
                for accordance_line in str(accordance_text).splitlines():
                    first_space = accordance_line.find(' ')
                    second_space = accordance_line.find(' ', first_space + 1)
                    new_verse = False
                    if second_space != -1:
                        try:
                            verse_ref_str = accordance_line[0:second_space].replace('.','')
                            content_body.current_verse = BibleVerse(verse_ref_str)
                            # If we got to here, the line begins with a verse reference, so it's a new verse
                            new_verse = True
                            accordance_line = accordance_line[second_space+1:]
                        except BibleRefParsingError:
                            # No valid verse ref means we insert start inserting linebreaks before each
                            # line of text from Accordance
                            linebreak_before_accord_lines = True
                            # TODO: We may also need to find the previous start-paragraph token and mark it as poetry.

                    paragraphs = accordance_line.split('¶ ')
                    for i in range(len(paragraphs)):
                        if len(paragraphs[i]) > 0:
                            if linebreak_before_accord_lines:
                                content_body.add_line_break()
                            if new_verse:
                                content_body.add_start_verse_num()
                                content_body.add_text(str(content_body.current_verse.verse_num))
                                content_body.add_end_verse_num()
                                new_verse = False
                            content_body.add_text(paragraphs[i])
                        if i < (len(paragraphs)-1):
                            content_body.add_end_paragraph()
                            content_body.add_start_paragraph()
                            # New paragraphs end any run of inserting linebreaks
                            linebreak_before_accord_lines = False


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


class AccordancePlatform:
    def __init__(self, bible_source: BibleSource):
        self.bible_source = bible_source
        self.DEFAULT_ACCORDANCE_DATA_PATH = None

    def get_ui_text_names(self):
        '''Returns the list of Accordance texts as displayed in the Get Verses dialog.'''
        return []
    
    def get_bible_text(self, accordance_module_id: str, bible_range_str: str):
        return ""
