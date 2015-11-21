from urequest import urlopen

f = urlopen("http://localhost/icons/ubuntu-logo.png")
print(f.read())
