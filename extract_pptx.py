import zipfile
import xml.etree.ElementTree as ET
import re
import os

def extract_text_from_pptx(pptx_path):
    text_content = []
    
    with zipfile.ZipFile(pptx_path, 'r') as z:
        # Get slide order from presentation.xml.rels
        # Actually simplest is just to iterate slide1.xml, slide2.xml... 
        # usually they are named sequentially but maybe not in presentation order.
        # Let's check presentation.xml for the order of slide references (rId)
        # then check presentation.xml.rels to map rId to filename.
        
        # 1. Map rId to slide filename
        rels_xml = z.read('ppt/_rels/presentation.xml.rels')
        rels_root = ET.fromstring(rels_xml)
        namespaces = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
        
        rId_to_target = {}
        for rel in rels_root.findall('rel:Relationship', namespaces):
            rId = rel.get('Id')
            target = rel.get('Target')
            # Target is usually like "slides/slide1.xml" or "/ppt/slides/slide1.xml"
            if 'slides/slide' in target:
                rId_to_target[rId] = target

        # 2. Get slide order from presentation.xml
        pres_xml = z.read('ppt/presentation.xml')
        pres_root = ET.fromstring(pres_xml)
        # The namespace for presentation is usually somewhat standard
        # searching for p:sldId
        # We can just search by tag name ignoring namespace to be robust
        
        slide_order = []
        for elem in pres_root.iter():
            if elem.tag.endswith('sldId'):
                rId = elem.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                if rId and rId in rId_to_target:
                    slide_order.append(rId_to_target[rId])
        
        # 3. Extract text from each slide in order
        for idx, slide_rel_path in enumerate(slide_order):
            # Resolve path (it might be relative to ppt/)
            if slide_rel_path.startswith('/'):
                path_in_zip = slide_rel_path[1:]
            else:
                path_in_zip = 'ppt/' + slide_rel_path
            
            try:
                slide_xml = z.read(path_in_zip)
                root = ET.fromstring(slide_xml)
                
                # Extract text from a:t elements
                slide_text = []
                # Namespace for main drawing is a
                # Again, search all elements ending in 't' (text)
                for elem in root.iter():
                    if elem.tag.endswith('}t'):
                        if elem.text:
                            slide_text.append(elem.text)
                
                text_content.append(f"--- Slide {idx + 1} ---")
                text_content.append("\n".join(slide_text))
                text_content.append("\n")
                
            except KeyError:
                print(f"Could not find {path_in_zip}")
                
    return "\n".join(text_content)

if __name__ == "__main__":
    pptx_file = "week2/slides/Lecture_9_29_25_public.pptx"
    try:
        print(extract_text_from_pptx(pptx_file))
    except Exception as e:
        print(f"Error: {e}")
