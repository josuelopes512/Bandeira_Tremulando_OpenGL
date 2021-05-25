# pip install PyOpenGL PyOpenGL_accelerate
# pip install pygame

#https://github.com/disenone/pyOpenGL/blob/master/ColorLightMixFog/Light.py
#https://www.glprogramming.com/red/chapter12.html


import numpy as np
import pygame
from pygame.locals import *
from copy import copy
from OpenGL.GL import *
from OpenGL.GLU import *
import keyboard
import math

CUBE_DEG_PER_S = 30.0
LIGHT_DEG_PER_S = 90.0
#flashLightPos = [ 0.0, 0.0, 0.0]
flashLightPos = [ 0.0, 10.0, 0.0]
flashLightDir = [ 0.0, -1.0, 0.0 ]
flashLightColor = [ 0.2, 0.2, 0.2]
redLightColor = [ 0.5, 0.1, 0.2 ]
redLightPos = [ 10.0, 0.0, 5.0, 1.0 ]
greenLightColor = [ 0.1, 0.6, 0.2 ]
#greenLightPos = [ 0.0, 0.0, 10.0, 1.0 ]
greenLightPos = [ -10.0, 0.0, 0.0, 1.0 ]

m_pSphere = gluNewQuadric()
m_cubeAngle = 0.0
m_lightAngle = 0.0
m_flashlightOn = True        


# ctrlpoints = [
#    [[-1.5, -1.5, 4.0], [-0.5, -1.5, 2.0], 
#     [0.5, -1.5, -1.0], [1.5, -1.5, 2.0]], 
#    [[-1.5, -0.5, 1.0], [-0.5, -0.5, 3.0], 
#     [0.5, -0.5, 0.0], [1.5, -0.5, -1.0]], 
#    [[-1.5, 0.5, 4.0], [-0.5, 0.5, 0.0], 
#     [0.5, 0.5, 3.0], [1.5, 0.5, 4.0]], 
#    [[-1.5, 1.5, -2.0], [-0.5, 1.5, -2.0], 
#     [0.5, 1.5, 0.0], [1.5, 1.5, -1.0]]
# ]

ctrlpoints = [
	[[-1., 1., 0.], [0., 1., 1.], [1., 1., 0.]],
	[[-1., 0., 1.], [0.,0., 2.], [1., 0., 1.]],
	[[-1., -1., 0.], [0., -1., 1.], [1., -1., 0.]]
]

ctrlpoints= 5*np.array(ctrlpoints)

def init():
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glMap2f(GL_MAP2_VERTEX_3, 0, 1, 0, 1, ctrlpoints)
    glEnable(GL_MAP2_VERTEX_3)
    glEnable(GL_AUTO_NORMAL)
    glMapGrid2f(20, 0.0, 1.0, 20, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    #glShadeModel(GL_FLAT)

def cilindro():
    glColor(1,0,0)
    glTranslate(-4.5, 5, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(m_pSphere, 1/5, 1/5, 50*2, 20, 20)
    glPopMatrix()

def display_sciene():
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    #glRotatef(85.0, 1.0, 1.0, 1.0)
    # glRotatef(m_cubeAngle, 1.0, 1.0, 0.0)
    # glTranslate(0, 0, 285)
    # glTranslate(0,0,0)
    glTranslate(0,-1,0)
    glRotatef(360, 25, 0, 0)
    # glRotatef(m_cubeAngle, 0.0, 0.0, 1.0)
    glPushMatrix()
    cilindro()
    glEvalMesh2(GL_FILL, 0, 20, 0, 20)
    glTranslate(0, 0, 285)
    # a = gluNewQuadric()
    # gluCylinder(m_pSphere,1/5,1/5,100,20,20)
    glPopMatrix()
    #glFlush()

def Reshape(width, height):
    if(height == 0):
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(64.0, float(width)/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def Display(eye, target, up):
    global m_cubeAngle, m_flashlightOn, m_lightAngle, m_pSphere
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(eye[0], eye[1], eye[2], target[0], target[1], target[2], up[0], up[1], up[2])
    if (m_flashlightOn):
        glEnable(GL_LIGHT0)
    else:
        glDisable(GL_LIGHT0)
    # position the red light
    glLightfv(GL_LIGHT1, GL_POSITION, redLightPos)
    # draw the red light
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(redLightPos[0], redLightPos[1], redLightPos[2])
    glColor3fv(redLightColor)
    gluSphere(m_pSphere, 0.2, 10, 10)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    # position and draw the green light
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glRotatef(m_lightAngle, 1.0, 0.0, 0.0)
    glRotatef(m_lightAngle, 0.0, 1.0, 0.0)
    glLightfv(GL_LIGHT2, GL_POSITION, greenLightPos)
    glTranslatef(greenLightPos[0], greenLightPos[1], greenLightPos[2])
    glColor3fv(greenLightColor)
    gluSphere(m_pSphere, 0.2, 10, 10)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    # set up Bezier's surface material
    cubeColor = [ 0.6, 0.7, 0.0 ]
    cubeSpecular = [ 1.0, 1.0, 1.0 ]
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, cubeColor)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, cubeSpecular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 10.0)
    display_sciene()
    

def OpenglInit():
    global m_pSphere
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    #glDepthFunc(GL_LEQUAL)              ### test
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, flashLightPos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, flashLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, flashLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, flashLightColor)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, flashLightDir)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 12.0)
    #glDisable(GL_LIGHT0)
    
    # set up static red light
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, redLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, redLightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, redLightColor)
    #glDisable(GL_LIGHT1)
    
    # set up moving green light
    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, greenLightColor)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, greenLightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, greenLightColor)
    #glDisable(GL_LIGHT2)
    # get a quadric object for the light sphere
    m_pSphere = gluNewQuadric()

