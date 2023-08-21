import xml.etree.ElementTree as ET
import os
import io


folder_path = "data"

def thing(file, filename):
    tree = ET.parse(file)
    root = tree.getroot()

    records=[]

    for record in root.iter('{http://www.openarchives.org/OAI/2.0/}metadata'):
        fields = {}
        for field in record.iter():
            tag = field.tag.split('}')[-1]
            if tag in ['title', 'creator', 'subject', 'description', 'date', 'identifier', 'language', 'relation']:
                if field.text is not None:
                    fields[tag] = field.text

        records.append(fields)

    root = ET.Element('add')
    for record in records:
        doc = ET.SubElement(root, 'doc')
        for field_name, field_value in record.items():
            if field_value:
                field = ET.SubElement(doc, 'field', name=field_name)
                field.text = field_value
    
    tree = ET.ElementTree(root)
    name='new/'+filename
    tree.write(name, xml_declaration=True, encoding='UTF-8')


for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        thing(file_path, filename)