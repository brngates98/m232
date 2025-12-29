#!/usr/bin/env python3
"""
Process ECU firmware with XDF definitions
Master script that can annotate assembly and extract data tables
"""

import sys
import argparse
from pathlib import Path
from parse_xdf import XDFParser
from annotate_asm import annotate_asm_file
from extract_xdf_data import extract_table_data

def main():
    parser = argparse.ArgumentParser(
        description='Process ECU firmware with XDF definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Annotate assembly with XDF labels
  %(prog)s --annotate TunerPro/m232.xdf decompiled/stock_AANABY_27c512.asm
  
  # Extract data tables from binary
  %(prog)s --extract TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin
  
  # Do both (using matching files)
  %(prog)s --all TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin decompiled/stock_AANABY_27c512.asm
        '''
    )
    
    parser.add_argument('xdf_file', help='XDF definition file (TunerPro format)')
    parser.add_argument('input_file', help='Binary (.bin) or assembly (.asm) file to process')
    parser.add_argument('asm_file', nargs='?', help='Assembly file (for --all mode)')
    
    parser.add_argument('--annotate', action='store_true',
                       help='Annotate assembly file with XDF labels')
    parser.add_argument('--extract', action='store_true',
                       help='Extract data tables from binary file')
    parser.add_argument('--all', action='store_true',
                       help='Do both annotation and extraction')
    
    parser.add_argument('--output-asm', metavar='FILE',
                       help='Output file for annotated assembly')
    parser.add_argument('--output-dir', metavar='DIR', default='xdf_extracted',
                       help='Output directory for extracted data (default: xdf_extracted)')
    
    args = parser.parse_args()
    
    # Determine mode
    if args.all:
        if not args.asm_file:
            print("Error: --all mode requires both binary and assembly files")
            print("Usage: process_xdf.py --all <xdf> <binary> <assembly>")
            sys.exit(1)
        do_annotate = True
        do_extract = True
        bin_file = args.input_file
        asm_file = args.asm_file
    elif args.annotate:
        do_annotate = True
        do_extract = False
        asm_file = args.input_file
        bin_file = None
    elif args.extract:
        do_annotate = False
        do_extract = True
        bin_file = args.input_file
        asm_file = None
    else:
        # Auto-detect based on file extension
        input_path = Path(args.input_file)
        if input_path.suffix.lower() == '.asm':
            do_annotate = True
            do_extract = False
            asm_file = args.input_file
            bin_file = None
        elif input_path.suffix.lower() == '.bin':
            do_annotate = False
            do_extract = True
            bin_file = args.input_file
            asm_file = None
        else:
            print("Error: Cannot determine mode from file extension")
            print("Please specify --annotate, --extract, or --all")
            sys.exit(1)
    
    # Parse XDF
    print(f"Loading XDF: {args.xdf_file}")
    xdf_parser = XDFParser(args.xdf_file)
    print(f"  Tables: {len(xdf_parser.tables)}")
    print(f"  Constants: {len(xdf_parser.constants)}")
    print(f"  Addresses: {len(xdf_parser.address_map)}")
    print()
    
    # Annotate assembly
    if do_annotate:
        print(f"Annotating assembly: {asm_file}")
        asm_path = Path(asm_file)
        output_path = Path(args.output_asm) if args.output_asm else None
        count, out_path = annotate_asm_file(asm_path, xdf_parser, output_path)
        print(f"  Annotations added: {count}")
        print(f"  Output file: {out_path}")
        print()
    
    # Extract data
    if do_extract:
        print(f"Extracting data from: {bin_file}")
        print(f"  Output directory: {args.output_dir}")
        count = extract_table_data(bin_file, xdf_parser, args.output_dir)
        print(f"  Items extracted: {count}")
        print()
    
    print("Complete!")

if __name__ == "__main__":
    main()
