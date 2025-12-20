# -*- coding: utf-8 -*-

import pygame

class Element():
    def __init__(self, pos):
        self.pos = pos
        self.shapes = []
        self.rect = None
        self.active = False
        self.color = pygame.Color(255,255,255)
        self.data = None
        self.key = None
        self.fontSize = 20
        self.fontColor = (0,0,0)
    
    def collide(self, pos):
        if self.rect is not None:
            return self.rect.collidepoint(pos)
        else:
            return False
    
    def handle(self, event):
        pass
    
    def draw(self, screen, centered=True):
        for s in self.shapes:
            if isinstance(s, pygame.Rect):
                if self.active:
                    pygame.draw.rect(screen, self.activeColor, self.rect)
                else:
                    pygame.draw.rect(screen, self.color, self.rect)
            
            elif isinstance(s, str):
                base_font = pygame.font.Font(None, self.fontSize)
                text_surface = base_font.render(s, True, self.fontColor)
                
                x0 = self.pos[0]
                y0 = self.pos[1]
                
                if self.height is not None:
                    y0 = y0 + (self.height - text_surface.get_height())/2
                    if centered and self.width is not None:
                        x0 = x0 + (self.width - text_surface.get_width())/2
                
                screen.blit(text_surface, (x0, y0))


class Button(Element):
    def __init__(self, pos, width, height, onpress, text="Button", key="button", value=True, instant=False, data={}):
        super(Button, self).__init__(pos)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.shapes.append(self.rect)
        self.shapes.append(text)
        
        self.onpress = onpress
        self.data = data
        self.key = key
        self.value = value
        self.text = text
        self.instant = instant
        self.data[self.key] = self.value
        
        if self.value:
            self.color=pygame.Color(180,200,255)
        else:
            self.color=pygame.Color(255, 255, 255)
        self.activeColor = self.color
        
    def handle(self, event):
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            self.value = not self.value
            self.data[self.key] = self.value
            
            self.onpress(self.value, self)
            if self.value:
                self.color=pygame.Color(180,200,255)
                self.activeColor=pygame.Color(180,200,255)
            else:
                self.color=pygame.Color(255, 255, 255)
                self.activeColor=pygame.Color(255, 255, 255)
            self.activeColor = self.color
        if self.instant:
            # reset the value on button up for instantaneous button
            if event.type == pygame.locals.MOUSEBUTTONUP:
                self.value = not self.value
                self.data[self.key] = self.value
                
                if self.value:
                    self.color=pygame.Color(180,200,255)
                    self.activeColor=pygame.Color(180,200,255)
                else:
                    self.color=pygame.Color(255, 255, 255)
                    self.activeColor=pygame.Color(255, 255, 255)
            
class TextInput(Element):
    def __init__(self, pos, width, height, key="text", value="", data={}):
        super(TextInput, self).__init__(pos)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.shapes.append(self.rect)
        self.color = pygame.Color("white")
        self.activeColor = pygame.Color(180,200,255)
        self.data = data
        self.key = key
        self.value = value
        self.shapes.append(self.value)
        
        self.data[self.key] = self.value
        
    def handle(self, event):
        if event.type == pygame.locals.KEYDOWN:
            self.shapes.remove(self.value)
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
                
            else:
                temp = self.value + event.unicode
                print(temp)
                self.value = temp
            self.data[self.key] = self.value
            self.shapes.append(self.value)


class NumInput(TextInput):
    def __init__(self, pos, width, height, key="text", value="0", data={}, highLim=99, kind=int):
        super(NumInput, self).__init__(pos, width, height, key, value, data)
        self.highLim = highLim
        self.kind = kind
    
    def handle(self, event):
        # override the handler to check for number length
        if event.type == pygame.locals.KEYDOWN:
            self.shapes.remove(self.value)
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
                
            else:
                temp = self.value + event.unicode
                print(temp)
                if self.kind == int:
                    if temp.isnumeric() and temp:
                        if int(temp) <= self.highLim:
                            self.value = temp
                elif self.kind == float:
                    try:
                        if float(temp) <= self.highLim and temp:
                            self.value = temp
                    except:
                        pass
                    
            self.data[self.key] = self.value
            self.shapes.append(self.value)
            
        
