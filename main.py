# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:40:49 2022

@author: b47133
"""
import pygame

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

def make_dialogo(texto, font, allowed_width, x, y, tela):
    lista_caracteres = [x for x in texto]
    linhas = []
    linha_atual = []
    while len(lista_caracteres) > 0:    
        linha_atual.append(lista_caracteres.pop(0))
        
        if font.size("".join(linha_atual))[0] > allowed_width * .9:
            last_char = linha_atual[len(linha_atual)-1]
            first_char = lista_caracteres[0]
            
            if ((last_char >= 'a' and last_char <= 'z') or (last_char >= 'A' and last_char <= 'Z')) and ((first_char >= 'a' and first_char <= 'z') or (first_char >= 'A' and first_char <= 'Z')):
                linha_atual.append(" -")
                
            linhas.append("".join(linha_atual))
            if first_char == " " : lista_caracteres.pop(0)
                
            linha_atual = []
            
    for i in range(len(linhas)):
        font_surface = font.render(linhas[i], False, (255,255,255))
        tela.blit(font_surface, (x + 25, y + 10 + i* 30))
    

class BoxText():
    def __init__(self, texto, fonte, action = None):
        self.conteudo_texto = texto
        self.acao = action
        self.font = fonte
        self.altura = 0
        self.largura = 0
        
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
                
        
        pygame.draw.rect(surface, converte_cor(background_color), self.ret_box)
        
        if self.ret_text.width > self.largura:
            fonte_dialogo = pygame.font.Font("config/PressStart2p.ttf", 16)
            make_dialogo(self.conteudo_texto, fonte_dialogo, self.largura, self.x, self.y, self.surface)
        else:
            dif_x = self.x  + (self.largura - self.ret_text.width)/2
            dif_y = self.y  + (self.altura - self.ret_text.height)/2
            surface.blit(self.texto_renderizado, (dif_x, dif_y))
        
    def hover(self, tipo: tuple):
        if tipo[0] == "scale":
            largura, altura = int(self.largura * tipo[1]), int(self.altura * tipo[1])
            espessura = 0
            dif_x, dif_y = largura - self.largura, altura - self.altura 
            x, y = int(self.x - dif_x/2) , int(self.y - dif_y/2)
            ret_scale = [x, y, largura,altura]
            
            if not self.box_shadow is None:
                ret_box_shadow = [int(x + tipo[1] * self.box_shadow[0]), int(y + tipo[1]* self.box_shadow[1]), largura, altura]
        
                pygame.draw.rect(self.surface, converte_cor(self.box_shadow[2]), ret_box_shadow)
            
            pygame.draw.rect(self.surface, converte_cor(self.background_color), ret_scale)
            
            if not self.borda is None:
                espessura = int(self.borda_espessura * tipo[1])
            
                ret_bordas = desenha_bordas(ret_scale, espessura)
                
                for ret in ret_bordas:
                    pygame.draw.rect(self.surface, converte_cor(self.borda[1]), ret)
                
            fonte = pygame.font.Font("config/PressStart2p.ttf", int(32 * tipo[1]))
                
            texto_renderizado = fonte.render(self.conteudo_texto, False, converte_cor(self.color))
            ret = texto_renderizado.get_rect()
            largura_texto, altura_texto = ret.width, ret.height
                
            self.surface.blit(texto_renderizado, ( int(x + (largura - largura_texto)/2) , int(y + (altura - altura_texto)/2 )))
            
            self.x, self.y, self.largura, self.altura = x, y, largura, altura
        
        elif tipo[0] == "color":
            self.draw(self.surface, self.background_color, self.color, (self.x, self.y), self.box_shadow, self.borda)
    
    

class Game():
    def __init__(self):
        #starta pygame modulo
        pygame.init()
        #ajustando variáveis iniciais
        self.run = True
        self.width =1280
        self.heigth = 720
        
        #ajusta variavel relogio
        self.relogio = pygame.time.Clock()
        
        #coloca tela
        self.tela = pygame.display.set_mode((self.width, self.heigth))
        
        #ajusta mouse
        pygame.mouse.set_visible(False)
        self.cursor_mouse = pygame.image.load("img/icon_mouse.png").convert()
        
        #ajusta fonte
        self.font_family = pygame.font.Font("config/PressStart2p.ttf", 32)
        
        #coloca o titulo
        pygame.display.set_caption("Welcome")
        
        #abre tela
        pygame.display.update()
        
        #roda loop do jogo
        self.loop()
        
    def menu_draw(self):
        self.lista_botoes = []
        start_btn = BoxText("start", self.font_family)
        config_btn = BoxText("config", self.font_family)
        exit_btn = BoxText("exit", self.font_family)
        
        self.lista_botoes.append(start_btn)
        self.lista_botoes.append(config_btn)
        self.lista_botoes.append(exit_btn)
        
        x, y = pygame.mouse.get_pos()
        
        for i in range(len(self.lista_botoes)):
            self.lista_botoes[i].draw(self.tela, "#ffffff", "#c2c2c2", (self.width / 2, 100 + i * 120), borda = (3, "#00ff00"), box_shadow = (5, 5, "#ff00ff"))
        
        
            if self.lista_botoes[i].x + self.lista_botoes[i].largura >= x >= self.lista_botoes[i].x and self.lista_botoes[i].y + self.lista_botoes[i].altura>= y >= self.lista_botoes[i].y:
                self.lista_botoes[i].hover(("color", ))
                self.lista_botoes[i].hover(("scale", 1.2))
        
    def dialogo_box(self):
        fonte_dialogo = pygame.font.Font("config/PressStart2p.ttf", 20)
        caixa_dialogo = BoxText("Estou confiante de que a comida aqui me envenenou. É a única comida que comi nas últimas 24 horas que não consegui comer nos dias seguintes. Não se deixe enganar pelo anúncio de preço baixo. É sem gosto, menos do que limpo, e simplesmente mau! A comida não era de boa qualidade e era muito cara. No geral foi uma experiência muito ruim. Necessitamos da informação [X] para ir adiantando aspetos de execução no projeto. Lembramos que estamos a necessitar da revisão dos conteúdos [X] para completar a tarefa [Y]. Relembráramos que o texto [X] deve ser revisado e devolvido para podermos completar a fase [Y] do projeto.", fonte_dialogo)
        caixa_dialogo.largura = self.width * .8
        caixa_dialogo.altura = self.heigth * .4
        caixa_dialogo.draw(self.tela, "#ffffff", "#ff0000", (self.width * .1, self.heigth * .55), borda = (1, "#ffffff"))
        
    def loop(self):
        while self.run:
            self.relogio.tick(64)
             
            for evento in  pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.run = False
                
            self.tela.fill(converte_cor("#000000"))
             
            #self.menu_draw()
            #self.dialogo_box()
            
            #desenhando mouse
            x, y = pygame.mouse.get_pos()
            self.ret_mouse = self.cursor_mouse.get_rect()
            self.tela.blit(self.cursor_mouse, (x - self.ret_mouse.width / 2, y - self.ret_mouse.height / 2))
            
            pygame.display.flip()
        
        #rodado caso o jogo encerre
        pygame.display.quit()
        
g = Game()
