import pygame
from settings import *
from random import randint
class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal':pygame.mixer.Sound('audio/heal.wav'),
            'flame':pygame.mixer.Sound('audio/Fire.wav'),
        }
    def heal(self,player,strength,cost,groups):
        if player.energy>=cost and player.health!=player.stats['health']:
            player.energy-=cost
            player.health+=strength
            if player.health>player.stats['health']:
                player.health = player.stats['health']
            self.sounds['heal'].play()
            self.animation_player.create_particle('heal',player.rect.center,groups)
            self.animation_player.create_particle('aura',player.rect.center,groups)
    def flames(self,player,strength,cost,groups):
        if player.energy>=cost:
            player.energy-=cost
            di = player.status.split('_')[0]
            if di == 'right':direction = pygame.math.Vector2(1,0)
            elif di == 'left':direction = pygame.math.Vector2(-1,0)
            elif di == 'up':direction = pygame.math.Vector2(0,-1)
            else:direction = pygame.math.Vector2(0,1)
            self.sounds['flame'].play()
            for i in range(1,6):
                offset_x = player.rect.centerx
                offset_y = player.rect.centery
                if direction.x:
                    offset_x +=direction.x *i*(TILESIZE//2) + randint(-TILESIZE//3,TILESIZE//3)
                else:
                    offset_y += direction.y*i*(TILESIZE//2) + randint(-TILESIZE//3,TILESIZE//3)
                self.animation_player.create_particle('flame',(offset_x,offset_y),groups)
            