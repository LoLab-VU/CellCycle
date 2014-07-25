"""An implementation of the model from:

Mathematical modeling of cell cycle regulation in response to DNA Damage: Exploring mechanisms of 
cell-fate determination. Kuzunari Iwamoto, Hiroyuki Hamada, Yukihiro Eguchi, Masahiro Okamoto. 
Biosystems. 2011 March, 103(2011), pp. 384-391
DOI: 10.1016/j.biosystems.2010.11.011

http://www.sciencedirect.com/science/article/pii/S0303264710002133

Implemented by: Corey Hayford
"""

from pysb import *
from pysb.util import *
from pysb.macros import *
from pysb.bng import *
from pysb.integrate import odesolve
import pylab as pl
from numpy import linspace
from sympy import sympify

Model()

def set_dna_damage(damage):
    model.parameters['DDS_0'].value = damage

def declare_monomers():
    """Declare the monomers in the Iwamoto model
    'state' is the activity state between the monomers
    'a' is the active conformation binding state
    'i' is the inactive conformation binding state
    'phos' is the phosphorylation state
    'u' is the unphosphorylated monomer
    'p' is the phosphorylated monomer
    'b' is the binding site between p## and other proteins"""
    
    Monomer("Signal")       #State can be on or off
    Monomer("SignalDamp")   #Dampens signal in Deg(t) function
        
    # **Regulatory proteins**
    
    Monomer('NF_Y')
    Monomer('CycB', ['c'])
    Monomer('Cdc25', ['b', 'state','state1', 'phos'], {'state':['i','a'], 'state1':['A','C'], 'phos':['u','p']})
    Monomer('CDK1_cyto',['phos','b','c'], {'phos':['u','p']})
    Monomer('CDK1_nuc',['phos','b','c'], {'phos':['u','p']})
    Monomer('B_Myb',['state'], {'state': ['i', 'a']})
    Monomer('APC', ['state', 'b'], {'state': ['i', 'a']})
    Monomer('Ccdc20', ['b'])
    Monomer('Ccdh1', ['b'])
    Monomer('Im')
    
def declare_parameters():
    
# ***Declare Initial Conditions***
    
    Parameter("Y5_0", 1.50)         #CDK2
    Parameter("Y6_0", 2.0)          #CycD/CDK4
    Parameter("Y11_0", 1.4)         #p27
    Parameter("Y25_0", 2.65e-2)     #p53
    Parameter("Y27_0", 0)           #ATM/ATR
    Parameter("Y28_0", 1.0e-3)      #iCdc25A
    Parameter("Y29_0", 1.0e-4)      #aCdc25A
    Parameter("Y30_0", 0.99)        #iChk1
    Parameter("Y31_0", 1.0e-2)      #aChk1
    Parameter("Y32_0", 0)           #NF_Y
    Parameter("Y33_0", 0)           #CycB
    Parameter("Y34_0", 1.0)         #CDK1
    Parameter("Y35_0", 1.0e-4)      #iCycB/CDK1_cyto
    Parameter("Y36_0", 1.0e-4)      #aCycB/CDK1_cyto
    Parameter("Y40_0", 0)           #iB-Myb
    Parameter("Y41_0", 0)           #aB-Myb
    Parameter("Y42_0", 1.0e-6)      #iCdc25C
    Parameter("Y43_0", 1.0e-6)      #aCdc25C
    Parameter("Y44_0", 3.0e-2)      #iCdc25CPs216
    Parameter("Y48_0", 0.9)         #iAPC/Ccdc20
    Parameter("Y49_0", 1.0e-1)      #aAPC/Ccdc20
    Parameter("Y50_0", 1.0e-1)      #iAPC/Ccdh1
    Parameter("Y51_0", 0.9)         #aAPC/Ccdh1
    Parameter("Y52_0", 0)           #iCycB/CDK1_nuc
    Parameter("Y53_0", 0)           #iCycB/CDK1_nuc
    
