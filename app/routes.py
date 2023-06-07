from app import app, render_template, request, flash

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    return render_template("extract.html")

@app.route('/products', methods=['GET', 'POST'])
def products():
    return render_template("products.html")

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/product', methods=['GET', 'POST'])
def product():
    return render_template("product.html")

@app.route('/charts', methods=['GET', 'POST'])
def charts():
    return render_template("charts.html")

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        else:
            flash('Account created!', category='success')

    return render_template("sign_up.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/name/', defaults={'name': "Anonim"})
@app.route('/name/<name>')
def name(name=None):
    return f"Hello, {name}!"