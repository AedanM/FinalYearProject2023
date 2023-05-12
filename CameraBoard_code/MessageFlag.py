

class MessageFlags:
    
    ObjectDetectedDef = (63)
    NoObjectDef = (00)
    DeactivateDef = (86)
    HumanDef = (11)
    PredatorDef = (33)
    OverrideDef = (127)
    
    def __init__(self,ODF,DF,HF,PF,NOF,ORF):
        self.ObjectDetectedFlag = ODF
        self.DeactivateFlag = DF
        self.HumanFlag = HF
        self.PredatorFlag = PF
        self.NoObjectFlag = NOF
        self.OverrideFlag = ORF
        
    def setFlags(self,message):
        
        if(message == self.OverrideDef):
            self.setFlags(self.DeactivateDef)
            self.OverrideFlag = 1
        
        if(not self.OverrideFlag == 1): 
            if(message == self.NoObjectDef):
                self.NoObjectFlag = 1
                self.ObjectDetectedFlag = 0
                self.PredatorFlag = 0
                self.HumanFlag = 0
                
                
            if(message == self.ObjectDetectedDef):
                self.ObjectDetectedFlag = 1
                self.NoObjectFlag = 0
            if(message == self.DeactivateDef):
                self.DeactivateFlag = 1
                self.ObjectDetectedFlag = 0
                self.PredatorFlag = 0
                self.HumanFlag = 0
                self.NoObjectFlag = 0
                
            if(message == self.HumanDef):
                self.PredatorFlag = 0
                self.HumanFlag = 1
                self.ObjectDetectedFlag = 1
                self.NoObjectFlag = 0
                
            if(message == self.PredatorDef):
                self.PredatorFlag = 1
                self.HumanFlag = 0
                self.ObjectDetectedFlag = 1
                self.NoObjectFlag = 0
    def flagCheck(self):
        print(f'Objects[{self.ObjectDetectedFlag}] None[{self.NoObjectFlag}] Human[{self.HumanFlag}] Predator[{self.PredatorFlag}] Deactivate[{self.DeactivateFlag}] Override[{self.OverrideFlag}]')