# *** Declare Kinetic Parameters ***

    Parameter("k1", 5.00e-4)
    Parameter("k5", 1.00e-1)
    Parameter("k7", 2.50e-3)
    Parameter("k8", 2.50e-5)
    Parameter("k9", 3.00e-4)
    Parameter("k11", 5.00e-4)
    Parameter("k14", 7.50e-3)
    Parameter("k15", 5.00e-3)
    Parameter("k16", 5.00e-3)
    Parameter("k17", 5.00e-2)
    Parameter("k22", 6.00e-3)
    Parameter("k26", 2.25e-2)
    Parameter("k28", 9.00e-4)
    Parameter("k29", 5.00e-5)
    Parameter("k35", 5.00e-2)
    Parameter("k38", 1.00e-3)
    Parameter("k61", 7.00e-2)
    Parameter("k81", 1.00e-3)
    Parameter("k84", 1.00e-3)
    Parameter("k85", 5.00e-3)
    Parameter("k86", 5.00e-4)
    Parameter("k89", 1.00e-3)
    Parameter("k90", 5.00e-4)
    Parameter("k91", 2.00e-2)
    Parameter("k92", 5.00e-3)
    Parameter("k93", 1.25e-3)
    Parameter("k94", 2.50e-4)
    Parameter("k95", 5.00e-2)
    Parameter("k96", 1.00e-4)
    Parameter("k97", 5.00e-3)
    Parameter("k98", 5.00e-3)
    Parameter("k103", 2.25e-2)
    Parameter("k104", 1.75e-4)
    Parameter("k105", 5.00e-2)
    Parameter("k106", 5.00e-2)
    Parameter("k107", 2.00e-3)
    Parameter("k109", 1.00e-2)
    Parameter("k111", 1.00e-3)
    Parameter("k113", 1.00e-3)
    Parameter("k114", 1.00e-4)
    Parameter("k116", 1.00e0)
    Parameter("k122", 5.00e-3)
    Parameter("k123", 1.00e-2)
    Parameter("k124", 1.00e-2)
    Parameter("k125", 5.00e-3)
    Parameter("k128", 1.00e-3)
    Parameter("k129", 3.00e-1)
    Parameter("k131", 1.00e-2)
    Parameter("k132", 5.00e-5)
    Parameter("k133", 5.00e-4)
    Parameter("k134", 1.00e-2)
    Parameter("k135", 5.00e-3)
    Parameter("k136", 5.00e-3)
    Parameter("k137", 3.00e-2)
    
### ** Initial Conditions **
def declare_initial_conditions():
      
    Initial(CDK2(phos='u',b=None,c=None), Y5_0)
    Initial(CycD(c=1) % CDK4(phos='p', b=None, c=1), Y6_0)
    Initial(p27(b=None), Y11_0)
    Initial(p53(b=None), Y25_0)
    Initial(ATM_ATR(b=None), Y27_0)
    Initial(Cdc25(b=None, state='i', state1='A', phos= 'u'), Y28_0) # added state1 = 'A'
    Initial(Cdc25(b=None, state='a', state1='A', phos= 'u'), Y29_0) # added state1 = "A"
    Initial(Chk1(phos='u'), Y30_0) #'u'= inactive
    Initial(Chk1(phos='p'), Y31_0) #'p' = active
    Initial(NF_Y(), Y32_0) # Not sure
    Initial(CycB(c=None), Y33_0)
    Initial(CDK1(phos='u', b=None, c=None), Y34_0)
    Initial(CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1), Y35_0)
    Initial(CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1), Y36_0)
    Initial(B_Myb(state='i'). Y40_0)
    Initial(B_Myb(state='a'), Y41_0)
    Initial(Cdc25(b=None, state='i', state1='C', phos= 'u'), Y42_0) # added state1 = 'C'
    Initial(Cdc25(b=None, state='a', state1='C', phos= 'u'), Y43_0) # added state1 = 'C'
    Initial(Cdc25(b=None, state='i', state1='C', phos= 'p'), Y44_0) # added state1 = 'C'
    Initial(Cdc25(b=None, state='a', state1='C', phos= 'p'), Y45_0) # added state1 = 'C'
    Initial(APC(state='i', b=1) % Ccdc20(b=1), Y48_0)
    Initial(APC(state='a', b=1) % Ccdc20(b=1), Y49_0)
    Initial(APC(state='i', b=1) % Ccdh1(b=1), Y50_0)
    Initial(APC(state='a', b=1) % Ccdh1(b=1), Y51_0)
    Initial(CycB(c=1) % CDK1_nuc(phos='u', b=None, c=1), Y52_0)
    Initial(CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1), Y53_0)

