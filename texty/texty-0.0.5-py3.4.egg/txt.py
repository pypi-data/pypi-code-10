import re

def tokenize_str(s, word_chars="0-9A-Za-z\-'_"):
    not_word_chars = "[^{0}]+".format(word_chars)
    tokens = re.split(r'{0}'.format(not_word_chars), s, flags=re.UNICODE)
    tokens = [_t for _t in tokens if _t]
    return tokens

def concatenate_textfiles(source, out_path, ext=".txt", recursive=False, seperator="\n",
                          verbose=False):
    text = ""
    if type(source) == list:
        for p in source:
            try:
                with open(p, "r") as handler:
                    if verbose:
                        print("Adding text from", p)
                    text = "{}{}{}".format(text, seperator, handler.read())
            except IOError:
                pass
    elif type(source) == str:
        if not source:
            source = os.getcwd()  # for empty string, use current working directory
        paths = []
        if recursive:
            for root, dirnames, filenames in os.walk(source):
                for f in filenames:
                    if ext:
                        if f.endswith(ext):
                            p = os.path.join(root, f)
                            paths.append(p)
                    else:
                        p = os.path.join(root, f)
                        paths.append(p)
        else:
            if ext:
                for p in os.listdir(source):
                    if p.endswith(ext):
                        paths.append(p)
            else:
                paths = os.listdir(source)
        for p in paths:
            try:
                with open(p, "r") as handler:
                    if verbose:
                        print("Adding text from", p)
                    text = "{}{}{}".format(text, seperator, handler.read())
            except IOError:
                pass
    with open(out_path, "w") as handler:
        handler.write(text)
        if verbose:
            print("The concatenated text was saved as", out_path)
        return text