from flask import Flask, render_template, request
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../bas_flask/templates', static_folder='../bas_flask/static')

@app.route("/")
def index():
    titulo = 'Hola!'
    lista = ['Luis', 'Paco', 'Pedro']
    return render_template("index.html", titulo=titulo, lista=lista)

@app.route("/distancia", methods=["GET", "POST"])
def distancia():
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    res = 0
    
    if request.method == "POST":
        x1 = float(request.form.get("x1", 0) or 0)
        y1 = float(request.form.get("y1", 0) or 0)
        x2 = float(request.form.get("x2", 0) or 0)
        y2 = float(request.form.get("y2", 0) or 0)
        
        res = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

    return render_template("distancia.html", x1=x1, y1=y1, x2=x2, y2=y2, res=res)

@app.route("/operasbas", methods=["GET", "POST"])
def operasbas():
    n1 = 0
    n2 = 0
    res = 0
    if request.method == "POST":
        n1 = float(request.form.get("n1", 0) or 0)
        n2 = float(request.form.get("n2", 0) or 0)
        
        operacion = request.form.get("operacion")
        if operacion == "suma":
            res = n1 + n2
        elif operacion == "resta":
            res = n1 - n2
        elif operacion == "multiplicar":
            res = n1 * n2

    return render_template("operasbas.html", n1=n1, n2=n2, res=res)

@app.route("/cinepolis", methods=["GET", "POST"])
def cinepolis():
    nombre = ""
    compradores = 0
    boletos = 0
    tarjetaCine = ""
    valorPagar = 0
    mensajeError = ""

    if request.method == "POST":
        nombre = request.form.get("nombre", "")
        compradores = int(request.form.get("compradores", 0) or 0)
        boletos = int(request.form.get("boletos", 0) or 0)
        tarjetaCine = request.form.get("tarjetaCine", "no")

        if boletos > compradores * 7:
            mensajeError = "No puedes comprar más de 7 boletos por persona"
        else:
            total = boletos * 12.00

            if boletos > 5:
                total = total * 0.85  
            elif 3 <= boletos <= 5:
                total = total * 0.90  

            if tarjetaCine == "si":
                total = total * 0.90  

            valorPagar = round(total, 2)

    return render_template(
        "cinepolis.html",
        nombre=nombre,
        compradores=compradores,
        boletos=boletos,
        tarjetaCine=tarjetaCine,
        valorPagar=valorPagar,
        mensajeError=mensajeError
    )

@app.route("/hola")
def hola():
    return "<h3>Saludo desde Hola</h3>"

@app.route("/user/<string:user>")
def user(user):
    return "Hola "+ user

@app.route("/user/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1, n2):
    return "La suma es: {}".format(n1+n2)

if __name__ == "__main__":
    app.run(debug=True)