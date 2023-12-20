from lexico import TipoToken as tt, Lexico
'''
# Nome Discente: Samuel Rodrigues Viana de Faria
# Matrícula: 0057497
# Data: 20/11/2023

# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias.

# Código responsável pela parte sintática do compilador, o mesmo funciona em conjunto com o Léxixo ao receber os Tokens formados 
# e utiliza de funções para representar sintaticamente o funcionamento da gramática a seguir:

P= {
    PROG → program id pvirg DECLS C-COMP
    DECLS → λ | var LIST-DECLS
    LIST-DECLS → DECL-TIPO D
    D → λ | LIST-DECLS
    DECL-TIPO → LIST-ID dpontos TIPO pvirg
    LIST-ID → id E
    E → λ | virg LIST-ID
    TIPO → int | real | bool | char
    C-COMP → abrech LISTA-COMANDOS fechach
    LISTA-COMANDOS → COMANDOS G
    G → λ | LISTA-COMANDOS
    COMANDOS → SE | ENQUANTO | LEIA | ESCREVA | ATRIBUICAO
    SE → if abrepar EXPR fechapar C-COMP H
    H → λ | else C-COMP
    ENQUANTO → while abrepar EXPR fechapar C-COMP
    LEIA → read abrepar LIST-ID fechapar pvirg
    ATRIBUICAO → id atrib EXPR pvirg
    ESCREVA → write abrepar LIST-W fechapar pvirg
    LIST-W → ELEM-W L
    L → λ | virg LIST-W
    ELEM-W → EXPR | cadeia
    EXPR → SIMPLES P
    P → λ | oprel SIMPLES
    SIMPLES → TERMO R
    R → λ | opad SIMPLES
    TERMO → FAT S
    S → λ | opmul TERMO
    FAT → id | cte | abrepar EXPR fechapar | true | false | opneg FAT
    }
'''
class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()

            self.tokenAtual = self.lex.getToken()

            self.PROG()
            self.consome(tt.FIMARQ)

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual( token ):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s", mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    # PROG → program id pvirg DECLS C-COMP
    def PROG(self):
        self.consome(tt.PROGRAM)
        self.consome(tt.ID)
        self.consome(tt.PVIRG)
        self.DECLS()
        self.CCOMP()

    # DECLS → λ | var LIST - DECLS
    def DECLS(self):
        if self.atualIgual(tt.VAR):
            self.consome(tt.VAR)
            self.LISTDECLS()
        else:
            pass

    # LIST - DECLS → DECL - TIPO D
    def LISTDECLS(self):
        self.DECLTIPO()
        self.D()

    # D → λ | LIST-DECLS
    def D(self):
        if self.atualIgual(tt.ID):
            self.LISTDECLS()
        else:
            pass

    # DECL-TIPO → LIST-ID dpontos TIPO pvirg
    def DECLTIPO(self):
        self.LISTID()
        self.consome(tt.DPONTOS)
        self.TIPO()
        self.consome(tt.PVIRG)

    # LIST-ID → id E
    def LISTID(self):
        self.consome(tt.ID)
        self.E()

    # E → λ | virg LIST-ID
    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LISTID()
        else:
            pass

    # TIPO → int | real | bool | char
    def TIPO(self):
        if self.atualIgual(tt.INT):
            self.consome(tt.INT)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        elif self.atualIgual(tt.BOOL):
            self.consome(tt.BOOL)
        elif self.atualIgual(tt.CHAR):
            self.consome(tt.CHAR)
        else:
            print(f'Erro sintático linha {self.tokenAtual.linha} era esperado {tt.INT}'
                  f'ou {tt.REAL} ou {tt.BOOL} ou {tt.CHAR}, mas veio " {self.tokenAtual.lexema} "')
            quit()

    # C-COMP → abrech LISTA-COMANDOS fechach
    def CCOMP(self):
        self.consome(tt.ABRECH)
        self.LISTACOMANDOS()
        self.consome(tt.FECHACH)

    # LISTA-COMANDOS → COMANDOS G
    def LISTACOMANDOS(self):
        self.COMANDOS()
        self.G()

    # G → λ | LISTA-COMANDOS
    def G(self):
        if self.atualIgual(tt.IF):
            self.LISTACOMANDOS()
        elif self.atualIgual(tt.WHILE):
            self.LISTACOMANDOS()
        elif self.atualIgual(tt.READ):
            self.LISTACOMANDOS()
        elif self.atualIgual(tt.WRITE):
            self.LISTACOMANDOS()
        elif self.atualIgual(tt.ID):
            self.LISTACOMANDOS()
        else:
            pass

    # COMANDOS → SE | ENQUANTO | LEIA | ESCREVA | ATRIBUICAO
    def COMANDOS(self):
        if self.atualIgual(tt.IF):
            self.SE()
        elif self.atualIgual(tt.WHILE):
            self.ENQUANTO()
        elif self.atualIgual(tt.READ):
            self.LEIA()
        elif self.atualIgual(tt.WRITE):
            self.ESCREVA()
        elif self.atualIgual(tt.ID):
            self.ATRIBUICAO()
        else:
            print(f'Erro sintático linha {self.tokenAtual.linha} era esperado {tt.IF}'
                  f'ou {tt.WHILE} ou {tt.READ} ou {tt.WRITE} ou {tt.ID}, mas veio " {self.tokenAtual.lexema} "')
            quit()

    # SE → if abrepar EXPR fechapar C-COMP H
    def SE(self):
        self.consome(tt.IF)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.CCOMP()
        self.H()

    # H → λ | else C-COMP
    def H(self):
        if self.atualIgual(tt.ELSE):
            self.consome(tt.ELSE)
            self.CCOMP()
        else:
            pass

    # ENQUANTO → while abrepar EXPR fechapar C-COMP
    def ENQUANTO(self):
        self.consome(tt.WHILE)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.CCOMP()

    # LEIA → read abrepar LIST-ID fechapar pvirg
    def LEIA(self):
        self.consome(tt.READ)
        self.consome(tt.ABREPAR)
        self.LISTID()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    # ATRIBUICAO → id atrib EXPR pvirg
    def ATRIBUICAO(self):
        self.consome(tt.ID)
        self.consome(tt.ATRIB)
        self.EXPR()
        self.consome(tt.PVIRG)

    # ESCREVA → write abrepar LIST-W fechapar pvirg
    def ESCREVA(self):
        self.consome(tt.WRITE)
        self.consome(tt.ABREPAR)
        self.LISTW()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    # LIST-W → ELEM-W L
    def LISTW(self):
        self.ELEMW()
        self.L()

    # L → λ | virg LIST-W
    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LISTW()
        else:
            pass

    # ELEM-W → EXPR | cadeia
    def ELEMW(self):
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
        elif self.atualIgual(tt.ID):
            self.EXPR()
        elif self.atualIgual(tt.CTE):
            self.EXPR()
        elif self.atualIgual(tt.ABREPAR):
            self.EXPR()
        elif self.atualIgual(tt.TRUE):
            self.EXPR()
        elif self.atualIgual(tt.FALSE):
            self.EXPR()
        elif self.atualIgual(tt.OPNEG):
            self.EXPR()
        else:
            print(f'Erro sintático linha {self.tokenAtual.linha} era esperado {tt.CADEIA}'
                  f' ou {tt.ID} ou {tt.CTE} ou {tt.ABREPAR} ou {tt.TRUE} ou {tt.FALSE}'
                  f' ou {tt.OPNEG}, mas veio " {self.tokenAtual.lexema} "')
            quit()

    # EXPR → SIMPLES P
    def EXPR(self):
        self.SIMPLES()
        self.P()

    # P → λ | oprel SIMPLES
    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL)
            self.SIMPLES()
        else:
            pass

    # SIMPLES → TERMO R
    def SIMPLES(self):
        self.TERMO()
        self.R()

    # R → λ | opad SIMPLES
    def R(self):
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD)
            self.SIMPLES()
        else:
            pass

    # TERMO → FAT S
    def TERMO(self):
        self.FAT()
        self.S()

    # S → λ | opmul TERMO
    def S(self):
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass

    # FAT → id | cte | abrepar EXPR fechapar | true | false | opneg FAT
    def FAT(self):

        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE)
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR)
            self.EXPR()
            self.consome(tt.FECHAPAR)
        elif self.atualIgual(tt.TRUE):
            self.consome(tt.TRUE)
        elif self.atualIgual(tt.FALSE):
            self.consome(tt.FALSE)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.FAT()
        else:
            print(f'Erro sintático linha {self.tokenAtual.linha} era esperado {tt.ID}'
                  f' ou {tt.CTE} ou {tt.ABREPAR} ou {tt.TRUE} ou {tt.FALSE}'
                  f' ou {tt.OPNEG}, mas veio " {self.tokenAtual.lexema} "')
            quit()


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo1.txt'

   lex = Lexico(nome)
   lex.abreArquivo()

   while (True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == tt.FIMARQ[0]:
           break
   lex.fechaArquivo()

   parser = Sintatico()
   parser.interprete(nome)
   print('O código fonte presente no arquivo escolhido foi compilado com SUCESSO!!!!')