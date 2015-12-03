#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MeCab

MECAB_MODE = "mecabrc"
PARSE_TEXT_ENCODING = 'utf-8'

class MecabAnalysis:

    def __init__(self, text):
        self.tagger = MeCab.Tagger(MECAB_MODE)
        self.text = text

    def test_(self):
        node = self.tagger.parseToNode(self.text)
        print self.text
        while node:
            print node.surface, node.feature
            node = node.next


    def splitByTO(self):
        # if "l" in self.text:
        #     self.text = self.text.replace("l", "L")
        # if "m" in self.text:
        #     self.text = self.text.replace("m", "M")
        # if "s" in self.text:
        #     self.text = self.text.replace("s", "S")
        if "ひとつ" in self.text:
            dst = self.text.replace("ひとつ", "ヒトツ")
            order = dst.split("と")
        else:
            order = self.text.split("と")
        return order

    def get_NameNumSize(self):
        node = self.tagger.parseToNode(self.text)
        noun = ""
        num = 1
        size = ""
        hot_or_ice = ""

        while node:
            pos = node.feature.split(',')[0]
            word = node.feature.split(',')[6]

            if pos == "数詞":
                num = word
            if pos == "名詞":
                noun = word
            if pos == "サイズ":
                size = word
            if pos == "あたたかさ":
                hot_or_ice = word

            node = node.next
        word_lists = {"noun": noun, "num": num, "size": size, "hot_or_ice": hot_or_ice}
        return word_lists


    def parseText(self):
        node = self.tagger.parseToNode(self.text)

        nouns = []
        verbs = []
        adjs = []
        particles = []

        while node:
            pos = node.feature.split(",")[0]
            word = node.surface

            if pos == "名詞":
                nouns.append(word)
            elif pos == "動詞":
                verbs.append(word)
            elif pos == "形容詞":
                adjs.append(word)
            elif pos == "助詞":
                particles.append(word)
            node = node.next
        word_lists = {
            "nouns": nouns,
            "verbs": verbs,
            "adjs": adjs,
            "particles": particles
        }
        return word_lists


if __name__ == '__main__':
    text = "コーヒー"
    b = MecabAnalysis(text)
    print b.test_()
    a = b.get_NameNumSize()
    for i in a:
        print i, a[i]

    # text = "mサイズのホットコーヒー"
    # a = MecabAnalysis(text)
    # a.test_()
    # text = "sサイズのホットコーヒー"
    # a = MecabAnalysis(text)
    # a.test_()
    # text = "lサイズのホットコーヒー"
    # a = MecabAnalysis(text)
    # a.test_()



