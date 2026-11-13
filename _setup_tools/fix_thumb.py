import os

full_name = '3sHhEwTZsGe70E7LSQBGhnkJamAHbpmSyDR6VO4CIrsDexUPQtNRXf-5PZX9Z_viufGA-G78T_D78g7wNg_TdGPSL-URw2BYWuQQtb48T3k6cYm_9_Nx7orsJZ6_TU4sGxfEE1-DG_G4ejXU3SyPt1KY6rGMCyW_dGXXVqwubdQuWFOLvZMPE1fd4M0sbKbM'
for root, dirs, files in os.walk('.'):
    if 'raw_pages' in root:
        continue
    for f in files:
        if f.endswith('.php'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                txt = fh.read()
            if f'{full_name}-150x150.jpeg' in txt:
                txt = txt.replace(f'{full_name}-150x150.jpeg', f'{full_name}.jpeg')
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(txt)
                print(f"Fixed {fp}")

print("Fixed thumbnail reference.")
