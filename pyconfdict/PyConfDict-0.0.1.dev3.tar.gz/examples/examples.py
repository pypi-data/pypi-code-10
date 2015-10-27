#! /usr/bin/env python3

import sys
import json 
sys.path.append("..")

from pyconfdict import PyConfDict

print("============================")
print("EXAMPLE 1")
print("============================")

print("loading dictionary 1 (from dict1.json)")
a=PyConfDict(json_fn="dict1.json")
print("loading dictionary 2 (from dict2.json)")
b=PyConfDict(json_fn="dict2.json")

print()
print("dictionary 1:",a)
print("dictionary 2:",b)

a.update(b)

print()
print("updating dictionary 1 using dictionary 2")
print("dictionary 1:",a)

print()
print("saving dictionary 1 to _dict1_updated.json")
a.save_to_json("_dict1_updated.json")


print()
print("============================")
print("EXAMPLE 2")
print("============================")

a=PyConfDict([
			("car","Skoda"),
			("shoes","Bata"),
		]
	)
print("dictionary 1:",a)
b=PyConfDict([
			("beer","Pilsner Urquel"),
			("car","Tatra"),
		]
	)
print("dictionary 2:",b)


print()
print("filling missing values in dictionary 1 from dictionary 2")
a.fill_missing(b)
print("dictionary 1:",a)

print()
print("saving dictionary 1 to _dict1_filled.json")
a.save_to_json("_dict1_filled.json")


