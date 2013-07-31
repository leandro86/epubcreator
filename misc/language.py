# -*- coding: utf-8 -*-

# Copyright (C) 2013 Leandro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Language:


    _languageNameMap = {}
    _languageCodeMap = {}


    @staticmethod
    def getSortedLanguagesNames():
        Language._loadLanguages()
        languages = [language for language in Language._languageNameMap.keys()]
        languages.sort()

        return languages


    @staticmethod
    def getLanguageName(code):
        Language._loadLanguages()
        return Language._languageCodeMap[code]


    @staticmethod
    def getLanguageCode(name):
        Language._loadLanguages()
        return Language._languageNameMap[name]


    @staticmethod
    def _loadLanguages():
        if len(Language._languageCodeMap) != 0:
            return

        languages = (("aa", "Afar"),
                     ("ab", "Abjaso (o abjasiano)"),
                     ("ae", "Avéstico"),
                     ("af", "Afrikaans"),
                     ("ak", "Akano"),
                     ("am", "Amárico"),
                     ("an", "Aragonés"),
                     ("ar", "árabe"),
                     ("as", "Asamés"),
                     ("av", "Avar"),
                     ("ay", "Aimara"),
                     ("az", "Azerí"),
                     ("ba", "Baskir"),
                     ("be", "Bielorruso"),
                     ("bg", "Búlgaro"),
                     ("bh", "Bhojpurí"),
                     ("bi", "Bislama"),
                     ("bm", "Bambara"),
                     ("bn", "Bengalí"),
                     ("bo", "Tibetano"),
                     ("br", "Bretón"),
                     ("bs", "Bosnio"),
                     ("ca", "Catalán"),
                     ("ce", "Checheno"),
                     ("ch", "Chamorro"),
                     ("co", "Corso"),
                     ("cr", "Cree"),
                     ("cs", "Checo"),
                     ("cu", "Eslavo eclesiástico antiguo"),
                     ("cv", "Chuvasio"),
                     ("cy", "Galés"),
                     ("da", "Danés"),
                     ("de", "Alemán"),
                     ("dv", "Maldivo"),
                     ("dz", "Dzongkha"),
                     ("ee", "Ewe"),
                     ("el", "Griego (moderno)"),
                     ("en", "Inglés"),
                     ("eo", "Esperanto"),
                     ("es", "Español (o castellano)"),
                     ("et", "Estonio"),
                     ("eu", "Euskera"),
                     ("fa", "Persa"),
                     ("ff", "Fula"),
                     ("fi", "Finés (o finlandés)"),
                     ("fj", "Fiyiano (o fiyi)"),
                     ("fo", "Feroés"),
                     ("fr", "Francés"),
                     ("fy", "Frisón (o frisio)"),
                     ("ga", "Irlandés (o gaélico)"),
                     ("gd", "Gaélico escocés"),
                     ("gl", "Gallego"),
                     ("gn", "Guaraní"),
                     ("gu", "Guyaratí (o guyaratí)"),
                     ("gv", "Manés (gaélico manés o de Isla de Man)"),
                     ("ha", "Hausa"),
                     ("he", "Hebreo"),
                     ("hi", "Hindi (o hindú)"),
                     ("ho", "Hiri motu"),
                     ("hr", "Croata"),
                     ("ht", "Haitiano"),
                     ("hu", "Húngaro"),
                     ("hy", "Armenio"),
                     ("hz", "Herero"),
                     ("ia", "Interlingua"),
                     ("id", "Indonesio"),
                     ("ie", "Occidental"),
                     ("ig", "Igbo"),
                     ("ii", "Yi de Sichuán"),
                     ("ik", "Inupiaq"),
                     ("io", "Ido"),
                     ("is", "Islandés"),
                     ("it", "Italiano"),
                     ("iu", "Inuktitut"),
                     ("ja", "Japonés"),
                     ("jv", "Javanés"),
                     ("ka", "Georgiano"),
                     ("kg", "Kongo"),
                     ("ki", "Kikuyu"),
                     ("kj", "Kuanyama"),
                     ("kk", "Kazajo (o kazajio)"),
                     ("kl", "Groenlandés (o kalaallisut)"),
                     ("km", "Camboyano (o jemer)"),
                     ("kn", "Canarés"),
                     ("ko", "Coreano"),
                     ("kr", "Kanuri"),
                     ("ks", "Cachemiro"),
                     ("ku", "Kurdo"),
                     ("kv", "Komi"),
                     ("kw", "Córnico"),
                     ("ky", "Kirguís"),
                     ("la", "Latín"),
                     ("lb", "Luxemburgués"),
                     ("lg", "Luganda"),
                     ("li", "Limburgués"),
                     ("ln", "Lingala"),
                     ("lo", "Lao"),
                     ("lt", "Lituano"),
                     ("lu", "Luba-katanga"),
                     ("lv", "Letón"),
                     ("mg", "Malgache (o malagasy)"),
                     ("mh", "Marshalés"),
                     ("mi", "Maorí"),
                     ("mk", "Macedonio"),
                     ("ml", "Malayalam"),
                     ("mn", "Mongol"),
                     ("mr", "Maratí"),
                     ("ms", "Malayo"),
                     ("mt", "Maltés"),
                     ("my", "Birmano"),
                     ("na", "Nauruano"),
                     ("nb", "Noruego bokmål"),
                     ("nd", "Ndebele del norte"),
                     ("ne", "Nepalí"),
                     ("ng", "Ndonga"),
                     ("nl", "Neerlandés (u holandés)"),
                     ("nn", "Nynorsk"),
                     ("no", "Noruego"),
                     ("nr", "Ndebele del sur"),
                     ("nv", "Navajo"),
                     ("ny", "Chichewa"),
                     ("oc", "Occitano"),
                     ("oj", "Ojibwa"),
                     ("om", "Oromo"),
                     ("or", "Oriya"),
                     ("os", "Osético"),
                     ("pa", "Panyabí (o penyabi)"),
                     ("pi", "Pali"),
                     ("pl", "Polaco"),
                     ("ps", "Pastú (o pashto)"),
                     ("pt", "Portugués"),
                     ("qu", "Quechua"),
                     ("rm", "Romanche"),
                     ("rn", "Kirundi"),
                     ("ro", "Rumano"),
                     ("ru", "Ruso"),
                     ("rw", "Ruandés"),
                     ("sa", "Sánscrito"),
                     ("sc", "Sardo"),
                     ("sd", "Sindhi"),
                     ("se", "Sami septentrional"),
                     ("sg", "Sango"),
                     ("si", "Cingalés"),
                     ("sk", "Eslovaco"),
                     ("sl", "Esloveno"),
                     ("sm", "Samoano"),
                     ("sn", "Shona"),
                     ("so", "Somalí"),
                     ("sq", "Albanés"),
                     ("sr", "Serbio"),
                     ("ss", "Suazi (swati o siSwati)"),
                     ("st", "Sesotho"),
                     ("su", "Sundanés"),
                     ("sv", "Sueco"),
                     ("sw", "Suajili"),
                     ("ta", "Tamil"),
                     ("te", "Telugú"),
                     ("tg", "Tayiko"),
                     ("th", "Tailandés"),
                     ("ti", "Tigriña"),
                     ("tk", "Turcomano"),
                     ("tl", "Tagalo"),
                     ("tn", "Setsuana"),
                     ("to", "Tongano"),
                     ("tr", "Turco"),
                     ("ts", "Tsonga"),
                     ("tt", "Tártaro"),
                     ("tw", "Twi"),
                     ("ty", "Tahitiano"),
                     ("ug", "Uigur"),
                     ("uk", "Ucraniano"),
                     ("ur", "Urdu"),
                     ("uz", "Uzbeko"),
                     ("ve", "Venda"),
                     ("vi", "Vietnamita"),
                     ("vo", "Volapük"),
                     ("wa", "Valón"),
                     ("wo", "Wolof"),
                     ("xh", "Xhosa"),
                     ("yi", "Yídish (o yiddish)"),
                     ("yo", "Yoruba"),
                     ("za", "Chuan (o zhuang)"),
                     ("zh", "Chino"),
                     ("zu", "Zulú"))

        for code, language in languages:
            Language._languageNameMap[language] = code
            Language._languageCodeMap[code] = language