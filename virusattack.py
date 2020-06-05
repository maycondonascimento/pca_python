# coding: utf-8
import pygame
import os
from random import choice, randint


DIR = os.getcwd()
FONT = DIR + "/fonts/ELEPHNT.TTF"

LARGURA = 800
ALTURA = 600

WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
SPRINGREEN = (0, 250, 154)
YELLOW = (255,255,0)
BLUE = (131,111,255)


class Edge(pygame.sprite.Sprite):
   
    def __init__(self, largura, altura, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((largura, altura))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
class Chefao(pygame.sprite.Sprite):

    def __init__(self, sprite, pos_x, pos_y, velocidade = 3.2):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
        self.velocidade = velocidade
    
    def update(self, *args):
        if (self.rect.x >= (LARGURA + 200)):
            self.kill()
        else:
            self.rect = self.rect.move(self.velocidade, 0)
            
            
class Virus(pygame.sprite.Sprite):

    def __init__(self, sprite, pos_x, pos_y, velocidade = 3):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = sprite.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.velocidade = velocidade
        
    def up_velocidade(self):
        self.velocidade += .5
    
    def dir_virosesabaixo(self):
        self.rect.y += 15

    def update(self, direction):
        self.rect = self.rect.move(self.velocidade * direction, 0)
    def laser(self):
        tiro = Tiro(self.rect.midtop, -1, velocidade = 5, color = GREEN)
        return tiro

    def __str__(self):
        return "Virus in (%s, %s)" % (self.rect.x, self.rect.y)
    
    
    
class Alcool(pygame.sprite.Sprite):
    
    def __init__(self, path, pos_x, pos_y, velocidade = 3):
        
        pygame.sprite.Sprite.__init__(self)
        self.__initial_position = (pos_x, pos_y)
        self.__image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.__image, (60, 60))
        self.rect = self.image.get_rect()
        self.velocidade = velocidade
        self.explosao_alcool = pygame.mixer.Sound(DIR + "/sons/explosaoalcool.wav")
        self.rect.y = pos_y
        self.rect.x = pos_x
        self.vidasalcool = 4
        self.__sound_shot = pygame.mixer.Sound(DIR + "/sons/laser.wav")
        

    
    def __str__(self):
        return "Alcool in (%s, %s)" % (self.rect.x, self.rect.y)
    
    

    def laser(self):
        self.__sound_shot.play()
        tiro = Tiro(self.rect.midtop, 5)
        return tiro

    def update(self, *args):
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.rect.right < (LARGURA - self.velocidade):
                self.rect.x += self.velocidade
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.rect.left > self.velocidade:
                self.rect.x -= self.velocidade

    def destruido(self):

        self.explosao_alcool.play()
        self.initial_position()
        self.vidasalcool -= 1
    
    def initial_position(self):

        self.rect.x = self.__initial_position[0]
        self.rect.y = self.__initial_position[1]



class Tiro(pygame.sprite.Sprite):

    def __init__(self, pos_xy, direction, color = GOLD, velocidade = 6):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_xy[0]
        self.rect.y = pos_xy[1]
        self.direction = direction
        self.velocidade = velocidade * direction

    def update(self, *args):

        self.rect.y -= self.velocidade
        if self.rect.bottom <= 0:
            self.kill()


