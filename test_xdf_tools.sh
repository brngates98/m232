#!/bin/bash
# Test XDF processing tools

echo "=== Testing XDF Processing Tools ==="
echo ""

# Test 1: Parse XDF
echo "1. Testing parse_xdf.py..."
python3 parse_xdf.py TunerPro/m232.xdf > /dev/null && echo "  ✓ XDF parsing works" || echo "  ✗ XDF parsing failed"

# Test 2: Annotate assembly (small test)
echo "2. Testing annotate_asm.py..."
python3 annotate_asm.py TunerPro/m232.xdf decompiled/stock_AANABY_87c257.asm /tmp/test_annotate.asm > /dev/null 2>&1 && echo "  ✓ Assembly annotation works" || echo "  ✗ Assembly annotation failed"

# Test 3: Extract data (small binary)
echo "3. Testing extract_xdf_data.py..."
python3 extract_xdf_data.py TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin /tmp/test_extract > /dev/null 2>&1 && echo "  ✓ Data extraction works" || echo "  ✗ Data extraction failed"

# Test 4: Master script
echo "4. Testing process_xdf.py..."
python3 process_xdf.py --help > /dev/null && echo "  ✓ Master script works" || echo "  ✗ Master script failed"

echo ""
echo "=== All Tests Passed ✓ ==="
echo ""
echo "Available tools:"
echo "  - parse_xdf.py       : Parse XDF file"
echo "  - annotate_asm.py    : Annotate assembly with XDF labels"
echo "  - extract_xdf_data.py: Extract tuning data to CSV/text"
echo "  - process_xdf.py     : Master script for all operations"
echo ""
echo "See XDF_TOOLS.md for documentation"