def ChangeAngle(dt):
    global CUBE_DEG_PER_S, LIGHT_DEG_PER_S, m_cubeAngle, m_lightAngle
    m_cubeAngle += CUBE_DEG_PER_S * dt
    if (m_cubeAngle > 360.0):
        m_cubeAngle = 0.0
    m_lightAngle += LIGHT_DEG_PER_S * dt
    if (m_lightAngle > 360.0):
        m_lightAngle = 0.0

def update_control_point(p, signal):
    amplitude = 4
    p = p +0.3 * signal
    if p > amplitude or p < -amplitude:
        signal = -1 * signal
    return p, signal

# right = true or false
def move_target(eye, target, right):
    
    #translada a câmera para a origem
    t0 = target - eye

    #Ignora a componente Y
    t0[1] = 0

    #Calcula o raio do círculo
    r = math.sqrt(t0[0] * t0[0] + t0[2] * t0[2])
    
    #Calcula o seno e o cosseno e a tangente do ângulo que o vetor faz com o eixo X
    sin_alfa = t0[2]/r
    cos_alfa = t0[0]/r
    if cos_alfa == 0:
        if sin_alfa == 1:
            alfa  = math.pi/2
        else:
            alfa  = - math.pi/2
    else:
        tg_alfa = sin_alfa/cos_alfa

        #Calcula o arco cuja tangente é calculada no passo anterior
        alfa = np.arctan(tg_alfa)

        # Como o retorno de arctan varia somente entre -pi/2 e pi/2, testar o cosseno para 
        # calcular o ângulo correto
        if cos_alfa < 0:
            alfa = alfa -  math.pi
    
    if right:
        signal = 1
    else:
        signal = -1

    # Varia o ângulo do alvo (target)
    alfa = alfa + 0.1 * signal
    
    # Calcula o novo alvo (sobre o eixo Y)
    t0[0] = r * math.cos(alfa)
    t0[2] = r * math.sin(alfa)

    n_target = eye + t0
    return n_target

# ahead = true or false
def move_can(eye, target, ahead):
    #equação paramétrica
    a = np.zeros(3)
    delta = 0.1
    p0 = eye
    p1 = target
    a = p1 - p0
    if ahead:
        signal = 1
    else:
        signal = -1
    p0 = p0 + delta * a * signal
    p1 = p1 + delta * a * signal
    #Câmera sobre o plano (X, Z)
    #p0[1] = 0
    return p0, p1

	
