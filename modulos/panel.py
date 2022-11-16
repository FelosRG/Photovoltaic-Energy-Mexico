"""
Módulo que define la clase del panel solar, así como 
la función que calcula la potencias producida.
"""
import numpy as np
import datos

explorador = datos.Explorador()

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

def gauss(x,mu,sigma):
    return np.exp((-((x - mu)**2)) / (2 * sigma**2)) / (np.sqrt(2 * np.pi * sigma**2))

def probabilidades(lat:float,lon:float,panel:PanelSolar):

    # Obtenemos key
    lat, lon = explorador.punto_cercano(lat,lon)
    key = explorador.obtener_key(lat,lon)

    datos_anuales = []
    for año in range(2000,2021):
        datos = explorador.extraer_datos(año,key)
        ghi , temp = datos.GHI.astype(np.float32) , datos.temp.astype(np.float32)
        potencia = panel.potencia_producida(ghi,temp)
        # Integramos
        energia = np.trapz(potencia,dx=1,axis=0) / 1000
        datos_anuales.append(energia)
    datos_anuales = np.array(datos_anuales)

    mean = np.mean(datos_anuales)
    std  = np.std(datos_anuales)

    # Generamos distribución
    n  = 1000
    xo = mean-5*std
    xf = mean+5*std
    dx = (xf-xo) / n

    x = np.linspace(xo,xf,n)
    y = gauss(x,mean,std)

    porcentajes = []

    # Integramos y vamos obteniendo los percentiles

    int_o = 0

    for i in range(n-2):

        int_f = int_o + np.trapz(y[i:i+2],dx=dx)
        
        if int_o < 0.05 and int_f > 0.05:
            x95 = x[i]
            porcentajes.append(x95)
            
        if int_o < 0.10 and int_f > 0.10:
            x90 = x[i]
            porcentajes.append(x90)
        
        if int_o < 0.50 and int_f > 0.50:
            x50 = x[i]
            porcentajes.append(x50)

            return porcentajes
        
        int_o = int_f


if __name__ == "__main__":

    panel = PanelSolar(
        G_ref = 1000,       # W/m2
        P_ref = 580 / 2.79, # W/m2
        T_ref = 25,         # °C
        CT    = -0.35 ,     # %/°C
        NOCT  = 45   ,      # °C
        modelo = "JAM78S30_580/MR"
    )

    #lat , lon = 18.911689, -99.174283   # Jiutepec, Morelos
    #lat , lon = 21.909747, -101.374865  # Villa arriaga, SLP
    #lat , lon = 29.174392, -111.735504  # La Ojeana, Hermosillo
    #lat , lon = 30.610468, -106.502920  # Ahumada, Chihuahua
    #lat , lon = 27.669658, -105.159317  # Cd.Camargo, Chihuahua
    lat , lon  = 19.542565, -97.323538  # Perote, Veracruz
    #lat , lon = 20.987921, -89.618171   # San ignacio, Yucatan
    #lat , lon = 29.956139, -112.642213 # Parque libertad, Sonora
    #lat , lon = 21.223955, -89.651455  # San ignacio, Yucatan
    #lat , lon = 19.581199, -97.582166 # Couyaco, Puebla
    #lat , lon = 24.0587975, -110.3228491 # Aura solar III, BCS
    #lat , lon = 23.750584, -99.099389 # Bientenario, Cd. Victoria.
    #lat , lon = 21.877004, -102.083204 # Solem I y II aguascalientes


    porcentajes = probabilidades(lat,lon,panel)

    print(f"P95: {round(porcentajes[0],2)} kWh/m2")
    print(f"P90: {round(porcentajes[1],2)} kWh/m2")
    print(f"P50: {round(porcentajes[2],2)} kWh/m2")
