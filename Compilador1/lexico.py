from os import path
'''
# Nome Discente: Samuel Rodrigues Viana de Faria
# Matrícula: 0057497
# Data: 20/11/2023

# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias.

# Código responsável pela parte léxica do compilador, o mesmo funciona em conjunto com o Sintático percorrendo o arquivo
# formando e classificando os tokens, a cada token formado ele retorna o respectivo token e o lexema formado.
'''
class TipoToken:
    PROGRAM = (1, 'program')
    ID = (2, 'id')
    VAR = (3, 'var')
    INT = (4, 'int')
    REAL = (5, 'real')
    BOOL = (6, 'bool')
    CHAR = (7, 'char')
    ABREPAR = (8, '(')
    FECHAPAR = (9, ')')
    IF = (10, 'if')
    ABRECH = (11, '{')
    FECHACH = (12, '}')
    ELSE = (13, 'else')
    WHILE = (14, 'while')
    READ = (15, 'read')
    ATRIB = (16, '=')
    WRITE = (17, 'write')
    CADEIA = (18, 'cadeia')
    CTE = (19, 'cte')
    TRUE = (20, 'true')
    FALSE = (21, 'false')
    OPREL = (22, 'oprel')
    OPAD = (23, 'opad')
    OPMUL = (24, 'opmul')
    OPNEG = (25, 'opneg')
    PVIRG = (26, ';')
    VIRG = (27, ',')
    DPONTOS = (28, ':')
    FIMARQ = (29, 'fim-arquivo')
    ERROR = (30, 'error')

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha

class Lexico:
    # dicionario de palavras reservadas
    reservadas = {'write': TipoToken.WRITE,
                  'read': TipoToken.READ,
                  'program': TipoToken.PROGRAM,
                  'VAR': TipoToken.VAR,
                  'int': TipoToken.INT,
                  'real': TipoToken.REAL,
                  'bool': TipoToken.BOOL,
                  'char': TipoToken.CHAR,
                  'if': TipoToken.IF,
                  'else': TipoToken.ELSE,
                  'while': TipoToken.WHILE,
                  'false': TipoToken.FALSE,
                  'true': TipoToken.TRUE
                  }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    # Função que recebe o car atual e verifica se o
    # mesmo faz parte do alfabeto de caracteres não especiais.
    def is_alpha(self, c):
        return 'A' <= c <= 'Z' or 'a' <= c <= 'z'

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                elif self.is_alpha(car):
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif car in {'=', '<', '>',
                             '*', '!', ';', ':', ',',
                             '(', ')', '{', '}'}:
                    estado = 4
                elif car == '/':
                    # verifica a existencia de comentário em linha ou bloco
                    car = self.getChar()
                    if car == '/' or car == "*":
                        estado = 5
                    else:
                        self.ungetChar(car)
                        car = '/'
                        estado = 4
                elif car == '\"':
                    estado = 6
                elif car == '+' or car == '-':
                    # verifica a existencia de constante com operador de + ou - no ínicio
                    # [+-]?dígito
                    car2 = car
                    car = self.getChar()

                    if car.isdigit():
                        # [+-]digito
                        lexema = lexema + car2
                        estado = 3
                    else:
                        #[+-]
                        # caso não haja uma constante à direita do operador
                        # significa que é apenas um operador comum e não uma constante
                        # acompanhada de um operador à sua esquerda

                        self.ungetChar(car)
                        car = car2
                        estado = 4
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isalnum()):
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        # Condição que verifica o tamanho do ID antes de retorná-lo
                        # Caso ele seja maior que 32 retorno um erro
                        if len(lexema) > 32:
                            return Token(TipoToken.ERROR, lexema, self.linha)
                        return Token(TipoToken.ID, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                # Condição que garante que o numero que está sendo
                # formado possui no maximo um ponto flutuante
                # Caso o car seja outro ponto, retorno Token error
                if '.' in lexema and car == '.':
                    lexema = lexema + car
                    return Token(TipoToken.ERROR, lexema, self.linha)
                else:
                    if car != '.' and (car is None or (not car.isdigit())):
                        self.ungetChar(car)
                        return Token(TipoToken.CTE, lexema, self.linha)

            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == '=':
                    car = self.getChar()
                    if car == '=':
                        lexema = lexema + car
                        return Token(TipoToken.OPREL, lexema, self.linha)
                    else:
                        self.ungetChar(car)
                        return Token(TipoToken.ATRIB, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PVIRG, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.ABREPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.FECHAPAR, lexema, self.linha)
                elif car == '<':
                    car = self.getChar()
                    if car == '=' or car == '>':
                        lexema = lexema + car
                        return Token(TipoToken.OPREL, lexema, self.linha)
                    else:
                        self.ungetChar(car)
                        return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '>':
                    car = self.getChar()
                    if car == '=':
                        lexema = lexema + car
                        return Token(TipoToken.OPREL, lexema, self.linha)
                    else:
                        self.ungetChar(car)
                        return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '+':
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '-':
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '/':
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '!':
                    return Token(TipoToken.OPNEG, lexema, self.linha)
                elif car == ':':
                    return Token(TipoToken.DPONTOS, lexema, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == '{':
                    return Token(TipoToken.ABRECH, lexema, self.linha)
                elif car == '}':
                    return Token(TipoToken.FECHACH, lexema, self.linha)

            elif estado == 5:
                # consumindo comentário em bloco ou linha
                if car == "*":
                    while not car is None:
                        if car == '\n':
                            self.linha = self.linha + 1
                        car = self.getChar()
                        if car == '*':
                            car = self.getChar()
                            if car == '/':
                                break
                else:
                    while (not car is None) and (car != '\n'):
                        car = self.getChar()
                estado = 1
            elif estado == 6:
                # consumindo cadeia de caracteres
                lexema = lexema + car
                car = self.getChar()
                while car != '\"':
                    if car == '\n':
                        self.linha = self.linha + 1
                    if car is None:
                        return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                    lexema = lexema + car
                    car = self.getChar()
                lexema = lexema + car
                return Token(TipoToken.CADEIA, lexema, self.linha)