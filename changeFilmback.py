import maya.cmds as mc

class changeFilmback():

    def __init__(self):
        ################################# UI
        self.win = 'changeFilmback'
        self.columnWidth = 100
        self.selCam_Name = ''
        self.selCam_Shape = ''
        self.selCam_imagePlane_Name = ''
        self.selCam_imagePlane_Shape = ''
        #################################
        
        ################################# Cam and Image plane info
        self.initCoverageX = 1920
        self.initCoverageY = 1080
        
        self.oriCoverageX = 0
        self.oriCoverageY = 0

        self.dewarpedCoverageX = 0
        self.dewarpedCoverageY = 0

        self.oriFilmbackWidth = 0
        self.oriFilmbackHeight = 0
        
        self.dewarpedFilmbackWidth = 0
        self.dewarpedFilmbackHeight = 0
        #################################
        
        self.display()

    def display(self):

        self.getCam_Info()
        self.getDewarped_widthHeight()

        if mc.window(self.win,exists = True):
            mc.deleteUI(self.win)

        mc.window(self.win, sizeable = False, resizeToFitChildren = True)
        mc.rowColumnLayout(nc = 1)
        
        mc.separator(height = 15, style = 'out')#############################
        
        mc.text(label= self.selCam_Name)
        
        mc.separator(height = 15, style = 'out')#############################
        
        mc.text(label = 'Dewarped Resolution')
        mc.rowColumnLayout(nc = 2, columnWidth = [(1,self.columnWidth),(2,self.columnWidth)])
        mc.text(label = self.dewarpedCoverageX)
        mc.text(label = self.dewarpedCoverageY)
        mc.setParent('..')

        mc.separator(height = 15, style = 'out')#############################
        
        mc.text(label= 'Original Resolution')
        mc.rowColumnLayout(nc = 2, columnWidth = [(1,self.columnWidth),(2,self.columnWidth)])
        mc.intField('oriCoverageX', value = self.initCoverageX)
        mc.intField('oriCoverageY', value = self.initCoverageY)
        mc.setParent('..')
        
        #mc.rowColumnLayout(nc = 2, columnWidth = [(1,self.columnWidth),(2,self.columnWidth)])
        #mc.button(label = '1920')
        #mc.button(label = '2048')
        #mc.setParent('..')
      
        mc.separator(height = 15, style = 'out')#############################
        
        mc.button(label = 'change filmback size', height = 40, command = self.run)

        mc.separator(height = 15, style = 'out')#############################
                
        mc.showWindow(self.win)
		
    def getCam_Info(self):
        selCam_Name = mc.ls(selection = True)[0]
        self.selCam_Name = selCam_Name
        
        selCam_Shape = mc.listRelatives(selCam_Name, shapes = True)[0]
        self.selCam_Shape = selCam_Shape
        
        selCam_imagePlane_Name = mc.listRelatives(selCam_Shape, c = True)[0]
        self.selCam_imagePlane_Name = selCam_imagePlane_Name
        
        selCam_imagePlane_Shape = mc.listRelatives(selCam_imagePlane_Name, shapes = True)[0]
        self.selCam_imagePlane_Shape = selCam_imagePlane_Shape
        
        self.oriFilmbackWidth = mc.getAttr(self.selCam_Shape + '.horizontalFilmAperture')
        self.oriFilmbackHeight = mc.getAttr(self.selCam_Shape + '.verticalFilmAperture')
        
        return
                
    def getDewarped_widthHeight(self):
        self.dewarpedCoverageX = mc.getAttr(self.selCam_imagePlane_Shape + '.coverageX')
        self.dewarpedCoverageY = mc.getAttr(self.selCam_imagePlane_Shape + '.coverageY')
        
        return
        
    def run(self,a):
        self.oriCoverageX = mc.intField('oriCoverageX', q = True, value = True)
        self.oriCoverageY = mc.intField('oriCoverageY', q = True, value = True)

        ### Convert Filmback Width/Height ###
        self.dewarpedFilmbackWidth = self.oriFilmbackWidth * ( self.dewarpedCoverageX / float(self.oriCoverageX))
        self.dewarpedFilmbackHeight = self.oriFilmbackHeight * ( self.dewarpedCoverageY / float(self.oriCoverageX))

        ### Set Converted Attributes to Camera ###
        mc.setAttr(self.selCam_Shape + '.horizontalFilmAperture',self.dewarpedFilmbackWidth)
        mc.setAttr(self.selCam_Shape + '.verticalFilmAperture',self.dewarpedFilmbackHeight)
        mc.setAttr(self.selCam_imagePlane_Shape + '.sizeX',self.dewarpedFilmbackWidth)
        mc.setAttr(self.selCam_imagePlane_Shape + '.sizeY',self.dewarpedFilmbackHeight)

        ### Lock Attributes ###
        mc.setAttr(self.selCam_Shape + '.horizontalFilmAperture', lock = True)
        mc.setAttr(self.selCam_Shape + '.verticalFilmAperture', lock = True)
        mc.setAttr(self.selCam_imagePlane_Shape + '.sizeX', lock = True)
        mc.setAttr(self.selCam_imagePlane_Shape + '.sizeY', lock = True)

        print [self.dewarpedFilmbackWidth,self.dewarpedFilmbackHeight]
        
        return
        
if __name__ == '__main__':
    changeFilmback().display()
