#!/usr/bin/env python3
"""
Parse XDF file and extract tuning parameter definitions
Maps memory addresses to parameter names and metadata
"""

import xml.etree.ElementTree as ET
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class XDFParser:
    def __init__(self, xdf_path):
        self.xdf_path = Path(xdf_path)
        self.tree = ET.parse(xdf_path)
        self.root = self.tree.getroot()
        self.categories = {}
        self.tables = []
        self.constants = []
        self.address_map = {}  # address -> list of definitions
        
        self._parse_categories()
        self._parse_tables()
        self._parse_constants()
        self._build_address_map()
    
    def _parse_categories(self):
        """Parse category definitions"""
        for cat in self.root.findall('.//CATEGORY'):
            idx = cat.get('index')
            name = cat.get('name')
            if idx and name:
                self.categories[idx] = name
    
    def _parse_tables(self):
        """Parse table definitions"""
        for table in self.root.findall('.//XDFTABLE'):
            title = table.find('title')
            if title is None or not title.text:
                continue
            
            table_data = {
                'type': 'table',
                'title': title.text,
                'uniqueid': table.get('uniqueid'),
                'categories': [],
                'addresses': []
            }
            
            # Get categories
            for catmem in table.findall('CATEGORYMEM'):
                cat_idx = catmem.get('category')
                if cat_idx in self.categories:
                    table_data['categories'].append(self.categories[cat_idx])
            
            # Get addresses from all axes
            for axis in table.findall('.//XDFAXIS'):
                embedded = axis.find('EMBEDDEDDATA')
                if embedded is not None:
                    addr = embedded.get('mmedaddress')
                    if addr:
                        table_data['addresses'].append(addr)
                        
                        # Get size info
                        size_bits = embedded.get('mmedelementsizebits', '8')
                        row_count = embedded.get('mmedrowcount', '1')
                        col_count = embedded.get('mmedcolcount', '1')
                        
                        table_data['element_size'] = size_bits
                        table_data['rows'] = row_count
                        table_data['cols'] = col_count
            
            # Get units if available
            units_elem = table.find('.//units')
            if units_elem is not None and units_elem.text:
                table_data['units'] = units_elem.text
            
            self.tables.append(table_data)
    
    def _parse_constants(self):
        """Parse constant definitions"""
        for const in self.root.findall('.//XDFCONSTANT'):
            title = const.find('title')
            if title is None or not title.text:
                continue
            
            const_data = {
                'type': 'constant',
                'title': title.text,
                'uniqueid': const.get('uniqueid'),
                'categories': []
            }
            
            # Get categories
            for catmem in const.findall('CATEGORYMEM'):
                cat_idx = catmem.get('category')
                if cat_idx in self.categories:
                    const_data['categories'].append(self.categories[cat_idx])
            
            # Get address
            embedded = const.find('EMBEDDEDDATA')
            if embedded is not None:
                addr = embedded.get('mmedaddress')
                if addr:
                    const_data['address'] = addr
                    
                    # Get size info
                    size_bits = embedded.get('mmedelementsizebits', '8')
                    const_data['element_size'] = size_bits
            
            # Get units if available
            units_elem = const.find('.//units')
            if units_elem is not None and units_elem.text:
                const_data['units'] = units_elem.text
            
            # Get math equation if available
            math_elem = const.find('.//MATH')
            if math_elem is not None:
                equation = math_elem.get('equation')
                if equation:
                    const_data['equation'] = equation
            
            self.constants.append(const_data)
    
    def _normalize_address(self, addr: str) -> str:
        """Normalize address to standard format"""
        if not addr:
            return None
        # Remove 0x prefix if present and convert to uppercase
        addr = addr.replace('0x', '').replace('0X', '').upper()
        # Add 0x prefix
        return '0x' + addr
    
    def _build_address_map(self):
        """Build a map of addresses to all definitions at that address"""
        for table in self.tables:
            for addr in table.get('addresses', []):
                norm_addr = self._normalize_address(addr)
                if norm_addr:
                    if norm_addr not in self.address_map:
                        self.address_map[norm_addr] = []
                    self.address_map[norm_addr].append(table)
        
        for const in self.constants:
            addr = const.get('address')
            if addr:
                norm_addr = self._normalize_address(addr)
                if norm_addr:
                    if norm_addr not in self.address_map:
                        self.address_map[norm_addr] = []
                    self.address_map[norm_addr].append(const)
    
    def get_definitions_at_address(self, address: str) -> List[Dict]:
        """Get all definitions at a specific address"""
        norm_addr = self._normalize_address(address)
        return self.address_map.get(norm_addr, [])
    
    def format_definition(self, defn: Dict) -> str:
        """Format a definition as a readable string"""
        parts = []
        parts.append(f"{defn['type'].upper()}: {defn['title']}")
        
        if defn.get('categories'):
            parts.append(f"  Categories: {', '.join(defn['categories'])}")
        
        if defn['type'] == 'table':
            if 'rows' in defn and 'cols' in defn:
                parts.append(f"  Size: {defn['rows']}x{defn['cols']}")
        
        if defn.get('units'):
            parts.append(f"  Units: {defn['units']}")
        
        if defn.get('equation'):
            parts.append(f"  Equation: {defn['equation']}")
        
        return '\n'.join(parts)
    
    def get_all_addresses(self) -> List[str]:
        """Get all unique addresses sorted"""
        addresses = list(self.address_map.keys())
        # Sort by hex value
        addresses.sort(key=lambda x: int(x, 16))
        return addresses
    
    def print_summary(self):
        """Print summary of XDF contents"""
        print(f"XDF File: {self.xdf_path}")
        print(f"Categories: {len(self.categories)}")
        print(f"Tables: {len(self.tables)}")
        print(f"Constants: {len(self.constants)}")
        print(f"Unique addresses: {len(self.address_map)}")
        print()
        
        print("Categories:")
        for idx, name in sorted(self.categories.items(), key=lambda x: int(x[0], 16)):
            print(f"  {idx}: {name}")
        print()

def main():
    if len(sys.argv) < 2:
        print("Usage: parse_xdf.py <xdf_file>")
        sys.exit(1)
    
    xdf_file = sys.argv[1]
    parser = XDFParser(xdf_file)
    
    parser.print_summary()
    
    # Print all definitions sorted by address
    print("Definitions by Address:")
    print("=" * 80)
    for addr in parser.get_all_addresses():
        print(f"\n{addr}:")
        definitions = parser.get_definitions_at_address(addr)
        for defn in definitions:
            print(parser.format_definition(defn))
            print()

if __name__ == "__main__":
    main()
