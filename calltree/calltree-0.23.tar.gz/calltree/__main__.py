"""
apiparse

Parse API and API groups from sources. List the API occurences from all
directories and sub directories

"""

# Main Routine
if __name__ == "__main__":
    import calltree
    f = calltree.calltree.calltree()
    f.showtree()
    f.showgraph()

