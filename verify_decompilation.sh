#!/bin/bash
# Verification script for decompilation

echo "=== Decompilation Verification ==="
echo ""

# Check all bin files exist
echo "1. Checking source bin files..."
for file in ECU/stock_AANABY_27c512.bin ECU/stock_AANABY_87c257.bin ECU/bigturbo_WMI_27c512.bin ECU/bigturbo_WMI_87c257.bin; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists ($(stat -c%s "$file") bytes)"
    else
        echo "  ✗ $file MISSING"
        exit 1
    fi
done
echo ""

# Check all asm files exist
echo "2. Checking decompiled asm files..."
for file in decompiled/stock_AANABY_27c512.asm decompiled/stock_AANABY_87c257.asm decompiled/bigturbo_WMI_27c512.asm decompiled/bigturbo_WMI_87c257.asm; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        echo "  ✓ $file exists ($lines lines)"
    else
        echo "  ✗ $file MISSING"
        exit 1
    fi
done
echo ""

# Check for proper assembly syntax
echo "3. Checking assembly file structure..."
for file in decompiled/*.asm; do
    if grep -q "^RESET:" "$file" && grep -q "^end$" "$file"; then
        echo "  ✓ $(basename $file) has proper structure (RESET vector and end directive)"
    else
        echo "  ✗ $(basename $file) missing structure"
        exit 1
    fi
done
echo ""

# Check decompile script
echo "4. Checking decompile.py..."
if [ -x "decompile.py" ]; then
    echo "  ✓ decompile.py is executable"
else
    echo "  ✗ decompile.py is not executable"
    exit 1
fi
echo ""

# Check MCU definition
echo "5. Checking MCU definition..."
if [ -f "sab80c515.mcu" ]; then
    sfr_count=$(grep -c "^[A-Z0-9_]*\s\+SFR" sab80c515.mcu)
    echo "  ✓ sab80c515.mcu exists ($sfr_count SFR definitions)"
else
    echo "  ✗ sab80c515.mcu MISSING"
    exit 1
fi
echo ""

# Check documentation
echo "6. Checking documentation..."
for file in README.md decompiled/README.md DECOMPILATION_SUMMARY.md; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file MISSING"
        exit 1
    fi
done
echo ""

echo "=== All Verifications Passed ✓ ==="
echo ""
echo "To regenerate decompiled files: python3 decompile.py"
echo "To view assembly: less decompiled/stock_AANABY_87c257.asm"
echo "To compare tunes: diff -u decompiled/stock_AANABY_87c257.asm decompiled/bigturbo_WMI_87c257.asm"
