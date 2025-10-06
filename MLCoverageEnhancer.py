#!/usr/bin/env python3
"""
ML-Enhanced Coverage Prediction and Improvement System
Uses machine learning techniques to predict and improve coverage
"""

import os
import json
import numpy as np
from typing import List, Dict, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class MLCoveragePredictor:
    """Machine learning based coverage predictor and improvement recommender"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.is_trained = False
        
    def extract_code_features(self, source_code: str) -> Dict:
        """Extract features from source code for ML analysis"""
        
        features = {
            # Basic metrics
            "lines_of_code": len(source_code.split('\n')),
            "char_count": len(source_code),
            
            # Complexity indicators
            "if_count": source_code.count('if'),
            "else_count": source_code.count('else'),
            "for_count": source_code.count('for'),
            "while_count": source_code.count('while'),
            "switch_count": source_code.count('switch'),
            "case_count": source_code.count('case'),
            
            # Function indicators
            "function_count": source_code.count('(') - source_code.count('if (') - source_code.count('while ('),
            "return_count": source_code.count('return'),
            
            # OOP indicators
            "class_count": source_code.count('class'),
            "public_count": source_code.count('public'),
            "private_count": source_code.count('private'),
            "virtual_count": source_code.count('virtual'),
            
            # Error handling
            "try_count": source_code.count('try'),
            "catch_count": source_code.count('catch'),
            "throw_count": source_code.count('throw'),
            
            # Memory management
            "new_count": source_code.count('new'),
            "delete_count": source_code.count('delete'),
            "malloc_count": source_code.count('malloc'),
            "free_count": source_code.count('free'),
            
            # STL usage
            "vector_count": source_code.count('vector'),
            "string_count": source_code.count('string'),
            "map_count": source_code.count('map'),
            "set_count": source_code.count('set'),
            
            # Calculated complexity
            "cyclomatic_complexity": (
                source_code.count('if') + source_code.count('while') + 
                source_code.count('for') + source_code.count('case') + 1
            ),
            
            # Comment ratio
            "comment_ratio": (source_code.count('//') + source_code.count('/*')) / max(len(source_code.split('\n')), 1)
        }
        
        return features
    
    def create_training_data(self, historical_projects: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """Create training data from historical project coverage results"""
        
        X_features = []
        y_coverage = []
        
        for project in historical_projects:
            if 'source_code' in project and 'coverage_percentage' in project:
                features = self.extract_code_features(project['source_code'])
                feature_vector = list(features.values())
                
                X_features.append(feature_vector)
                y_coverage.append(project['coverage_percentage'])
        
        return np.array(X_features), np.array(y_coverage)
    
    def train_model(self, historical_projects: List[Dict]):
        """Train the ML model on historical coverage data"""
        
        if len(historical_projects) < 5:
            print("⚠️  Insufficient training data for ML model")
            return False
        
        X, y = self.create_training_data(historical_projects)
        
        if len(X) == 0:
            print("⚠️  No valid training features extracted")
            return False
        
        self.model.fit(X, y)
        self.is_trained = True
        
        print(f"✅ ML model trained on {len(X)} samples")
        return True
    
    def predict_coverage(self, source_code: str) -> float:
        """Predict expected coverage for given source code"""
        
        if not self.is_trained:
            return 50.0  # Default prediction
        
        features = self.extract_code_features(source_code)
        feature_vector = np.array([list(features.values())])
        
        predicted_coverage = self.model.predict(feature_vector)[0]
        return max(0.0, min(100.0, predicted_coverage))
    
    def identify_coverage_improvement_areas(self, source_code: str, current_coverage: float) -> List[Dict]:
        """Identify areas most likely to improve coverage using ML insights"""
        
        predicted_coverage = self.predict_coverage(source_code)
        gap = predicted_coverage - current_coverage
        
        features = self.extract_code_features(source_code)
        
        improvements = []
        
        # ML-based improvement recommendations
        if gap > 10:  # Significant improvement potential
            if features['if_count'] > 3:
                improvements.append({
                    "type": "branch_coverage_priority",
                    "confidence": min(gap / 10, 1.0),
                    "description": "High branch coverage improvement potential detected",
                    "focus": "conditional_statements"
                })
            
            if features['cyclomatic_complexity'] > 5:
                improvements.append({
                    "type": "complexity_reduction_testing",
                    "confidence": min(gap / 15, 1.0), 
                    "description": "Complex code detected - focus on path coverage",
                    "focus": "execution_paths"
                })
            
            if features['try_count'] > 0 and features['catch_count'] == 0:
                improvements.append({
                    "type": "exception_path_testing",
                    "confidence": 0.8,
                    "description": "Exception handling coverage needed",
                    "focus": "error_paths"
                })
        
        return improvements

class CoveragePatternAnalyzer:
    """Analyzes patterns in coverage data to identify improvement strategies"""
    
    def __init__(self):
        self.coverage_patterns = {}
    
    def analyze_coverage_patterns(self, coverage_history: List[Dict]) -> Dict:
        """Analyze patterns in coverage improvement over time"""
        
        patterns = {
            "improvement_trend": self._calculate_improvement_trend(coverage_history),
            "plateau_detection": self._detect_coverage_plateau(coverage_history),
            "strategy_effectiveness": self._analyze_strategy_effectiveness(coverage_history),
            "optimal_iteration_count": self._calculate_optimal_iterations(coverage_history)
        }
        
        return patterns
    
    def _calculate_improvement_trend(self, history: List[Dict]) -> Dict:
        """Calculate coverage improvement trend"""
        
        if len(history) < 2:
            return {"trend": "insufficient_data"}
        
        coverages = [h.get("coverage", 0) for h in history]
        
        # Calculate trend
        if len(coverages) >= 3:
            recent_trend = coverages[-1] - coverages[-2]
            overall_trend = coverages[-1] - coverages[0]
            
            return {
                "trend": "improving" if recent_trend > 0 else "declining" if recent_trend < 0 else "stable",
                "recent_change": recent_trend,
                "overall_change": overall_trend,
                "improvement_rate": overall_trend / len(coverages)
            }
        
        return {"trend": "insufficient_data"}
    
    def _detect_coverage_plateau(self, history: List[Dict]) -> Dict:
        """Detect if coverage has plateaued"""
        
        if len(history) < 3:
            return {"plateau": False}
        
        recent_coverages = [h.get("coverage", 0) for h in history[-3:]]
        variance = np.var(recent_coverages) if len(recent_coverages) > 1 else 0
        
        plateau_detected = variance < 1.0  # Less than 1% variance
        
        return {
            "plateau": plateau_detected,
            "variance": variance,
            "recommendation": "try_alternative_strategies" if plateau_detected else "continue_current_approach"
        }
    
    def _analyze_strategy_effectiveness(self, history: List[Dict]) -> Dict:
        """Analyze which strategies were most effective"""
        
        strategy_effectiveness = {}
        
        for i, iteration in enumerate(history):
            if i > 0:  # Compare with previous iteration
                improvement = iteration.get("coverage", 0) - history[i-1].get("coverage", 0)
                strategies = iteration.get("strategies_applied", [])
                
                for strategy in strategies:
                    if strategy not in strategy_effectiveness:
                        strategy_effectiveness[strategy] = {"total_improvement": 0, "count": 0}
                    
                    strategy_effectiveness[strategy]["total_improvement"] += improvement
                    strategy_effectiveness[strategy]["count"] += 1
        
        # Calculate average effectiveness
        for strategy, data in strategy_effectiveness.items():
            if data["count"] > 0:
                data["average_improvement"] = data["total_improvement"] / data["count"]
        
        return strategy_effectiveness
    
    def _calculate_optimal_iterations(self, history: List[Dict]) -> int:
        """Calculate optimal number of iterations based on historical data"""
        
        if len(history) < 2:
            return 3  # Default
        
        # Find point of diminishing returns
        improvements = []
        for i in range(1, len(history)):
            improvement = history[i].get("coverage", 0) - history[i-1].get("coverage", 0)
            improvements.append(improvement)
        
        # Find where improvement drops below threshold
        threshold = 2.0  # 2% improvement
        optimal_iterations = len(improvements)
        
        for i, improvement in enumerate(improvements):
            if improvement < threshold:
                optimal_iterations = i + 1
                break
        
        return min(max(optimal_iterations, 2), 5)  # Between 2 and 5

class IntelligentTestGenerator:
    """Generates intelligent tests based on coverage analysis and ML insights"""
    
    def __init__(self):
        self.ml_predictor = MLCoveragePredictor()
        self.pattern_analyzer = CoveragePatternAnalyzer()
    
    def generate_targeted_tests(self, source_code: str, coverage_data: Dict, 
                              improvement_areas: List[Dict]) -> List[str]:
        """Generate targeted test cases based on ML analysis"""
        
        test_cases = []
        
        for area in improvement_areas:
            area_type = area.get("type", "")
            confidence = area.get("confidence", 0.5)
            
            if area_type == "branch_coverage_priority" and confidence > 0.7:
                test_cases.extend(self._generate_branch_tests(source_code, area))
            
            elif area_type == "complexity_reduction_testing" and confidence > 0.6:
                test_cases.extend(self._generate_complexity_tests(source_code, area))
            
            elif area_type == "exception_path_testing" and confidence > 0.8:
                test_cases.extend(self._generate_exception_tests(source_code, area))
        
        return test_cases
    
    def _generate_branch_tests(self, source_code: str, area: Dict) -> List[str]:
        """Generate branch-focused test cases"""
        
        # Extract if statements and generate tests
        if_patterns = self._extract_if_patterns(source_code)
        
        tests = []
        for pattern in if_patterns[:3]:  # Limit to top 3
            tests.append(f"""
