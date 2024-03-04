import typer
import re
from typing import Optional

def format_organism(organism: str, organism_len: str) -> str:
    """
    Format the organism name based on the length.
    """
    # Homo sapiens  H.sapiens Homsap
    if organism_len == 'L':
        return organism

    first_part = organism.split(" ")[0]
    second_part = organism.split(" ")[1]

    if organism_len == 'M':
        return f"{first_part[0]}. {second_part}"

    return f"{first_part[:3]}{second_part[:3]}"


def main(filepath: str, id_type: str, organism_len: str, separator: str, additional: bool):
    """
    Convert GenBank file to FASTA format.

    Args:
        filepath (str): Path to the GenBank file.
        id_type (str): Type of ID to use. Can be 'LOCUS' or 'ID'.
        organism_len (str): Length of the organism name. Can be 'S' for short,
            'M' for medium, or 'L' for long.
        additional (bool): if True, an additional part will be added: 
            - additional information (via gp2fasta.netmark.pl):
                P -> PREDICTED
                s -> similar
                h -> hypothetical protein
                u -> unnamed protein product
                n -> novel
                p -> putative
                o -> open reading frame

    Returns:
        str: The content of the GenBank file in FASTA format.
    """
    assert id_type in ['LOCUS', 'GI'], 'id_type must be either LOCUS or ID'
    assert organism_len in ['S', 'M', 'L'], 'organism_len must be either S, M, or L'

    with open(filepath, 'r', encoding='UTF-8') as f:
        gb = f.readlines()

    output_file = ""

    # Parsing-related variables
    _id: Optional[str] = None
    organism: Optional[str] = None
    origin_started = False
    sequence = ''
    part_start = 0

    for idx, line in enumerate(gb):
        if line.startswith('//'):
            assert organism is not None

            # Get all lines from part_start to idx 
            part = gb[part_start:idx]
            additional_str = ''

            if additional:
                if re.search(r'hypothetical', ''.join(part), re.IGNORECASE):
                    additional_str += 'h'
                if re.search(r'predicted', ''.join(part), re.IGNORECASE):
                    additional_str += 'P'
                if re.search(r'unnamed', ''.join(part), re.IGNORECASE):
                    additional_str += 'u'
                if re.search(r'similar', ''.join(part), re.IGNORECASE):
                    additional_str += 's'
                if re.search(r'novel', ''.join(part), re.IGNORECASE):
                    additional_str += 'n'
                if re.search(r'putative', ''.join(part), re.IGNORECASE):
                    additional_str += 'p'
                if re.search(r'open reading frame', ''.join(part), re.IGNORECASE):
                    additional_str += 'o'

            output_file += f'>{format_organism(organism, organism_len)}{separator}{_id}{separator + additional_str if additional and additional_str != "" else ""}\n'
            output_file += sequence + '\n'

            _id = None
            organism = None
            origin_started = False
            sequence = ''
            part_start = idx

        is_organism = re.search(r'^\s*ORGANISM\s*(.*)$', line)
        if is_organism:
            organism = is_organism.group(1)


        if id_type == 'LOCUS':           
            is_id = re.search(fr'^{id_type}\s+(\w+)', line)
            if is_id:
                _id = is_id.group(1)
        else: # GI
            is_id = re.search(r'GI:(\d+)', line)
            if is_id:
                _id = is_id.group(1)

        if not origin_started:
            origin_started = line.startswith('ORIGIN')

        if origin_started:
            seq_parts = re.findall(r'^\s*\d+\s+([a-z\s]+)', line)
            seq_part = ''.join(seq_parts)
            seq_part = seq_part.replace(' ', '').replace('\n', '').upper()
            sequence += seq_part

    return output_file

if __name__ == "__main__":
    typer.run(main)
