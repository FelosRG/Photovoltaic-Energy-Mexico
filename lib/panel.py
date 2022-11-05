"""
Módulo que define la clase del panel solar, así como 
la función que calcula la potencias producida.
"""

class PanelSolar:
    
    def __init__(self,G_ref,P_ref,T_ref,CT,NOCT,modelo):
        self.modelo = modelo
        self.G_ref  = G_ref
        self.P_ref  = P_ref
        self.T_ref  = T_ref
        self.NOCT   = NOCT
        self.CT     = CT / 100  # Pasamos de porcentaje a fracción
        
        assert self.CT < 0, "El coeficiente de temperatura debe de ser menor a 0"
        
    def T_panel(self,T_a,G):
        alpha = (self.NOCT - 20) / 800
        return T_a + alpha*G
        
    def potencia_producida(self,G,T):
        T_p    = self.T_panel(T,G)
        frac_G = G / self.G_ref
        a  =  1 + self.CT*(T_p - self.T_ref)
        return self.P_ref*frac_G*a