### ** Declare Observables **
def declare_observables():
    
    Observable("OBS_p27", p27(b=None))
    Observable("OBS_CycE", CycE(c=None))
    Observable("OBS_aCycE_CDK2", CycE(c=1) % CDK2(phos='p', b=None, c=1))
    Observable("OBS_CycA", CycA(c=None))
    Observable("OBS_CycB", CycB(c=None))
    Observable("OBS_APC_Ccdc20", APC(state='a', b=1) % Ccdc20(b=1)) # state= 'a', 'i', both?

### ** Functions **
def declare_functions():
#     
#     Expression("create_p16", sympify("k41/((One + k42*OBS_Rb) - (k43*OBS_p16 + k44*OBS_p16*OBS_CycD_CDK46))"))
#     Expression("create_Rb", sympify("k58/(One + k59*OBS_p16)"))
    Expression("create_Mdm2", sympify("k66*OBS_Im**50/(k65**50 + OBS_Im**50)"))
#     Expression("create_Int", sympify("(k70*OBS_p53*signal)/(One + k71*OBS_p53*OBS_Mdm2)"))
#     Expression("sig_deg", sympify("k74 - k73*(signal-signal_damp)"))
#     Expression("kdamp_DDS0", sympify("k75*DDS_0"))
    
### ** Rules **
def declare_rules():
    
