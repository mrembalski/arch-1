import os

from main import main

gp_files = [f for f in os.listdir('tests/') if f.endswith('.gp')]

for gp_file in gp_files:
    output_file = f'tests/{gp_file}.fasta'

    with open(output_file, 'w', encoding='UTF-8') as f:
        f.write('')

    for id_type in ['GI', 'LOCUS']:
        for organism_len in ['L', 'M', 'S']:
            for additional in [True]:
                # append the output of main.py to output_file
                with open(output_file, 'a', encoding='UTF-8') as f:
                    f.write(main(f'tests/{gp_file}', id_type, organism_len, '-', additional))
