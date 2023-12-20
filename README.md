# Simulador-de-Compilador
Implementação dos analisadores léxico, sintático e semântico para a linguagem de programação Z, dada pela gramática a seguir:</br>

P= {</br>
PROG → program id pvirg DECLS C-COMP</br>
DECLS → λ | var LIST-DECLS</br>
LIST-DECLS → DECL-TIPO D</br>
D → λ | LIST-DECLS</br>
DECL-TIPO → LIST-ID dpontos TIPO pvirg</br>
LIST-ID → id E</br>
E → λ | virg LIST-ID</br>
TIPO → int | real | bool | char</br>
C-COMP → abrech LISTA-COMANDOS fechach</br>
LISTA-COMANDOS → COMANDOS G</br>
G → λ | LISTA-COMANDOS</br>
COMANDOS → SE | ENQUANTO | LEIA | ESCREVA | ATRIBUICAO</br>
SE → if abrepar EXPR fechapar C-COMP H</br>
H → λ | else C-COMP</br>
ENQUANTO → while abrepar EXPR fechapar C-COMP</br>
LEIA → read abrepar LIST-ID fechapar pvirg</br>
ATRIBUICAO → id atrib EXPR pvirg</br>
ESCREVA → write abrepar LIST-W fechapar pvirg</br>
LIST-W → ELEM-W L</br>
L → λ | virg LIST-W</br>
ELEM-W → EXPR | cadeia</br>
EXPR → SIMPLES P</br>
P → λ | oprel SIMPLES</br>
SIMPLES → TERMO R</br>
R → λ | opad SIMPLES</br>
TERMO → FAT S</br>
S → λ | opmul TERMO</br>
FAT → id | cte | abrepar EXPR fechapar | true | false | opneg FAT}</br>
</br>
Mais informações de toda a implementação na descrição de cada Compiçador nos PDFs presentes no repositório principal.</br>
Cada compilador possui sua própria documentação anexada em seus respectivos diretórios.