## *** New Terms *** ##    
    Rule('E2F_Create_CycA', E2F(b=None) >> E2F(b=None) + CycA(c=None), k130)
    Rule('NF_Y_Create_CycA', NF_Y() >> NF_Y() + CycA(c=None), k75)
    Rule('aAPC_Ccdc20_Create_CycA', CycA(c=None) + APC(state='a', b=1) % Ccdc20(b=1) >> APC(state='a', b=1) % Ccdc20(b=1), k126)
    Rule('aAPC_Ccdh1_Create_CycA', CycA(c=None) + APC(state='a', b=1) % Ccdh1(b=1) >> APC(state='a', b=1) % Ccdh1(b=1), k127)
    Rule('iAPC_Ccdc20_Degrade_CycA', CycA(c=1) % CDK2(phos='u', b=None, c=1) + APC(state='i', b=1) % Ccdc20(b=1) >> CDK2(b=None, c=None) + APC(state='i', b=1) % Ccdc20(b=1), k15)
    Rule('aAPC_Ccdc20_Degrade_CycA', CycA(c=1) % CDK2(phos='p', b=None, c=1) + APC(state='a', b=1) % Ccdc20(b=1) >> CDK2(b=None, c=None) + APC(state='a', b=1) % Ccdc20(b=1), k14)
    Rule('iAPC_Ccdh1_Degrade_CycA', CycA(c=1) % CDK2(phos='u', b=None, c=1) + APC(state='i', b=1) % Ccdh1(b=1) >> CDK2(b=None, c=None) + APC(state='i', b=1) % Ccdh1(b=1), k15)
    Rule('aAPC_Ccdh1_Degrade_CycA', CycA(c=1) % CDK2(phos='p', b=None, c=1) + APC(state='a', b=1) % Ccdh1(b=1) >> CDK2(b=None, c=None) + APC(state='a', b=1) % Ccdh1(b=1), k14)
    Rule('aCdc25A_Activate_CycE_CDK2', CycE(c=1) % CDK2(phos='u', b=None, c=1) + Cdc25(b=None, state='a', state1='A', phos= 'u') >> CycE(c=1) % CDK2(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='A', phos= 'u'), k22)
    Rule('aCdc25A_Activate_CycA_CDK2', CycA(c=1) % CDK2(phos='u', b=None, c=1) + Cdc25(b=None, state='a', state1='A', phos= 'u') >> CycA(c=1) % CDK2(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='A', phos= 'u'), k28)
    Rule('p27_CycD_CDK4_Degrade_CycD_CDK4', CycD(c=2) % CDK4(phos='p',b=1,c=2) % p27(b=1) >> p27(b=None), k21)
    Rule('Create_p21_CycB_CDK1', p21(b=None) + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) >> CycB(c=2) % CDK1(phos='p',b=1,c=2) % p21(b=1), k103) #Rate Constant
    Rule('ATM_ATR_Create_p53', ATM_ATR(b=None) >> p53(b=None), k61)
    Rule('Create_Mdm2', None >> Mdm2(), create_Mdm2)
    Rule('Degrade_ATM_ATR', ATM_ATR(b=None) >> None, k79) #Rate Constant
    Rule('E2F_Create_iCdc25A', E2F(b=None) >> E2F(b=None) + Cdc25(b=None, state='i', state1='A', phos= 'u'), k80)
    Rule('Deactivate_aCdc25A', Cdc25(b=None, state='a', state1='A', phos= 'u') >> Cdc25(b=None, state='i', state1='A', phos= 'u'), k55) #Rate Constant
    Rule('aChk1_Degrade_iCdc25A', Chk1(phos='p') + Cdc25(b=None, state='i', state1='A', phos= 'u') >> Chk1(phos='p'), k81) #Rate Constant
    Rule('aCycE_CDK2_Activate_Cdc25A', CycE(c=1) % CDK2(phos='p',b=None,c=1) + Cdc25(b=None, state='i', state1='A', phos= 'u') >> CycE(c=1) % CDK2(phos='p',b=None,c=1) + Cdc25(b=None, state='a', state1='A', phos= 'u'), k82)
    Rule('aCycA_CDK2_Activate_Cdc25A', CycA(c=1) % CDK2(phos='p',b=None,c=1) + Cdc25(b=None, state='i', state1='A', phos= 'u') >> CycA(c=1) % CDK2(phos='p',b=None,c=1) + Cdc25(b=None, state='a', state1='A', phos= 'u'), k82)
    Rule('aChk1_Degrade_aCdc25A', Chk1(phos='p') + Cdc25(b=None, state='a', state1='A', phos= 'u') >> Chk1(phos='p', k84)) #Rate Constant
    Rule('Degrade_aCdc25', Cdc25(b=None, state='a', state1='A', phos= 'u') >> None, k85) #Rate Constant
    Rule('Degrade1_aCdc25', Cdc25(b=None, state='a', state1='A', phos= 'u') >> None, k86) #Rate Constant
    Rule('p21_CycB_CDK1_Degrade_p21', CycB(c=2) % CDK1(phos='p',b=1,c=2) % p21(b=1) >> CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1), k104) #Rate Constant
    Rule('aCycB_CDK1_cyto_Activate_Cdc25C', CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + Cdc25(b=None, state='i', state1='C', phos='u') >> CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='u'), k110)
    Rule('aCycB_CDK1_nuc_Activate_Cdc25C', CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) + Cdc25(b=None, state='i', state1='C', phos='u') >> CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='u'), k110)
    Rule('aChk1_Phos_iCdc25C', Chk1(phos='p') + Cdc25(b=None, state='i', state1='C', phos='u') >> Chk1(phos='p') + Cdc25(b=None, state='a', state1='C', phos='p'), k111) #Rate Constant
    Rule('Degrade1_aCdc25C', Cdc25(b=None, state='a', state1='C', phos='u') + Cdc25(b=None, state='a', state1='C', phos='u') >> None, k109)
    Rule('aChk1_Degrade_aCdc25C', Cdc25(b=None, state='a', state1='C', phos='u') + Chk1(phos='u') >> Chk1(phos='u'), k113)
    Rule('Degrade2_aCdc25C', Cdc25(b=None, state='a', state1='C', phos='u') >> None, k114)
    Rule('aCycB_CDK1_cyto_Activate_Cdc25CPs216', Cdc25(b=None, state='i', state1='C', phos='p') + CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) >> CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='p'), k116)
    Rule('aCycB_CDK1_nuc_Activate_Cdc25CPs216', Cdc25(b=None, state='i', state1='C', phos='p') + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) >> CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='p'), k116)
    Rule('Wee1_Deactivate_CycB_CDK1_nuc', CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) + Wee1(phos='u') >> CycB(c=1) % CDK1_nuc(phos='u', b=None, c=1) + Wee1(phos='u'), k133) #Rate Constant
    Rule('aCdc25C_Activate_CycB_CDK1_nuc', CycB(c=1) % CDK1_nuc(phos='u', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='u') >> CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='u'), k134) #Rate Constant
    Rule('aCdc25CPs216_Activate_CycB_CDK1_nuc', CycB(c=1) % CDK1_nuc(phos='u', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='p') >> CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='p'), k134) #Rate Constant
    Rule('aAPC_Ccdc20_Degrade_iCycB_CDK1_nuc', APC(state='a', b=1) % Ccdc20(b=1) + CycB(c=1) % CDK1_nuc(phos='u', b=None, c=1) >> APC(state='a', b=1) % Ccdc20(b=1), k136)
    Rule('aAPC_Ccdc20_Degrade_aCycB_CDK1_nuc', APC(state='a', b=1) % Ccdh1(b=1) + CycB(c=1) % CDK1_nuc(phos='u', b=None, c=1) >> APC(state='a', b=1) % Ccdh1(b=1), k136)
    Rule('aAPC_Ccdh1_Degrade_iCycB_CDK1_nuc', CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) >> CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1), k131)
    Rule('aAPC_Ccdh1_Degrade_aCycB_CDK1_nuc', APC(state='a', b=1) % Ccdc20(b=1) + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) >> APC(state='a', b=1) % Ccdc20(b=1), k135)
    Rule('aCycB_CDK1_cyto_Create_aCycB_CDK1_nuc', APC(state='a', b=1) % Ccdh1(b=1) + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) >> APC(state='a', b=1) % Ccdh1(b=1), k137)
    
