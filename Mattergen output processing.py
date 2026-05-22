import os
import re
from pymatgen.core import Structure, Lattice

# Input string containing all structures
#data = """Full Formula (Na1 Ce1 O2) Reduced Formula: NaCeO2 abc : 3.621799 3.625049 6.076167 angles: 72.335636 72.454106 59.999521 pbc : True True True Sites (4) # SP a b c --- ---- -------- -------- -------- 0 O 0.490362 0.122088 0.382507 1 O 0.967391 0.598324 0.954485 2 Na 0.728369 0.359601 0.670329 3 Ce 0.228393 0.859718 0.170194 Full Formula (Na2 Lu2 O2) Reduced Formula: NaLuO abc : 4.533363 4.531405 6.251353 angles: 111.196420 111.103552 90.018048 pbc : True True True Sites (6) # SP a b c --- ---- -------- -------- -------- 0 Lu 0.052794 0.194396 0.624485 1 Na 0.802732 0.444177 0.124284 2 Na 0.303199 0.944759 0.125206 3 O 0.551011 0.192416 0.621618 4 Lu 0.552001 0.694019 0.623605 5 O 0.054917 0.695349 0.627444"""
with open("structures.txt", "r", encoding="utf-8") as file:
    data = file.read()
# Output directory for CIF files
output_dir = "generated_cifs"
os.makedirs(output_dir, exist_ok=True)

# Split text based on "Full Formula" headers
blocks = re.split(r'(?=Full Formula)', data.strip())

for idx, block in enumerate(blocks):
    if not block.strip():
        continue
    
    try:
        # Extract metadata cleanly using regex whitespace indicators
        formula_match = re.search(r'Reduced Formula:\s*([A-Za-z0-9]+)', block)
        abc_match = re.search(r'abc\s*:\s*([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)', block)
        angles_match = re.search(r'angles\s*:\s*([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)', block)
        
        formula = formula_match.group(1) if formula_match else f"crystal_{idx}"
        
        # Parse Lattice parameters
        a, b, c = map(float, abc_match.groups())
        alpha, beta, gamma = map(float, angles_match.groups())
        lattice = Lattice.from_parameters(a, b, c, alpha, beta, gamma)
        
        # FIX: Find all occurrences of the pattern: index, element, x, y, z
        # Example target: "0 V 0.991396 0.520421 0.529853"
        # Regex explanation: \d+ (index), \s+ (spaces), [A-Za-z]+ (element), \s+ (spaces), and three decimal numbers
        site_pattern = r'\d+\s+([A-Za-z]+)\s+([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)'
        matches = re.findall(site_pattern, block)
        
        species = []
        coords = []
        
        for match in matches:
            el, x, y, z = match
            species.append(el)
            coords.append([float(x), float(y), float(z)])
        
        # CRITICAL CHECK: Ensure we actually extracted sites
        if not species:
            print(f"Skipping entry {idx} ({formula}) - No valid atomic sites parsed.")
            continue
            
        # Construct Structure object and write to CIF file
        structure = Structure(lattice, species, coords)
        filename = os.path.join(output_dir, f"gen_{idx}_{formula}.cif")
        structure.to(fmt="cif", filename=filename)
        print(f"Successfully wrote: {filename}")
        
    except Exception as e:
        print(f"Skipping block {idx} due to parsing error: {e}")
