import typer
from main import main

def main_runner(filepath: str, id_type: str, organism_len: str, separator: str, additional: bool):
    out = main(filepath, id_type, organism_len, separator, additional)

    with open(f'{filepath[:-3]}.fas', 'w', encoding='UTF-8') as f:
        f.write(out)

if __name__ == "__main__":
    typer.run(main_runner)
