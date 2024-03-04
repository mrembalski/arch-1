Example usage: 
```
python convert.py tests/MR_1.gp LOCUS S '|' False
```

```
python convert.py filepath id_type organism_len separator additional
```

Where: 
- id_type - LOCUS/GI
- organism_len - S/M/L for Homsap/H.sapiens/Homo sapiens equivalents 
- separator - FASTA separator
- additional - whether to add additional properties in the FASTA header (via [gp2fasta](https://gp2fasta.netmark.pl/)): 
    P -> PREDICTED
    s -> similar
    h -> hypothetical protein
    u -> unnamed protein product
    n -> novel
    p -> putative
    o -> open reading frame