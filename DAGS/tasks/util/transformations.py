import re

def extrair_polegadas(nome):
    padrao = r'(\d{2,3})\s*(polegada|polegadas|[\"]{1,2})'
    match = re.search(padrao, nome, flags=re.IGNORECASE)
    return float(match.group(1)) if match else None

def extrair_marca(nome):
    marcas = ['Samsung', 'LG', 'TCL', 'Philips', 'AOC', 'Sony', 'Panasonic', 'Philco', 'Semp']
    for marca in marcas:
        if re.search(rf'\b{marca}\b', nome, flags=re.IGNORECASE):
            return marca
    return None

def extrair_painel(nome):
    tipos = ['OLED', 'QLED', 'LED', 'Crystal', 'Mini LED', 'NanoCell']
    for tipo in tipos:
        if re.search(rf'\b{tipo}\b', nome, flags=re.IGNORECASE):
            return tipo
    return None

def extrair_resolucao(nome):
    resolucoes = ['8K', '4K', 'Full HD', 'HD']
    for res in resolucoes:
        if re.search(rf'\b{res}\b', nome, flags=re.IGNORECASE):
            return res
    return None
