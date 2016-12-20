import os
from xml.etree.ElementTree import fromstring, Element, ElementTree
from .hulkEqParser import hmlEquation2latex
import json, codecs


with codecs.open(os.path.join(os.path.dirname(__file__),
                              "config.json"),
                 "r", "utf8") as f:
    config = json.load(f)

def parseHml(fileName: str) -> ElementTree:
    '''
    This is the sample code for parse .hml document and make ElementTree.
    
    Parameters
    ----------------------
    fileName : str
        fileName to be parsed.
    Returns
    ----------------------
    out : ElementTree
        An parsed ElementTree object.
    '''
    xmlText = open(fileName, 'r').read()
    
    hwpml = fromstring(xmlText)
    body = hwpml.find("BODY")
    section = body.find("SECTION")

    docRoot = Element(config["NodeNames"]["root"])

    paragraphs = section.findall("P")

    for paragraph in paragraphs:

        paragraphNode = Element(config["NodeNames"]["paragraph"])

        if paragraph.get("PageBreak") == "true":
            paragraphNode.attrib[config["NodeAttributes"]["newPage"]] = "true"
        else:
            paragraphNode.attrib[config["NodeAttributes"]["newPage"]] = "false"

        # I suupposed that there is one text tag or no text tag in one paragraph.
        # If there are more than one text, you must use `findall` method to find all text tags.
        
        text = paragraph.find("TEXT")
        if text is not None:
            for child in text.getchildren():
                if child.tag == "CHAR":
                    value = child.text

                    if value is not None:  # For EQUATION tag, there is a </CHAR> tag and it has no information.
                        leafNode = Element(config["NodeNames"]["char"])
                        leafNode.text = value
                        paragraphNode.append(leafNode)

                elif child.tag == "EQUATION":
                    script = child.find("SCRIPT")
                    value = script.text
                    
                    leafNode = Element(config["NodeNames"]["equation"])
                    leafNode.text = value
                    paragraphNode.append(leafNode)
                    
                else:
                    print("not supported tag: {}".format(child.tag))

            docRoot.append(paragraphNode)

    return ElementTree(docRoot)


def convertEquation(doc: ElementTree) -> str:
    '''
    Convert equation with sample ElementTree.
    '''
    for paragraph in doc.findall(config["NodeNames"]["paragraph"]):
        for child in paragraph.getchildren():
            if child.tag == config["NodeNames"]["equation"]:
                child.text = hmlEquation2latex(child.text)
    return doc


def extract2HtmlStr(doc: ElementTree) -> str:
    '''
    Convert sample ElementTree to html
    '''
    def convertSpace2nbsp(string: str) -> str:
        return string.replace(' ', r'&nbsp;')
    htmlStringList = []
    
    for paragraph in doc.findall(config["NodeNames"]["paragraph"]):
        paragraphStringList = []
        
        if paragraph.get(config["NodeAttributes"]["newPage"]) == "true":
            paragraphStringList.append("<br>======================<br>")

        for child in paragraph.getchildren():
            if child.tag == config["NodeNames"]["char"]:
                paragraphStringList.append(convertSpace2nbsp(child.text))
            elif child.tag == config["NodeNames"]["equation"]:
                paragraphStringList.append("$" + child.text + "$")
        paragraphString = ''.join(paragraphStringList)
        htmlStringList.append(paragraphString)
    return config["htmlHeader"] + '<br>\n'.join(htmlStringList) + config["htmlFooter"]


if __name__=='__main__':
    import sys
    script, hmlDoc, dst = sys.argv

    doc = parseHml(hmlDoc)
    doc = convertEquation(doc)
    doc.write(dst + '.xml')
    
    with codecs.open(dst + ".html", "w", "utf8") as f:
        f.write(extract2HtmlStr(doc))
