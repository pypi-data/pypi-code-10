'''
Created on 16.11.2011

@author: michi
'''

'''MARC language codes for GeoCoding service language/locale support
   http://www.loc.gov/marc/languages/language_code.html
   Order matches QLocale::Language'''

marc_language_code_list = [
    "\0\0\0",# // Unused
    "\0\0\0",# // C
    "abk", #// Abkhazian
    "\0\0\0",# // Afan
    "aar", # Afar
    "afr", # Afrikaans
    "alb", # Albanian
    "amh", # Amharic
    "ara", # Arabic
    "arm", # Armenian
    "asm", # Assamese
    "aym", # Aymara
    "aze", # Azerbaijani
    "bak", # Bashkir
    "baq", # Basque
    "ben", # Bengali
    "\0\0\0", # Bhutani
    "bih", # Bihari
    "bis", # Bislama
    "bre", # Breton
    "bul", # Bulgarian
    "bur", # Burmese
    "bel", # Byelorussian
    "khm", # Cambodian
    "cat", # Catalan
    "chi", # Chinese
    "cos", # Corsican
    "hrv", # Croatian
    "cze", # Czech
    "dan", # Danish
    "dut", # Dutch
    "eng", # English
    "epo", # Esperanto
    "est", # Estonian
    "fao", # Faroese
    "fij", # FijiLanguage
    "fin", # Finnish
    "fre", # French
    "fry", # Frisian
    "gla", # Gaelic
    "glg", # Galician
    "geo", # Georgian
    "ger", # German
    "gre", # Greek
    "\0\0\0", # Greenlandic
    "grn", # Guarani
    "guj", # Gujarati
    "hau", # Hausa
    "heb", # Hebrew
    "hin", # Hindi
    "hun", # Hungarian
    "ice", # Icelandic
    "ind", # Indonesian
    "ina", # Interlingua
    "ile", # Interlingue
    "iku", # Inuktitut
    "ipk", # Inupiak
    "gle", # Irish
    "ita", # Italian
    "jpn", # Japanese
    "jav", # Javanese
    "kan", # Kannada
    "kas", # Kashmiri
    "kaz", # Kazakh
    "kin", # Kinyarwanda
    "kir", # Kirghiz
    "kor", # Korean
    "kur", # Kurdish
    "\0\0\0", # Kurundi
    "lao", # Laothian
    "lat", # Latin
    "lav", # Latvian
    "lin", # Lingala
    "lit", # Lithuanian
    "mac", # Macedonian
    "mlg", # Malagasy
    "may", # Malay
    "mal", # Malayalam
    "mlt", # Maltese
    "mao", # Maori
    "mar", # Marathi
    "mol", # Moldavian
    "mon", # Mongolian
    "nau", # NauruLanguage
    "nep", # Nepali
    "nor", # Norwegian
    "oci", # Occitan
    "ori", # Oriya
    "\0\0\0", # Pashto
    "per", # Persian
    "pol", # Polish
    "por", # Portuguese
    "pan", # Punjabi
    "que", # Quechua
    "roh", # RhaetoRomance
    "rum", # Romanian
    "rus", # Russian
    "smo", # Samoan
    "sag", # Sangho
    "san", # Sanskrit
    "srp", # Serbian
    "\0\0\0", # SerboCroatian
    "\0\0\0", # Sesotho
    "\0\0\0", # Setswana
    "sna", # Shona
    "snd", # Sindhi
    "\0\0\0", # Singhalese
    "\0\0\0", # Siswati
    "slo", # Slovak
    "slv", # Slovenian
    "som", # Somali
    "spa", # Spanish
    "sun", # Sundanese
    "swa", # Swahili
    "swe", # Swedish
    "tgl", # Tagalog
    "tgk", # Tajik
    "tam", # Tamil
    "tat", # Tatar
    "tel", # Telugu
    "tha", # Thai
    "tib", # Tibetan
    "tir", # Tigrinya
    "tog", # TongaLanguage
    "tso", # Tsonga
    "tur", # Turkish
    "tuk", # Turkmen
    "twi", # Twi
    "uig", # Uigur
    "ukr", # Ukrainian
    "urd", # Urdu
    "uzb", # Uzbek
    "vie", # Vietnamese
    "vol", # Volapuk
    "wel", # Welsh
    "wol", # Wolof
    "xho", # Xhosa
    "yid", # Yiddish
    "yor", # Yoruba
    "zha", # Zhuang
    "zul", # Zulu
    "nno", # NorwegianNynorsk
    "bos", # Bosnian
    "div", # Divehi
    "glv", # Manx
    "cor", # Cornish
    "aka", # Akan
    "kok", # Konkani
    "gaa", # Ga
    "ibo", # Igbo
    "kam", # Kamba
    "syc", # Syriac
    "\0\0\0", # Blin
    "\0\0\0", # Geez
    "\0\0\0", # Koro
    "sid", # Sidamo
    "\0\0\0", # Atsam
    "tig", # Tigre
    "\0\0\0", # Jju
    "fur", # Friulian
    "ven", # Venda
    "ewe", # Ewe
    "\0\0\0", # Walamo
    "haw", # Hawaiian
    "\0\0\0", # Tyap
    "\0\0\0", # Chewa
    "fil", # Filipino
    "gsw", # SwissGerman
    "iii", # SichuanYi
    "kpe", # Kpelle
    "nds", # LowGerman
    "nbl", # SouthNdebele
    "nso", # NorthernSotho
    "sme", # NorthernSami
    "\0\0\0", # Taroko
    "\0\0\0", # Gusii
    "\0\0\0", # Taita
    "ful", # Fulah
    "kik", # Kikuyu
    "\0\0\0", # Samburu
    "\0\0\0", # Sena
    "nde", # NorthNdebele
    "\0\0\0", # Rombo
    "\0\0\0", # Tachelhit
    "kab", # Kabyle
    "nyn", # Nyankole
    "\0\0\0", # Bena
    "\0\0\0", # Vunjo
    "bam", # Bambara
    "\0\0\0", # Embu
    "chr", # Cherokee
    "\0\0\0", # Morisyen
    "\0\0\0", # Makonde
    "\0\0\0", # Langi
    "lug", # Ganda
    "bem", # Bemba
    "\0\0\0", # Kabuverdianu
    "\0\0\0", # Meru
    "\0\0\0", # Kalenjin
    "\0\0\0", # Nama
    "\0\0\0", # Machame
    "\0\0\0", # Colognian
    "mas", # Masai
    "\0\0\0", # Soga
    "\0\0\0", # Luyia
    "\0\0\0", # Asu
    "\0\0\0", # Teso
    "\0\0\0", # Saho
    "\0\0\0", # KoyraChiini
    "\0\0\0", # Rwa
    "luo", # Luo
    "\0\0\0", # Chiga
    "\0\0\0", # CentralMoroccoTamazight
    "\0\0\0", # KoyraboroSenni
    "\0\0\0"]# // Shambala    ;
