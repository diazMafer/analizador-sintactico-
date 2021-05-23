from parser import analyze
from scanner import scan
from generate_scanner import create

def main():
    print("archivo?")
    archivo = 'Aritmetica.atg'
    input_file = open("./input/" + archivo)
    data = input_file.read()
    input_file.close()
    name, characters, keywords, tokens, productions = scan(data)
    final_dfa, dfas = analyze(name, characters, keywords, tokens, productions)
    create(final_dfa, dfas, name)
    
if __name__ == "__main__":
    main()