// ML-Generated Branch Test for: {pattern}
TEST(MLBranchCoverage, {pattern.replace(' ', '_')[:30]}) {{
    // Test true branch
    EXPECT_TRUE(/* condition that makes {pattern} true */);
    
    // Test false branch  
    EXPECT_FALSE(/* condition that makes {pattern} false */);
    
    // Test edge cases
    // TODO: Add specific edge case tests based on condition type
}}
""")
        
        return tests
    
    def _generate_complexity_tests(self, source_code: str, area: Dict) -> List[str]:
        """Generate tests for complex code paths"""
        
        return [f"""
// ML-Generated Complexity Test
TEST(MLComplexityReduction, ComplexPathCoverage) {{
    // Test primary execution path
    // TODO: Add tests that exercise the most complex code paths
    
    // Test alternative paths
    // TODO: Add tests for less common execution paths
    
    // Test boundary conditions in complex logic
    // TODO: Add boundary tests for complex conditional logic
}}
"""]
    
    def _generate_exception_tests(self, source_code: str, area: Dict) -> List[str]:
        """Generate exception handling tests"""
        
        return [f"""
// ML-Generated Exception Test
TEST(MLExceptionCoverage, ExceptionPathTesting) {{
    // Test normal execution (no exception)
    EXPECT_NO_THROW(/* normal operation */);
    
    // Test exception scenarios
    EXPECT_THROW(/* operation that should throw */, std::exception);
    
    // Test exception handling and recovery
    // TODO: Add tests for exception handling and state recovery
}}
"""]
    
    def _extract_if_patterns(self, source_code: str) -> List[str]:
        """Extract if statement patterns for test generation"""
        
        import re
        
        if_pattern = r'if\s*\(([^)]+)\)'
        matches = re.findall(if_pattern, source_code)
        
        # Clean and return unique patterns
        patterns = []
        for match in matches:
            cleaned = match.strip()
            if cleaned and len(cleaned) < 100:  # Reasonable length
                patterns.append(cleaned)
        
        return list(set(patterns))  # Remove duplicates

def create_demo_advanced_improvement():
    """Create a demonstration of advanced improvement mechanisms"""
    
    print("🧠 ADVANCED COVERAGE IMPROVEMENT MECHANISMS")
    print("=" * 55)
    
    # Sample source code for analysis
    sample_code = '''
class Calculator {
public:
    int divide(int a, int b) {
        if (b == 0) {
            throw std::invalid_argument("Division by zero");
        }
        return a / b;
    }
    
    int factorial(int n) {
        if (n < 0) return -1;
        if (n == 0 || n == 1) return 1;
        
        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
    
    bool isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        return true;
    }
};
'''
    
    # Initialize ML predictor
    ml_predictor = MLCoveragePredictor()
    
    # Extract features
    features = ml_predictor.extract_code_features(sample_code)
    print("🔍 EXTRACTED CODE FEATURES:")
    for key, value in features.items():
        print(f"   {key}: {value}")
    
    # Predict coverage (without training, uses default)
    predicted_coverage = ml_predictor.predict_coverage(sample_code)
    print(f"\n🎯 PREDICTED COVERAGE: {predicted_coverage:.1f}%")
    
    # Identify improvement areas
    current_coverage = 65.0  # Sample current coverage
    improvements = ml_predictor.identify_coverage_improvement_areas(sample_code, current_coverage)
    
    print(f"\n💡 IMPROVEMENT RECOMMENDATIONS:")
    for i, improvement in enumerate(improvements, 1):
        print(f"   {i}. {improvement['type']} (Confidence: {improvement['confidence']:.1f})")
        print(f"      {improvement['description']}")
        print(f"      Focus: {improvement['focus']}")
    
    # Generate intelligent tests
    test_generator = IntelligentTestGenerator()
    test_cases = test_generator.generate_targeted_tests(sample_code, {}, improvements)
    
    print(f"\n🧪 GENERATED TEST CASES:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"   Test Case {i}:")
        print(f"   {test_case}")
    
    # Save demonstration results
    os.makedirs("output/AdvancedImprovements", exist_ok=True)
    
    demo_report = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "extracted_features": features,
        "predicted_coverage": predicted_coverage,
        "current_coverage": current_coverage,
        "improvement_recommendations": improvements,
        "generated_test_cases": test_cases
    }
    
    with open("output/AdvancedImprovements/demo_advanced_analysis.json", 'w') as f:
        json.dump(demo_report, f, indent=2)
    
    print(f"\n📄 Demo results saved to: output/AdvancedImprovements/demo_advanced_analysis.json")
    
    return demo_report

if __name__ == "__main__":
    try:
        # Install required ML packages if not available
        import sklearn
        import numpy as np
        
        create_demo_advanced_improvement()
        
    except ImportError:
        print("⚠️  ML packages not available. Installing...")
        print("   Run: pip install scikit-learn numpy")
        print("   Then re-run this script for ML-enhanced coverage improvement")
        
        # Create basic demo without ML
        print("\n🔧 BASIC ADVANCED IMPROVEMENT DEMO:")
        print("   - Code complexity analysis")
        print("   - Pattern-based improvement suggestions")  
        print("   - Intelligent test case templates")
        
        features = {
            "lines_of_code": 45,
            "cyclomatic_complexity": 8,
            "if_count": 6,
            "for_count": 2,
            "try_count": 1
        }
        
        print(f"\n📊 Sample Feature Analysis: {features}")
        print("💡 Recommendations: Focus on branch coverage and exception testing")