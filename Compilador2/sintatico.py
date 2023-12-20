from lexico import TipoToken as tt, Lexico
from tabela import TabelaSimbolos
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

        # campos utilizados na tabela de símbolos
        self.saveTable = False
        self.tabsimb = TabelaSimbolos()
        self.listaID = []
        self.tipoID = ''

        # campos utilizados no modo pânico
        self.deuErro = False
        self.modoPanico = False
        self.tokensDeSincronismo = [tt.PVIRG, tt.FIMARQ, tt.ELSE, tt.WHILE,
                                    tt.READ, tt.WRITE, tt.IF, tt.FECHACH]
        self.follows = {
            'PROG': [tt.FIMARQ],
            'DECLS': [tt.ABRECH],
            'CCOMP': [tt.ID, tt.FECHACH, tt.IF, tt.ELSE, tt.WHILE, tt.READ, tt.WRITE],
            'LISTDECLS': [tt.ABRECH],
            'DECLTIPO': [tt.ID, tt.ABRECH],
            'D': [tt.ABRECH],
            'LISTID': [tt.DPONTOS, tt.FECHAPAR],
            'TIPO': [tt.PVIRG],
            'E': [tt.DPONTOS, tt.FECHAPAR],
            'LISTACOMANDOS': [tt.FECHACH],
            'COMANDOS': [tt.ID, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE],
            'G': [tt.FECHACH],
            'SE': [tt.ID, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE],
            'ENQUANTO': [tt.ID, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE],
            'LEIA': [tt.ID, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE],
            'ESCREVA': [tt.ID, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE],
            'ATRIBUICAO': [tt.ID, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE],
            'EXPR': [tt.PVIRG, tt.VIRG, tt.FECHAPAR],
            'H': [tt.ID, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE],
            'LISTW': [tt.FECHAPAR],
            'ELEMW': [tt.VIRG, tt.FECHAPAR],
            'L': [tt.FECHAPAR],
            'SIMPLES': [tt.PVIRG, tt.VIRG, tt.FECHAPAR, tt.OPREL],
            'P': [tt.PVIRG, tt.VIRG, tt.FECHAPAR],
            'TERMO': [tt.PVIRG, tt.VIRG, tt.FECHAPAR, tt.OPREL, tt.OPAD],
            'R': [tt.PVIRG, tt.VIRG, tt.FECHAPAR, tt.OPREL],
            'FAT': [tt.PVIRG, tt.VIRG, tt.FECHAPAR, tt.OPREL, tt.OPAD, tt.OPMUL],
            'S': [tt.PVIRG, tt.VIRG, tt.FECHAPAR, tt.OPREL, tt.OPAD]
        }

    def interprete(self, entrada):

        #Análise da entrada do usuário
        if (' ') in entrada:
            self.saveTable = True
            entrada = entrada.split(' ')
            if entrada[1] == '-t':
                nomeArquivoCod = entrada[0]
                nomeArquivoTable = entrada[2]
                self.saveTable = True
            else:
                print('Entrada Inválida.')
                quit()
        else:
            nomeArquivoCod = entrada

        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivoCod)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.tabsimb = TabelaSimbolos()
            self.PROG()
            self.consome(tt.FIMARQ, 'PROG')

            self.lex.fechaArquivo()

            # Criação do arquivo de tabela de símbolos
            if self.saveTable:
                with open(nomeArquivoTable, "w") as arquivo:
                    for tab in self.tabsimb.tabela:
                        arquivo.write(tab + " : " + self.tabsimb.tabela[tab] + "\n")

        return self.deuErro

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    # Procura do token de sincronismo
    def tokenEsperadoEncontrado(self, token):
        (const, msg) = token
        if self.tokenAtual.const == const:
            return True
        else:
            return False

    def consome(self, token, var):

        # Implementação do modo pânico
        if not self.modoPanico and self.tokenEsperadoEncontrado(token):
            self.tokenAtual = self.lex.getToken()
        elif not self.modoPanico:
            self.deuErro = True
            self.modoPanico = True
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s", mas veio "%s"'
            % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))

            # Verifica se o tokenAtual é um PVIRG
            # Caso seja, já encontrei o ponto de sincronismo
            # E desligo o modo pânico
            if token[0] == tt.PVIRG[0]:
                self.modoPanico = False
                return

            procuraTokenSincronismo = True

            # Junção dos tokens de sincronismo padrão: ; e eof
            # com os follows do não-terminal atual(var)
            tokensSinc = []
            tokensSinc.extend(self.follows[var])
            tokensSinc.extend(self.tokensDeSincronismo)

            while procuraTokenSincronismo:
                self.tokenAtual = self.lex.getToken()
                for tk in tokensSinc:
                    (const, msg) = tk
                    if self.tokenAtual.const == const:
                        # Token atual é um token de sincronismo
                        procuraTokenSincronismo = False
                        break
        elif self.tokenEsperadoEncontrado(token):
            # Ponto de sincronismo
            self.tokenAtual = self.lex.getToken()
            self.modoPanico = False
        else:
            # Prossegue a compilação do código
            pass

    # PROG → program id pvirg DECLS C-COMP
    def PROG(self):
        self.consome(tt.PROGRAM, 'PROG')
        self.consome(tt.ID, 'PROG')
        self.consome(tt.PVIRG, 'PROG')
        self.DECLS()
        self.CCOMP()

    # DECLS → λ | var LIST - DECLS
    def DECLS(self):
        if self.atualIgual(tt.VAR):
            self.consome(tt.VAR, 'DECLS')
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
        self.consome(tt.DPONTOS, 'DECLTIPO')
        self.TIPO()
        for i in self.listaID:
            self.tabsimb.declaraIdent(i, self.tipoID)
        self.consome(tt.PVIRG, 'DECLTIPO')
        self.listaID = []
        self.tipoID = ''

    # LIST-ID → id E
    def LISTID(self):
        self.listaID.append(self.tokenAtual.lexema)
        self.consome(tt.ID, 'LISTID')
        self.E()

    # E → λ | virg LIST-ID
    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG, 'E')
            self.LISTID()
        else:
            pass

    # TIPO → int | real | bool | char
    def TIPO(self):
        if self.atualIgual(tt.INT):
            self.consome(tt.INT, 'TIPO')
            self.tipoID = 'int'
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL, 'TIPO')
            self.tipoID = 'real'
        elif self.atualIgual(tt.BOOL):
            self.consome(tt.BOOL, 'TIPO')
            self.tipoID = 'bool'
        else:
            self.consome(tt.CHAR, 'TIPO')
            self.tipoID = 'char'


    # C-COMP → abrech LISTA-COMANDOS fechach
    def CCOMP(self):
        self.consome(tt.ABRECH, 'CCOMP')
        self.LISTACOMANDOS()
        self.consome(tt.FECHACH, 'CCOMP')

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
        else:
            self.ATRIBUICAO()


    # SE → if abrepar EXPR fechapar C-COMP H
    def SE(self):
        self.consome(tt.IF, 'SE')
        self.consome(tt.ABREPAR, 'SE')
        self.EXPR()
        self.consome(tt.FECHAPAR, 'SE')
        self.CCOMP()
        self.H()

    # H → λ | else C-COMP
    def H(self):
        if self.atualIgual(tt.ELSE):
            self.consome(tt.ELSE, 'H')
            self.CCOMP()
        else:
            pass

    # ENQUANTO → while abrepar EXPR fechapar C-COMP
    def ENQUANTO(self):
        self.consome(tt.WHILE, 'ENQUANTO')
        self.consome(tt.ABREPAR, 'ENQUANTO')
        self.EXPR()
        self.consome(tt.FECHAPAR, 'ENQUANTO')
        self.CCOMP()

    # LEIA → read abrepar LIST-ID fechapar pvirg
    def LEIA(self):
        self.consome(tt.READ, 'LEIA')
        self.consome(tt.ABREPAR, 'LEIA')
        self.LISTID()
        self.consome(tt.FECHAPAR, 'LEIA')
        self.consome(tt.PVIRG, 'LEIA')

    # ATRIBUICAO → id atrib EXPR pvirg
    def ATRIBUICAO(self):
        self.consome(tt.ID, 'ATRIBUICAO')
        self.consome(tt.ATRIB, 'ATRIBUICAO')
        self.EXPR()
        self.consome(tt.PVIRG, 'ATRIBUICAO')

    # ESCREVA → write abrepar LIST-W fechapar pvirg
    def ESCREVA(self):
        self.consome(tt.WRITE, 'ESCREVA')
        self.consome(tt.ABREPAR, 'ESCREVA')
        self.LISTW()
        self.consome(tt.FECHAPAR, 'ESCREVA')
        self.consome(tt.PVIRG, 'ESCREVA')

    # LIST-W → ELEM-W L
    def LISTW(self):
        self.ELEMW()
        self.L()

    # L → λ | virg LIST-W
    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG, 'L')
            self.LISTW()
        else:
            pass

    # ELEM-W → EXPR | cadeia
    def ELEMW(self):
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA, 'ELEMW')
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
        else:
            self.EXPR()


    # EXPR → SIMPLES P
    def EXPR(self):
        self.SIMPLES()
        self.P()

    # P → λ | oprel SIMPLES
    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL, 'P')
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
            self.consome(tt.OPAD, 'R')
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
            self.consome(tt.OPMUL, 'S')
            self.TERMO()
        else:
            pass

    # FAT → id | cte | abrepar EXPR fechapar | true | false | opneg FAT
    def FAT(self):

        if self.atualIgual(tt.FALSE):
            self.consome(tt.FALSE, 'FAT')
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE, 'FAT')
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR, 'FAT')
            self.EXPR()
            self.consome(tt.FECHAPAR, 'FAT')
        elif self.atualIgual(tt.TRUE):
            self.consome(tt.TRUE, 'FAT')
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG, 'FAT')
            self.FAT()
        else:
            self.consome(tt.ID, 'FAT')


if __name__== "__main__":

    entrada = input()
    parser = Sintatico()

    if not(parser.interprete(entrada)):
        print('O código fonte presente no arquivo escolhido foi compilado com SUCESSO!!!!')
    else:
        print('O código fonte presente no arquivo escolhido não foi compilado corretamente.')