class GroupInput(Element):
    # container for row of elements to define a group
    rowStart = 8
    colors = [
        pygame.Color("blue"),
        pygame.Color("purple"),
        pygame.Color("red"),
        pygame.Color("orange")
        ]
    
    def __init__(self, pos, width, height, groupID, data={}):
        super(GroupInput, self).__init__(pos)
        self.width = width
        self.height = height
        self.groupID = groupID
        self.data = data
        self.key = "group_{}".format(groupID)
        
        self.internalData = {}
        
        
        self.color = GroupInput.colors[groupID]
        #self.rect = pygame.Rect(pos[0], pos[1], width, height)
        #self.shapes.append(self.rect)
        
        colWidth = 60
        cols = [pos[0] + colWidth*i for i in range(5)]
        inputHeight = 25
        inputY = pos[1] + (height - inputHeight)/2
        inputWidth = 50
        
        elements = [
            Label(pos, height=height, size=24, text=str(groupID), fontColor=self.color),
            NumInput((cols[1],inputY),inputWidth, inputHeight, key="radius", value="0.5", kind=float, highLim=10, data=self.internalData),
            NumInput((cols[2],inputY),inputWidth, inputHeight, key="mass", value="1", kind=float, highLim=100, data=self.internalData),
            TextInput((cols[3],inputY),inputWidth, inputHeight, key="connections", value=str(self.groupID), data=self.internalData),
            NumInput((self.width - inputWidth,inputY),inputWidth, inputHeight, key="num", value="400", kind=int, highLim=5000, data=self.internalData)
            ]
        
        
        self.elements = elements
        
        self.data[self.key] = self
        
    def collide(self, pos):
        # ignore clicks on group
        return False
    
    def getData(self):
        rad = float(self.internalData["radius"])
        m = float(self.internalData["mass"])
        conarr = self.internalData["connections"].split(",")
        connections = []
        for c in range(len(conarr)):
            try:
                temp = int(conarr[c])
                connections.append(temp)
            except:
                print("Invalid connection string: '{}'".format(conarr[c]))
        
        n = int(self.internalData["num"])
        
        return (rad, m, self.color, self.groupID, connections, n)
        
    
#    def draw(self, screen, centered=False):
#        super(GroupInput, self).draw(screen, centered)
#        for e in self.elements:
#            e.draw(screen, centered)


class Label(Element):
    def __init__(self, pos, width=None, height=None, size=20, text="", fontColor=(0,0,0)):
        super(Label, self).__init__(pos)
        self.text=text
        self.shapes.append(text)
        self.height = height
        self.width = width
        self.fontSize = size
        self.fontColor = fontColor


