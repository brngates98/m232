#!/bin/bash
# Annotate all assembly files with XDF labels

echo "=== Annotating All Assembly Files with XDF Labels ==="
echo ""

XDF_FILE="TunerPro/m232.xdf"

# Array of assembly files
ASM_FILES=(
    "decompiled/stock_AANABY_27c512.asm"
    "decompiled/stock_AANABY_87c257.asm"
    "decompiled/bigturbo_WMI_27c512.asm"
    "decompiled/bigturbo_WMI_87c257.asm"
)

# Annotate each file
for asm_file in "${ASM_FILES[@]}"; do
    if [ -f "$asm_file" ]; then
        output_file="${asm_file%.asm}_annotated.asm"
        echo "Annotating: $asm_file"
        echo "  Output: $output_file"
        
        python3 annotate_asm.py "$XDF_FILE" "$asm_file" "$output_file"
        
        if [ $? -eq 0 ]; then
            echo "  ✓ Success"
        else
            echo "  ✗ Failed"
        fi
        echo ""
    else
        echo "Warning: $asm_file not found"
        echo ""
    fi
done

echo "=== Annotation Complete ==="
echo ""
echo "Annotated files created in decompiled/ directory:"
ls -lh decompiled/*_annotated.asm
