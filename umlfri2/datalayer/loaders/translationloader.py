from umlfri2.addon.translation import Translation
from ..constants import ADDON_NAMESPACE, ADDON_SCHEMA


class TranslationLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load translation: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        language = self.__xmlroot.attrib["lang"]
        translations = []
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                translations.append(('element', child.attrib["id"], child.attrib["label"]))
            elif child.tag == "{{{0}}}Connection".format(ADDON_NAMESPACE):
                translations.append(('connection', child.attrib["id"], child.attrib["label"]))
            elif child.tag == "{{{0}}}Diagram".format(ADDON_NAMESPACE):
                translations.append(('diagram', child.attrib["id"], child.attrib["label"]))
            elif child.tag == "{{{0}}}Attribute".format(ADDON_NAMESPACE):
                translations.append(('attribute', child.attrib["path"], child.attrib["label"]))
            elif child.tag == "{{{0}}}EnumItem".format(ADDON_NAMESPACE):
                translations.append(('enumitem', child.attrib["path"], child.attrib["label"]))
            else:
                raise Exception
        
        return Translation(language, translations)
    
    def __format_text(self, text):
        current_text = []
        current_line = []
        for line in text.splitlines():
            line = self.__SPACES.sub(' ', line.strip())
            if line:
                current_line.append(line)
            elif current_line:
                current_text.append(' '.join(current_line))
                current_line = []
        return '\n'.join(current_text)
