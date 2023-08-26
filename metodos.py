import servicio as serv
class Metodos:

    def Limpiado_respuesta(cadena):
        cadena=cadena+":"
        b={}
        a=""
        cont2=1
        for i in cadena:
            if ( i != ":" and i !="," and i != "[" and i!="]"):
                if(i != "{" and i != "}"):
                    a=a+i
            else:
                b[cont2]=a
                cont2=cont2+1
                a=""
        return b
                
    def Devolver_nombre(self):
        usuario = serv.Servicio(self.Usuario,self.Contrasenia,self.Ip)
        respuesta_string = usuario.Opciones_show(1)
        vector_respuesta={}
        vector_respuesta=self.Limpiado_respuesta(respuesta_string)
        mensaje="El nombre del dispositivo es: " +vector_respuesta[3]
        return mensaje
    def Devolver_dns(self):
        dns= serv.Servicio(self.Usuario,self.Contrasenia,self.Ip)
        respuest_string = dns.Opciones_show(2)
        return respuest_string 
    def Devolver_interfaces(self):
        interface= serv.Servicio(self.Usuario,self.Contrasenia,self.Ip)
        respuesta_string= interface.Opciones_show(3)
        vector_respuesta=self.Limpiado_respuesta(respuesta_string)
        return vector_respuesta

#metodos=Metodos('admin','cisco12345','10.10.10.1')
#mensaje=metodos.Devolver_nombre()
#print(mensaje)