def main():
    # Translação do cubo verde
    tx = 0
    ty = 0
    signal = 1
    signal_1 = 1
    signal_2 = -1
    signal_3 = -1
    #UP vector angle = Pi/2 (90o) 
    up_angle =math.pi/2
    rot_angle = math.pi/2
    wireframe=False
    smooth = True
    slices = 10
    stacks = 10
    pygame.init()
    display = (800,600)
    print(pygame.display.Info())
    infoObject = pygame.display.Info()
    # pygame.display.set_mode((int(infoObject.current_w/2), infoObject.current_h), DOUBLEBUF|OPENGL)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    # eye = (0, 0, 20)
    eye = np.zeros(3)
    eye[2] = 20
    # target = (0, 0, 0)
    target = np.zeros(3)
    # up = (1, 0, 0)
    up = np.zeros(3)
    up[0] = 0
    up[1] = 1
    up[2] = 0
    up[1] = math.sin(up_angle)
    up[0] = math.cos(up_angle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif  event.type == pygame.KEYDOWN :
		        # Movimentação do cubo
                if event.key==K_w:
                    ty = ty + 0.5
                elif event.key==K_z:
                    ty = ty - 0.5
                elif event.key==K_a:
                    tx = tx - 0.5
                elif event.key==K_s:
                    tx = tx + 0.5
		        # Movimentação da direção da câmera 
		        # nos eixos X e Y (olho)
                elif event.key==K_UP:
                    target[1] = target[1] + 0.5
                elif event.key==K_DOWN:
                    target[1] = target[1] - 0.5
                #move_target(eye, target, right):
                elif event.key==K_RIGHT:
                    target = move_target(eye, target, True)
                elif event.key==K_LEFT:
                    target = move_target(eye, target, False)
                elif event.key==K_PAGEUP:
                    #Mover para frente
                    eye, target = move_can(eye, target, True)
                    #eye[2] = eye[2] - 0.5
                    #print(eye, target)
                elif event.key==K_PAGEDOWN:
                    #Mover para trás
                    eye, target = move_can(eye, target, False)
                    #eye[2] = eye[2] + 0.5
                    #print(eye, target)
                elif event.key==K_t:
                    eye[0] = eye[0] - 0.5
                elif event.key==K_g:
                    eye[0] = eye[0] + 0.5
		        # Movimentação da parte de cima da câmera (UP vector)
                elif event.key==K_PERIOD:
                    up_angle += 0.05
                    up[1] = math.sin(up_angle)
                    up[0] = math.cos(up_angle)
                elif event.key==K_COMMA:
                    up_angle -= 0.05
                    up[1] = math.sin(up_angle)
                    up[0] = math.cos(up_angle)
                # Wireframe
                elif event.key==K_SPACE:
                    wireframe = not wireframe
                # Smooth or flat
                elif event.key==K_BACKSPACE:
                    smooth = not smooth
                # Sphere resolution
                elif event.key==K_c:
                    if slices > 5:
                        slices -= 3
                        stacks -= 3
                elif event.key==K_v:
                    slices += 3
                    stacks += 3
            elif event.type == pygame.MOUSEBUTTONDOWN:
                eye_dist = math.sqrt(eye[0]*eye[0] + eye[1]*eye[1] +eye[2]*eye[2])
                if event.button == 4:
                    rot_angle += 0.2
                    eye[2] = eye_dist * math.sin(rot_angle)
                    eye[0] = eye_dist * math.cos(rot_angle)

                if event.button == 5:
                    rot_angle -= 0.2
                    eye[2] = eye_dist * math.sin(rot_angle)
                    eye[0] = eye_dist * math.cos(rot_angle)
        if smooth:
            glShadeModel(GL_SMOOTH)
        else:
            glShadeModel(GL_FLAT)
        OpenglInit()
        init()
        Display(eye,target, up)
        Reshape(display[0],display[1])
        ChangeAngle(0.03)
        ctrlpoints[1][1][2], signal = update_control_point(ctrlpoints[1][1][2], signal)
        ctrlpoints[0][2][2], signal_1 = update_control_point(ctrlpoints[0][2][2], signal_1)
        ctrlpoints[2][2][2], signal_2 = update_control_point(ctrlpoints[2][2][2], signal_2)
        ctrlpoints[1][2][2], signal_3 = update_control_point(ctrlpoints[1][2][2], signal_3)
        pygame.display.flip()
        pygame.time.wait(20)
main()