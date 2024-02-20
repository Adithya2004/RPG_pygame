import pygame
from support import import_folder
from random import choice
class AnimatePlayer:
    def __init__(self) -> None:
        self.frames = {
            'flame': import_folder('graphics/particles/flame/frames'),
            'heal':import_folder('graphics/particles/heal/frames'),
            'aura':import_folder('graphics/particles/aura'),

            'claw':import_folder('graphics/particles/claw'),
            'slash':import_folder('graphics/particles/slash'),
            'sparkle':import_folder('graphics/particles/sparkle'),
            'leaf_attack':import_folder('graphics/particles/leaf_attack'),
            'thunder':import_folder('graphics/particles/thunder'),


            'squid':import_folder('graphics/particles/smoke_orange'),
            'raccoon':import_folder('graphics/particles/raccoon'),
            'spirit':import_folder('graphics/particles/nova'),
            'bamboo':import_folder('graphics/particles/bamboo'),

            'leaf':(
                import_folder('graphics/particles/leaf1'),
                import_folder('graphics/particles/leaf2'),
                import_folder('graphics/particles/leaf3'),
                import_folder('graphics/particles/leaf4'),
                import_folder('graphics/particles/leaf5'),
                import_folder('graphics/particles/leaf6'),
                self.reflect_images(import_folder('graphics/particles/leaf1')),
                self.reflect_images(import_folder('graphics/particles/leaf2')),
                self.reflect_images(import_folder('graphics/particles/leaf3')),
                self.reflect_images(import_folder('graphics/particles/leaf4')),
                self.reflect_images(import_folder('graphics/particles/leaf5')),
                self.reflect_images(import_folder('graphics/particles/leaf6')),
            )
        }

    def reflect_images(self,frames):
        new_frame = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frame.append(flipped_frame)
        return new_frame

    def create_grass_particle(self,pos,group):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos,animation_frames,group)

    def create_particle(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups) -> None:
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect =self.image.get_rect(center = pos)
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
        
    def update(self):
        self.animate()
