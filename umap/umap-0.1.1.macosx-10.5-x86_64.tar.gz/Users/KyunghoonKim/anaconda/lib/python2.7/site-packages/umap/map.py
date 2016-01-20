# -*- coding: utf-8 -*-

from IPython.display import HTML
import folium

def inline_map(map):
    """
    Embeds the HTML source of the map directly into the IPython notebook.

    This method will not work if the map depends on any files (json data). Also this uses
    the HTML5 srcdoc attribute, which may not be supported in all browsers.
    """
    if isinstance(map, folium.Map):
        map._build_map()
        srcdoc = map.HTML.replace('"', '&quot;')
        embed = HTML('<iframe srcdoc="{srcdoc}" '
                     'style="width: 100%; height: 500px; '
                     'border: none"></iframe>'.format(srcdoc=srcdoc))
    else:
        raise ValueError('{!r} is not a folium Map instance.')
    return embed

def embed_map(map, path="map.html"):
    path = path
    """
    Embeds a linked iframe to the map into the IPython notebook.

    Note: this method will not capture the source of the map into the notebook.
    This method should work for all maps (as long as they use relative urls).
    """
    map.create_map(path=path)
    return HTML('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>'.format(path=path))

def export_map(map, path="export_data.html", js="test.js"):
    path = path
    map.create_map(path=path)

    # Open the HTML file
    f = open(path, 'r')
    text = f.read()
    f.close()

    # Parsing HTML for circles
    pos = text.find('var circle_1')
    if len(splited) > 1:
        circles = text[pos:]
    else:
        print 'Length is 1'
    circles = circles.replace('</script>','').replace('</body>','')
    cv = ''
    vs = []
    for i in circles.split('\n'):
        if 'map' not in i:
            cv += i.replace('  ','')+'\n'
        if 'var ' in i:
            i = i.replace('  ','')
            vs.append(i.split(' ')[1])
    # Making a new JS file
    head = """var circle_group = L.layerGroup("""
    vs = str(vs).replace("'", '')
    tail = """);"""
    java_1 = cv
    java_2 = head+vs+tail
    f = open(js, 'w')
    filename = js.split('.')[0]+'_'
    f.write(java_1.replace('circle_', filename))
    f.write(java_2.replace('circle_', filename))
    f.close()
    return js