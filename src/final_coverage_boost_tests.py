#!/usr/bin/env python3
"""
Final Test Generator to Push Coverage to 75%+
Focuses on uncovered methods and edge cases
"""

import subprocess
from pathlib import Path
import json

class FinalCoverageBoostGenerator:
    """Generate final tests to reach 75% coverage"""
    
    def __init__(self, project_root: Path, output_dir: Path):
        self.project_root = project_root
        self.output_dir = output_dir
        self.test_dir = output_dir / "tests"
        self.bin_dir = output_dir / "bin"
        self.test_metadata = []
        
    def generate_all_tests(self):
        """Generate all final coverage boost tests"""
        print("="*70)
        print("Final Coverage Boost Generator - Target: 75%+")
        print("="*70)
        print()
        
        # Generate tests for Query methods variants
        self.generate_query_variant_tests()
        
        # Generate attribute manipulation tests
        self.generate_attribute_tests()
        
        # Generate double/unsigned/int64 tests
        self.generate_numeric_variant_tests()
        
        # Generate more XMLPrinter tests
        self.generate_printer_variant_tests()
        
        # Generate whitespace handling tests
        self.generate_whitespace_tests()
        
        # Generate ShallowClone/ShallowEqual tests
        self.generate_clone_tests()
        
        # Save metadata
        self.save_metadata()
        
        print(f"\n✅ Generated {len(self.test_metadata)} final tests")
        return self.test_metadata
    
    def generate_query_variant_tests(self):
        """Generate tests for Query method variants"""
        print("Generating Query variant tests...")
        
        tests = [
            ("QueryDoubleAttribute", self._test_querydoubleattribute),
            ("QueryUnsignedAttribute", self._test_queryunsignedattribute),
            ("QueryInt64Attribute", self._test_queryint64attribute),
            ("QueryUnsigned64Attribute", self._test_queryunsigned64attribute),
            ("QueryDoubleText", self._test_querydoubletext),
            ("QueryBoolText", self._test_querybooltext),
            ("QueryUnsignedText", self._test_queryunsignedtext),
            ("QueryInt64Text", self._test_queryint64text),
            ("QueryUnsigned64Text", self._test_queryunsigned64text),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Final_{name}", "XMLElement", name, content)
    
    def generate_attribute_tests(self):
        """Generate attribute manipulation tests"""
        print("Generating Attribute manipulation tests...")
        
        tests = [
            ("DeleteAttribute", self._test_deleteattribute),
            ("FindAttribute", self._test_findattribute),
            ("DoubleAttribute", self._test_doubleattribute),
            ("UnsignedAttribute", self._test_unsignedattribute),
            ("Int64Attribute", self._test_int64attribute),
            ("Unsigned64Attribute", self._test_unsigned64attribute),
            ("BoolAttribute", self._test_boolattribute),
            ("FloatAttribute", self._test_floatattribute),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Final_{name}", "XMLElement", name, content)
    
    def generate_numeric_variant_tests(self):
        """Generate numeric type variant tests"""
        print("Generating Numeric variant tests...")
        
        tests = [
            ("DoubleValue", self._test_doublevalue),
            ("Int64Value", self._test_int64value),
            ("Unsigned64Value", self._test_unsigned64value),
            ("UnsignedValue", self._test_unsignedvalue),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Final_{name}", "XMLAttribute", name, content)
    
    def generate_printer_variant_tests(self):
        """Generate XMLPrinter variant tests"""
        print("Generating XMLPrinter variant tests...")
        
        tests = [
            ("PushComment", self._test_pushcomment),
            ("PushDeclaration", self._test_pushdeclaration),
            ("PushUnknown", self._test_pushunknown),
            ("CStrSize", self._test_cstrsize),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Final_Printer_{name}", "XMLPrinter", name, content)
    
    def generate_whitespace_tests(self):
        """Generate whitespace handling tests"""
        print("Generating Whitespace tests...")
        
        content = self._test_whitespace_modes()
        self._write_test_file("tinyxml2_Final_WhitespaceModes", "XMLDocument", "Whitespace", content)
    
    def generate_clone_tests(self):
        """Generate ShallowClone and ShallowEqual tests"""
        print("Generating Clone/Equal tests...")
        
        tests = [
            ("ShallowClone_Element", self._test_shallowclone_element),
            ("ShallowClone_Text", self._test_shallowclone_text),
            ("ShallowEqual", self._test_shallowequal),
        ]
        
        for name, gen_func in tests:
            content = gen_func()
            self._write_test_file(f"tinyxml2_Final_{name}", "XMLNode", name, content)
    
    # Query variant test generators
    def _test_querydoubleattribute(self) -> str:
        return '''// Test XMLElement::QueryDoubleAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryDoubleAttribute, ValidDouble) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", 3.14159);
    double val = 0.0;
    EXPECT_EQ(elem->QueryDoubleAttribute("value", &val), XML_SUCCESS);
    EXPECT_DOUBLE_EQ(val, 3.14159);
}

TEST(XMLElement_QueryDoubleAttribute, LargeNumber) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", 1.23456789e10);
    double val = 0.0;
    EXPECT_EQ(elem->QueryDoubleAttribute("value", &val), XML_SUCCESS);
}

TEST(XMLElement_QueryDoubleAttribute, SmallNumber) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", 1.23456789e-10);
    double val = 0.0;
    EXPECT_EQ(elem->QueryDoubleAttribute("value", &val), XML_SUCCESS);
}
'''
    
    def _test_queryunsignedattribute(self) -> str:
        return '''// Test XMLElement::QueryUnsignedAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryUnsignedAttribute, ValidUnsigned) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", 42u);
    unsigned val = 0;
    EXPECT_EQ(elem->QueryUnsignedAttribute("value", &val), XML_SUCCESS);
    EXPECT_EQ(val, 42u);
}

TEST(XMLElement_QueryUnsignedAttribute, MaxValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", UINT_MAX);
    unsigned val = 0;
    EXPECT_EQ(elem->QueryUnsignedAttribute("value", &val), XML_SUCCESS);
}
'''
    
    def _test_queryint64attribute(self) -> str:
        return '''// Test XMLElement::QueryInt64Attribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryInt64Attribute, ValidInt64) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    int64_t large_val = 9223372036854775807LL;  // Max int64
    elem->SetAttribute("value", large_val);
    int64_t val = 0;
    EXPECT_EQ(elem->QueryInt64Attribute("value", &val), XML_SUCCESS);
}
'''
    
    def _test_queryunsigned64attribute(self) -> str:
        return '''// Test XMLElement::QueryUnsigned64Attribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryUnsigned64Attribute, ValidUnsigned64) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    uint64_t large_val = 18446744073709551615ULL;  // Max uint64
    elem->SetAttribute("value", large_val);
    uint64_t val = 0;
    EXPECT_EQ(elem->QueryUnsigned64Attribute("value", &val), XML_SUCCESS);
}
'''
    
    def _test_querydoubletext(self) -> str:
        return '''// Test XMLElement::QueryDoubleText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryDoubleText, ValidDouble) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetText(3.14159);
    double val = 0.0;
    EXPECT_EQ(elem->QueryDoubleText(&val), XML_SUCCESS);
    EXPECT_DOUBLE_EQ(val, 3.14159);
}
'''
    
    def _test_querybooltext(self) -> str:
        return '''// Test XMLElement::QueryBoolText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryBoolText, TrueValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetText(true);
    bool val = false;
    EXPECT_EQ(elem->QueryBoolText(&val), XML_SUCCESS);
    EXPECT_TRUE(val);
}

TEST(XMLElement_QueryBoolText, FalseValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetText(false);
    bool val = true;
    EXPECT_EQ(elem->QueryBoolText(&val), XML_SUCCESS);
    EXPECT_FALSE(val);
}
'''
    
    def _test_queryunsignedtext(self) -> str:
        return '''// Test XMLElement::QueryUnsignedText
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryUnsignedText, ValidUnsigned) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetText(42u);
    unsigned val = 0;
    EXPECT_EQ(elem->QueryUnsignedText(&val), XML_SUCCESS);
    EXPECT_EQ(val, 42u);
}
'''
    
    def _test_queryint64text(self) -> str:
        return '''// Test XMLElement::QueryInt64Text
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryInt64Text, ValidInt64) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    int64_t large_val = 9223372036854775807LL;
    elem->SetText(large_val);
    int64_t val = 0;
    EXPECT_EQ(elem->QueryInt64Text(&val), XML_SUCCESS);
}
'''
    
    def _test_queryunsigned64text(self) -> str:
        return '''// Test XMLElement::QueryUnsigned64Text
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_QueryUnsigned64Text, ValidUnsigned64) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    uint64_t large_val = 18446744073709551615ULL;
    elem->SetText(large_val);
    uint64_t val = 0;
    EXPECT_EQ(elem->QueryUnsigned64Text(&val), XML_SUCCESS);
}
'''
    
    # Attribute manipulation test generators
    def _test_deleteattribute(self) -> str:
        return '''// Test XMLElement::DeleteAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_DeleteAttribute, DeleteExisting) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("attr", "value");
    elem->DeleteAttribute("attr");
    EXPECT_EQ(elem->Attribute("attr"), nullptr);
}

TEST(XMLElement_DeleteAttribute, DeleteNonExistent) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->DeleteAttribute("nonexistent");  // Should not crash
    SUCCEED();
}

TEST(XMLElement_DeleteAttribute, DeleteOneOfMany) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("a", "1");
    elem->SetAttribute("b", "2");
    elem->SetAttribute("c", "3");
    elem->DeleteAttribute("b");
    EXPECT_NE(elem->Attribute("a"), nullptr);
    EXPECT_EQ(elem->Attribute("b"), nullptr);
    EXPECT_NE(elem->Attribute("c"), nullptr);
}
'''
    
    def _test_findattribute(self) -> str:
        return '''// Test XMLElement::FindAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_FindAttribute, FindExisting) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("key", "value");
    const XMLAttribute* attr = elem->FindAttribute("key");
    ASSERT_NE(attr, nullptr);
    EXPECT_STREQ(attr->Name(), "key");
}

TEST(XMLElement_FindAttribute, FindNonExistent) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    const XMLAttribute* attr = elem->FindAttribute("missing");
    EXPECT_EQ(attr, nullptr);
}
'''
    
    def _test_doubleattribute(self) -> str:
        return '''// Test XMLElement::DoubleAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_DoubleAttribute, GetDouble) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", 2.71828);
    EXPECT_DOUBLE_EQ(elem->DoubleAttribute("value"), 2.71828);
}

TEST(XMLElement_DoubleAttribute, DefaultValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    EXPECT_DOUBLE_EQ(elem->DoubleAttribute("missing", 1.5), 1.5);
}
'''
    
    def _test_unsignedattribute(self) -> str:
        return '''// Test XMLElement::UnsignedAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_UnsignedAttribute, GetUnsigned) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", 123u);
    EXPECT_EQ(elem->UnsignedAttribute("value"), 123u);
}

TEST(XMLElement_UnsignedAttribute, DefaultValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    EXPECT_EQ(elem->UnsignedAttribute("missing", 99u), 99u);
}
'''
    
    def _test_int64attribute(self) -> str:
        return '''// Test XMLElement::Int64Attribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_Int64Attribute, GetInt64) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    int64_t val = 9223372036854775807LL;
    elem->SetAttribute("value", val);
    EXPECT_EQ(elem->Int64Attribute("value"), val);
}
'''
    
    def _test_unsigned64attribute(self) -> str:
        return '''// Test XMLElement::Unsigned64Attribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_Unsigned64Attribute, GetUnsigned64) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    uint64_t val = 18446744073709551615ULL;
    elem->SetAttribute("value", val);
    EXPECT_EQ(elem->Unsigned64Attribute("value"), val);
}
'''
    
    def _test_boolattribute(self) -> str:
        return '''// Test XMLElement::BoolAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_BoolAttribute, GetTrue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("flag", true);
    EXPECT_TRUE(elem->BoolAttribute("flag"));
}

TEST(XMLElement_BoolAttribute, GetFalse) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("flag", false);
    EXPECT_FALSE(elem->BoolAttribute("flag"));
}

TEST(XMLElement_BoolAttribute, DefaultValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    EXPECT_TRUE(elem->BoolAttribute("missing", true));
}
'''
    
    def _test_floatattribute(self) -> str:
        return '''// Test XMLElement::FloatAttribute
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLElement_FloatAttribute, GetFloat) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("value", 2.5f);
    EXPECT_FLOAT_EQ(elem->FloatAttribute("value"), 2.5f);
}

TEST(XMLElement_FloatAttribute, DefaultValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    EXPECT_FLOAT_EQ(elem->FloatAttribute("missing", 1.5f), 1.5f);
}
'''
    
    # Numeric variant test generators for XMLAttribute
    def _test_doublevalue(self) -> str:
        return '''// Test XMLAttribute::DoubleValue
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_DoubleValue, GetValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("attr", 3.14);
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_DOUBLE_EQ(attr->DoubleValue(), 3.14);
}
'''
    
    def _test_int64value(self) -> str:
        return '''// Test XMLAttribute::Int64Value
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_Int64Value, GetValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    int64_t val = 9223372036854775807LL;
    elem->SetAttribute("attr", val);
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_EQ(attr->Int64Value(), val);
}
'''
    
    def _test_unsigned64value(self) -> str:
        return '''// Test XMLAttribute::Unsigned64Value
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_Unsigned64Value, GetValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    uint64_t val = 18446744073709551615ULL;
    elem->SetAttribute("attr", val);
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_EQ(attr->Unsigned64Value(), val);
}
'''
    
    def _test_unsignedvalue(self) -> str:
        return '''// Test XMLAttribute::UnsignedValue
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLAttribute_UnsignedValue, GetValue) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("elem");
    elem->SetAttribute("attr", 42u);
    const XMLAttribute* attr = elem->FirstAttribute();
    ASSERT_NE(attr, nullptr);
    EXPECT_EQ(attr->UnsignedValue(), 42u);
}
'''
    
    # XMLPrinter variant test generators
    def _test_pushcomment(self) -> str:
        return '''// Test XMLPrinter::PushComment
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_PushComment, SimpleComment) {
    XMLPrinter printer;
    printer.OpenElement("root");
    printer.PushComment("This is a comment");
    printer.CloseElement();
    const char* result = printer.CStr();
    ASSERT_NE(result, nullptr);
    EXPECT_NE(strstr(result, "comment"), nullptr);
}
'''
    
    def _test_pushdeclaration(self) -> str:
        return '''// Test XMLPrinter::PushDeclaration
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_PushDeclaration, XMLDeclaration) {
    XMLPrinter printer;
    printer.PushDeclaration("xml version=\\"1.0\\"");
    printer.OpenElement("root");
    printer.CloseElement();
    EXPECT_NE(printer.CStr(), nullptr);
}
'''
    
    def _test_pushunknown(self) -> str:
        return '''// Test XMLPrinter::PushUnknown
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_PushUnknown, UnknownContent) {
    XMLPrinter printer;
    printer.OpenElement("root");
    printer.PushUnknown("unknown content");
    printer.CloseElement();
    EXPECT_NE(printer.CStr(), nullptr);
}
'''
    
    def _test_cstrsize(self) -> str:
        return '''// Test XMLPrinter::CStrSize
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLPrinter_CStrSize, SizeAfterPrint) {
    XMLPrinter printer;
    printer.OpenElement("elem");
    printer.PushText("text");
    printer.CloseElement();
    int size = printer.CStrSize();
    EXPECT_GT(size, 0);
    EXPECT_EQ(size, (int)strlen(printer.CStr()));
}
'''
    
    # Whitespace test generator
    def _test_whitespace_modes(self) -> str:
        return '''// Test XMLDocument whitespace modes
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLDocument_Whitespace, PreserveMode) {
    const char* xml = "<root>  Text with spaces  </root>";
    XMLDocument doc(true, PRESERVE_WHITESPACE);
    doc.Parse(xml);
    EXPECT_NE(doc.RootElement()->GetText(), nullptr);
}

TEST(XMLDocument_Whitespace, CollapseMode) {
    const char* xml = "<root>  Text with spaces  </root>";
    XMLDocument doc(true, COLLAPSE_WHITESPACE);
    doc.Parse(xml);
    EXPECT_NE(doc.RootElement()->GetText(), nullptr);
}
'''
    
    # Clone test generators
    def _test_shallowclone_element(self) -> str:
        return '''// Test XMLNode::ShallowClone for elements
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_ShallowClone, CloneElement) {
    XMLDocument doc;
    XMLElement* elem = doc.NewElement("original");
    elem->SetAttribute("attr", "value");
    
    XMLNode* clone = elem->ShallowClone(&doc);
    ASSERT_NE(clone, nullptr);
    EXPECT_NE(clone, elem);  // Different objects
}
'''
    
    def _test_shallowclone_text(self) -> str:
        return '''// Test XMLNode::ShallowClone for text
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_ShallowClone, CloneText) {
    XMLDocument doc;
    XMLText* text = doc.NewText("Hello");
    
    XMLNode* clone = text->ShallowClone(&doc);
    ASSERT_NE(clone, nullptr);
    EXPECT_NE(clone, text);
}
'''
    
    def _test_shallowequal(self) -> str:
        return '''// Test XMLNode::ShallowEqual
#include <gtest/gtest.h>
#include "tinyxml2.h"

using namespace tinyxml2;

TEST(XMLNode_ShallowEqual, SameElements) {
    XMLDocument doc;
    XMLElement* elem1 = doc.NewElement("elem");
    XMLElement* elem2 = doc.NewElement("elem");
    EXPECT_TRUE(elem1->ShallowEqual(elem2));
}

TEST(XMLNode_ShallowEqual, DifferentElements) {
    XMLDocument doc;
    XMLElement* elem1 = doc.NewElement("elem1");
    XMLElement* elem2 = doc.NewElement("elem2");
    EXPECT_FALSE(elem1->ShallowEqual(elem2));
}

TEST(XMLNode_ShallowEqual, SameText) {
    XMLDocument doc;
    XMLText* text1 = doc.NewText("Hello");
    XMLText* text2 = doc.NewText("Hello");
    EXPECT_TRUE(text1->ShallowEqual(text2));
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
        except Exception as e:
            print(f"  ❌ {test_name} - Exception: {e}")
    
    def save_metadata(self):
        """Save metadata"""
        metadata_file = self.output_dir / "final_test_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.test_metadata, f, indent=2)
        print(f"\n✅ Metadata saved to {metadata_file}")


def main():
    """Main entry point"""
    project_root = Path("/workspaces/CppMicroAgent/TestProjects/tinyxml2")
    output_dir = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    
    generator = FinalCoverageBoostGenerator(project_root, output_dir)
    metadata = generator.generate_all_tests()
    
    print("\n" + "="*70)
    print(f"✅ Generated {len(metadata)} final coverage boost tests")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    exit(main())
