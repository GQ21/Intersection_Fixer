######################################
#####     Intersection Fixer    #####
#####         V0.1               #####      
######################################
  ###                            ###
######################################
##### Authored and Maintained by #####
#####       Gin Jankus           #####      
######################################
 
import maya.cmds as mc
import intersection as it


class IT_OptionsWindow(object):
    """Class for an UI options window"""   
    def __init__(self):
        """Initialize common data attributes"""
        self.window = 'it_optionswindow'
        self.title = 'Intersection Fixer'
        self.size = (300,150)
    def create(self):
        """Draw the window"""
        if mc.window(self.window, exists = True):
            mc.deleteUI(self.window, window = True)
        self.window = mc.window(
            self.window,
            title = self.title,
            widthHeight = self.size,
            menuBar = True
        )
        self.main_form = mc.formLayout(nd=100)
        self.common_menu()   
        self.common_buttons()            
        self.options_border = mc.tabLayout(
            scrollable = True,
            tabsVisible = False,
            height = 1,
            childResizable = True
        )
        mc.formLayout(
            self.main_form,
            e=True,
            attachForm = (
                [self.options_border, 'top',0],
                [self.options_border, 'left',2],
                [self.options_border, 'right',2]
            ) ,       
            attachControl=(
                [self.options_border,'bottom',5,self.move_btn]
            )
        )
        self.options_form = mc.formLayout(nd=100)
        self.display_options()
        mc.showWindow()
        mc.window(
            self.window,
            e=True,
            widthHeight = self.size
            )
    def common_menu(self):
        """Create common menu items for all option boxes"""
        self.help_menu = mc.menu(label = 'Info')
        self.help_menu_item = mc.menuItem(
            label = "More info",
            command = self.help_menu_cmd
        )
    def common_buttons(self):
        """Create common buttons for all option boxes"""
        self.common_btn_size = (278,26)
        self.check_btn = mc.button(
            label = 'Check Selected',
            width = self.common_btn_size[0],
            height = self.common_btn_size[1],                         
            command = self.check_btn_cmd
        )
        self.move_btn = mc.button(
            label =  'Check And Move Selected',
            width = self.common_btn_size[0],
            height = self.common_btn_size[1],
            command = self.move_btn_cmd
        )                
        mc.formLayout(
            self.main_form,
            e= True,
            attachForm = (
                [self.check_btn,'left',5],
                [self.check_btn,'bottom',10],
                [self.move_btn,'bottom',40],
                [self.move_btn,'left',5],
                
                ),
            attachPosition = (
                [self.check_btn,'right',0,99],                        
                [self.move_btn,'right',0,99],
                )
        )
    def help_menu_cmd(self, *args):
        """Display help command"""
        mc.launch(web = 'https://github.com/GQ21') 
    def check_btn_cmd(self, *args):
        """Check button command"""
        it.intersection()
    def move_btn_cmd(self, *args):
        """Move button command"""
        self.offset = 100 / mc.floatFieldGrp(
            self.move,
            q = True,
            value = True
        )[0]      
        it.intersection(self.offset)
    def display_options(self):
        """Create option items"""
        self.xform_grp = mc.frameLayout(
                        label = 'Move Options',
                        collapsable = True
        )
        mc.formLayout(
            self.options_form,
            e = True,
            attachForm = (                
                [self.xform_grp, 'left',0],
                [self.xform_grp, 'right',0],
            )
        )
        self.xform_col = mc.columnLayout()
        self.move = mc.floatFieldGrp( 
            label = 'Offset',                      
            value1 = 10.0
        )
                
win = IT_OptionsWindow()  
win.create()
