#!/bin/bash
# Test all code examples and exercises in the textbook

# Purpose: Execute all Python code examples to verify they run without errors
# Usage: bash scripts/test-exercises.sh [chapter_directory]

set -e  # Exit on first error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

echo "=========================================="
echo "Testing Python Code Examples"
echo "=========================================="

# Determine target directory
if [ -n "$1" ]; then
    TARGET_DIR="$1"
else
    TARGET_DIR="docs"
fi

echo "Target directory: $TARGET_DIR"
echo ""

# Find all Python files in exercises directories
PYTHON_FILES=$(find "$TARGET_DIR" -name "*.py" -path "*/exercises/*" 2>/dev/null || true)

if [ -z "$PYTHON_FILES" ]; then
    echo "No Python exercise files found in $TARGET_DIR"
    exit 0
fi

# Count total files
TOTAL_TESTS=$(echo "$PYTHON_FILES" | wc -l)
echo "Found $TOTAL_TESTS Python exercise files"
echo ""

# Test each file
for py_file in $PYTHON_FILES; do
    echo "Testing: $py_file"

    # Run pylint/flake8 for code quality (optional, non-blocking)
    if command -v flake8 &> /dev/null; then
        if flake8 "$py_file" --max-line-length=100 --ignore=E501,W503 2>&1 | grep -v "no-member"; then
            echo -e "${YELLOW}  ⚠ Code quality warnings (non-blocking)${NC}"
        fi
    fi

    # Check if file contains executable code (not just templates with TODO)
    if grep -q "TODO:" "$py_file"; then
        echo -e "${YELLOW}  ⊘ SKIP: File contains TODO placeholders${NC}"
        ((TOTAL_TESTS--)) || true
        echo ""
        continue
    fi

    # Try to run the file
    if python3 "$py_file" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ PASS${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}  ✗ FAIL${NC}"
        # Show error for debugging
        python3 "$py_file" 2>&1 | head -n 5
        ((FAILED_TESTS++))
    fi

    echo ""
done

# Run pytest if test files exist
echo "=========================================="
echo "Running pytest on test files"
echo "=========================================="

if find "$TARGET_DIR" -name "test_*.py" -o -name "*_test.py" | grep -q .; then
    if command -v pytest &> /dev/null; then
        if pytest "$TARGET_DIR" -v --tb=short; then
            echo -e "${GREEN}✓ pytest PASSED${NC}"
        else
            echo -e "${RED}✗ pytest FAILED${NC}"
            ((FAILED_TESTS++))
        fi
    else
        echo -e "${YELLOW}⚠ pytest not installed, skipping unit tests${NC}"
    fi
else
    echo "No pytest test files found"
fi

# Print summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Total files tested: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"

if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
    echo ""
    echo "✗ SOME TESTS FAILED"
    exit 1
else
    echo "Failed: 0"
    echo ""
    echo "✓ ALL TESTS PASSED"
    exit 0
fi
