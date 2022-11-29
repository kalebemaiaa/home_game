# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:40:49 2022

@author: b47133
"""
import pygame, json

def converte_cor(cor):
    if isinstance(cor,tuple):
        return cor
    color = cor.lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    return color

def desenha_bordas(ret, espessura):
    x,y,largura,altura = ret[0], ret[1], ret[2], ret[3]
    
    x_start, x_end = x - espessura, x + largura
    y_start, y_end = y - espessura, y + altura
    
    bordas_ret = [[x, y_start, largura, espessura], #borda up
              [x, y_end,largura, espessura], #borda down
              [x_start, y_start, espessura, altura + 2 * espessura], #borda left
              [x_end, y_start, espessura, altura + 2 * espessura] #bordar right
              ]
    
    return bordas_ret

def make_dialogo(texto, font, largura_maxima, altura_maxima, x, y, tela):
    lista_caracteres = [x for x in texto]
    
    linhas = []
    linha_atual = []
    while len(lista_caracteres) > 0:    
        linha_atual.append(lista_caracteres.pop(0))
        
        if font.size("".join(linha_atual))[0] > largura_maxima * .9:
            last_char = linha_atual[len(linha_atual)-1]
            first_char = lista_caracteres[0]
            
            if ((last_char >= 'a' and last_char <= 'z') or (last_char >= 'A' and last_char <= 'Z')) and ((first_char >= 'a' and first_char <= 'z') or (first_char >= 'A' and first_char <= 'Z')):
                linha_atual.append(" -")
                
            linhas.append("".join(linha_atual))
            if first_char == " " : lista_caracteres.pop(0)
                
            linha_atual = []
            
    pages = []
    tamanho_linha = font.size(linhas[0])[1] + 4
    altura_max = .8 * altura_maxima
    n_linhas = altura_max / tamanho_linha
    page = []
    
    while len(linhas) > 0:
        page.append(linhas.pop(0))
        if len(page) == int(n_linhas - 1):
            pages.append(page)
            page = []
            
    return pages

def importa_cores():
    cores = {}
    with open("./config/config.json", "r") as f:
        d = json.load(f)
        for cor in d["colors"]:
            cores[cor] = converte_cor(d["colors"][cor])
        
    return cores

class BoxText():
    def __init__(self, texto, fonte, action = None):
        self.conteudo_texto = texto
        self.acao = action
        self.font = fonte
        self.altura = 0
        self.largura = 0
        self.text_page = 0
        self.hovered_scale, self.hovered_color = False, False
        self.escala = 1
        
    #box_shadow é uma tupla ou lista onde o primeiro elemento é a quantidade no eixo x
    #o segundo é a quantidade no eixo y e o terceiro é a cor.
    #borda se refere a espessura
    def draw(self, surface, color, background_color, coordenada, box_shadow = None, borda = None):
        self.texto_renderizado = self.font.render(self.conteudo_texto, False, converte_cor(color))
        self.ret_text = self.texto_renderizado.get_rect()
        self.x = coordenada[0] 
        self.y = coordenada[1] 
        self.borda = borda
        self.box_shadow = box_shadow
        self.surface = surface
        self.color = color
        self.background_color = background_color
        self.x_text = [0, self.x + 20] #old x new
        self.y_text = [0, self.y + 20] #old x new
        
        if self.largura == 0 and self.altura == 0:
            self.largura = self.ret_text.width + 40
            self.altura = self.ret_text.height + 40
            self.x -= 20
            self.y -= 20
            
        
        self.ret_box = [self.x, self.y, self.largura, self.altura]
        
        if not box_shadow is None and borda is None:
            ret_box_shadow = [self.x + box_shadow[0], self.y + box_shadow[1], self.largura, self.altura]
    
            pygame.draw.rect(surface, converte_cor(box_shadow[2]), ret_box_shadow)
        
        if not borda is None:
            espessura = borda[0]
            
            self.bordas = desenha_bordas(self.ret_box, espessura)
        
            self.box_x, self.box_y, self.box_largura, self.box_altura = self.x - espessura, self.y - espessura, self.largura + espessura, self.altura + espessura
            self.borda_espessura = espessura
            
            if not box_shadow is None:
                ret_shadow = [self.x + box_shadow[0], self.y + box_shadow[1], self.box_largura, self.box_altura]
        
                pygame.draw.rect(surface, converte_cor(box_shadow[2]), ret_shadow)
            
            for ret in self.bordas:
                pygame.draw.rect(surface, converte_cor(borda[1]), ret)
                
        
        self.background_ret = pygame.draw.rect(surface, converte_cor(background_color), self.ret_box)
        
        if self.ret_text.width > self.largura:
            self.fonte_dialogo = pygame.font.Font("config/PressStart2p.ttf", 16)
            self.paginas_texto = make_dialogo(self.conteudo_texto,self.fonte_dialogo, self.largura,self.altura, self.x, self.y, self.surface)
            
            for i in range(len(self.paginas_texto[self.text_page])):
                row = self.fonte_dialogo.render(self.paginas_texto[self.text_page][i], False, converte_cor(self.color))
                self.surface.blit(row, (self.x + self.largura * .025, self.y + 10 + i * 25))
            
            
        else:
            dif_x = self.x  + (self.largura - self.ret_text.width)/2
            dif_y = self.y  + (self.altura - self.ret_text.height)/2
            surface.blit(self.texto_renderizado, (dif_x, dif_y))
        
    def hover(self, tipo: tuple):
        if self.hovered_color: return
        
        self.draw(self.surface, self.background_color, self.color, (self.x, self.y), self.box_shadow, self.borda)
        self.hovered_color = True
    
    def click(self):
        if self.action == "pass_text":
            if len(self.paginas_texto) - 1 == self.text_page: return
            self.text_page += 1
            self.draw(self.surface, self.color, self.background_color, (self.x, self.y), self.box_shadow, self.borda)

    def update_text(self, key_word, backspace):
        if backspace == True:    
            if len(self.conteudo_texto) == 0: return
            last_char = self.font.size(self.conteudo_texto[-1])
            
            wi, he = last_char[0], last_char[1]
    
            if self.y_text[0] < self.y:
                self.y_text[0] = self.y + 20
                self.x_text[0] = self.x + 20
    
            pygame.draw.rect(self.surface, (25,25,25), (self.x_text[0], self.y_text[0], wi, he))
            
            self.x_text[1] = self.x_text[0]
            self.y_text[1] = self.y_text[0]
            self.x_text[0] -= wi
            
            
            
            if self.x_text[0] < self.x + 20:
                self.x_text[0] = self.x + self.largura -int(self.largura / wi) - 20
                self.y_text[0] = self.y_text[1] - he
            
            self.conteudo_texto = self.conteudo_texto[:-1]
            
            
        else:
            letra_renderizada = self.font.render(key_word, False, converte_cor(self.color))
            
            wi, he = letra_renderizada.get_width(), letra_renderizada.get_height()
            
            self.surface.blit(letra_renderizada, (self.x_text[1], self.y_text[1]))
            
            self.x_text[0] = self.x_text[1]
            self.x_text[1] += wi
            self.y_text[0] = self.y_text[1]
            
            if self.x_text[1] + wi > self.largura + self.x:
                self.x_text[1] = self.x + 20
                self.y_text[1] += he
            
            self.conteudo_texto += key_word

class Box():
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura 

    def draw(self,surface, coordenada, background_color, centralizado = False, box_shadow = None, borda = None):
        self.x = coordenada[0] 
        self.y = coordenada[1]
        self.background_color = background_color
        tmp = 0

        if centralizado:
            self.x -= self.largura / 2
            self.y -= self.altura / 2

        ret_inside = [self.x, self.y, self.largura, self.altura]

        ret_bordas = []

        if not borda is None:
            espessura = borda[0]
            x_start, x_end = self.x - espessura, self.x + self.largura
            y_start, y_end = self.y - espessura, self.y + self.altura

            ret_bordas = [[x_start, y_start, espessura, self.altura + 2 * espessura],
                            [self.x, y_start, self.largura, espessura],
                            [self.x, y_end, self.largura, espessura],
                            [x_end, y_start, espessura, self.altura + 2 * espessura]]

            tmp = espessura

        if not box_shadow is None:
            x_bs, y_bs = box_shadow[0], box_shadow[1]
            ret_box_shadow = [self.x + x_bs, self.y + y_bs, self.largura + tmp, self.altura + tmp]

            pygame.draw.rect(surface, box_shadow[2], ret_box_shadow)
        
        pygame.draw.rect(surface, self.background_color, ret_inside)

        for ret in ret_bordas:
            pygame.draw.rect(surface, borda[1], ret)

class Text():
    def __init__(self, texto, font_family, font_size, color):
        self.font = pygame.font.Font(font_family , font_size)
        self.conteudo_texto = texto
        self.texto_renderizado = self.font.render(texto, False, color)
        self.rect = self.texto_renderizado.get_rect()

    def draw(self, surface, coordenada, text_shadow=None, background_color=None, centralizado=False, box_shadow=None, borda=None, padding = 5):
        if background_color is None:
            x, y = coordenada
            if centralizado:
                x = coordenada[0] - self.rect.width / 2
                y = coordenada[1] - self.rect.height / 2
            
            if not text_shadow is None:
                texto = self.font.render(self.conteudo_texto, False, text_shadow[2])
                surface.blit(texto, (x + text_shadow[0], y + text_shadow[1]))
            surface.blit(self.texto_renderizado, (x, y))
            return 

        box_bg = Box(self.rect.width + 2 * padding, self.rect.height + 2 * padding)
        box_bg.draw(surface=surface, coordenada=coordenada,background_color=background_color, centralizado=centralizado, box_shadow=box_shadow, borda=borda)
        
    
        x = box_bg.x + (box_bg.largura - self.rect.width) / 2 
        y = box_bg.y + (box_bg.altura - self.rect.height) / 2 

        if not text_shadow is None:
            texto = self.font.render(self.conteudo_texto, False, text_shadow[2])
            surface.blit(texto, (x + text_shadow[0], y + text_shadow[1]))

        surface.blit(self.texto_renderizado, (x, y))

class Game():
    def __init__(self):
        #starta pygame modulo
        
        pygame.init()
        #ajustando variáveis iniciais
        self.run = True
        self.width =1280
        self.heigth = 720
        
        self.lista_botoes = []
        self.componentes = []
        self.desenhada = False
        
        #importando ores
        self.colors = importa_cores()
        
        #ajusta variavel relogio
        self.relogio = pygame.time.Clock()
        
        #coloca tela
        self.tela = pygame.display.set_mode((self.width, self.heigth))
        
        #ajusta mouse
        # pygame.mouse.set_visible(False)
        # self.cursor_mouse = pygame.image.load("img/icon_mouse.png").convert()
        
        #ajusta fonte
        self.font_family = "config/PressStart2p.ttf"
        
        #coloca o titulo
        pygame.display.set_caption("Welcome")
        
        #abre tela
        pygame.display.update()
        
        #roda loop do jogo
        self.loop()
        
    def menu_draw(self, once = False):
        if once:
            start_btn = BoxText("start", self.font_family)
            config_btn = BoxText("config", self.font_family)
            exit_btn = BoxText("exit", self.font_family)
            
            self.lista_botoes.append(start_btn)
            self.lista_botoes.append(config_btn)
            self.lista_botoes.append(exit_btn)
        
        x, y = pygame.mouse.get_pos()
        
        for i in range(len(self.lista_botoes)):
            w_ = self.lista_botoes[i].font.size(self.lista_botoes[i].conteudo_texto)[0]
            self.lista_botoes[i].draw(self.tela, self.colors["azul_branco"], self.colors["violeta"], ((self.width / 2) - w_/2, 180 + i * 120), borda = (2, self.colors["powder_blue"]), box_shadow = (6, 6, self.colors["azul_depth"]))
        
    def dialogo_box(self, once = False):
        if once:
            fonte_dialogo = pygame.font.Font("config/PressStart2p.ttf", 20)
            caixa_dialogo = BoxText("Mais uma noite como todas as anteriores. Pego minha caneca de café cheia, acendo meu ultimo cigarro e corro pra velha janela do quarto. Observo a noite fria e chuvosa, até parece confortável por um momento, se não fossem as dezenas de preocupações que me desmotivam a cada dia. Penso em você, mesmo sabendo o quão longe está de mim, sinto aquele amor que continua a me desgraçar intensamente a cada dia, e penso quando enfim poderei te ter comigo. Sei lá, o café chega ao fim e trago a ultima ponta, nada muda. É como se eu fosse passar por isso mais uns longos anos a frente. Cada vez mais tenho a sensação de incertezas e inseguranças e tento me manter firme apesar disso. Algumas coisas parecem dar certo e maioria não, tipo você. Então após 10 minutos refletindo, largo tudo, fecho a janela e volto pro meu mundo dentro do quarto. Não sei até quando, não sei o porquê, só sei que tá tudo tão errado e quero me livrar disso o quanto antes. E tu não tem nem ideia do quanto, amor meu. Quero te ver de novo, poder te abraçar forte e fazer cara de quem tá nem aí contigo e fingir que nem lembrava de ti até te encontrar. Quero um encontro casual e trocar umas palavras impensadas, quem sabe relembrar aqueles momentos nossos, quem sabe te arrancar aquele sorriso que acho lindo. Quero saborear teu beijo, com desejo… Aquele mesmo que tive ao te ver me esperando na esquina da rua; e aquele frio no estômago que sentia de te ver tão perto e não poder tocar teu rosto. Quero reviver aquele dia no ônibus, em meio àquela sensação de impotência quando não arrisquei te beijar enquanto meu ponto se aproximava mas que você o fez, e ainda com esse jeitinho bobo e sarcástico, riu da situação e me fez ganhar meu dia. Quero você, te quero em meus braços. Quero passar uma tarde em um lugar qualquer perto de casa, te beijar na frente daqueles bobos que ainda se espantam com nossa paixão lésbica. Quero te ouvir me chamar de pequena e me irritar contigo enquanto tira meu cigarro da boca, joga no chão e amassa com o pé. Quero que pegue na minha mão na hora de voltar e diga que eu devia ter ficado mais tempo. Quero ver tua mensagem no dia seguinte dizendo que adorou me ver e quer de novo. Quero ouvir essa tua voz boba, tuas risadas debochadas e sorrir igual uma otária. Quero novamente despertar teu interesse em mim e fazer dos nossos encontros inesquecíveis. E por fim, quero parar de escrever esses textos de saudade e me inspirar numa realidade.", fonte_dialogo, action= "pass_text")
            caixa_dialogo.largura = self.width * .8
            caixa_dialogo.altura = self.heigth * .4
            self.lista_botoes.append(caixa_dialogo)
        
        self.lista_botoes[0].draw(self.tela, self.colors["pink_neon"], self.colors["preto_neon"], (self.width * .1, self.heigth * .55), borda = (3, self.colors["cinza_claro"]))
        
    def get_name(self, once = False):
        if once == True:
            label = BoxText("Digite seu nome", pygame.font.Font("config/PressStart2p.ttf",48))
            input_place = BoxText("", self.font_family, action = "show_text")
            input_place.largura = self.width * .7
            input_place.altura = self.heigth * .2
            self.componentes.append(label)
            self.componentes.append(input_place)
        w_ = label.font.size(label.conteudo_texto)[0]
        label.draw(self.tela, self.colors["rosa_choque"], self.colors["verde_agua"], (self.width/2 - w_/2, 200))
        
        input_place.draw(self.tela, self.colors["pink_neon"], self.colors["branco_comum"], (self.width/2 - input_place.largura / 2, self.heigth/2 ), borda = (3,self.colors["preto_neon"]))
        
    def short_menu(self, once = False):
        if once == True:
            container = BoxText("", self.font_family)
            container.largura, container.altura = self.width * .4, self.heigth * .8
            self.componentes.append(container)
        container.draw(self.tela, "#ffffff", self.colors["preto_neon"], (self.width/2 - container.largura/2, (self.heigth - container.altura)/2), borda = (3, converte_cor("#f0eeee")))
    
    def draw_cenario(self):
        # PS: se as bordas nao alterarem a largura e altura nao é preciso de dois bg_life
        bg_life= Box(self.width * .35, self.heigth * .05)
        x = (self.width * .05, self.width * .95 - bg_life.largura )
        y = self.heigth * .05
        bg_life.draw(coordenada = (x[0],y), surface = self.tela, background_color = self.colors["violeta"], borda = [5, self.colors["azul_depth"]])
        bg_life.draw(coordenada = (x[1],y), surface = self.tela, background_color = self.colors["violeta"], borda = [5, self.colors["azul_depth"]])
        life_p1 = Box(self.width * .2, self.heigth * .05)
        life_p2 = Box(self.width * .3, self.heigth * .05)
        life_p1.draw(coordenada = (x[0], y), surface = self.tela, background_color = self.colors["pink_neon"])
        life_p2.draw(coordenada = (x[1], y), surface = self.tela, background_color = self.colors["pink_neon"])

        self.componentes.append(life_p1)
        self.componentes.append(life_p2)

        texto_teste = Text("VS", self.font_family, font_size= 40, color = self.colors["preto_neon"])
        texto_teste.draw(self.tela, (self.width /2, self.heigth * .1), centralizado= True, text_shadow=[3,3, self.colors["coral"]] )

    def loop(self):
        while self.run:
            self.relogio.tick(12)
            x, y = pygame.mouse.get_pos()
            
            if not self.desenhada:
                self.background_color = self.colors["verde_agua"]
                self.tela.fill(self.background_color )
                #self.dialogo_box(once = True)    
                #self.menu_draw(once = True)
                #self.get_name(once = True)
                #self.short_menu(once = True)
                self.draw_cenario()

                pygame.display.flip()
                self.desenhada = True
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.run = False
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.lista_botoes:
                        if btn.x + btn.largura >= x >= btn.x and btn.y + btn.altura>= y >= btn.y:
                            btn.click()
                            
                if evento.type == pygame.KEYDOWN:
                    for btn in self.componentes:
                        if btn.action == "show_text":
                            backspace = False
                            if evento.unicode == "\x08":
                                backspace = True
                            btn.update_text(evento.unicode, backspace)
                
            # hover
            # for btn in self.lista_botoes:
            #     if btn.x + btn.largura >= x >= btn.x and btn.y + btn.altura>= y >= btn.y:
            #         btn.hover(("color", ))
                
            #     else:
            #         if btn.hovered_color == True:
            #             btn.hovered_color = False
            #             btn.hover(("color", ))
            #             btn.hovered_color = False
            pygame.display.flip()
        
        #rodado caso o jogo encerre
        pygame.display.quit()
        
g = Game()
