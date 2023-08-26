from flask import Flask, render_template,request,redirect,url_for,jsonify
import servicio as ser
import metodos as met
import aspose.pdf as ap
#Vlan = ser.Servicio('cisco','cisco12345','10.10.10.1')
#Vlan.Vlan_interface("Vlan1002",'20.20.20.20','255.255.0')

aplicacion=Flask(__name__)
#Rutas de la aplicación web, pagina principal
@aplicacion.route('/')
def principalr():
    return render_template('index.html')
#Rutas de la aplicación web, pagina de configuraciones
@aplicacion.route('/configuracion')
def configuracion():
    return render_template('configuraciones.html')
#Rutas de la aplicación web, pagina de informacion
@aplicacion.route('/informacion')
def informacion():
    return render_template('informacion.html')
#Rutas de la aplicación web, pagina de informacion
@aplicacion.route('/reportes',methods=['GET','POST'])
def reportes():
    return render_template('reportes.html')

#Metodos para ingresar datos
@aplicacion.route('/agregarnombre',methods=['POST'])
def agregarnombre():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        direccionip = request.form['direccionip']
        nombreDispositivo = request.form['nombreDispositivo']
        print(f"El usuario es  {usuario} y la contraseña es {contrasenia} ademas se ingreso el nombre de loockbackp{nombreDispositivo} y la direccion IP es  {direccionip}")
        nombre = ser.Servicio(usuario,contrasenia,direccionip)
        print(nombre.Nombre_dispositivo(nombreDispositivo))
        return redirect(url_for('configuracion'))   
@aplicacion.route('/agregarVlan', methods=['POST'] ) 
def agregarVlan():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        direccionip = request.form['direccionip']
        nombreVlan = request.form['nombreVlan']
        direccionipVlan = request.form['direccionipVlan']
        mascaraVlan = request.form['mascaraVlan']
        vlan = ser.Servicio(usuario,contrasenia,direccionip)
        vlan.Vlan_interface(nombreVlan,direccionipVlan,mascaraVlan)
        return redirect(url_for('configuracion'))
@aplicacion.route('/agregarDHCP',methods=['GET','POST'])
def agregarDHCP():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        direccionip = request.form['direccionip']
        ipmaxexcluida = request.form['Ipmaxexcluida']
        ipminexcluida = request.form['Ipminexcluida']
        nombredhcp = request.form['NombreDHCP']
        gateway = request.form['Gateway']
        direccionred = request.form['DireccionRed']
        mascarared = request.form['MascaraRed']
        dhcp = ser.Servicio(usuario,contrasenia,direccionip)
        dhcp.Configuracion_DHCP(ipminexcluida,ipmaxexcluida,nombredhcp,gateway,mascarared,direccionred)
        return redirect(url_for('configuracion'))
@aplicacion.route('/agregarloopback', methods=['GET', 'POST'])
def agregaloopback():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        direccionip = request.form['direccionip']
        nombreloopback = request.form['nombreloockback']
        iploopback = request.form['direccioniploockback']
        mascaraloopback = request.form['mascaraloocback']
        loopback = ser.Servicio(usuario,contrasenia,direccionip)
        loopback.Interfaces_loopback(nombreloopback,iploopback,mascaraloopback)
        return redirect(url_for('configuracion'))
    
@aplicacion.route('/agregarSNMP', methods=['GET','POST'])
def agregarSNMP():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        direccionip = request.form['direccionip']
        nombresnmp = request.form['nombresnmp']
        opcion = request.form['opcionsnmp']
        print(opcion)
        snmp = ser.Servicio(usuario,contrasenia,direccionip)
        snmp.Snmp(nombresnmp,opcion)
        return redirect(url_for('configuracion'))                        
    
@aplicacion.route('/agregarIP', methods=['GET','POST'])
def agregarIP():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        direccionip = request.form['direccionip']
        interfazurl = request.form['interfaz']
        direccionipinterfaz = request.form['direccionipInterfaz']
        mascarainterfaz = request.form['mascaraInterfaz']
        if interfazurl == 'GigabitEthernet0%2F0%2F0':
            interfazcambio = 'GigabitEthernet0/0/0'
        else:
            interfazcambio = 'GigabitEthernet0/0/1'
        interfaz = ser.Servicio(usuario,contrasenia,direccionip)
        interfaz.interface(interfazurl,interfazcambio,direccionipinterfaz,mascarainterfaz)
        return redirect(url_for('configuracion'))                        


#Metodos para mostrar resultados
@aplicacion.route('/consultar', methods=['GET','POST'] )
def consultar():
    global mensaje
    global encabezado
    if request.method == 'POST':
        nombre = request.form["usuario"]
        contrasenia = request.form["contrasenia"]
        direccionip = request.form['direccionip']
        opcion = request.form["opcion"]
        consulta = ser.Servicio(nombre,contrasenia,direccionip)
        print(opcion)
        match opcion:
             case '1':
                encabezado ='El nombre del equipo es: '
                mensaje = consulta.Opciones_show(1)
                print(mensaje)
             case '2':
                encabezado = 'Las interfaces  fisicas son: '
                mensaje = consulta.Opciones_show(3)
             case '3':
                encabezado = 'Las vlans son: '
                mensaje = consulta.Opciones_show(6)

             case '4':
                encabezado = 'Los DHCP disponibles son: '
                mensaje = consulta.Opciones_show(2)
             case '5':
                encabezado = 'Las direcciones IP'
             case '6': 
                encabezado = 'Comunidades SNMP: '
                mensaje = consulta.Opciones_show(11)        
             case _:
                mensaje='Error' 
    return jsonify({'Respuesta':[encabezado,mensaje]}) 
#Metodos para generar reportes
@aplicacion.route('/exporpdf', methods=['GET','POST'] )
def exporpdf():
    
    if request.method == 'POST':
       
        nombre = request.form["usuario"]
        contrasenia = request.form["contrasenia"]
        direccionip = request.form['direccionip']
        opcion = request.form['Opcion']
        conexion=ser.Servicio(nombre,contrasenia,direccionip)
        match opcion:
             case '1':
                reporte1=conexion.Opciones_show(4)
                imprimirpdf(reporte1,'configuracion')
             case '2':
                reporte1=conexion.Opciones_show(8)
                reporte2=conexion.Opciones_show(9)
                reporte3=conexion.Opciones_show(10)
                reportef=reporte1+reporte2+reporte3
                print('terminado')
                imprimirpdf(reportef,'estadodispositivo')
             case '3':
                reporte4=conexion.Opciones_show(7)
                imprimirpdf(reporte4,'Vecinos')
        pdfmensaje = 'Guardado'
                
    return jsonify({'Respuesta':[pdfmensaje]})

def imprimirpdf(texto,nombre):
    pdf = nombre+'.pdf'
    print(pdf)
    document = ap.Document()
    page = document.pages.add()
    a=''
    for i in texto:
        if (  i !="," and i != "[" and i!="]"):
           if(i != "{" and i != "}"):
               a=a+i
        else:
        #print(a)
            text_fragment = ap.text.TextFragment(a)
            page.paragraphs.add(text_fragment)
            a=""
    document.save(pdf)        


#Abrimos la aplicación central
if __name__=='__main__':
    aplicacion.run(debug=True)

    