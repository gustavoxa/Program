from flask import Flask, render_template

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
#Abrimos la aplicación central
if __name__=='__main__':
    aplicacion.run(debug=True)
    