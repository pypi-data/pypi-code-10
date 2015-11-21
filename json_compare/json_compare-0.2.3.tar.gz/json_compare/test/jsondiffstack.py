#!/usr/bin/env python

import json_compare

a = {
    "failureReason" : "Invalid request entity",
    "fieldValidationErrors" : [
        {
            "field" : "normal value 1",
            "reason" : "may not be smelly"
        },
        {
            "field" : "Catalog.name",
            "reason" : "may not be null"
        }
    ]
}
b = {
    "failureReason" : "Invalid request entity",
    "fieldValidationErrors" : [
        {
            "field" : "crazy value 2",
            "reason" : "may not be null"
        },
        {
            "field" : "Catalog.catalogOwner",
            "reason" : "may not be null"
        }
    ]
}
print(json_compare.are_same(a, b)[1])
