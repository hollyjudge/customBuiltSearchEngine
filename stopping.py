import os
import xml.etree.ElementTree as ET

def count_records(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return len(root.findall(".//{http://www.openarchives.org/OAI/2.0/}record"))

directory = './'  # Replace with the path to your directory containing the XML files

xml_files = [file for file in os.listdir(directory) if file.endswith('.xml')]

sum = 0;
os.system("mkdir dataset")
for file in xml_files:
    file_path = os.path.join(directory, file)
    record_count = count_records(file_path)
    print(f"Total records in {file}: {record_count}")
    sum += record_count
    os.system("mv {} dataset".format(file_path))
    if sum > 100000:
        break
    


print(f"Total records: {sum}")