#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rdflib
from rdflib.Graph import ConjunctiveGraph
from rdflib import Namespace

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
owls = Namespace("http://www.daml.org/services/owl-s/1.0DL/Process.owl#")

cafemenu_class = Namespace("http://www.yamaguti.comp.ae.keio.ac.jp/CafeMenuOntology/class/")
cafemenu_property = Namespace("http://www.yamaguti.comp.ae.keio.ac.jp/CafeMenuOntology/property/")
cafemenu_instance = Namespace("http://www.yamaguti.comp.ae.keio.ac.jp/CafeMenuOntology/instance/")

common_menu = ["カフェモカ", "カフェラテ", "コーヒー", "ココア", "ミルク", "抹茶ラテ", "ティー", "ミルクティー", "レモンティー", "紅茶"]


class OntologyProcessor:
    def __init__(self):
        self.CafeMenuOntology = ConjunctiveGraph()
        # self.CafeMenuOntology.load("/home/k-nakamura/Desktop/ontology/CafeMenuOntology_new.owl")
        self.CafeMenuOntology.load("/home/k-nakamura/catkin_ws/src/practice_1/ontology/CafeOntology_withoutPCD_V6.owl")
        self.CafeMenuOntology.load("/home/k-nakamura/catkin_ws/src/practice_1/ontology/CafeOntology_withoutPCD_V14_2.owl")
        self.endClassList = []

    def label_query(self, text):
        print type(text)
        text = unicode(text, 'utf-8')
        print type(text)
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?s
        where {
        ?s rdfs:label %s .
        }
        """ % text)
        print results

    def subClass_length(self, text):
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?s
        where {
        ?s rdfs:subClassOf cafemenu_class:%s .
        }
        """ % text)

        # print class_name
        return len(results)


        # print class_name
        # print len(results)
        # for raw in results:
        #     for uri in raw:
        #         menu_name = uri.split('/')[-1]

    # 末端のインスタンスについたlabelを返す
    # 要は、フツーにメニューを返すだけ
    # def get_menu(self):
    #     results = self.CafeMenuOntology.query("""
    #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #     select ?label
    #     where {
    #     ?s2 rdfs:subClassOf ?s1 .
    #     ?s3 rdfs:subClassOf ?s2 .
    #     ?s4 rdfs:subClassOf ?s3 .
    #     ?instance rdf:type ?s4 .
    #     ?instance rdfs:label ?label .
    #     }
    #     """)
    #     menuList = []
    #     for raw in results:
    #         for i in raw:
    #             menu_name = i.split('/')[-1]
    #             menuList.append(menu_name)
    #     return menuList
    def get_menu(self):
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?label
        where {
        ?instance cafemenu_property:hotORice ?o .
        ?instance rdfs:label ?label .
        }
        """)
        menuList = []
        for raw in results:
            for i in raw:
                menu_name = i.split('/')[-1]
                menuList.append(menu_name)
        return menuList

    def get_menu_as_instance(self):
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?instance
        where {
        ?instance cafemenu_property:hotORice ?o .
        }
        """)
        menuList = []
        for raw in results:
            for i in raw:
                menu_name = i.split('/')[-1]
                menuList.append(menu_name)
        return menuList

    def get_milk(self):
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?p ?o
        where {
        cafemenu_class:OrangeJuice ?p ?o .
        }
        """)
        menuList = []
        for raw in results:
            for i in raw:
                menuList.append(i)
                # menu_name = i.split('/')[-1]
                # menuList.append(menu_name)
        return menuList

    # 引数のラベルがついたインスタンスorクラスを返す
    def labeled_resource_len(self, label):
        # label = "\"" + label + "\"@ja"
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?o
        where {
        cafemenu_class:%s rdfs:label ?o .
        }""" % label)
        # print "len: ", len(results)
        # for raw in results:
        #     for uri in raw:
        #         menu_name = uri.split("/")[-1]
        #         return menu_name
        return len(results)

    # textラベルがついたクラスをA_classとすると、A_classの下の階層にあるクラスorインスタンスについたラベルを返す
    # 例えば、"コーヒー"っていわれたときに、こんなホットコーヒーとかアイスコーヒーなんかがありますよってのを返す
    # textラベルがついたものがインスタンスだった場合は、lenは0
    def return_candidate(self, text):
        text = "\"" + text + "\"@ja"
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?label
        where {
        ?class rdfs:label %s .
        ?instance rdf:type ?class .
        ?instance rdfs:label ?label .
        }""" % text)

        menuList = []
        for raw in results:
            for uri in raw:
                menu_name = uri.split("/")[-1]
                menuList.append(menu_name)

        return menuList

    def get_blank(self, hot_or_ice, menu):
        menu = "\"" + menu + "\"@ja"

        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?label
        where {
        ?class rdfs:label %s .
        ?instance rdf:type ?class .
        ?instance rdfs:label ?label .
        }""" % menu)
        menuList = []
        for raw in results:
            for uri in raw:
                menu_name = uri.split("/")[-1]
                if hot_or_ice in menu_name:
                    menuList.append(menu_name)
        return menuList

    def show_size(self, hot_or_ice, menu):
        menu = "\"" + menu + "\"@ja"

        if hot_or_ice == "ホット":
            hot_or_ice = "Hot"
        elif hot_or_ice == "アイス":
            hot_or_ice = "Ice"

        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?label
        where {
        ?class rdfs:label %s .
        ?instance rdf:type ?class .
        ?instance cafemenu_property:hotORice "%s"^^xsd:string .
        ?instance rdfs:label ?label .
        }""" % (menu, hot_or_ice))
        menuList = []
        for raw in results:
            for uri in raw:
                menu_name = uri.split('/')[-1]
                menuList.append(menu_name)
        return menuList

    def show_HotIce(self, size, menu):
        menu = "\"" + menu + "\"@ja"

        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?label
        where {
        ?class rdfs:label %s .
        ?instance rdf:type ?class .
        ?instance cafemenu_property:Size "%s"^^xsd:string .
        ?instance rdfs:label ?label .
        }""" % (menu, size))
        menuList = []
        for raw in results:
            for uri in raw:
                menu_name = uri.split('/')[-1]
                menuList.append(menu_name)
        return menuList

    def get_hotORice_from_menu(self, menu):
        menu = "\"" + menu + "\"@ja"

        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?o
        where {
        ?class rdfs:label %s .
        ?instance rdf:type ?class .
        ?instance cafemenu_property:hotORice ?o .
        }""" % menu)

        hotORice_set = set()
        for raw in results:
            for elm in raw:
                if str(elm) == "Hot":
                    elm = "ホット"
                else:
                    elm = "アイス"
                hotORice_set.add(elm)
        return list(hotORice_set)

    def return_instance(self, menu):
        menu = "\"" + menu + "\"@ja"

        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?instance
        where {
        ?instance rdfs:label %s .
        }""" % menu)

        for raw in results:
            for elm in raw:
                elm = elm.split('/')[-1]
                return elm

    def get_size_from_menu(self, menu):
        menu = "\"" + menu + "\"@ja"

        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?o
        where {
        ?class rdfs:label %s .
        ?instance rdf:type ?class .
        ?instance cafemenu_property:Size ?o .
        }""" % menu)

        size_set = set()
        for raw in results:
            for elm in raw:
                size_set.add(elm)
        return list(size_set)

    def from_instance_to_classLabel(self, menu):
        menu = "\"" + menu + "\"@ja"

        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?o
        where {
        ?instance rdfs:label %s .
        ?instance rdfs:subClassOf ?class .
        ?class rdfs:label ?o .
        }""" % menu)

        size_set = set()
        for raw in results:
            for elm in raw:
                size_set.add(elm)
        return list(size_set)

    def from_label_to_instance(self, label):
        label = "\"" + label + "\"@ja"
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?instance
        where {
        ?instance rdfs:label %s .
        }""" % label)

        instance_name = ''
        for raw in results:
            for elm in raw:
                instance_name = elm.split('/')[-1]
        return instance_name

    def from_class_to_label(self, _class):
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?label
        where {
        cafemenu_class:%s rdfs:label ?label .
        }""" % _class)

        class_name = ''
        for raw in results:
            for elm in raw:
                class_name = elm.split('/')[-1]
        return class_name


    def from_instance_to_label(self, instance):
        results = self.CafeMenuOntology.query("""
        PREFIX cafemenu_class: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/class/>
        PREFIX cafemenu_property: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/property/>
        PREFIX cafemenu_instance: <http://www.yamaguti.comp.ae.keio.ac.jp/CafeOntology/Menu/instance/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select ?label
        where {
        cafemenu_instance:%s rdfs:label ?label .
        }""" % instance)

        instance_name = ''
        for raw in results:
            for elm in raw:
                instance_name = elm.split('/')[-1]
        return instance_name

if __name__ == '__main__':
    a = OntologyProcessor()
    # print a.return_instance('Mサイズホットコーヒー')
    # print a.labeled_resource('')
    # for i in a.get_menu_as_instance():
    #     print i

    # print '\n'
    # for i in a.from_instance_to_classLabel('Lサイズオレンジジュース'):
    #     print i
    # print a.from_label_to_instance('コーヒー')
    # print a.labeled_resource_len('Tea')
    print a.from_class_to_label('Coffee')
    # print a.from_instance_to_label('LsizeHotCoffee')
