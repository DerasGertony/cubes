from perlin_noise import PerlinNoise
import pygame
import settings


class generation:
    def world(height=4, wd1=32, wd2=32, offset=0):
        info = 0
        blocks = []
        block_name = []
        pn = PerlinNoise(octaves=4)
        for x in range(wd1 + 1):
            for z in range(wd2 + 1):
                dy = int((pn([x / wd1, z / wd2]) + 0.6) * height)
                blocks.append([x - wd1 // 2, -dy - offset, z - wd2 // 2])
                block_name.append(0)
                for y in range(dy):
                    blocks.append([x - wd1 // 2, -y - offset, z - wd2 // 2])
                    block_name.append(1 if dy - y < 4 else 2)
        """blocks = []
        for i in range(27):
            blocks.append([i%3-1,(i//3)%3-1,i//9-1])"""
        # blocks = sorted(blocks, key = lambda x: x[1])
        normals = ((0, 0, -1), (-1, 0, 0), (0, -1, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0))
        visible = []
        pygame.init()
        height = 40
        if settings.fullscreen:
            info = pygame.display.Info()
            screen = pygame.display.set_mode([info.current_w, info.current_h])
            x, y = info.current_w // 2, info.current_h // 2
            width = info.current_w // 2
        else:
            screen = pygame.display.set_mode(settings.resolution)
            x, y = settings.resolution[0] // 2, settings.resolution[1] // 2
            width = settings.resolution[0] // 2
        x -= width // 2
        y -= height // 2
        for num, n in enumerate(blocks):
            f = []
            for i, j in enumerate(normals):
                if [n[0] + j[0], n[1] + j[1], n[2] + j[2]] not in blocks:
                    if n[1] == 0 and j[1] == 1:
                        continue
                    f.append(i)
            visible.append(f if f else [-1])
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        exit(0)
            screen.fill((255, 255, 255))
            percent = num / len(blocks)
            print(percent)
            pygame.draw.rect(
                screen, (100, 100, 100), (x, y, int(width * percent), height)
            )
            pygame.draw.rect(
                screen, (10, 10, 10), (x, y, int(width * percent), height), 1
            )
            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (x + int(width * percent), y, int(width * (1 - percent)), height),
            )
            pygame.display.update()
        if offset:
            for x in range(wd1 + 1):
                for z in range(wd2 + 1):
                    for y in range(offset):
                        blocks.append([x - wd1 // 2, y, z - wd2 // 2])
                        block_name.append(2 if y != 0 else 3)
                        visible.append([-1])
        return blocks, visible, block_name
        # return np.array(blocks), np.array(visible), np.array(block_name)