class GUI():
    
    def __init__(self, screen, simResetCallback, pos=(10,10), width=0, height=0, alpha=200):
        self.screen = screen
        self.pos = pos
        self.simResetCallback = simResetCallback
        
        self.width = width if width > 0 else screen.get_width()*2/7
        self.height = height if height > 0 else screen.get_height()*2/3
        
        self.surface = pygame.Surface((self.width,self.height))
        self.surface.set_alpha(alpha)
        
        # Dict of all simulation input variables
        self.inputVars = {}
        
        background = Element(pos)
        background.rect = pygame.Rect(0,0, self.width, self.height)
        background.shapes.append(background.rect)
        background.color = pygame.Color(180,180,180)
        
        self.surfaceElements = [background]
        
        # create button to show and hide menu
        self.showBtn = Button((5,5),50,20, text="Menu", onpress=self.toggleVisible, key="showMenu", value=True, data=self.inputVars)
        self.screenElements = [self.showBtn]
        
        # create button to pause and play simulation
        self.addElement(Button((65,5),50,20, text="II", onpress=self.togglePausePlay, key="paused", value=False, data=self.inputVars),False)
        
        
        self.visible = True
        self.updated = True
        self.activeElement = self.showBtn
        self.prevElement = self.showBtn
        
        ##### set up input for simulation #####
        
        # define rows to make alignment easier
        rowBuffer = 5
        rowHeight = 26
        
        colBuffer = 10
        colWidth = 50
        
        rows = 15
        rowy = [rowBuffer*(i+1)+rowHeight*(i) for i in range(0,rows)]
        colx = [colBuffer*i + colWidth*i for i in range(8)]
        
        leftAlign = 10
        rightAlign = self.width - 10 # subtract element width from this
        
        numInputWidth = 50
        
        self.rowy=rowy
        self.rowHeight=rowHeight
        self.leftAlign=leftAlign
        
        # row 1: dissociation rate
        self.addElement(NumInput((rightAlign-numInputWidth, rowy[0]), numInputWidth, rowHeight, key="dissocRate", value="15", highLim=100, kind=float, data=self.inputVars))
        self.addElement(Label((leftAlign, rowy[0]), height=rowHeight, size=20, text="Dissociation rate (%/s):"))
        
        # row 2: joint cooldown
        self.addElement(NumInput((rightAlign-numInputWidth, rowy[1]), numInputWidth, rowHeight, key="cooldown", value="0.2", highLim=5, kind=float, data=self.inputVars))
        self.addElement(Label((leftAlign, rowy[1]), height=rowHeight, size=20, text="Bond cooldown (s):"))
        
        # row 3: joint stiffness
        self.addElement(NumInput((rightAlign-numInputWidth, rowy[2]), numInputWidth, rowHeight, key="stiffness", value="10", highLim=30, kind=float, data=self.inputVars))
        self.addElement(Label((leftAlign, rowy[2]), height=rowHeight, size=20, text="Bond stiffness (≤30 hZ, 0=rigid):"))
        
        # row 4: gravity
        self.addElement(Label((leftAlign, rowy[3]), height=rowHeight, size=20, text="Gravity (+x direction)"))
        self.addElement(NumInput((rightAlign-numInputWidth, rowy[3]), numInputWidth, rowHeight, key="gravity", value="0.0", highLim=10, kind=float, data=self.inputVars))
        
        # row 5: temperature (ish)
        self.addElement(Label((leftAlign, rowy[4]), height=rowHeight, size=20, text="Temp analog(0-100)"))
        self.addElement(NumInput((rightAlign-numInputWidth, rowy[4]), numInputWidth, rowHeight, key="temp", value="20", highLim=100, kind=float, data=self.inputVars))
        
        # row 6: button options:
        self.addElement(Button((leftAlign,rowy[5]),150,20, text="Allow Bond Rotation", onpress=self.noneCallback, key="allowRotation", value=True, instant=False, data=self.inputVars))
        
        
        r = 7
        # row i: Number of groups
        
        self.addElement(Label((leftAlign, rowy[r]), height=rowHeight, size=20, text="# of particle types:"))
        self.addElement(NumInput((leftAlign, rowy[r+1]), numInputWidth, rowHeight, key="nGroupTypes", value="1", highLim=4, kind=int, data=self.inputVars))
        self.addElement(Button((rightAlign-50,rowy[r+1]+3),50,20, text="Apply", onpress=self.makeGroupRows, key="applyNum", value=False, instant=True, data=self.inputVars))
        
        # row 6: group entry lables
        self.addElement(Label((leftAlign, rowy[r+2]), height=rowHeight, size=20, text="Group    Radius   Mass   Interactions(0,1)   Count", fontColor="black"))
        
        GroupInput.rowStart = r+3
        
        # rows 7+: group entry
        self.groupRows = []
        self.makeGroupRows()
        # row -1: reset sim button
        
        self.addElement(Button((leftAlign,rowy[r+7]),150,20, text="Reset Simulation", onpress=simResetCallback, key="reset", value=False, instant=True, data=self.inputVars))
        
    
    def addElement(self, element, surface=True):
        if surface:
            self.surfaceElements.append(element)
        else:
            self.screenElements.append(element)
    
    def removeElement(self, element, surface=True):
        if surface:
            if element in self.surfaceElements:
                self.surfaceElements.remove(element)
        else:
            if element in self.screenElements:
                self.screenElements.remove(element)
        
    def togglePausePlay(self, val, button):
        button.shapes.remove(button.text)
        if val:
            button.text="II"
        else:
            button.text="II"
        button.shapes.append(button.text)
    
    def toggleVisible(self, val, button):
        self.visible = val
    
    def noneCallback(self, val, button):
        pass
    
    def makeGroupRows(self, val=None, button=None):
        rowStart = GroupInput.rowStart
        n = int(self.inputVars["nGroupTypes"])
        if len(self.groupRows) > n:
            for r in self.groupRows[n:]:
                # clear the previous existing rows
                for el in r.elements:
                    self.removeElement(el)
                self.inputVars.pop(r.key)
                self.removeElement(r)
            self.groupRows = self.groupRows[:n]
        
        for i in range(len(self.groupRows), n):
            # create the desired number of new group rows
            g = GroupInput((self.leftAlign, self.rowy[i+rowStart]), self.width-20, height=self.rowHeight, groupID=i, data=self.inputVars)
            self.groupRows.append(g)
            self.addElement(g)
            
            for el in g.elements:
                self.addElement(el)
        
        
    def handleClick(self, event):
        #if self.element[0].collide():
        #collided = False
        #print("  ".join([str(e) for e in self.screenElements]))
        for e in self.screenElements:
            if e.collide(event.pos):
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    self.prevElement = self.activeElement
                    self.prevElement.active = False
                    self.activeElement = e
                    e.active = True
                    #print("active element:" + (e.key if e.key is not None else "None"))
                e.handle(event)
                
        if self.visible:
            for e in self.surfaceElements[1:]:
                # apply transformation to event position to convert to local coordinates
                if e.collide((event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])):
                    if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        self.prevElement = self.activeElement
                        self.prevElement.active = False
                        self.activeElement = e
                        e.active = True
                        #print("active element:" + (e.key if e.key is not None else "None"))
                    
                    e.handle(event)
                    self.updated = True
        #if not collided:
        #    self.prevElement = self.screenElements[0]
        #    if self.prevElement is not None:
        #        self.prevElement.active = False
        #    self.activeElement = None
            
        
    def handleKey(self, event):
        elements = self.screenElements + self.surfaceElements[1:] if self.visible else self.screenElements
        for e in elements:
            if e.active and isinstance(e, TextInput):
                e.handle(event)
                self.updated = True
    
    
    def draw(self):
        if self.visible:
            # only redraw if an event has been handled
            if self.updated:
                for e in self.surfaceElements:
                    e.draw(self.surface)
                    self.updated = False
            self.screen.blit(self.surface, self.pos)
        
        #draw the hide/show button to the main screen
        for e in self.screenElements:
            e.draw(self.screen)
        
        


