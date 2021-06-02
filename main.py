from parser import analyze
from scanner import scan
from generate_scanner import create
from parsed_productions import analyze_productions

def main():
    print("archivo?")
    archivo = 'Double.ATG'
    input_file = open("./input/" + archivo)
    data = input_file.read()
    input_file.close()
    name, characters, keywords, tokens, productions = scan(data)
    analyze_productions(productions, tokens, keywords)
    final_dfa, dfas = analyze(name, characters, keywords, tokens)
    create(final_dfa, dfas, name)
    
if __name__ == "__main__":
    main()