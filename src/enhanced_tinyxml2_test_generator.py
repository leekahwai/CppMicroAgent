#!/usr/bin/env python3
"""
Enhanced Test Generator for TinyXML2
This script generates sophisticated tests specifically for TinyXML2 classes to achieve higher coverage.
It understands the XML DOM structure and generates appropriate tests for each class type.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Set, Tuple

class TinyXML2TestGenerator:
    """Generate comprehensive tests for TinyXML2 library"""
    
    def __init__(self, project_root: Path, output_dir: Path):
        self.project_root = project_root
        self.output_dir = output_dir
        self.test_dir = output_dir / "tests"
        self.bin_dir = output_dir / "bin"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        self.test_metadata = []
        
    def generate_all_tests(self):
        """Generate all comprehensive tests for TinyXML2"""
        print("="*70)
        print("Enhanced TinyXML2 Test Generator")
        print("="*70)
        print()
        
        # Generate tests for each major class
        self.generate_xmlelement_tests()
        self.generate_xmlnode_tests()
        self.generate_xmlattribute_tests()
        self.generate_xmltext_tests()
        self.generate_xmlcomment_tests()
        self.generate_xmldeclaration_tests()
        self.generate_xmlunknown_tests()
        self.generate_xmlhandle_tests()
        self.generate_xmlprinter_tests()
        
        # Save metadata
        self.save_metadata()
        
        print(f"\n✅ Generated {len(self.test_metadata)} enhanced tests")
        return self.test_metadata
    
    def generate_xmlelement_tests(self):
        """Generate comprehensive tests for XMLElement class"""
        print("Generating XMLElement tests...")
        
        test_cases = [
            ("SetName", self._test_xmlelement_setname),
            ("Name", self._test_xmlelement_name),
            ("SetAttribute", self._test_xmlelement_setattribute),
            ("Attribute", self._test_xmlelement_attribute),
            ("QueryIntAttribute", self._test_xmlelement_queryintattribute),
            ("QueryFloatAttribute", self._test_xmlelement_queryfloatattribute),
            ("QueryBoolAttribute", self._test_xmlelement_queryboolattribute),
            ("FirstChildElement", self._test_xmlelement_firstchildelement),
            ("NextSiblingElement", self._test_xmlelement_nextsiblingelement),
            ("InsertEndChild", self._test_xmlelement_insertendchild),
            ("DeleteChild", self._test_xmlelement_deletechild),
            ("FirstAttribute", self._test_xmlelement_firstattribute),
            ("GetText", self._test_xmlelement_gettext),
            ("SetText", self._test_xmlelement_settext),
            ("QueryIntText", self._test_xmlelement_queryinttext),
            ("QueryFloatText", self._test_xmlelement_queryfloattext),
        ]
        
        for method_name, generator_func in test_cases:
            test_content = generator_func()
            self._write_test_file(f"tinyxml2_XMLElement_{method_name}", "XMLElement", method_name, test_content)
    
    def generate_xmlnode_tests(self):
        """Generate comprehensive tests for XMLNode class"""
        print("Generating XMLNode tests...")
        
        test_cases = [
            ("Parent", self._test_xmlnode_parent),
            ("NextSibling", self._test_xmlnode_nextsibling),
            ("PreviousSibling", self._test_xmlnode_previoussibling),
            ("FirstChild", self._test_xmlnode_firstchild),
            ("LastChild", self._test_xmlnode_lastchild),
            ("Value", self._test_xmlnode_value),
            ("SetValue", self._test_xmlnode_setvalue),
            ("NoChildren", self._test_xmlnode_nochildren),
        ]
        
        for method_name, generator_func in test_cases:
            test_content = generator_func()
            self._write_test_file(f"tinyxml2_XMLNode_{method_name}", "XMLNode", method_name, test_content)
    
    def generate_xmlattribute_tests(self):
        """Generate comprehensive tests for XMLAttribute class"""
        print("Generating XMLAttribute tests...")
        
        test_cases = [
            ("Name", self._test_xmlattribute_name),
            ("Value", self._test_xmlattribute_value),
            ("QueryIntValue", self._test_xmlattribute_queryintvalue),
            ("QueryFloatValue", self._test_xmlattribute_queryfloatvalue),
            ("QueryBoolValue", self._test_xmlattribute_queryboolvalue),
            ("SetAttribute", self._test_xmlattribute_setattribute),
            ("Next", self._test_xmlattribute_next),
        ]
        
        for method_name, generator_func in test_cases:
            test_content = generator_func()
            self._write_test_file(f"tinyxml2_XMLAttribute_{method_name}", "XMLAttribute", method_name, test_content)
    
    def generate_xmltext_tests(self):
        """Generate comprehensive tests for XMLText class"""
        print("Generating XMLText tests...")
        
        test_cases = [
            ("SetCData", self._test_xmltext_setcdata),
            ("CData", self._test_xmltext_cdata),
        ]
        
        for method_name, generator_func in test_cases:
            test_content = generator_func()
            self._write_test_file(f"tinyxml2_XMLText_{method_name}", "XMLText", method_name, test_content)
    
    def generate_xmlcomment_tests(self):
        """Generate tests for XMLComment class"""
        print("Generating XMLComment tests...")
        test_content = self._test_xmlcomment_value()
        self._write_test_file("tinyxml2_XMLComment_Value", "XMLComment", "Value", test_content)
    
    def generate_xmldeclaration_tests(self):
        """Generate tests for XMLDeclaration class"""
        print("Generating XMLDeclaration tests...")
        test_content = self._test_xmldeclaration_value()
        self._write_test_file("tinyxml2_XMLDeclaration_Value", "XMLDeclaration", "Value", test_content)
    
    def generate_xmlunknown_tests(self):
        """Generate tests for XMLUnknown class"""
        print("Generating XMLUnknown tests...")
        test_content = self._test_xmlunknown_value()
        self._write_test_file("tinyxml2_XMLUnknown_Value", "XMLUnknown", "Value", test_content)
    
    def generate_xmlhandle_tests(self):
        """Generate tests for XMLHandle class"""
        print("Generating XMLHandle tests...")
        
        test_cases = [
            ("FirstChild", self._test_xmlhandle_firstchild),
            ("FirstChildElement", self._test_xmlhandle_firstchildelement),
            ("NextSibling", self._test_xmlhandle_nextsibling),
            ("ToElement", self._test_xmlhandle_toelement),
            ("ToNode", self._test_xmlhandle_tonode),
        ]
        
        for method_name, generator_func in test_cases:
            test_content = generator_func()
            self._write_test_file(f"tinyxml2_XMLHandle_{method_name}", "XMLHandle", method_name, test_content)
    
    def generate_xmlprinter_tests(self):
        """Generate tests for XMLPrinter class"""
        print("Generating XMLPrinter tests...")
        
        test_cases = [
            ("PushText", self._test_xmlprinter_pushtext),
            ("OpenElement", self._test_xmlprinter_openelement),
            ("CloseElement", self._test_xmlprinter_closeelement),
            ("PushAttribute", self._test_xmlprinter_pushattribute),
            ("CStr", self._test_xmlprinter_cstr),
        ]
        
        for method_name, generator_func in test_cases:
            test_content = generator_func()
            self._write_test_file(f"tinyxml2_XMLPrinter_{method_name}", "XMLPrinter", method_name, test_content)
    
    # XMLElement test generators
    def _test_xmlelement_setname(self) -> str:
        return '''// Enhanced test for XMLElement::SetName
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_SetName, BasicSetName) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("OldName");
    ASSERT_NE(elem, nullptr);
    
    elem->SetName("NewName");
    EXPECT_STREQ(elem->Name(), "NewName");
}

TEST(XMLElement_SetName, EmptyString) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Name");
    elem->SetName("");
    EXPECT_STREQ(elem->Name(), "");
}

TEST(XMLElement_SetName, SpecialCharacters) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Name");
    elem->SetName("name-with_special123");
    EXPECT_STREQ(elem->Name(), "name-with_special123");
}

TEST(XMLElement_SetName, MultipleChanges) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Name1");
    elem->SetName("Name2");
    elem->SetName("Name3");
    EXPECT_STREQ(elem->Name(), "Name3");
}
'''
    
    def _test_xmlelement_name(self) -> str:
        return '''// Enhanced test for XMLElement::Name
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_Name, GetNameAfterCreation) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("TestElement");
    ASSERT_NE(elem, nullptr);
    EXPECT_STREQ(elem->Name(), "TestElement");
}

TEST(XMLElement_Name, NamePersistsAfterDocumentOperations) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("Root");
    XMLElement* child = doc.NewElement("Child");
    root->InsertEndChild(child);
    doc.InsertEndChild(root);
    
    EXPECT_STREQ(root->Name(), "Root");
    EXPECT_STREQ(child->Name(), "Child");
}

TEST(XMLElement_Name, NameNotNull) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    EXPECT_NE(elem->Name(), nullptr);
}
'''
    
    def _test_xmlelement_setattribute(self) -> str:
        return '''// Enhanced test for XMLElement::SetAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_SetAttribute, StringAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("attr", "value");
    EXPECT_STREQ(elem->Attribute("attr"), "value");
}

TEST(XMLElement_SetAttribute, IntAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("count", 42);
    int value = 0;
    elem->QueryIntAttribute("count", &value);
    EXPECT_EQ(value, 42);
}

TEST(XMLElement_SetAttribute, FloatAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("ratio", 3.14f);
    float value = 0.0f;
    elem->QueryFloatAttribute("ratio", &value);
    EXPECT_FLOAT_EQ(value, 3.14f);
}

TEST(XMLElement_SetAttribute, BoolAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("flag", true);
    bool value = false;
    elem->QueryBoolAttribute("flag", &value);
    EXPECT_TRUE(value);
}

TEST(XMLElement_SetAttribute, OverwriteExisting) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("attr", "old");
    elem->SetAttribute("attr", "new");
    EXPECT_STREQ(elem->Attribute("attr"), "new");
}

TEST(XMLElement_SetAttribute, MultipleAttributes) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("attr1", "value1");
    elem->SetAttribute("attr2", "value2");
    elem->SetAttribute("attr3", "value3");
    EXPECT_STREQ(elem->Attribute("attr1"), "value1");
    EXPECT_STREQ(elem->Attribute("attr2"), "value2");
    EXPECT_STREQ(elem->Attribute("attr3"), "value3");
}
'''
    
    def _test_xmlelement_attribute(self) -> str:
        return '''// Enhanced test for XMLElement::Attribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_Attribute, GetExistingAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("key", "value");
    EXPECT_STREQ(elem->Attribute("key"), "value");
}

TEST(XMLElement_Attribute, GetNonExistingAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    EXPECT_EQ(elem->Attribute("nonexistent"), nullptr);
}

TEST(XMLElement_Attribute, CaseSensitive) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("Key", "value");
    EXPECT_EQ(elem->Attribute("key"), nullptr);
    EXPECT_STREQ(elem->Attribute("Key"), "value");
}
'''
    
    def _test_xmlelement_queryintattribute(self) -> str:
        return '''// Enhanced test for XMLElement::QueryIntAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryIntAttribute, ValidInt) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("count", 123);
    int value = 0;
    XMLError err = elem->QueryIntAttribute("count", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_EQ(value, 123);
}

TEST(XMLElement_QueryIntAttribute, NegativeInt) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("count", -456);
    int value = 0;
    XMLError err = elem->QueryIntAttribute("count", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_EQ(value, -456);
}

TEST(XMLElement_QueryIntAttribute, NonExistentAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    int value = 99;
    XMLError err = elem->QueryIntAttribute("missing", &value);
    EXPECT_NE(err, XML_SUCCESS);
}

TEST(XMLElement_QueryIntAttribute, ZeroValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("zero", 0);
    int value = 99;
    XMLError err = elem->QueryIntAttribute("zero", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_EQ(value, 0);
}
'''
    
    def _test_xmlelement_queryfloatattribute(self) -> str:
        return '''// Enhanced test for XMLElement::QueryFloatAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryFloatAttribute, ValidFloat) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("ratio", 3.14159f);
    float value = 0.0f;
    XMLError err = elem->QueryFloatAttribute("ratio", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_FLOAT_EQ(value, 3.14159f);
}

TEST(XMLElement_QueryFloatAttribute, NegativeFloat) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("ratio", -2.5f);
    float value = 0.0f;
    XMLError err = elem->QueryFloatAttribute("ratio", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_FLOAT_EQ(value, -2.5f);
}

TEST(XMLElement_QueryFloatAttribute, ZeroValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("zero", 0.0f);
    float value = 99.0f;
    XMLError err = elem->QueryFloatAttribute("zero", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_FLOAT_EQ(value, 0.0f);
}
'''
    
    def _test_xmlelement_queryboolattribute(self) -> str:
        return '''// Enhanced test for XMLElement::QueryBoolAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryBoolAttribute, TrueValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("flag", true);
    bool value = false;
    XMLError err = elem->QueryBoolAttribute("flag", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_TRUE(value);
}

TEST(XMLElement_QueryBoolAttribute, FalseValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("flag", false);
    bool value = true;
    XMLError err = elem->QueryBoolAttribute("flag", &value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_FALSE(value);
}
'''
    
    def _test_xmlelement_firstchildelement(self) -> str:
        return '''// Enhanced test for XMLElement::FirstChildElement
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_FirstChildElement, WithChildren) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    
    XMLElement* result = parent->FirstChildElement();
    ASSERT_NE(result, nullptr);
    EXPECT_STREQ(result->Name(), "Child");
}

TEST(XMLElement_FirstChildElement, NoChildren) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* result = parent->FirstChildElement();
    EXPECT_EQ(result, nullptr);
}

TEST(XMLElement_FirstChildElement, WithName) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child1 = doc.NewElement("FirstChild");
    XMLElement* child2 = doc.NewElement("SecondChild");
    parent->InsertEndChild(child1);
    parent->InsertEndChild(child2);
    
    XMLElement* result = parent->FirstChildElement("SecondChild");
    ASSERT_NE(result, nullptr);
    EXPECT_STREQ(result->Name(), "SecondChild");
}

TEST(XMLElement_FirstChildElement, TextAndElement) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLText* text = doc.NewText("Some text");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(text);
    parent->InsertEndChild(child);
    
    XMLElement* result = parent->FirstChildElement();
    ASSERT_NE(result, nullptr);
    EXPECT_STREQ(result->Name(), "Child");
}
'''
    
    def _test_xmlelement_nextsiblingelement(self) -> str:
        return '''// Enhanced test for XMLElement::NextSiblingElement
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_NextSiblingElement, WithSiblings) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child1 = doc.NewElement("Child1");
    XMLElement* child2 = doc.NewElement("Child2");
    parent->InsertEndChild(child1);
    parent->InsertEndChild(child2);
    
    XMLElement* result = child1->NextSiblingElement();
    ASSERT_NE(result, nullptr);
    EXPECT_STREQ(result->Name(), "Child2");
}

TEST(XMLElement_NextSiblingElement, NoSiblings) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    
    XMLElement* result = child->NextSiblingElement();
    EXPECT_EQ(result, nullptr);
}
'''
    
    def _test_xmlelement_insertendchild(self) -> str:
        return '''// Enhanced test for XMLElement::InsertEndChild
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_InsertEndChild, InsertElement) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    XMLNode* result = parent->InsertEndChild(child);
    
    ASSERT_NE(result, nullptr);
    EXPECT_EQ(parent->FirstChildElement(), child);
}

TEST(XMLElement_InsertEndChild, InsertMultiple) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child1 = doc.NewElement("Child1");
    XMLElement* child2 = doc.NewElement("Child2");
    
    parent->InsertEndChild(child1);
    parent->InsertEndChild(child2);
    
    EXPECT_EQ(parent->FirstChildElement(), child1);
    EXPECT_EQ(child1->NextSiblingElement(), child2);
}
'''
    
    def _test_xmlelement_deletechild(self) -> str:
        return '''// Enhanced test for XMLElement::DeleteChild
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_DeleteChild, DeleteSingleChild) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    
    parent->DeleteChild(child);
    EXPECT_EQ(parent->FirstChildElement(), nullptr);
}

TEST(XMLElement_DeleteChild, DeleteFromMultiple) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child1 = doc.NewElement("Child1");
    XMLElement* child2 = doc.NewElement("Child2");
    XMLElement* child3 = doc.NewElement("Child3");
    parent->InsertEndChild(child1);
    parent->InsertEndChild(child2);
    parent->InsertEndChild(child3);
    
    parent->DeleteChild(child2);
    EXPECT_EQ(parent->FirstChildElement(), child1);
    EXPECT_EQ(child1->NextSiblingElement(), child3);
}
'''
    
    def _test_xmlelement_firstattribute(self) -> str:
        return '''// Enhanced test for XMLElement::FirstAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_FirstAttribute, WithAttributes) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("attr", "value");
    
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_STREQ(attr->Name(), "attr");
}

TEST(XMLElement_FirstAttribute, NoAttributes) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    
    const XMLAttribute* attr = elem->FirstAttribute();
    EXPECT_EQ(attr, nullptr);
}

TEST(XMLElement_FirstAttribute, MultipleAttributes) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("first", "1");
    elem->SetAttribute("second", "2");
    
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_STREQ(attr->Name(), "first");
}
'''
    
    def _test_xmlelement_gettext(self) -> str:
        return '''// Enhanced test for XMLElement::GetText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_GetText, WithText) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    XMLText* text = doc.NewText("Hello World");
    elem->InsertEndChild(text);
    
    const char* result = elem->GetText();
    ASSERT_NE(result, nullptr);
    EXPECT_STREQ(result, "Hello World");
}

TEST(XMLElement_GetText, NoText) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    
    const char* result = elem->GetText();
    EXPECT_EQ(result, nullptr);
}

TEST(XMLElement_GetText, EmptyText) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    XMLText* text = doc.NewText("");
    elem->InsertEndChild(text);
    
    const char* result = elem->GetText();
    // Empty text node should still return a valid pointer
    EXPECT_NE(result, nullptr);
}
'''
    
    def _test_xmlelement_settext(self) -> str:
        return '''// Enhanced test for XMLElement::SetText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_SetText, StringValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetText("Test Text");
    
    EXPECT_STREQ(elem->GetText(), "Test Text");
}

TEST(XMLElement_SetText, IntValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetText(42);
    
    int value = 0;
    elem->QueryIntText(&value);
    EXPECT_EQ(value, 42);
}

TEST(XMLElement_SetText, FloatValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetText(3.14f);
    
    float value = 0.0f;
    elem->QueryFloatText(&value);
    EXPECT_FLOAT_EQ(value, 3.14f);
}

TEST(XMLElement_SetText, OverwriteExisting) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetText("Old Text");
    elem->SetText("New Text");
    
    EXPECT_STREQ(elem->GetText(), "New Text");
}
'''
    
    def _test_xmlelement_queryinttext(self) -> str:
        return '''// Enhanced test for XMLElement::QueryIntText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryIntText, ValidInt) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetText(123);
    
    int value = 0;
    XMLError err = elem->QueryIntText(&value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_EQ(value, 123);
}

TEST(XMLElement_QueryIntText, NoText) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    
    int value = 99;
    XMLError err = elem->QueryIntText(&value);
    EXPECT_NE(err, XML_SUCCESS);
}
'''
    
    def _test_xmlelement_queryfloattext(self) -> str:
        return '''// Enhanced test for XMLElement::QueryFloatText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryFloatText, ValidFloat) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetText(3.14f);
    
    float value = 0.0f;
    XMLError err = elem->QueryFloatText(&value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_FLOAT_EQ(value, 3.14f);
}

TEST(XMLElement_QueryFloatText, NoText) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    
    float value = 99.0f;
    XMLError err = elem->QueryFloatText(&value);
    EXPECT_NE(err, XML_SUCCESS);
}
'''
    
    # XMLNode test generators
    def _test_xmlnode_parent(self) -> str:
        return '''// Enhanced test for XMLNode::Parent
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_Parent, ElementWithParent) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    
    EXPECT_EQ(child->Parent(), parent);
}

TEST(XMLNode_Parent, NoParent) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    EXPECT_EQ(elem->Parent(), nullptr);
}
'''
    
    def _test_xmlnode_nextsibling(self) -> str:
        return '''// Enhanced test for XMLNode::NextSibling
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_NextSibling, WithSiblings) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child1 = doc.NewElement("Child1");
    XMLElement* child2 = doc.NewElement("Child2");
    parent->InsertEndChild(child1);
    parent->InsertEndChild(child2);
    
    EXPECT_EQ(child1->NextSibling(), child2);
}

TEST(XMLNode_NextSibling, NoSiblings) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    
    EXPECT_EQ(child->NextSibling(), nullptr);
}
'''
    
    def _test_xmlnode_previoussibling(self) -> str:
        return '''// Enhanced test for XMLNode::PreviousSibling
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_PreviousSibling, WithSiblings) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child1 = doc.NewElement("Child1");
    XMLElement* child2 = doc.NewElement("Child2");
    parent->InsertEndChild(child1);
    parent->InsertEndChild(child2);
    
    EXPECT_EQ(child2->PreviousSibling(), child1);
}

TEST(XMLNode_PreviousSibling, FirstChild) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    
    EXPECT_EQ(child->PreviousSibling(), nullptr);
}
'''
    
    def _test_xmlnode_firstchild(self) -> str:
        return '''// Enhanced test for XMLNode::FirstChild
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_FirstChild, WithChildren) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    
    EXPECT_EQ(parent->FirstChild(), child);
}

TEST(XMLNode_FirstChild, NoChildren) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    EXPECT_EQ(parent->FirstChild(), nullptr);
}
'''
    
    def _test_xmlnode_lastchild(self) -> str:
        return '''// Enhanced test for XMLNode::LastChild
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_LastChild, WithMultipleChildren) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child1 = doc.NewElement("Child1");
    XMLElement* child2 = doc.NewElement("Child2");
    parent->InsertEndChild(child1);
    parent->InsertEndChild(child2);
    
    EXPECT_EQ(parent->LastChild(), child2);
}

TEST(XMLNode_LastChild, NoChildren) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    EXPECT_EQ(parent->LastChild(), nullptr);
}
'''
    
    def _test_xmlnode_value(self) -> str:
        return '''// Enhanced test for XMLNode::Value
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_Value, ElementValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    EXPECT_STREQ(elem->Value(), "Element");
}

TEST(XMLNode_Value, TextValue) {
    XMLDocument doc;
    XMLText* text = doc.NewText("Hello");
    EXPECT_STREQ(text->Value(), "Hello");
}
'''
    
    def _test_xmlnode_setvalue(self) -> str:
        return '''// Enhanced test for XMLNode::SetValue
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_SetValue, ChangeElementName) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("OldName");
    elem->SetValue("NewName");
    EXPECT_STREQ(elem->Value(), "NewName");
}

TEST(XMLNode_SetValue, ChangeTextValue) {
    XMLDocument doc;
    XMLText* text = doc.NewText("Old");
    text->SetValue("New");
    EXPECT_STREQ(text->Value(), "New");
}
'''
    
    def _test_xmlnode_nochildren(self) -> str:
        return '''// Enhanced test for XMLNode::NoChildren
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_NoChildren, EmptyElement) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    EXPECT_TRUE(elem->NoChildren());
}

TEST(XMLNode_NoChildren, ElementWithChild) {
    XMLDocument doc;
    XMLElement* parent = doc.NewElement("Parent");
    XMLElement* child = doc.NewElement("Child");
    parent->InsertEndChild(child);
    EXPECT_FALSE(parent->NoChildren());
}
'''
    
    # XMLAttribute test generators
    def _test_xmlattribute_name(self) -> str:
        return '''// Enhanced test for XMLAttribute::Name
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_Name, GetName) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("testattr", "value");
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_STREQ(attr->Name(), "testattr");
}
'''
    
    def _test_xmlattribute_value(self) -> str:
        return '''// Enhanced test for XMLAttribute::Value
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_Value, GetValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("attr", "testvalue");
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_STREQ(attr->Value(), "testvalue");
}
'''
    
    def _test_xmlattribute_queryintvalue(self) -> str:
        return '''// Enhanced test for XMLAttribute::QueryIntValue
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_QueryIntValue, ValidInt) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("count", 42);
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    int value = 0;
    XMLError err = attr->QueryIntValue(&value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_EQ(value, 42);
}
'''
    
    def _test_xmlattribute_queryfloatvalue(self) -> str:
        return '''// Enhanced test for XMLAttribute::QueryFloatValue
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_QueryFloatValue, ValidFloat) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("ratio", 3.14f);
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    float value = 0.0f;
    XMLError err = attr->QueryFloatValue(&value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_FLOAT_EQ(value, 3.14f);
}
'''
    
    def _test_xmlattribute_queryboolvalue(self) -> str:
        return '''// Enhanced test for XMLAttribute::QueryBoolValue
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_QueryBoolValue, TrueValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("flag", true);
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    bool value = false;
    XMLError err = attr->QueryBoolValue(&value);
    EXPECT_EQ(err, XML_SUCCESS);
    EXPECT_TRUE(value);
}
'''
    
    def _test_xmlattribute_setattribute(self) -> str:
        return '''// Enhanced test for XMLAttribute::SetAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_SetAttribute, UpdateValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("attr", "old");
    elem->SetAttribute("attr", "new");
    EXPECT_STREQ(elem->Attribute("attr"), "new");
}
'''
    
    def _test_xmlattribute_next(self) -> str:
        return '''// Enhanced test for XMLAttribute::Next
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_Next, MultipleAttributes) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("first", "1");
    elem->SetAttribute("second", "2");
    const XMLAttribute* attr1 = elem->FirstAttribute();
    ASSERT_NE(attr1, nullptr);
    const XMLAttribute* attr2 = attr1->Next();
    ASSERT_NE(attr2, nullptr);
    EXPECT_STREQ(attr2->Name(), "second");
}

TEST(XMLAttribute_Next, LastAttribute) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    elem->SetAttribute("only", "value");
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_EQ(attr->Next(), nullptr);
}
'''
    
    # XMLText test generators
    def _test_xmltext_setcdata(self) -> str:
        return '''// Enhanced test for XMLText::SetCData
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLText_SetCData, SetTrue) {
    XMLDocument doc;
    XMLText* text = doc.NewText("data");
    text->SetCData(true);
    EXPECT_TRUE(text->CData());
}

TEST(XMLText_SetCData, SetFalse) {
    XMLDocument doc;
    XMLText* text = doc.NewText("data");
    text->SetCData(true);
    text->SetCData(false);
    EXPECT_FALSE(text->CData());
}
'''
    
    def _test_xmltext_cdata(self) -> str:
        return '''// Enhanced test for XMLText::CData
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLText_CData, DefaultNotCData) {
    XMLDocument doc;
    XMLText* text = doc.NewText("data");
    EXPECT_FALSE(text->CData());
}

TEST(XMLText_CData, AfterSet) {
    XMLDocument doc;
    XMLText* text = doc.NewText("data");
    text->SetCData(true);
    EXPECT_TRUE(text->CData());
}
'''
    
    # XMLComment test generator
    def _test_xmlcomment_value(self) -> str:
        return '''// Enhanced test for XMLComment::Value
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLComment_Value, GetValue) {
    XMLDocument doc;
    XMLComment* comment = doc.NewComment("This is a comment");
    EXPECT_STREQ(comment->Value(), "This is a comment");
}
'''
    
    # XMLDeclaration test generator
    def _test_xmldeclaration_value(self) -> str:
        return '''// Enhanced test for XMLDeclaration::Value
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLDeclaration_Value, GetValue) {
    XMLDocument doc;
    XMLDeclaration* decl = doc.NewDeclaration("xml version=\\"1.0\\"");
    EXPECT_NE(decl->Value(), nullptr);
}
'''
    
    # XMLUnknown test generator
    def _test_xmlunknown_value(self) -> str:
        return '''// Enhanced test for XMLUnknown::Value
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLUnknown_Value, GetValue) {
    XMLDocument doc;
    XMLUnknown* unknown = doc.NewUnknown("unknown content");
    EXPECT_STREQ(unknown->Value(), "unknown content");
}
'''
    
    # XMLHandle test generators
    def _test_xmlhandle_firstchild(self) -> str:
        return '''// Enhanced test for XMLHandle::FirstChild
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLHandle_FirstChild, ValidChild) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("Root");
    XMLElement* child = doc.NewElement("Child");
    root->InsertEndChild(child);
    doc.InsertEndChild(root);
    
    XMLHandle handle(root);
    XMLHandle childHandle = handle.FirstChild();
    EXPECT_NE(childHandle.ToNode(), nullptr);
}
'''
    
    def _test_xmlhandle_firstchildelement(self) -> str:
        return '''// Enhanced test for XMLHandle::FirstChildElement
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLHandle_FirstChildElement, ValidElement) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("Root");
    XMLElement* child = doc.NewElement("Child");
    root->InsertEndChild(child);
    doc.InsertEndChild(root);
    
    XMLHandle handle(root);
    XMLHandle childHandle = handle.FirstChildElement();
    EXPECT_NE(childHandle.ToElement(), nullptr);
}
'''
    
    def _test_xmlhandle_nextsibling(self) -> str:
        return '''// Enhanced test for XMLHandle::NextSibling
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLHandle_NextSibling, ValidSibling) {
    XMLDocument doc;
    XMLElement* root = doc.NewElement("Root");
    XMLElement* child1 = doc.NewElement("Child1");
    XMLElement* child2 = doc.NewElement("Child2");
    root->InsertEndChild(child1);
    root->InsertEndChild(child2);
    
    XMLHandle handle1(child1);
    XMLHandle handle2 = handle1.NextSibling();
    EXPECT_NE(handle2.ToNode(), nullptr);
}
'''
    
    def _test_xmlhandle_toelement(self) -> str:
        return '''// Enhanced test for XMLHandle::ToElement
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLHandle_ToElement, ValidElement) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    XMLHandle handle(elem);
    EXPECT_EQ(handle.ToElement(), elem);
}

TEST(XMLHandle_ToElement, NullHandle) {
    XMLHandle handle(nullptr);
    EXPECT_EQ(handle.ToElement(), nullptr);
}
'''
    
    def _test_xmlhandle_tonode(self) -> str:
        return '''// Enhanced test for XMLHandle::ToNode
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLHandle_ToNode, ValidNode) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("Element");
    XMLHandle handle(elem);
    EXPECT_EQ(handle.ToNode(), elem);
}
'''
    
    # XMLPrinter test generators
    def _test_xmlprinter_pushtext(self) -> str:
        return '''// Enhanced test for XMLPrinter::PushText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_PushText, SimpleText) {
    XMLPrinter printer;
    printer.OpenElement("Element");
    printer.PushText("Hello");
    printer.CloseElement();
    EXPECT_NE(printer.CStr(), nullptr);
}
'''
    
    def _test_xmlprinter_openelement(self) -> str:
        return '''// Enhanced test for XMLPrinter::OpenElement
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_OpenElement, SimpleElement) {
    XMLPrinter printer;
    printer.OpenElement("Root");
    printer.CloseElement();
    const char* result = printer.CStr();
    ASSERT_NE(result, nullptr);
    // Should contain the element name
    EXPECT_NE(strstr(result, "Root"), nullptr);
}
'''
    
    def _test_xmlprinter_closeelement(self) -> str:
        return '''// Enhanced test for XMLPrinter::CloseElement
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_CloseElement, MatchingClose) {
    XMLPrinter printer;
    printer.OpenElement("Element");
    EXPECT_NO_THROW(printer.CloseElement());
}
'''
    
    def _test_xmlprinter_pushattribute(self) -> str:
        return '''// Enhanced test for XMLPrinter::PushAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_PushAttribute, StringAttribute) {
    XMLPrinter printer;
    printer.OpenElement("Element");
    printer.PushAttribute("attr", "value");
    printer.CloseElement();
    const char* result = printer.CStr();
    ASSERT_NE(result, nullptr);
    EXPECT_NE(strstr(result, "attr"), nullptr);
}
'''
    
    def _test_xmlprinter_cstr(self) -> str:
        return '''// Enhanced test for XMLPrinter::CStr
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_CStr, NotNull) {
    XMLPrinter printer;
    printer.OpenElement("Element");
    printer.CloseElement();
    EXPECT_NE(printer.CStr(), nullptr);
}

TEST(XMLPrinter_CStr, ContainsContent) {
    XMLPrinter printer;
    printer.OpenElement("TestElement");
    printer.CloseElement();
    const char* result = printer.CStr();
    ASSERT_NE(result, nullptr);
    EXPECT_NE(strstr(result, "TestElement"), nullptr);
}
'''
    
    def _write_test_file(self, test_name: str, class_name: str, method_name: str, content: str):
        """Write test file and compile it"""
        test_file = self.test_dir / f"{test_name}.cpp"
        with open(test_file, 'w') as f:
            f.write(content)
        
        # Compile test
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
        """Save test metadata"""
        metadata_file = self.output_dir / "enhanced_test_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.test_metadata, f, indent=2)
        print(f"\n✅ Metadata saved to {metadata_file}")


def main():
    """Main entry point"""
    project_root = Path("/workspaces/CppMicroAgent/TestProjects/tinyxml2")
    output_dir = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    
    generator = TinyXML2TestGenerator(project_root, output_dir)
    metadata = generator.generate_all_tests()
    
    print("\n" + "="*70)
    print(f"✅ Generated {len(metadata)} enhanced tests")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    exit(main())
