#!/usr/bin/env python3
"""
Additional Comprehensive Tests for TinyXML2 to Reach 75% Coverage
Focuses on: error handling, file I/O, parsing, printing, and edge cases
"""

import os
import subprocess
from pathlib import Path
import json

class AdditionalTestGenerator:
    """Generate additional tests to improve coverage to 75%"""
    
    def __init__(self, project_root: Path, output_dir: Path):
        self.project_root = project_root
        self.output_dir = output_dir
        self.test_dir = output_dir / "tests"
        self.bin_dir = output_dir / "bin"
        self.test_metadata = []
        
    def generate_all_tests(self):
        """Generate all additional tests"""
        print("="*70)
        print("Additional TinyXML2 Test Generator - Target: 75% Coverage")
        print("="*70)
        print()
        
        # Generate XML file I/O tests
        self.generate_file_io_tests()
        
        # Generate XML parsing tests
        self.generate_parsing_tests()
        
        # Generate error handling tests
        self.generate_error_handling_tests()
        
        # Generate XMLVisitor tests
        self.generate_visitor_tests()
        
        # Generate complex XML structure tests
        self.generate_complex_structure_tests()
        
        # Generate StrPair tests
        self.generate_strpair_tests()
        
        # Save metadata
        self.save_metadata()
        
        print(f"\n✅ Generated {len(self.test_metadata)} additional tests")
        return self.test_metadata
    
    def generate_file_io_tests(self):
        """Generate comprehensive file I/O tests"""
        print("Generating File I/O tests...")
        
        tests = [
            ("LoadFile_XMLFile", self._test_loadfile_xmlfile),
            ("LoadFile_NonExistent", self._test_loadfile_nonexistent),
            ("SaveFile_ValidPath", self._test_savefile_validpath),
            ("ParseXML_String", self._test_parsexml_string),
            ("ParseXML_EmptyString", self._test_parsexml_emptystring),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_FileIO_{name}", "XMLDocument", name, content)
    
    def generate_parsing_tests(self):
        """Generate XML parsing tests"""
        print("Generating Parsing tests...")
        
        tests = [
            ("Parse_ValidXML", self._test_parse_validxml),
            ("Parse_NestedElements", self._test_parse_nested),
            ("Parse_WithAttributes", self._test_parse_attributes),
            ("Parse_WithText", self._test_parse_text),
            ("Parse_WithCDATA", self._test_parse_cdata),
            ("Parse_WithComments", self._test_parse_comments),
            ("Parse_WithDeclaration", self._test_parse_declaration),
            ("Parse_MalformedXML", self._test_parse_malformed),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Parse_{name}", "XMLDocument", name, content)
    
    def generate_error_handling_tests(self):
        """Generate error handling tests"""
        print("Generating Error Handling tests...")
        
        tests = [
            ("Error_NoError", self._test_error_noerror),
            ("Error_AfterBadParse", self._test_error_badparse),
            ("Error_ErrorID", self._test_error_errorid),
            ("Error_GetErrorStr1", self._test_error_geterrorstr1),
            ("Error_GetErrorStr2", self._test_error_geterrorstr2),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Error_{name}", "XMLDocument", name, content)
    
    def generate_visitor_tests(self):
        """Generate XMLVisitor tests"""
        print("Generating XMLVisitor tests...")
        
        content = self._test_visitor_traverse()
        self._write_test_file("tinyxml2_Visitor_Traverse", "XMLVisitor", "Traverse", content)
    
    def generate_complex_structure_tests(self):
        """Generate tests for complex XML structures"""
        print("Generating Complex Structure tests...")
        
        tests = [
            ("DeepNesting", self._test_complex_deepnesting),
            ("ManyChildren", self._test_complex_manychildren),
            ("MixedContent", self._test_complex_mixedcontent),
            ("LargeDocument", self._test_complex_largedoc),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Complex_{name}", "XMLDocument", name, content)
    
    def generate_strpair_tests(self):
        """Generate StrPair utility tests"""
        print("Generating StrPair tests...")
        
        tests = [
            ("XMLUtil_IsWhiteSpace", self._test_xmlutil_iswhitespace),
            ("XMLUtil_StringEqual", self._test_xmlutil_stringequal),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_{name}", "XMLUtil", name, content)
    
    # File I/O test generators
    def _test_loadfile_xmlfile(self) -> str:
        return '''// Test XMLDocument::LoadFile with actual XML file
#include <gtest/gtest.h>
#include "tinyxml2.h"
#include <fstream>

using namespace tinyxml2;

TEST(XMLDocument_LoadFile, ValidXMLFile) {
    // Create a test XML file
    std::ofstream file("/tmp/test_valid.xml");
    file << "<?xml version=\\"1.0\\"?>\\n";
    file << "<root>\\n";
    file << "  <child>Test</child>\\n";
    file << "</root>\\n";
    file.close();
    
    XMLDocument doc;
    XMLError err = doc.LoadFile("/tmp/test_valid.xml");
    EXPECT_EQ(err, XML_SUCCESS);
    
    XMLElement* root = doc.RootElement();
    ASSERT_NE(root, nullptr);
    EXPECT_STREQ(root->Name(), "root");
    
    // Cleanup
    std::remove("/tmp/test_valid.xml");
}

TEST(XMLDocument_LoadFile, ComplexXMLFile) {
    // Create a more complex XML file
    std::ofstream file("/tmp/test_complex.xml");
    file << "<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?>\\n";
    file << "<document>\\n";
    file << "  <section id=\\"1\\" name=\\"First\\">\\n";
    file << "    <item count=\\"5\\">Item 1</item>\\n";
    file << "    <item count=\\"10\\">Item 2</item>\\n";
    file << "  </section>\\n";
    file << "  <section id=\\"2\\" name=\\"Second\\"/>\\n";
    file << "</document>\\n";
    file.close();
    
    XMLDocument doc;
    XMLError err = doc.LoadFile("/tmp/test_complex.xml");
    EXPECT_EQ(err, XML_SUCCESS);
    
    XMLElement* root = doc.RootElement();
    ASSERT_NE(root, nullptr);
    
    XMLElement* section = root->FirstChildElement("section");
    ASSERT_NE(section, nullptr);
    EXPECT_EQ(section->IntAttribute("id"), 1);
    
    XMLElement* item = section->FirstChildElement("item");
    ASSERT_NE(item, nullptr);
    EXPECT_EQ(item->IntAttribute("count"), 5);
    
    // Cleanup
    std::remove("/tmp/test_complex.xml");
}
'''
    
    def _test_loadfile_nonexistent(self) -> str:
        return '''// Test XMLDocument::LoadFile with non-existent file
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLDocument_LoadFile, NonExistentFile) {
    XMLDocument doc;
    XMLError err = doc.LoadFile("/nonexistent/file/path.xml");
    EXPECT_NE(err, XML_SUCCESS);
}

TEST(XMLDocument_LoadFile, EmptyFilePath) {
    XMLDocument doc;
    XMLError err = doc.LoadFile("");
    EXPECT_NE(err, XML_SUCCESS);
}
'''
    
    def _test_savefile_validpath(self) -> str:
        return '''// Test XMLDocument::SaveFile
#include <gtest/gtest.h>
#include "tinyxml2.h"
#include <cstdio>

using namespace tinyxml2;

TEST(XMLDocument_SaveFile, BasicSave) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("root");
    doc.InsertEndChild(root);
    
    XMLElement* child = doc.NewElement("child");
    child->SetText("Hello World");
    root->InsertEndChild(child);
    
    XMLError err = doc.SaveFile("/tmp/test_save.xml");
    EXPECT_EQ(err, XML_SUCCESS);
    
    // Load it back to verify
    XMLDocument doc2;
    err = doc2.LoadFile("/tmp/test_save.xml");
    EXPECT_EQ(err, XML_SUCCESS);
    
    XMLElement* root2 = doc2.RootElement();
    ASSERT_NE(root2, nullptr);
    EXPECT_STREQ(root2->Name(), "root");
    
    // Cleanup
    std::remove("/tmp/test_save.xml");
}

TEST(XMLDocument_SaveFile, WithAttributes) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("config");
    root->SetAttribute("version", "1.0");
    root->SetAttribute("encoding", "UTF-8");
    doc.InsertEndChild(root);
    
    XMLError err = doc.SaveFile("/tmp/test_save_attr.xml");
    EXPECT_EQ(err, XML_SUCCESS);
    
    // Cleanup
    std::remove("/tmp/test_save_attr.xml");
}
'''
    
    def _test_parsexml_string(self) -> str:
        return '''// Test XMLDocument::Parse
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLDocument_Parse, SimpleXML) {
    const char* xml = "<root><child>Text</child></root>";
    XMLDocument doc;
    XMLError err = doc.Parse(xml);
    EXPECT_EQ(err, XML_SUCCESS);
    
    XMLElement* root = doc.RootElement();
    ASSERT_NE(root, nullptr);
    EXPECT_STREQ(root->Name(), "root");
}

TEST(XMLDocument_Parse, WithDeclaration) {
    const char* xml = "<?xml version=\\"1.0\\"?><root/>";
    XMLDocument doc;
    XMLError err = doc.Parse(xml);
    EXPECT_EQ(err, XML_SUCCESS);
}
'''
    
    def _test_parsexml_emptystring(self) -> str:
        return '''// Test XMLDocument::Parse with empty/invalid input
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLDocument_Parse, EmptyString) {
    XMLDocument doc;
    XMLError err = doc.Parse("");
    EXPECT_NE(err, XML_SUCCESS);
}

TEST(XMLDocument_Parse, NullPointer) {
    XMLDocument doc;
    XMLError err = doc.Parse(nullptr);
    EXPECT_NE(err, XML_SUCCESS);
}
'''
    
    # Parsing test generators
    def _test_parse_validxml(self) -> str:
        return '''// Test parsing valid XML
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_ValidXML, SimpleElement) {
    const char* xml = "<element/>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
}

TEST(XMLParse_ValidXML, ElementWithText) {
    const char* xml = "<element>Text content</element>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    EXPECT_STREQ(doc.RootElement()->GetText(), "Text content");
}
'''
    
    def _test_parse_nested(self) -> str:
        return '''// Test parsing nested elements
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_Nested, TwoLevels) {
    const char* xml = "<root><child/></root>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    
    XMLElement* root = doc.RootElement();
    ASSERT_NE(root, nullptr);
    XMLElement* child = root->FirstChildElement();
    EXPECT_NE(child, nullptr);
}

TEST(XMLParse_Nested, DeepNesting) {
    const char* xml = "<a><b><c><d><e>Deep</e></d></c></b></a>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    
    XMLElement* e = doc.RootElement()
        ->FirstChildElement("b")
        ->FirstChildElement("c")
        ->FirstChildElement("d")
        ->FirstChildElement("e");
    ASSERT_NE(e, nullptr);
    EXPECT_STREQ(e->GetText(), "Deep");
}
'''
    
    def _test_parse_attributes(self) -> str:
        return '''// Test parsing attributes
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_Attributes, SingleAttribute) {
    const char* xml = "<elem attr=\\"value\\"/>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    EXPECT_STREQ(doc.RootElement()->Attribute("attr"), "value");
}

TEST(XMLParse_Attributes, MultipleAttributes) {
    const char* xml = "<elem a=\\"1\\" b=\\"2\\" c=\\"3\\"/>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    XMLElement* elem = doc.RootElement();
    EXPECT_STREQ(elem->Attribute("a"), "1");
    EXPECT_STREQ(elem->Attribute("b"), "2");
    EXPECT_STREQ(elem->Attribute("c"), "3");
}

TEST(XMLParse_Attributes, IntegerAttribute) {
    const char* xml = "<elem count=\\"42\\"/>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    EXPECT_EQ(doc.RootElement()->IntAttribute("count"), 42);
}
'''
    
    def _test_parse_text(self) -> str:
        return '''// Test parsing text content
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_Text, SimpleText) {
    const char* xml = "<elem>Hello World</elem>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    EXPECT_STREQ(doc.RootElement()->GetText(), "Hello World");
}

TEST(XMLParse_Text, TextWithWhitespace) {
    const char* xml = "<elem>  Text with spaces  </elem>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    EXPECT_NE(doc.RootElement()->GetText(), nullptr);
}

TEST(XMLParse_Text, IntegerText) {
    const char* xml = "<elem>123</elem>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
    int value = 0;
    EXPECT_EQ(doc.RootElement()->QueryIntText(&value), XML_SUCCESS);
    EXPECT_EQ(value, 123);
}
'''
    
    def _test_parse_cdata(self) -> str:
        return '''// Test parsing CDATA sections
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_CDATA, BasicCDATA) {
    const char* xml = "<elem><![CDATA[Some data]]></elem>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
}

TEST(XMLParse_CDATA, CDATAWithSpecialChars) {
    const char* xml = "<elem><![CDATA[<>&\\"]]></elem>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
}
'''
    
    def _test_parse_comments(self) -> str:
        return '''// Test parsing comments
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_Comments, SimpleComment) {
    const char* xml = "<root><!-- Comment --></root>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
}

TEST(XMLParse_Comments, MultipleComments) {
    const char* xml = "<!-- Start --><root><!-- Middle --></root><!-- End -->";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
}
'''
    
    def _test_parse_declaration(self) -> str:
        return '''// Test parsing XML declaration
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_Declaration, SimpleDeclaration) {
    const char* xml = "<?xml version=\\"1.0\\"?><root/>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
}

TEST(XMLParse_Declaration, WithEncoding) {
    const char* xml = "<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?><root/>";
    XMLDocument doc;
    EXPECT_EQ(doc.Parse(xml), XML_SUCCESS);
}
'''
    
    def _test_parse_malformed(self) -> str:
        return '''// Test parsing malformed XML
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLParse_Malformed, UnclosedTag) {
    const char* xml = "<root>";
    XMLDocument doc;
    EXPECT_NE(doc.Parse(xml), XML_SUCCESS);
}

TEST(XMLParse_Malformed, MismatchedTags) {
    const char* xml = "<root></wrong>";
    XMLDocument doc;
    EXPECT_NE(doc.Parse(xml), XML_SUCCESS);
}

TEST(XMLParse_Malformed, InvalidCharacters) {
    const char* xml = "<root<>>";
    XMLDocument doc;
    EXPECT_NE(doc.Parse(xml), XML_SUCCESS);
}
'''
    
    # Error handling test generators
    def _test_error_noerror(self) -> str:
        return '''// Test error state when no error
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLError_NoError, InitialState) {
    XMLDocument doc;
    EXPECT_FALSE(doc.Error());
    EXPECT_EQ(doc.ErrorID(), XML_SUCCESS);
}

TEST(XMLError_NoError, AfterValidParse) {
    XMLDocument doc;
    doc.Parse("<root/>");
    EXPECT_FALSE(doc.Error());
}
'''
    
    def _test_error_badparse(self) -> str:
        return '''// Test error state after bad parse
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLError_BadParse, ErrorStateSet) {
    XMLDocument doc;
    doc.Parse("<root>");  // Unclosed tag
    EXPECT_TRUE(doc.Error());
    EXPECT_NE(doc.ErrorID(), XML_SUCCESS);
}

TEST(XMLError_BadParse, ErrorLineNum) {
    XMLDocument doc;
    doc.Parse("<root>");
    EXPECT_GT(doc.ErrorLineNum(), 0);
}
'''
    
    def _test_error_errorid(self) -> str:
        return '''// Test ErrorID method
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLError_ErrorID, ValidID) {
    XMLDocument doc;
    doc.Parse("<root>");
    XMLError err = doc.ErrorID();
    EXPECT_NE(err, XML_SUCCESS);
}
'''
    
    def _test_error_geterrorstr1(self) -> str:
        return '''// Test GetErrorStr1 method
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLError_GetErrorStr1, AfterError) {
    XMLDocument doc;
    doc.Parse("<root>");
    const char* errStr = doc.ErrorStr();
    EXPECT_NE(errStr, nullptr);
}
'''
    
    def _test_error_geterrorstr2(self) -> str:
        return '''// Test error string methods
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLError_ErrorStr, ErrorName) {
    XMLDocument doc;
    doc.Parse("<root>");
    const char* name = doc.ErrorName();
    EXPECT_NE(name, nullptr);
}
'''
    
    # Visitor test generator
    def _test_visitor_traverse(self) -> str:
        return '''// Test XMLVisitor traversal
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

class CountingVisitor : public XMLVisitor {
public:
    int elementCount = 0;
    int textCount = 0;
    
    bool VisitEnter(const XMLElement&, const XMLAttribute*) override {
        elementCount++;
        return true;
    }
    
    bool Visit(const XMLText&) override {
        textCount++;
        return true;
    }
};

TEST(XMLVisitor_Traverse, CountElements) {
    const char* xml = "<root><a/><b/><c/></root>";
    XMLDocument doc;
    doc.Parse(xml);
    
    CountingVisitor visitor;
    doc.Accept(&visitor);
    EXPECT_GT(visitor.elementCount, 0);
}

TEST(XMLVisitor_Traverse, CountText) {
    const char* xml = "<root>Text1<child>Text2</child>Text3</root>";
    XMLDocument doc;
    doc.Parse(xml);
    
    CountingVisitor visitor;
    doc.Accept(&visitor);
    EXPECT_GT(visitor.textCount, 0);
}
'''
    
    # Complex structure test generators
    def _test_complex_deepnesting(self) -> str:
        return '''// Test deeply nested structures
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLComplex_DeepNesting, Create10Levels) {
    XMLDocument doc;
    XMLElement* current = doc.NewElement("level0");
    doc.InsertEndChild(current);
    
    for (int i = 1; i < 10; i++) {
        XMLElement* child = doc.NewElement(("level" + std::to_string(i)).c_str());
        current->InsertEndChild(child);
        current = child;
    }
    
    // Verify we can traverse all levels
    XMLElement* elem = doc.RootElement();
    int count = 0;
    while (elem) {
        count++;
        elem = elem->FirstChildElement();
    }
    EXPECT_EQ(count, 10);
}
'''
    
    def _test_complex_manychildren(self) -> str:
        return '''// Test many children
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLComplex_ManyChildren, Create100Children) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("root");
    doc.InsertEndChild(root);
    
    for (int i = 0; i < 100; i++) {
        XMLElement* child = doc.NewElement("child");
        child->SetAttribute("id", i);
        root->InsertEndChild(child);
    }
    
    // Count children
    int count = 0;
    for (XMLElement* child = root->FirstChildElement(); child; child = child->NextSiblingElement()) {
        count++;
    }
    EXPECT_EQ(count, 100);
}
'''
    
    def _test_complex_mixedcontent(self) -> str:
        return '''// Test mixed content
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLComplex_MixedContent, TextAndElements) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("root");
    doc.InsertEndChild(root);
    
    root->InsertEndChild(doc.NewText("Text1"));
    root->InsertEndChild(doc.NewElement("elem1"));
    root->InsertEndChild(doc.NewText("Text2"));
    root->InsertEndChild(doc.NewElement("elem2"));
    root->InsertEndChild(doc.NewText("Text3"));
    
    // Verify we can traverse
    int nodeCount = 0;
    for (XMLNode* child = root->FirstChild(); child; child = child->NextSibling()) {
        nodeCount++;
    }
    EXPECT_EQ(nodeCount, 5);
}
'''
    
    def _test_complex_largedoc(self) -> str:
        return '''// Test large document
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLComplex_LargeDoc, Create1000Elements) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("root");
    doc.InsertEndChild(root);
    
    for (int i = 0; i < 1000; i++) {
        XMLElement* section = doc.NewElement("section");
        section->SetAttribute("id", i);
        root->InsertEndChild(section);
        
        for (int j = 0; j < 5; j++) {
            XMLElement* item = doc.NewElement("item");
            item->SetText(j);
            section->InsertEndChild(item);
        }
    }
    
    // Verify we can count all elements
    int count = 0;
    for (XMLElement* section = root->FirstChildElement(); section; section = section->NextSiblingElement()) {
        count++;
    }
    EXPECT_EQ(count, 1000);
}
'''
    
    # XMLUtil test generators
    def _test_xmlutil_iswhitespace(self) -> str:
        return '''// Test XMLUtil::IsWhiteSpace
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLUtil_IsWhiteSpace, Space) {
    EXPECT_TRUE(XMLUtil::IsWhiteSpace(' '));
}

TEST(XMLUtil_IsWhiteSpace, Tab) {
    EXPECT_TRUE(XMLUtil::IsWhiteSpace('\\t'));
}

TEST(XMLUtil_IsWhiteSpace, Newline) {
    EXPECT_TRUE(XMLUtil::IsWhiteSpace('\\n'));
}

TEST(XMLUtil_IsWhiteSpace, Letter) {
    EXPECT_FALSE(XMLUtil::IsWhiteSpace('a'));
}
'''
    
    def _test_xmlutil_stringequal(self) -> str:
        return '''// Test XMLUtil::StringEqual
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLUtil_StringEqual, EqualStrings) {
    EXPECT_TRUE(XMLUtil::StringEqual("test", "test"));
}

TEST(XMLUtil_StringEqual, DifferentStrings) {
    EXPECT_FALSE(XMLUtil::StringEqual("test", "other"));
}

TEST(XMLUtil_StringEqual, EmptyStrings) {
    EXPECT_TRUE(XMLUtil::StringEqual("", ""));
}
'''
    
    def _write_test_file(self, test_name: str, class_name: str, method_name: str, content: str):
        """Write and compile test file"""
        test_file = self.test_dir / f"{test_name}.cpp"
        with open(test_file, 'w') as f:
            f.write(content)
        
        bin_file = self.bin_dir / test_name
        compile_cmd = [
            "g++",
            "-std=c++14",
            "-o", str(bin_file),
            str(test_file),
            str(self.project_root / "tinyxml2.cpp"),
            "-I", str(self.project_root),
            "-I", "/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include",
            "-L", "/workspaces/CppMicroAgent/googletest-1.16.0/build/lib",
            "-lgtest",
            "-lgtest_main",
            "-lpthread",
            "--coverage",
            "-fprofile-arcs",
            "-ftest-coverage"
        ]
        
        try:
            result = subprocess.run(compile_cmd, capture_output=True, timeout=30)
            if result.returncode == 0:
                print(f"  ✅ {test_name}")
                self.test_metadata.append({
                    "test_name": test_name,
                    "class_name": class_name,
                    "method_name": method_name,
                    "test_file": str(test_file),
                    "binary": str(bin_file),
                    "compiled": True
                })
            else:
                print(f"  ❌ {test_name} - Compilation failed")
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                if len(error_msg) > 200:
                    error_msg = error_msg[:200] + "..."
                print(f"     Error: {error_msg}")
        except Exception as e:
            print(f"  ❌ {test_name} - Exception: {e}")
    
    def save_metadata(self):
        """Save metadata"""
        metadata_file = self.output_dir / "additional_test_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.test_metadata, f, indent=2)
        print(f"\n✅ Metadata saved to {metadata_file}")


def main():
    """Main entry point"""
    project_root = Path("/workspaces/CppMicroAgent/TestProjects/tinyxml2")
    output_dir = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    
    generator = AdditionalTestGenerator(project_root, output_dir)
    metadata = generator.generate_all_tests()
    
    print("\n" + "="*70)
    print(f"✅ Generated {len(metadata)} additional tests")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    exit(main())
