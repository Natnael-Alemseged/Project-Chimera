#!/bin/bash
# Project Chimera - Spec Alignment Checker
# Verifies that code references specs/ and SRS terms (Planner, Worker, Judge, MCP, etc.)

set -e

echo "🔍 Checking spec alignment..."

# Track if any issues are found
ISSUES=0

# Check 1: Look for references to specs/ directory in Python files
echo "  Checking for specs/ references in code..."
if ! grep -r "specs/" --include="*.py" . > /dev/null 2>&1; then
    echo "  ⚠️  WARNING: No references to specs/ found in Python files"
    ISSUES=$((ISSUES + 1))
else
    echo "  ✅ Found references to specs/ in code"
fi

# Check 2: Look for SRS architectural terms (Planner, Worker, Judge, MCP)
echo "  Checking for SRS architectural terms..."
ARCH_TERMS=("Planner" "Worker" "Judge" "MCP" "FastRender" "HITL")
FOUND_TERMS=0

for term in "${ARCH_TERMS[@]}"; do
    if grep -r "$term" --include="*.py" --include="*.md" . > /dev/null 2>&1; then
        FOUND_TERMS=$((FOUND_TERMS + 1))
    fi
done

if [ $FOUND_TERMS -eq 0 ]; then
    echo "  ⚠️  WARNING: No SRS architectural terms found in code/docs"
    ISSUES=$((ISSUES + 1))
else
    echo "  ✅ Found $FOUND_TERMS/${#ARCH_TERMS[@]} SRS architectural terms"
fi

# Check 3: Verify specs/ directory exists and has key files
echo "  Checking specs/ directory structure..."
REQUIRED_SPECS=("specs/_meta.md" "specs/functional.md" "specs/technical.md")
MISSING_SPECS=0

for spec in "${REQUIRED_SPECS[@]}"; do
    if [ ! -f "$spec" ]; then
        echo "  ⚠️  WARNING: Missing required spec file: $spec"
        MISSING_SPECS=$((MISSING_SPECS + 1))
    fi
done

if [ $MISSING_SPECS -eq 0 ]; then
    echo "  ✅ All required spec files present"
else
    ISSUES=$((ISSUES + MISSING_SPECS))
fi

# Summary
echo ""
if [ $ISSUES -eq 0 ]; then
    echo "✅ Spec check passed!"
    exit 0
else
    echo "❌ Spec check found $ISSUES issue(s)"
    echo "   Review warnings above and ensure code aligns with specs/"
    exit 1
fi