## *** New Species *** ##
    Rule('aCycA_CDK2_Create_NF_Y', CycA(c=1) % CDK2(phos='p', b=None, c=1) >> CycA(c=1) % CDK2(phos='p', b=None, c=1) + NF_Y(), k89)
    Rule('Degrade_NF_Y', NF_Y() >> None, k90)
    Rule('NF_Y_Create_CycB', NF_Y() >> NF_Y() + CycB(c=None), k91)
    Rule('iCycB_CDK1_cyto_Degrade_CDK1', CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1) >> CycB(c=None), k95)
    Rule('Degrade_CycB', CycB(c=None) >> None, k92)
    Rule('CycB_CDK1_Create CycB_CDK1_cyto', CycB(c=None) + CDK1(phos='u', b=None, c=None) >> CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1), k93)
    Rule('aAPC_Ccdc20_Degrade_CycB', CycB(c=None) + APC(state='a', b=1) % Ccdc20(b=1) >> APC(state='a', b=1) % Ccdc20(b=1), k128)
    Rule('aAPC_Ccdh1_Degrade_CycB', CycB(c=None) + APC(state='a', b=1) % Ccdh1(b=1) >> APC(state='a', b=1) % Ccdh1(b=1), k129)
    Rule('iCycB_CDK1_cyto_Degrade_CycB', CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1) >> CDK1(phos='u', b=None, c=None), k94)
    Rule('aAPC_Ccdc20_Degrade_iCycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1) + CycB(c=None) + APC(state='a', b=1) % Ccdc20(b=1) >> CDK1(phos='u', b=None, c=None) + CycB(c=None) + APC(state='a', b=1) % Ccdc20(b=1), k97)
    Rule('aAPC_Ccdh1_Degrade_iCycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1) + CycB(c=None) + APC(state='a', b=1) % Ccdh1(b=1) >> CDK1(phos='u', b=None, c=None) + CycB(c=None) + APC(state='a', b=1) % Ccdh1(b=1), k97)
    Rule('aAPC_Ccdc20_Degrade_aCycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + CycB(c=None) + APC(state='a', b=1) % Ccdc20(b=1) >> CDK1(phos='u', b=None, c=None) + CycB(c=None) + APC(state='a', b=1) % Ccdc20(b=1), k98)
    Rule('aAPC_Ccdh1_Degrade_aCycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + CycB(c=None) + APC(state='a', b=1) % Ccdh1(b=1) >> CDK1(phos='u', b=None, c=None) + CycB(c=None) + APC(state='a', b=1) % Ccdh1(b=1), k98)
    Rule('Deactivate_CycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) >> CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1), k96)
    Rule('aCdc25C_Activate_CycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='u') >> CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='u'), k95)
    Rule('aCdc25CPs216_Activate_CycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='u', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='p') >> CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) + Cdc25(b=None, state='a', state1='C', phos='p'), k95)
    Rule('aCycB_CDK1_nuc_to_cyto', CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) >> CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1), k132)
    Rule('Degrade_aCycB_CDK1_cyto', CycB(c=1) % CDK1_cyto(phos='p', b=None, c=1) >> None, k96)
    Rule('E2F_Create_iB_Myb', E2F(b=None) >> B_Myb(state='i'), k105)
    Rule('aCycA_CDK2_Activate_B_Myb', CycA(c=1) % CDK2(phos='p', b=None, c=1) + B_Myb(state='i') >> CycA(c=1) % CDK2(phos='p', b=None, c=1) + B_Myb(state='a'), k106)
    Rule('Degrade_aB_Myb', B_Myb(state='a') >> None, k107)
    Rule('aAPC_Ccdh1_Deactivate_APC_Ccdc20', APC(state='a', b=1) % Ccdc20(b=1) + APC(state='a', b=1) % Ccdh1(b=1) >> APC(state='i', b=1) % Ccdc20(b=1) + APC(state='a', b=1) % Ccdh1(b=1), k122)
    Rule('aCycB_CDK1_nuc_Activate_APC_Ccdc20', APC(state='i', b=1) % Ccdc20(b=1) + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) >> APC(state='a', b=1) % Ccdc20(b=1) + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1), k123)
    Rule('aCycB_CDK1_nuc_Deactivate_APC_Ccdh1', APC(state='a', b=1) % Ccdh1(b=1) + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1) >> APC(state='i', b=1) % Ccdh1(b=1) + CycB(c=1) % CDK1_nuc(phos='p', b=None, c=1), k124)
    Rule('aCycA_CDK2_Deactivate_APC_Ccdh1', APC(state='a', b=1) % Ccdh1(b=1) + CycA(c=1) % CDK2(phos='p', b=None, c=1) >> APC(state='i', b=1) % Ccdh1(b=1) + CycA(c=1) % CDK2(phos='p', b=None, c=1), k124)
    Rule('Activate_APC_Ccdh1', APC(state='i', b=1) % Ccdh1(b=1) >> APC(state='a', b=1) % Ccdh1(b=1), k125)