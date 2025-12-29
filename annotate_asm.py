#!/usr/bin/env python3
"""
Annotate assembly files with XDF parameter definitions
Adds comments to .asm files showing what tuning parameters are at each address
"""

import sys
import re
from pathlib import Path
from parse_xdf import XDFParser

def annotate_asm_file(asm_path, xdf_parser, output_path=None):
    """
    Annotate an assembly file with XDF definitions
    
    Args:
        asm_path: Path to input .asm file
        xdf_parser: XDFParser instance
        output_path: Path to output file (if None, prints to stdout)
    """
    if output_path is None:
        output_path = asm_path.parent / (asm_path.stem + '_annotated.asm')
    
    with open(asm_path, 'r') as f:
        lines = f.readlines()
    
    annotated_lines = []
    annotations_added = 0
    
    # Pattern to match address comments like [8D09h] or org directives
    addr_pattern = re.compile(r'\[([0-9A-Fa-f]+)h\]')
    org_pattern = re.compile(r'^\s*(?:;org|org)\s+([0-9A-Fa-f]+)h', re.IGNORECASE)
    
    for i, line in enumerate(lines):
        # Check for org directive
        org_match = org_pattern.match(line)
        if org_match:
            addr = org_match.group(1)
            definitions = xdf_parser.get_definitions_at_address('0x' + addr)
            if definitions:
                annotated_lines.append(f"; {'=' * 76}\n")
                for defn in definitions:
                    annotated_lines.append(f"; XDF: {defn['title']}\n")
                    if defn['type'] == 'table' and 'rows' in defn and 'cols' in defn:
                        annotated_lines.append(f";      Table: {defn['rows']}x{defn['cols']} elements\n")
                    if defn.get('units'):
                        annotated_lines.append(f";      Units: {defn['units']}\n")
                    if defn.get('equation'):
                        annotated_lines.append(f";      Equation: {defn['equation']}\n")
                annotated_lines.append(f"; {'=' * 76}\n")
                annotations_added += 1
        
        # Check for address in data comments
        addr_match = addr_pattern.search(line)
        if addr_match and 'db ' in line:
            addr = addr_match.group(1)
            definitions = xdf_parser.get_definitions_at_address('0x' + addr)
            
            # Only add annotation if we haven't seen this address yet
            if definitions and (i == 0 or addr_pattern.search(lines[i-1]) is None or 
                              addr_pattern.search(lines[i-1]).group(1) != addr):
                annotated_lines.append(f"\n; === XDF: Address 0x{addr.upper()} ===\n")
                for defn in definitions:
                    comment = f"; {defn['title']}"
                    if defn['type'] == 'table' and 'rows' in defn and 'cols' in defn:
                        comment += f" [{defn['rows']}x{defn['cols']}]"
                    if defn.get('units'):
                        comment += f" ({defn['units']})"
                    annotated_lines.append(comment + '\n')
                annotations_added += 1
        
        annotated_lines.append(line)
    
    # Write output
    with open(output_path, 'w') as f:
        f.writelines(annotated_lines)
    
    return annotations_added, output_path

def main():
    if len(sys.argv) < 3:
        print("Usage: annotate_asm.py <xdf_file> <asm_file> [output_file]")
        print()
        print("Annotates assembly file with XDF parameter definitions")
        print()
        print("Examples:")
        print("  annotate_asm.py TunerPro/m232.xdf decompiled/stock_AANABY_87c257.asm")
        print("  annotate_asm.py TunerPro/m232.xdf decompiled/stock_AANABY_87c257.asm output.asm")
        sys.exit(1)
    
    xdf_file = sys.argv[1]
    asm_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"Parsing XDF: {xdf_file}")
    xdf_parser = XDFParser(xdf_file)
    print(f"  Found {len(xdf_parser.tables)} tables, {len(xdf_parser.constants)} constants")
    print(f"  Mapped {len(xdf_parser.address_map)} unique addresses")
    print()
    
    print(f"Annotating: {asm_file}")
    asm_path = Path(asm_file)
    
    if output_file:
        output_path = Path(output_file)
    else:
        output_path = None
    
    count, out_path = annotate_asm_file(asm_path, xdf_parser, output_path)
    
    print(f"  Added {count} XDF annotations")
    print(f"  Output: {out_path}")
    print()
    print("Done!")

if __name__ == "__main__":
    main()
