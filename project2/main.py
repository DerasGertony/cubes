impimport pygame
from pygame.locals import *

# pip install PyOpenGL PyOpenGL_accelerate
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, radians
import settings
import numpy as np
from generation import generation
from time import time
import pygame_widgets
from pygame_widgets.textbox import TextBox


class game:
    def __init__(self, n, surf, name):
        self.vertices = (
            (0.5, -0.5, -0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, 0.5),
            (0.5, 0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (-0.5, 0.5, 0.5),
        )
        # surfaces paired with normals
        self.surfaces = (
            (3, 2, 7, 6),
            (4, 0, 3, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (0, 1, 2, 3),
        )
        # beta[[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255]]
        # 0-grass[[139,69,19],[139,69,19],[0,255,0],[139,69,19],[139,69,19],[139,69,19]]
        # 1-dirt[[50,24,17],[50,24,17],[50,24,17],[50,24,17],[50,24,17],[50,24,17]]
        # 2-stone[[128,128,128],[128,128,128],[128,128,128],[128,128,128],[128,128,128],[128,128,128]]
        # 3-custom[[0,38,41],[0,38,41],[0,38,41],[0,38,41],[0,38,41],[0,38,41]]
        self.normals = (
            (0, 0, -1),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, 1),
            (1, 0, 0),
            (0, 1, 0),
        )
        self.edges = [
            [(3, 2), (3, 6), (2, 7), (6, 7)],
            [(0, 3), (0, 4), (3, 6), (4, 6)],
            [(4, 5), (4, 6), (5, 7), (6, 7)],
            [(0, 1), (0, 4), (1, 5), (4, 5)],
            [(1, 2), (1, 5), (2, 7), (5, 7)],
            [(0, 1), (0, 3), (1, 2), (2, 3)],
        ]
        self.edges2 = (
            (3, 0),
            (3, 2),
            (3, 6),
            (5, 1),
            (5, 4),
            (5, 7),
            (0, 1),
            (0, 4),
            (1, 2),
            (2, 7),
            (4, 6),
            (6, 7),
        )
        pygame.init()
        if settings.fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode(
                [info.current_w, info.current_h], DOUBLEBUF | OPENGL
            )
            prop = info.current_w / info.current_h
        else:
            self.screen = pygame.display.set_mode(
                settings.resolution, DOUBLEBUF | OPENGL
            )
            prop = settings.resolution[0] / settings.resolution[1]
        GL_TEXTURE_3D
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
        self.sphere = gluNewQuadric()
        glMatrixMode(GL_PROJECTION)
        gluPerspective(max(min(settings.FOV, 120), 80), prop, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, 1, 0, 0, 0, 0, 0, 0, 1)
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLoadIdentity()
        glClearColor(0, 0.5, 1, 1)
        self.displayCenter = [self.screen.get_size()[i] // 2 for i in range(2)]
        self.mouseMove = [0, 0]
        pygame.mouse.set_pos(self.displayCenter)
        # fixlater pygame.time.set_timer(pygame.USEREVENT, 100)
        self.vert_angle = 0.0
        self.paused = False
        self.run = True
        self.reset = 0
        self.clock = pygame.time.Clock()
        self.gravity = 1 / 25
        self.jumpspeed = -0.1
        self.vert_speed = -0.1
        self.world = n
        self.visible = surf
        self.bl_name = name
        self.cur = self.world[self.visible != -1]
        self.cur_visible = self.visible[self.visible != -1]
        self.cur_name = self.bl_name[self.visible != -1]
        self.pos = [0, 0, 0, 0]
        self.colors = [
            [
                [139, 69, 19],
                [139, 69, 19],
                [0, 255, 0],
                [139, 69, 19],
                [139, 69, 19],
                [139, 69, 19],
            ],
            [
                [50, 24, 17],
                [50, 24, 17],
                [50, 24, 17],
                [50, 24, 17],
                [50, 24, 17],
                [50, 24, 17],
            ],
            [
                [128, 128, 128],
                [128, 128, 128],
                [128, 128, 128],
                [128, 128, 128],
                [128, 128, 128],
                [128, 128, 128],
            ],
            [
                [0, 128, 128],
                [0, 128, 128],
                [0, 128, 128],
                [0, 128, 128],
                [0, 128, 128],
                [0, 128, 128],
            ],
            [
                [255, 0, 0],
                [0, 255, 0],
                [0, 0, 255],
                [255, 255, 0],
                [0, 255, 255],
                [255, 0, 255],
            ],
        ]
        self.colors = [[[k / 255 for k in j] for j in i] for i in self.colors]
        self.timer = time()
        self.loop()

    def loop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.USEREVENT:
                    pass
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.run = False
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                        pygame.mouse.set_cursor(0)
                        pygame.mouse.set_pos(self.displayCenter)
                if not self.paused and event.type == pygame.MOUSEMOTION:
                    self.mouseMove = [
                        event.pos[i] - self.displayCenter[i] for i in range(2)
                    ]
                    pygame.mouse.set_pos(self.displayCenter)
            if self.paused and not self.reset:
                self.paused = False
                pass
            if self.reset == 60:
                self.reset = 0
                self.paused = True
            if not self.paused:
                pygame.mouse.set_cursor(
                    (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)
                )
                self.screen.fill(pygame.Color(0, 255, 255))
                keypress = pygame.key.get_pressed()
                # init model view matrix
                glLoadIdentity()
                # apply the look up and down
                self.vert_angle += self.mouseMove[1]
                if self.vert_angle > 90:
                    self.vert_angle = 90
                if self.vert_angle < -90:
                    self.vert_angle = -90
                glRotatef(self.vert_angle, 1.0, 0.0, 0.0)
                # init the view matrix
                glPushMatrix()
                glLoadIdentity()
                # apply the movement
                mov = [0, 0, 0]
                if keypress[pygame.K_w]:
                    mov[2] += 0.08
                if keypress[pygame.K_s]:
                    mov[2] -= 0.08
                if keypress[pygame.K_d]:
                    mov[0] -= 0.08
                if keypress[pygame.K_a]:
                    mov[0] += 0.08
                if mov[0] != 0 and mov[2] != 0:
                    mov[0] /= 2 ** 0.8
                    mov[2] /= 2 ** 0.8
                if keypress[pygame.K_LSHIFT]:
                    mov[2] *= 1.6
                    mov[0] *= 1.6
                self.pos[3] += self.mouseMove[0]
                ix, iz, iy = round(self.pos[0]), round(self.pos[2]), int(self.pos[1])
                g = self.cur
                g = g[np.logical_and(g[::, 0] == ix, g[::, 2] == iz)]
                dt = [self.pos[0], self.pos[2]]
                dt[0] -= mov[0] * sin(radians(self.pos[3])) + mov[2] * cos(
                    radians(self.pos[3])
                )
                dt[1] -= mov[2] * sin(radians(self.pos[3])) - mov[0] * cos(
                    radians(self.pos[3])
                )
                # collision
                self.pos[0] = dt[0]
                self.pos[2] = dt[1]
                try:
                    g = sorted(g, key=lambda x: x[1])[0]
                except IndexError:
                    g = [ix, 0, iz]
                    # g = [0, iz, 0]
                    # self.pos[0] = 0
                    # self.pos[1] = iz
                    # self.pos[2] = 0
                idy = self.world[
                    np.logical_and(self.world[::, 0] == ix, self.world[::, 2] == iz)
                ][::, 1]
                if iy - 1 in idy or iy - 2 in idy:
                    self.vert_speed += -0.1
                elif -1e-4 < self.pos[1] - iy < 1e-4 and iy in idy:
                    self.vert_speed = 0
                else:
                    self.vert_speed = min(
                        self.vert_speed + self.gravity, abs(g[1] - self.pos[1]) / 1.3
                    )
                if (
                    keypress[pygame.K_SPACE]
                    and -1e-2 < self.pos[1] - iy < 1e-2
                    and iy in idy
                    and iy - 3 not in idy
                ):
                    self.vert_speed = 4.2 * self.jumpspeed - self.gravity
                if abs(self.vert_speed) > 0.7:
                    self.vert_speed = self.vert_speed / abs(self.vert_speed) * 0.7
                mov[1] = self.vert_speed
                self.pos[1] += mov[1]
                glTranslate(*mov)
                glRotatef(self.mouseMove[0], 0.0, 1.0, 0.0)
                glColor4f(0, 0.5, 0, 0.1)
                glMultMatrixf(self.viewMatrix)
                self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
                # apply view matrix
                glPopMatrix()
                glMultMatrixf(self.viewMatrix)
                glLightfv(GL_LIGHT0, GL_POSITION, [-0.5, 1, -0.5, 0])
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glPushMatrix()
                glTranslatef(0, 1, -2)
                dt = np.logical_and(
                    np.logical_and(
                        self.visible != -1, abs(self.world[::, 0] - g[0]) < 6
                    ),
                    abs(self.world[::, 2] - g[2]) < 6,
                )
                self.cur = self.world[dt]
                self.cur_visible = self.visible[dt]
                self.cur_name = self.bl_name[dt]
                for j, i in enumerate(self.cur):
                    glTranslatef(i[2], i[0], -i[1])
                    if -1 not in self.cur_visible[j]:
                        self.Cube(self.cur_visible[j], self.colors[self.cur_name[j]])
                    glTranslatef(-i[2], -i[0], i[1])
                for i in (1, 2, 3):
                    view_pos = [
                        round(
                            self.pos[0]
                            - cos(radians(self.pos[3]))
                            * round(i + int(self.pos[0] - self.pos[0]))
                            * cos(radians(self.vert_angle))
                        ),
                        round(self.pos[1] - 2 + i * sin(radians(self.vert_angle))),
                        round(
                            self.pos[2]
                            - sin(radians(self.pos[3]))
                            * round(i + int(self.pos[2] - self.pos[2]))
                            * cos(radians(self.vert_angle))
                        ),
                    ]
                    try:
                        view = self.cur[
                            np.logical_and(
                                np.logical_and(
                                    self.cur[::, 0] == view_pos[0],
                                    self.cur[::, 2] == view_pos[2],
                                ),
                                self.cur[::, 1] == view_pos[1],
                            )
                        ][0]
                    except IndexError:
                        continue
                    glTranslatef(view_pos[2], view_pos[0], -view_pos[1])
                    self.square()
                    glTranslatef(-view_pos[2], -view_pos[0], view_pos[1])
                    if len(view):
                        if pygame.mouse.get_pressed()[0] and not self.mouse[0]:
                            self.delete_surface(view)
                            dt = np.logical_or(
                                np.logical_or(
                                    self.world[::, 0] != view_pos[0],
                                    self.world[::, 2] != view_pos[2],
                                ),
                                self.world[::, 1] != view_pos[1],
                            )
                            self.visible = self.visible[dt]
                            self.bl_name = self.bl_name[dt]
                            self.world = self.world[dt]
                        elif pygame.mouse.get_pressed()[2] and not self.mouse[2]:
                            g = [
                                view[0] - self.pos[0],
                                view[1] - self.pos[1] + 2,
                                view[2] - self.pos[2],
                            ]
                            n = sorted([0, 1, 2], key=lambda x: -abs(g[x]))
                            view[n[0]] -= int(np.sign(g[n[0]]))
                            if (
                                view[1]
                                not in self.world[
                                    np.logical_and(
                                        self.world[::, 0] == view[0],
                                        self.world[::, 2] == view[2],
                                    )
                                ][::, 1].tolist()
                            ):
                                self.bl_name = np.append(self.bl_name, [3])
                                self.world = np.vstack([self.world, view])
                                self.update_surface(view)
                    break
                glPopMatrix()
                self.draw_crosshair()
                self.mouse = pygame.mouse.get_pressed()
                self.reset += 1
                pygame.display.flip()
            if self.pos[1] > 2:
                self.timer = time() - self.timer
                break
            self.clock.tick(62)
            # print(f'fps:{self.clock.get_fps()}')
        else:
            bl, vis, bl_name = self.world, self.visible, self.bl_name
            with open(settings.load_path, "wt") as file:
                file.write(
                    "\n".join(
                        [
                            ",".join(
                                [str(j) for j in bl[i]]
                                + [str(j) for j in vis[i]]
                                + [str(bl_name[i])]
                            )
                            for i in range(len(bl))
                        ]
                    )
                )
            pygame.quit()
            exit(0)
        self.draw_win()
        exit(0)

    def delete_surface(self, coord):
        for i, j in enumerate(self.normals):
            dt = [coord[0] + j[0], coord[1] + j[1], coord[2] + j[2]]
            try:
                g = np.logical_and(
                    np.logical_and(
                        self.world[::, 0] == dt[0], self.world[::, 2] == dt[2]
                    ),
                    self.world[::, 1] == dt[1],
                )
                if -1 in self.visible[g.tolist().index(True)]:
                    self.visible[g.tolist().index(True)] = []
                self.visible[g.tolist().index(True)] = self.visible[g].tolist()[0] + [
                    (i + 3) % 6
                ]
            except ValueError:
                continue

    def update_surface(self, coord):
        f = []
        for i, j in enumerate(self.normals):
            dt = [coord[0] + j[0], coord[1] + j[1], coord[2] + j[2]]
            try:
                g = np.logical_and(
                    np.logical_and(
                        self.world[::, 0] == dt[0], self.world[::, 2] == dt[2]
                    ),
                    self.world[::, 1] == dt[1],
                )
                n = self.visible[g.tolist().index(True)]
                if len(n) == 1:
                    self.visible[g.tolist().index(True)] = [-1]
                else:
                    n.remove((i + 3) % 6)
                    self.visible[g.tolist().index(True)] = n
                self.visible[g.tolist().index(True)]
            except ValueError:
                f.append(i)
        self.visible = np.array(self.visible.tolist() + [f])

    def Cube(self, visible, color):
        glBegin(GL_QUADS)
        for i_surface, surface in enumerate(self.surfaces):
            if i_surface not in visible:
                continue
            glNormal3fv(
                self.normals[(i_surface + 3) % 6]
            )  # set the normal vector the vertices of the surface
            glColor3f(*color[i_surface])
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def square(self):
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        for edge in self.edges2:
            for index in edge:
                glVertex3fv(self.vertices[index])
        glEnd()

    def draw_win(self):
        pygame.quit()
        pygame.init()
        pygame.mouse.set_cursor(0)
        win = pygame.display.set_mode(settings.resolution)
        seed = "set" if settings.load else "random"
        run = True
        win.fill((255, 255, 255))
        font = pygame.font.Font("mine.ttf", 20)
        text_coord = 30
        string_rendered = font.render(f"Any% {seed} seed speedrun time: {self.timer:.4f}", 1, pygame.Color("green"))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        win.blit(string_rendered, intro_rect)
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        run = False
            pygame.display.update()
            

    def draw_crosshair(self):
        height = self.screen.get_height()
        width = self.screen.get_width()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_COLOR_LOGIC_OP)
        glLogicOp(GL_INVERT)
        glTranslatef(width / 2 - 10, height / 2 - 10, 0)
        glLineWidth(2)
        glBegin(GL_LINES)
        glColor3f(1, 1, 1)
        glVertex3f(10, 20, 0)
        glVertex3f(10, 0, 0)
        glVertex3f(0, 10, 0)
        glVertex3f(20, 10, 0)
        glEnd()
        glDisable(GL_COLOR_LOGIC_OP)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glMatrixMode(GL_MODELVIEW)

    """def Cube(self, sides):
        glBegin(GL_QUADS)
        for i_surface, surface in enumerate(self.surfaces):
            if i_surface not in sides:
                continue
            glNormal3fv(self.normals[i_surface]) # set the normal vector the vertices of the surface
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glBegin(GL_LINES)
        glColor3f(0,0,255)
        for edge in self.edges:
            for index in edge:
                glVertex3fv(self.vertices[index])
        glEnd()"""


def main():
    if settings.load:
        with open(settings.load_path) as file:
            f = file.read().split("\n")
            bl, vis, bl_name = [], [], []
            for i in f:
                d = list(map(int, i.split(",")))
                bl.append(d[:3])
                vis.append(d[3:-1])
                bl_name.append(d[-1])
    else:
        bl, vis, bl_name = generation.world(*settings.world_params)
        with open(settings.load_path, "wt") as file:
            file.write(
                "\n".join(
                    [
                        ",".join(
                            [str(j) for j in bl[i]]
                            + [str(j) for j in vis[i]]
                            + [str(bl_name[i])]
                        )
                        for i in range(len(bl))
                    ]
                )
            )
    game(np.array(bl), np.array(vis), np.array(bl_name))


if __name__ == "__main__":
    main()
from generation import generation
from itertools import permutations as pm
class game():
    def __init__(self, n, surf, name):
        self.vertices = (
            ( 0.5, -0.5, -0.5),
            ( 0.5,  0.5, -0.5),
            (-0.5,  0.5, -0.5),
            (-0.5, -0.5, -0.5),
            ( 0.5, -0.5,  0.5),
            ( 0.5,  0.5,  0.5),
            (-0.5, -0.5,  0.5),
            (-0.5,  0.5,  0.5),
            )
        #surfaces paired with normals
        self.surfaces = ((3,2,7,6),(4,0,3,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(0,1,2,3))
        #beta[[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255]]
        #0-grass[[139,69,19],[139,69,19],[0,255,0],[139,69,19],[139,69,19],[139,69,19]]
        #1-dirt[[50,24,17],[50,24,17],[50,24,17],[50,24,17],[50,24,17],[50,24,17]]
        #2-stone[[128,128,128],[128,128,128],[128,128,128],[128,128,128],[128,128,128],[128,128,128]]
        #3-custom[[0,38,41],[0,38,41],[0,38,41],[0,38,41],[0,38,41],[0,38,41]]
        self.normals = ((0, 0, -1),(-1, 0, 0),(0, -1, 0),(0, 0, 1),(1, 0, 0),(0, 1, 0))
        self.edges = [[(3,2),(3,6),(2,7),(6,7)],[(0,3),(0,4),(3,6),(4,6)],[(4,5),(4,6),(5,7),(6,7)],[(0,1),(0,4),(1,5),(4,5)],[(1,2),(1,5),(2,7),(5,7)],[(0,1),(0,3),(1,2),(2,3)]]
        self.edges2 = ((3,0),(3,2),(3,6),(5,1),(5,4),(5,7),(0,1),(0,4),(1,2),(2,7),(4,6),(6,7))
        pygame.init()
        if settings.fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode([info.current_w, info.current_h], DOUBLEBUF | OPENGL)
            prop = info.current_w/info.current_h
        else:
            self.screen = pygame.display.set_mode(settings.resolution, DOUBLEBUF | OPENGL)
            prop = settings.resolution[0]/settings.resolution[1]
        GL_TEXTURE_3D
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
        self.sphere = gluNewQuadric() 
        glMatrixMode(GL_PROJECTION)
        gluPerspective(max(min(settings.FOV,120),80), prop, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, 1, 0, 0, 0, 0, 0, 0, 1)
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLoadIdentity()
        glClearColor(0,0.5,1,1)
        self.displayCenter = [self.screen.get_size()[i] // 2 for i in range(2)]
        self.mouseMove = [0, 0]
        pygame.mouse.set_pos(self.displayCenter)
        #fixlater pygame.time.set_timer(pygame.USEREVENT, 100)
        self.vert_angle = 0.0
        self.paused = False
        self.run = True
        self.reset = 0
        self.clock = pygame.time.Clock()
        self.gravity = 1/25
        self.jumpspeed = -0.1
        self.vert_speed = -0.1
        self.world = n
        self.visible = surf
        self.bl_name = name
        self.cur = self.world[self.visible != -1]
        self.cur_visible = self.visible[self.visible != -1]
        self.cur_name = self.bl_name[self.visible != -1]
        self.pos = [0,0,0,0]
        self.colors = [[[139,69,19],[139,69,19],[0,255,0],[139,69,19],[139,69,19],[139,69,19]],
                       [[50,24,17],[50,24,17],[50,24,17],[50,24,17],[50,24,17],[50,24,17]],
                       [[128,128,128],[128,128,128],[128,128,128],[128,128,128],[128,128,128],[128,128,128]],
                       [[0,128,128],[0,128,128],[0,128,128],[0,128,128],[0,128,128],[0,128,128]],
                       [[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255]]]
        self.colors = [[[k/255 for k in j]for j in i] for i in self.colors]
        self.loop()
    def loop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.USEREVENT:
                    pass
                    #print(1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.run = False
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                        pygame.mouse.set_cursor(0)
                        pygame.mouse.set_pos(self.displayCenter)
                if not self.paused and event.type == pygame.MOUSEMOTION:
                        self.mouseMove = [event.pos[i] - self.displayCenter[i] for i in range(2)]
                        pygame.mouse.set_pos(self.displayCenter)    
            if self.paused and not self.reset:
                self.paused = False
                pass
            if self.reset == 60:
                self.reset = 0
                self.paused = True
            if not self.paused:
                pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
                self.screen.fill(pygame.Color(0,255,255))
                keypress = pygame.key.get_pressed()
                # init model view matrix
                glLoadIdentity()
                # apply the look up and down
                self.vert_angle += self.mouseMove[1]
                if self.vert_angle > 90:
                    self.vert_angle = 90
                if self.vert_angle < -90:
                    self.vert_angle = -90
                glRotatef(self.vert_angle, 1.0, 0.0, 0.0)
                # init the view matrix
                glPushMatrix()
                glLoadIdentity()
                # apply the movement
                mov = [0,0,0]
                if keypress[pygame.K_w]:
                    mov[2] += 0.08
                if keypress[pygame.K_s]:
                    mov[2] -= 0.08
                if keypress[pygame.K_d]:
                    mov[0] -= 0.08
                if keypress[pygame.K_a]:
                    mov[0] += 0.08
                if mov[0] != 0 and mov[2] != 0:
                    mov[0] /= 2**0.8
                    mov[2] /= 2**0.8
                if keypress[pygame.K_LSHIFT]:
                    mov[2] *= 1.6
                    mov[0] *= 1.6
                self.pos[3] += self.mouseMove[0]
                ix, iz, iy = round(self.pos[0]), round(self.pos[2]), int(self.pos[1])
                g = self.cur
                g = g[np.logical_and(g[::,0] == ix, g[::,2] == iz)]
                dt = [self.pos[0],self.pos[2]]
                dt[0] -= mov[0]*sin(radians(self.pos[3])) + mov[2]*cos(radians(self.pos[3]))
                dt[1] -= mov[2]*sin(radians(self.pos[3])) - mov[0]*cos(radians(self.pos[3]))
                #collision
                self.pos[0] = dt[0]
                self.pos[2] = dt[1]
                try:
                    g = sorted(g,key=lambda x: x[1])[0]
                except IndexError:
                    g = [ix, 0, iz]
                    #g = [0, iz, 0]
                    #self.pos[0] = 0
                    #self.pos[1] = iz
                    #self.pos[2] = 0
                idy = self.world[np.logical_and(self.world[::, 0] == ix, self.world[::, 2] == iz)][::, 1]
                if iy-1 in idy or iy-2 in idy:
                    self.vert_speed += -0.1
                elif -1e-4 < self.pos[1] - iy < 1e-4 and iy in idy:
                    self.vert_speed = 0
                else:
                    self.vert_speed = min(self.vert_speed+self.gravity, abs(g[1]-self.pos[1])/1.3)
                if keypress[pygame.K_SPACE] and -1e-2 < self.pos[1] - iy < 1e-2 and iy in idy and iy-3 not in idy:
                    self.vert_speed = 4.2*self.jumpspeed - self.gravity
                #print(self.world[np.logical_and(self.world[::,0]==ix, self.world[::,2]==iz)])
                if abs(self.vert_speed)>0.7:
                    self.vert_speed = self.vert_speed/abs(self.vert_speed)*0.7
                mov[1] = self.vert_speed
                self.pos[1] += mov[1]
                glTranslate(*mov)
                glRotatef(self.mouseMove[0], 0.0, 1.0, 0.0)
                glColor4f(0,0.5,0,0.1)
                glMultMatrixf(self.viewMatrix)
                self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
                # apply view matrix
                glPopMatrix() 
                glMultMatrixf(self.viewMatrix)
                glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 256, 0])
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                glPushMatrix()
                glTranslatef(0,1,-2)
                dt = np.logical_and(np.logical_and(self.visible != -1, abs(self.world[::,0]-g[0]) < 6), abs(self.world[::,2]-g[2]) < 6)
                self.cur = self.world[dt]
                self.cur_visible = self.visible[dt]
                self.cur_name = self.bl_name[dt]
                for j, i in enumerate(self.cur):
                    glTranslatef(i[2],i[0],-i[1])
                    if -1 not in self.cur_visible[j]:
                        self.Cube(self.cur_visible[j], self.colors[self.cur_name[j]])
                    glTranslatef(-i[2],-i[0],i[1])
                for i in (1,2,3):
                    view_pos = [round(self.pos[0]-cos(radians(self.pos[3]))*round(i+int(self.pos[0]-self.pos[0]))*cos(radians(self.vert_angle))),
                                round(self.pos[1]-2+i*sin(radians(self.vert_angle))),
                                round(self.pos[2]-sin(radians(self.pos[3]))*round(i+int(self.pos[2]-self.pos[2]))*cos(radians(self.vert_angle)))]
                    try:
                        view = self.cur[np.logical_and(np.logical_and(self.cur[::, 0] == view_pos[0], self.cur[::, 2] == view_pos[2]), self.cur[::, 1] == view_pos[1])][0]
                    except IndexError:
                        continue
                    glTranslatef(view_pos[2],view_pos[0],-view_pos[1])
                    self.square()
                    glTranslatef(-view_pos[2],-view_pos[0],view_pos[1])
                    if len(view):
                        if pygame.mouse.get_pressed()[0] and not self.mouse[0]:
                            self.delete_surface(view)
                            dt = np.logical_or(np.logical_or(self.world[::, 0] != view_pos[0], self.world[::, 2] != view_pos[2]), self.world[::, 1] != view_pos[1])
                            self.visible = self.visible[dt]
                            self.bl_name = self.bl_name[dt] 
                            self.world = self.world[dt]
                        elif pygame.mouse.get_pressed()[2] and not self.mouse[2]:
                            g = [view[0]-self.pos[0],view[1]-self.pos[1]+2,view[2]-self.pos[2]]
                            n = sorted([0,1,2], key = lambda x: -abs(g[x]))
                            view[n[0]] -= int(np.sign(g[n[0]]))
                            if view[1] not in self.world[np.logical_and(self.world[::, 0] == view[0], self.world[::, 2] == view[2])][::, 1].tolist():
                                self.bl_name = np.append(self.bl_name, [3])
                                self.world = np.vstack([self.world, view])
                                self.update_surface(view)
                    break
                        #else:
                            #print(str(np.array(i)),str(self.cur))
                glPopMatrix()
                self.draw_crosshair()
                self.mouse = pygame.mouse.get_pressed()
                self.reset += 1
                pygame.display.flip()
            self.clock.tick(62)
            print(f'fps:{self.clock.get_fps()}')
        print()
        bl, vis, bl_name = self.world, self.visible, self.bl_name
        with open(settings.load_path, 'wt') as file:
            file.write('\n'.join([','.join([str(j) for j in bl[i]] + [str(j) for j in vis[i]] + [str(bl_name[i])]) for i in range(len(bl))]))
        pygame.quit()
    def delete_surface(self, coord):
        for i,j in enumerate(self.normals):
            dt = [coord[0]+j[0],coord[1]+j[1],coord[2]+j[2]]
            try:
                g = np.logical_and(np.logical_and(self.world[::, 0] ==dt[0], self.world[::, 2] == dt[2]), self.world[::, 1] == dt[1])
                if -1 in self.visible[g.tolist().index(True)]:
                    self.visible[g.tolist().index(True)] = []
                print(self.visible[g].tolist()[0]+[(i+3)%6])
                self.visible[g.tolist().index(True)] = self.visible[g].tolist()[0] + [(i+3)%6]
            except ValueError:
                continue
    def update_surface(self, coord):
        f = []
        for i,j in enumerate(self.normals):
            dt = [coord[0]+j[0],coord[1]+j[1],coord[2]+j[2]]
            try:
                g = np.logical_and(np.logical_and(self.world[::, 0] == dt[0], self.world[::, 2] == dt[2]), self.world[::, 1] == dt[1])
                n = self.visible[g.tolist().index(True)]
                if len(n) == 1:
                    self.visible[g.tolist().index(True)] = [-1]
                else:
                    n.remove((i+3)%6)
                    self.visible[g.tolist().index(True)] = n
                self.visible[g.tolist().index(True)]
            except ValueError:
                f.append(i)
        print(self.visible)
        print(f)
        self.visible = np.array(self.visible.tolist() + [f])
    def Cube(self, visible, color):
        glBegin(GL_QUADS)
        for i_surface, surface in enumerate(self.surfaces):
            if i_surface not in visible:
                continue
            #glNormal3fv(self.normals[i_surface]) # set the normal vector the vertices of the surface
            glColor3f(*color[i_surface])
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        '''glBegin(GL_LINES)
        glColor3f(0,0,255)
        usd = []
        for i, edge in enumerate(self.edges):
            if i not in visible:
                continue
            for index in edge:
                if index in usd:
                    continue
                usd.append(index)
                for j in index:
                    glVertex3fv(self.vertices[j])
        glEnd()'''
    def square(self):
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor3f(0,0,0)
        for edge in self.edges2:
            for index in edge:
                glVertex3fv(self.vertices[index])
        glEnd()
    def draw_crosshair(self):
        height = self.screen.get_height()
        width = self.screen.get_width()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_COLOR_LOGIC_OP)
        glLogicOp(GL_INVERT)
        glTranslatef(width/2-10,height/2-10, 0)
        glLineWidth(2)
        glBegin(GL_LINES)
        glColor3f(1,1,1)
        glVertex3f(10, 20, 0)
        glVertex3f(10, 0, 0)
        glVertex3f(0, 10, 0)
        glVertex3f(20, 10, 0)
        glEnd()
        glDisable(GL_COLOR_LOGIC_OP)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glMatrixMode(GL_MODELVIEW)
    '''def Cube(self, sides):
        glBegin(GL_QUADS)
        for i_surface, surface in enumerate(self.surfaces):
            if i_surface not in sides:
                continue
            glNormal3fv(self.normals[i_surface]) # set the normal vector the vertices of the surface
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glBegin(GL_LINES)
        glColor3f(0,0,255)
        for edge in self.edges:
            for index in edge:
                glVertex3fv(self.vertices[index])
        glEnd()'''
def main():
    if settings.load:
        with open(settings.load_path) as file:
            f = file.read().split('\n')
            bl, vis, bl_name = [], [], []
            for i in f:
                d = list(map(int, i.split(',')))
                bl.append(d[:3])
                vis.append(d[3:-1])
                bl_name.append(d[-1])                   
    else:
        bl, vis, bl_name = generation.world(*settings.world_params)
        with open(settings.load_path, 'wt') as file:
            file.write('\n'.join([','.join([str(j) for j in bl[i]] + [str(j) for j in vis[i]] + [str(bl_name[i])]) for i in range(len(bl))]))
    game(np.array(bl), np.array(vis), np.array(bl_name))
if __name__ == '__main__':
    main()
