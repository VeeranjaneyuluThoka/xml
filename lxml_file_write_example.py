from lxml import etree as ET
import xml.dom.minidom

def writexml(filepath):
    parser = ET.XMLParser(resolve_entities=False, strip_cdata=False)
    tree = ET.parse(filepath, parser)
    root = tree.getroot()
    a=[]     
    for v in root.iter('publishers'):
        for a in v:
            if a.tag == "hudson.plugins.emailext.ExtendedEmailPublisher":
                t1=ET.SubElement(v,'org.jenkinsci.plugins.postbuildscript.PostBuildScript',{'plugin':"postbuildscript@0.17"})
                t2=ET.SubElement(t1,"buildSteps")
                t3=ET.SubElement(t2,'hudson.tasks.Shell')
                t4=ET.SubElement(t3,"command")
                t4.text = "bash -x /d0/jenkins/scripts/parent-pom-enforcer.sh"
                t5 = ET.SubElement(t1,'scriptOnlyIfSuccess')
                t5.text = "false"
                t6 = ET.SubElement(t1,'scriptOnlyIfFailure')
                t6.text = "false"
                t7= ET.SubElement(t1,'markBuildUnstable')
                t7.text = "true"
    xml1 = xml.dom.minidom.parseString(ET.tostring(root, pretty_print=True))
    pretty_xml_as_string = xml1.toprettyxml()
    f = open(filepath, "w")
    for v in str(pretty_xml_as_string).split("\n"):
        if v.strip():
            f.write(v+"\n")
    f.close()

def main():
    writexml('../../data/ibug_300W_large_face_landmark_dataset/dlib_exp.xml')
    
if __name__ == "__main__":
    main()