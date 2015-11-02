# Python 2 and 3
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
"""
Build the content.xml elements.
Fill the Presentation objects lists: new_styleL and new_draw_pageL
"""
from copy import deepcopy
from collections import OrderedDict
from odpslides.find_obj import find_elem_w_attrib, elem_set, NS_attrib, NS
from odpslides.diffs import get_elem_diffs

import sys
if sys.version_info < (3,):
    import odscharts.ElementTree_27OD as ET
else:
    import odscharts.ElementTree_34OD as ET

def init_ref_content_elements( presObj ):
    """
    Get some reference style:style and draw:page elements from ref template.
    Add them as attributes to presObj.
    
    :param presObj: a Presentation object from presentation.py
    :type  presObj: Presentation
    :return: None
    :rtype: None
    """
    style_styleL = presObj.content_xml_obj.findall('office:automatic-styles/style:style')
    text_list_styleL = presObj.content_xml_obj.findall('office:automatic-styles/text:list-style')
    all_styleL = style_styleL + text_list_styleL
    
    drawPageL = presObj.content_xml_obj.findall('office:body/office:presentation/draw:page')
    print( '# Styles=%i,   # Pages=%i'%(len(style_styleL), len(drawPageL)) )

    presObj.targ_ref_stylesD = {} # index=style:name, value=list of [page index, targ_elem, target short tag]

    # First figure out what kind of targets for styles are being used in ref template
    for ipage, page in enumerate( drawPageL ):
        for targ_elem in page.iter():
        #for targ_elem in presObj.body_presentation.iter():
            keyL = targ_elem.keys()
            for key in keyL:
                if key.endswith('}style-name'):
                    style_name = targ_elem.get( key )
                    short_name = presObj.content_xml_obj.qnameOD[ targ_elem.tag ]
                    #print( short_name, style_name )
                    if style_name not in presObj.targ_ref_stylesD:
                        presObj.targ_ref_stylesD[style_name] = []
                    presObj.targ_ref_stylesD[style_name].extend( [ipage, targ_elem, 'targ_elem.tag=%20s'%short_name] )
    
    style_nameSet = set()
    all_styleD = {} # index=style_name, value=elem
    for style in all_styleL:
        #family = style.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}family')
        style_name = style.get('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name')
        style_nameSet.add( style_name )
        all_styleD[ style_name ] = style

    ref_style_keyL = presObj.targ_ref_stylesD.keys()
    ref_style_keyL.sort()
    for key in ref_style_keyL:
        print( key, presObj.targ_ref_stylesD[key] )
        if key not in style_nameSet:
            print('   WARNING... %s NOT USED'%key )
    
    for ikey1 in range(0, len(ref_style_keyL)-1):
        key1 = ref_style_keyL[ikey1]
        ipage1 = presObj.targ_ref_stylesD[key1][0]
        short_tag1 = presObj.targ_ref_stylesD[key1][-1].split()[-1]
        for key2 in ref_style_keyL[ikey1+1:]:
            ipage2 = presObj.targ_ref_stylesD[key2][0]
            short_tag2 = presObj.targ_ref_stylesD[key2][-1].split()[-1]
            
            if ipage1 != ipage2:
                continue
            if presObj.targ_ref_stylesD[key1][-1] == presObj.targ_ref_stylesD[key2][-1]:
                resultL = get_elem_diffs(presObj, all_styleD[ key1 ], all_styleD[ key2 ], ignore_attrL=['style:name'] )
                print( key1, key2, short_tag1, short_tag2, resultL, end='\n\n' )
    
        