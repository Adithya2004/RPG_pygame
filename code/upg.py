import pygame
from settings import *

class Upgrade:
    def __init__(self,player):
        self.display_surface= pygame.display.get_surface()
        self.player = player
        self.attributes_nr = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())

        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        self.height = self.display_surface.get_size()[1]*0.8
        self.width = self.display_surface.get_size()[0]//6
        self.create_items()

        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.can_move and self.selection_index<self.attributes_nr-1:
            self.selection_index+=1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            
        elif keys[pygame.K_LEFT] and self.can_move and self.selection_index>=1:
            self.selection_index-=1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            

        if keys[pygame.K_SPACE] and self.can_move:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.item_list[self.selection_index].trigger(self.player)
            
    def create_items(self):
        self.item_list = []
        for i,item in enumerate(range(self.attributes_nr)):
            top = self.display_surface.get_size()[1]*0.1
            full_width = self.display_surface.get_size()[0]
            increment = full_width//self.attributes_nr
            left = (i*increment) + (increment - self.width) //2
            item = Item(left,top,self.width,self.height,i,self.font)
            self.item_list.append(item)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if (current_time - self.selection_time)>=300:
                self.can_move = True
    
    def display(self):
        self.input()
        self.selection_cooldown()
        for index,item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    def display_names(self,surface,name,cost,selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        # Title Display
        title_surfface = self.font.render(name,False,color)
        title_rect = title_surfface.get_rect(midtop = self.rect.midtop+pygame.math.Vector2(0,20))
        # Cost Display
        cost_surfface = self.font.render(str(cost),False,color)
        cost_rect = cost_surfface.get_rect(midbottom = self.rect.midbottom+pygame.math.Vector2(0,-20))
        # Draw
        surface.blit(title_surfface,title_rect)
        surface.blit(cost_surfface,cost_rect)
    
    def display_bar(self,surface,value,max_value,selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        full_height = bottom[1]-top[1]
        relative_number = (value/max_value)*full_height
        value_rect = pygame.Rect(top[0]-15,bottom[1]-relative_number,30,10)

        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)

    def trigger(self,player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        if player.exp>=player.upgrade_costs[upgrade_attribute] and player.stats[upgrade_attribute]<=player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_costs[upgrade_attribute]
            if upgrade_attribute in ['health','energy']:
                player.stats[upgrade_attribute]+=10
            elif upgrade_attribute in ['speed','magic']:
                player.stats[upgrade_attribute]+=1
            else:
                player.stats[upgrade_attribute]+=2
            player.upgrade_costs[upgrade_attribute]=min(int(player.upgrade_costs[upgrade_attribute]*1.2),500)

    def display(self,surface,selection_num,name,value,max_value,cost):
        # Draw rectangle
        if self.index == selection_num:
            selected = True
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        else:
            selected = False
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        # Draw details inside rectangle
        self.display_names(surface,name,cost,selected)
        self.display_bar(surface,value,max_value,selected)