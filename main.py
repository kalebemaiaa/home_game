# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:40:49 2022

@author: b47133
"""
import sys, pygame

class Button():
    def __init__(self, texto, font):
        self.btn = font.render(texto, False, (255,255,255))
        self.ret_btn = self.btn.get_rect()
    
    def draw(self, superfice, position_x, position_y):
        self.ret_btn.x = position_x
        self.ret_btn.y = position_y
        self.superfice = superfice
        pygame.draw.rect(superfice, (0,0,0), self.ret_btn)
        superfice.blit(self.btn, self.ret_btn)
        
    def highlight(self):
        self.btn = pygame.transform.scale2x(self.btn)
        self.ret_btn.width = self.ret_btn.width * 2
        self.ret_btn.height = self.ret_btn.height * 2
        pygame.draw.rect(self.superfice, (170,70,50), self.ret_btn)
        self.superfice.blit(self.btn, self.ret_btn)

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
        self.tela = pygame.display.set_mode((self.width, self.heigth), pygame.FULLSCREEN, 32)
        
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
        btn_exit = Button("Sair", self.font_family)
        btn_play = Button("Play", self.font_family)
        
        self.list_btn = [btn_play, btn_exit]
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        
        for i in range(len(self.list_btn)):
            self.list_btn[i].draw(self.tela, 50 ,50 + i * 100)
            x_1, x_2 = self.list_btn[i].ret_btn.x, self.list_btn[i].ret_btn.width + self.list_btn[i].ret_btn.x
            y_1, y_2 = self.list_btn[i].ret_btn.y, self.list_btn[i].ret_btn.height + self.list_btn[i].ret_btn.y
            
            if self.mouse_x >= x_1 and self.mouse_x <= x_2 and self.mouse_y >= y_1 and self.mouse_y <= y_2:
                self.list_btn[i].highlight()
        
    def loop(self):
        while self.run:
            self.relogio.tick(64)
             
            for evento in  pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.run = False
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x_1, x_2 = self.list_btn[1].ret_btn.x, self.list_btn[1].ret_btn.width + self.list_btn[1].ret_btn.x
                    y_1, y_2 = self.list_btn[1].ret_btn.y, self.list_btn[1].ret_btn.height + self.list_btn[1].ret_btn.y
                    
                    if self.mouse_x >= x_1 and self.mouse_x <= x_2 and self.mouse_y >= y_1 and self.mouse_y <= y_2:
                        self.run = False
            self.tela.fill((122,122,0))
            
            #desenhando mouse
            x, y = pygame.mouse.get_pos()
            self.ret_mouse = self.cursor_mouse.get_rect()
            self.tela.blit(self.cursor_mouse, (x - self.ret_mouse.width / 2, y - self.ret_mouse.height / 2))
             
            self.menu_draw()
            pygame.display.flip()
        
        #rodado caso o jogo encerre
        pygame.display.quit()
        
G = Game()