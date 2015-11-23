"""
打印list or str
"""
def printList(item):
    if(isinstance(item, list)):
        for item_item in item:
            printList(item_item);
    else:
        print(item);