class VirusAttack():

    def fontjogo(self, size):
        return pygame.font.Font(FONT, size)
    
    def __init__(self):
        
        self.pontuacao = 0
        self.level = 0
        self.velocidade = 0
        self.alcoolgel_lase = pygame.sprite.GroupSingle()
        self.invader_shot = pygame.sprite.Group()
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Vírus_Attack")        
        self.font = self.fontjogo(65)
        self.pontuacao_font = self.fontjogo(15)
        background_image = pygame.image.load(DIR + "/imagens/fundo.jpg")
        self.sexplosao = pygame.mixer.Sound(DIR + "/sons/explosaovirus.wav")
        self.path_image_alcoolgel = DIR + "/imagens/nave.png"
        vidasalcool_image = pygame.image.load(DIR + "/imagens/vida.png")
        imgexplosao = pygame.image.load(DIR + "/imagens/explosao.png")
        self.alcoolgel = pygame.sprite.GroupSingle(
                                Alcool(self.path_image_alcoolgel, (LARGURA - 50) // 2, 
                                        (ALTURA - 110)))
        self.alcoolgel_sprite = self.alcoolgel.sprites()[0]
        imgchefe = pygame.image.load(DIR + "/imagens/chefe1.png")
        self.imgchefe = pygame.transform.scale(imgchefe, [60, 40])
        self.chefoes = pygame.sprite.GroupSingle(
                                Chefao(self.imgchefe, self.posicaoalt(), 15))
        self.background = pygame.transform.scale(background_image, (LARGURA, ALTURA))
        self.vidasalcool_image = pygame.transform.scale(vidasalcool_image, (25, 25))
        self.imgexplosao = pygame.transform.scale(imgexplosao, (
                                    (LARGURA // 10), (LARGURA // 10)))
        self.clock = pygame.time.Clock()
        self.viroses = pygame.sprite.OrderedUpdates()
        self.viroses_direction = 1
        self.increment_velocidade = False
        
        self.left_edge = pygame.sprite.GroupSingle(Edge(5, ALTURA, 0, 0))
        self.right_edge = pygame.sprite.GroupSingle(Edge(5, ALTURA, 795, 0))
        self.bottom_edge = pygame.sprite.GroupSingle(Edge(LARGURA, 5, 0, 560))
        self.groups = pygame.sprite.Group(self.alcoolgel_lase, self.invader_shot, 
                                    self.viroses, self.chefoes)

    
    def tnivel(self):

        self.level += 1
        
            
        if (self.level > 1 and self.level < 6):
            self.velocidade += 0.5
            
            
        elif (self.level == 1):
            self.velocidade += 1
        
        font = self.fontjogo(100)
        text = font.render('NIVEL: ' + str(self.level), True, YELLOW)
        self.time = pygame.time.get_ticks()

        while ((pygame.time.get_ticks() - self.time) < 1500):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.window.blit(self.background, [0, 0])
            self.window.blit(text, [(LARGURA - 510) // 2, 220])
            pygame.display.update()
            
    def posicaoalt(self):

        return choice([-1700, -1900, -2200, -2500, -1500])       
            
    def telainicial(self):
        telainic = True
        
        text = self.font.render("  VÍRUS ATTACK", True, YELLOW)
        self.font = self.fontjogo(16)
        btiniciar = self.font.render(" ENTER : INICIAR ", True, WHITE, None)
        btsair = self.font.render("   ESC : SAIR      ", True, WHITE, None)
        btiniciar_rect = btiniciar.get_rect(center = (LARGURA // 2, ALTURA - 100))
        btsair_rect = btsair.get_rect(center = ((LARGURA + 15) // 2, ALTURA - 50))
        
        chefoes = pygame.image.load(DIR + "/imagens/virusinicial.png")
        chefoes = pygame.transform.scale(chefoes, [110, 60])
        velocidade = [-1, 1]
        movimento_chefoes = chefoes.get_rect(center = (LARGURA -200, ALTURA - 400))

        self.window.fill(BLACK)
        self.window.blit(text, [(LARGURA - 620) // 2, 50])
        self.window.blit(btiniciar, btiniciar_rect)
        self.window.blit(btsair, btsair_rect)
        pygame.display.update()

        while telainic:
            
            movimento_chefoes.left = 345
            
            if movimento_chefoes.left < 0 or movimento_chefoes.right > 500:
                velocidade[0] = -velocidade[0]
            if movimento_chefoes.top < 150 or movimento_chefoes.bottom > 400:
                velocidade[1] = -velocidade[1]
            
            movimento_chefoes.y += velocidade[1]
            movimento_chefoes.x += velocidade[0]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.iniciajogo()
                        return True

                    if event.key == pygame.K_ESCAPE:
                        return False

            self.window.fill(BLACK)
            self.window.blit(chefoes, movimento_chefoes)
            self.window.blit(text, [(LARGURA - 620) // 2, 50])
            self.window.blit(btiniciar, btiniciar_rect)
            self.window.blit(btsair, btsair_rect)
            self.clock.tick(60)
            pygame.display.update()
    
    
    
    
    
    def telafinal(self):

        self.telafimdejogo()

        self.font35 = self.fontjogo(35)
        self.font20 = self.fontjogo(20)

        tpontosfinal = self.font35.render("PONTUAÇÃO FINAL: %d" % self.pontuacao, True, GOLD)
        tjogonovo = self.font20.render("PRESSIONE ENTER PARA JOGAR NOVAMENTE", True, WHITE)
        tsair = self.font20.render("PRESSIONE ESC PARA SAIR", True, GOLD)

        tpontosfinal_rect = tpontosfinal.get_rect(center = (LARGURA // 2, ALTURA - 350))
        tjogonovo_rect = tjogonovo.get_rect(center = (LARGURA // 2, ALTURA - 100))
        tsair_rect = tsair.get_rect(center = (LARGURA // 2, ALTURA - 40))

        self.window.fill(BLUE)
        self.window.blit(tpontosfinal, tpontosfinal_rect)
        self.window.blit(tjogonovo, tjogonovo_rect)
        self.window.blit(tsair, tsair_rect)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.level = 0
                        self.velocidade = 0
                        self.alcoolgel = pygame.sprite.GroupSingle(
                                Alcool(self.path_image_alcoolgel, (LARGURA) // 2, (ALTURA - 110)))
                        self.alcoolgel_sprite = self.alcoolgel.sprites()[0]
                        self.iniciajogo()
                        return
						
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
        
    

    def iniciajogo(self):
        self.groups.add(self.alcoolgel)
        self.viroses_direction = 1
        self.viroses.empty()
        self.chefoes.empty()
        self.invader_shot.empty()
        self.alcoolgel_lase.empty()
        self.tnivel()
        self.iniciavirus()
        self.alcoolgel_sprite.initial_position()
        self.update()
	
    def telafimdejogo(self):

        font = self.fontjogo(80)
        text = font.render('FIM DE JOGO', True, BLUE)
        time = pygame.time.get_ticks()

        while ((pygame.time.get_ticks() - time) < 2500):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.window.blit(self.background, [0, 0])
            self.window.blit(text, [(LARGURA - 610) // 2, 220])
            pygame.display.update()

    def iniciavirus(self):

        tvirus = []

        for i in range(1, 8):
            tvirus.append(pygame.image.load(DIR + ("/imagens/virus%d.png" % (i % 3))))
        x = 25
        #10
        for j in range(10):
            y = 60
            #6
            for i in range(6):
                sprite = pygame.transform.scale(tvirus[i], 
                                ((LARGURA // 20), (LARGURA // 20)))
                self.viroses.add(Virus(sprite, x, y, self.velocidade))
                y += 45
            x += 62
            


    def mostravidas(self):
        y = 10
        for i in range(self.alcoolgel_sprite.vidasalcool):
            self.window.blit(self.vidasalcool_image, (y, 570))
            y += 40

    def laservirus(self):
        evirus = [i for i in self.viroses]
        
        for i in range(2):
            invader = choice(evirus)
            self.invader_shot.add(invader.laser())
            
            
    

    def update(self):
        pontuacao = self.pontuacao_font.render("PONTOS: %d" % self.pontuacao, True, WHITE)

        current_time = pygame.time.get_ticks()

        if (current_time % 1500.0 < 20):
            self.laservirus()
        
        if ((len(self.chefoes) == 0)):
            self.chefoes.add(Chefao(self.imgchefe, self.posicaoalt(), 15))

        self.window.blit(self.background, [0, 0])
        self.window.blit(pontuacao, (LARGURA - 150, ALTURA - 30))
        self.groups.draw(self.window)

        self.groups.update(self.viroses_direction)
        self.dir_viroses()
        self.bateu()
        self.mostravidas()

        self.groups = pygame.sprite.Group(self.alcoolgel, self.alcoolgel_lase, self.invader_shot, self.viroses, 
                                    self.left_edge, self.bottom_edge, self.right_edge, self.chefoes)
        self.clock.tick(60)
        pygame.display.update()
    
    def bateu(self):

        if pygame.sprite.groupcollide(self.alcoolgel_lase, self.invader_shot, True, True):
            self.pontuacao += randint(5, 20)
        pygame.sprite.groupcollide(self.invader_shot, self.bottom_edge, True, False)
        
        if pygame.sprite.groupcollide(self.alcoolgel, self.viroses, False, False):
            self.alcoolgel_sprite.destruido()
        
        if pygame.sprite.groupcollide(self.chefoes, self.alcoolgel_lase, True, True):
            self.pontuacao += choice([25, 35])
            self.sexplosao.play()
        
        for atingidos in pygame.sprite.groupcollide(self.alcoolgel_lase, self.viroses, True, True).values():
            for invasor in atingidos:
                self.sexplosao.play()
                self.window.blit(self.imgexplosao, (invasor.rect.x, invasor.rect.y))
                self.pontuacao += choice([10, 20, 25])
        
        if pygame.sprite.groupcollide(self.alcoolgel, self.invader_shot, False, True):
            self.sexplosao.play()
            self.window.blit(self.imgexplosao, (self.alcoolgel_sprite.rect.x, self.alcoolgel_sprite.rect.y))
            self.alcoolgel_sprite.destruido()  

    def dir_viroses(self):
        mostravir = self.viroses.sprites()
        first = mostravir[0]
        last = mostravir[-1]
        
        if ((last.rect.x > (LARGURA - last.rect.width - 10)) or (first.rect.x < 10)):
            self.viroses_direction *= -1
            current_time = pygame.time.get_ticks()
            if (current_time - self.time > (3000 // self.velocidade)):
                self.dir_virosesabaixo(mostravir)
    
    def dir_virosesabaixo(self, mostravir):
        up_velocidade = (len(self.viroses) <= 8)

        for evirus in mostravir:
            if up_velocidade:
                evirus.up_velocidade()
            evirus.dir_virosesabaixo()

    

    def main(self):

        jogando = True
        telainic = True
        
        while telainic:
            command = self.telainicial()

            if not command:
                telainic = False
                pygame.quit()
                exit()
        
            while jogando:
                if self.alcoolgel_sprite.vidasalcool <= 0:
                    self.telafinal()
                    self.pontuacao = 0
                elif len(self.viroses) == 0:
                    self.iniciajogo()
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            jogando, telainic = False, False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                jogando, telainic = False, False
                            if ((event.key == pygame.K_UP or event.key == pygame.K_SPACE) and not self.alcoolgel_lase):
                                self.alcoolgel_lase.add(self.alcoolgel_sprite.laser())

                    self.update()




if __name__ == "__main__":
    pygame.init()
    pygame.mixer.pre_init(22050, -16, 2, 1024)
    pygame.mixer.init(22050, -16, 2, 1024)
    game = VirusAttack()
    game.main()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.quit()
