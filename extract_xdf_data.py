#!/usr/bin/env python3
"""
Extract tuning data from binary files using XDF definitions
Creates readable CSV/text files for each table and constant
"""

import sys
import csv
from pathlib import Path
from parse_xdf import XDFParser

def read_binary_data(bin_path, address, size_bytes):
    """Read data from binary file at specified address"""
    with open(bin_path, 'rb') as f:
        f.seek(address)
        return f.read(size_bytes)

def extract_table_data(bin_path, xdf_parser, output_dir):
    """
    Extract all tables and constants from binary file using XDF definitions
    
    Args:
        bin_path: Path to binary file
        xdf_parser: XDFParser instance
        output_dir: Directory to write output files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    bin_path = Path(bin_path)
    
    extracted_count = 0
    
    # Extract tables
    for i, table in enumerate(xdf_parser.tables):
        if not table.get('addresses'):
            continue
        
        # Use first address (main data address)
        addr_str = table['addresses'][0]
        addr = int(addr_str, 16)
        
        title = table['title'].replace('/', '_').replace(' ', '_')
        title = ''.join(c for c in title if c.isalnum() or c in ('_', '-'))
        
        rows = int(table.get('rows', 1))
        cols = int(table.get('cols', 1))
        element_size = int(table.get('element_size', 8))
        bytes_per_element = element_size // 8
        
        total_bytes = rows * cols * bytes_per_element
        
        try:
            data = read_binary_data(bin_path, addr, total_bytes)
            
            # Write as CSV
            csv_path = output_dir / f"{title}_{addr_str}.csv"
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([f"# {table['title']}"])
                writer.writerow([f"# Address: {addr_str}"])
                writer.writerow([f"# Size: {rows}x{cols}"])
                if table.get('units'):
                    writer.writerow([f"# Units: {table['units']}"])
                writer.writerow([])
                
                # Data
                for row in range(rows):
                    row_data = []
                    for col in range(cols):
                        idx = (row * cols + col) * bytes_per_element
                        if bytes_per_element == 1:
                            value = data[idx]
                        elif bytes_per_element == 2:
                            value = int.from_bytes(data[idx:idx+2], 'big')
                        else:
                            value = int.from_bytes(data[idx:idx+bytes_per_element], 'big')
                        row_data.append(value)
                    writer.writerow(row_data)
            
            extracted_count += 1
            
        except Exception as e:
            print(f"  Warning: Could not extract table '{table['title']}' at {addr_str}: {e}")
    
    # Extract constants
    for i, const in enumerate(xdf_parser.constants):
        addr_str = const.get('address')
        if not addr_str:
            continue
        
        addr = int(addr_str, 16)
        
        title = const['title'].replace('/', '_').replace(' ', '_')
        title = ''.join(c for c in title if c.isalnum() or c in ('_', '-'))
        
        element_size = int(const.get('element_size', 8))
        bytes_per_element = element_size // 8
        
        try:
            data = read_binary_data(bin_path, addr, bytes_per_element)
            
            if bytes_per_element == 1:
                value = data[0]
            elif bytes_per_element == 2:
                value = int.from_bytes(data[0:2], 'big')
            else:
                value = int.from_bytes(data, 'big')
            
            # Write as text file
            txt_path = output_dir / f"{title}_{addr_str}.txt"
            with open(txt_path, 'w') as f:
                f.write(f"{const['title']}\n")
                f.write(f"Address: {addr_str}\n")
                f.write(f"Raw value: {value} (0x{value:X})\n")
                if const.get('units'):
                    f.write(f"Units: {const['units']}\n")
                if const.get('equation'):
                    f.write(f"Equation: {const['equation']}\n")
                    # Try to evaluate simple equations
                    try:
                        import math
                        # Simple substitution for common functions
                        eq = const['equation'].replace('X', str(value))
                        eq = eq.replace('SQR', 'math.sqrt')
                        calculated = eval(eq)
                        f.write(f"Calculated value: {calculated:.4f}\n")
                    except:
                        pass
            
            extracted_count += 1
            
        except Exception as e:
            print(f"  Warning: Could not extract constant '{const['title']}' at {addr_str}: {e}")
    
    return extracted_count

def main():
    if len(sys.argv) < 3:
        print("Usage: extract_xdf_data.py <xdf_file> <bin_file> [output_dir]")
        print()
        print("Extracts tuning data from binary file using XDF definitions")
        print()
        print("Examples:")
        print("  extract_xdf_data.py TunerPro/m232.xdf ECU/stock_AANABY_87c257.bin extracted_data")
        sys.exit(1)
    
    xdf_file = sys.argv[1]
    bin_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else 'extracted_data'
    
    print(f"Parsing XDF: {xdf_file}")
    xdf_parser = XDFParser(xdf_file)
    print(f"  Found {len(xdf_parser.tables)} tables, {len(xdf_parser.constants)} constants")
    print()
    
    print(f"Extracting data from: {bin_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    count = extract_table_data(bin_file, xdf_parser, output_dir)
    
    print()
    print(f"Successfully extracted {count} items")
    print(f"Output directory: {output_dir}")
    print()
    print("Done!")

if __name__ == "__main__":
    main()
