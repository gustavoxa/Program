from flask import Flask, render_template,request
import servicio as ser

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
@aplicacion.route('/reportes')
def reportes():
    return render_template('reportes.html')
@aplicacion.route('/agregar_cambios',methods=['POST'])
def agregar_cambios():
    if request.method == 'POST':
        usuario= request.form['usuario']
        print(usuario)
        return 'recibido'
#Abrimos la aplicación central
if __name__=='__main__':
    aplicacion.run(debug=True)
    