from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SECRET_KEY'] = 'secret-key'

db = SQLAlchemy(app)


class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    plataforma = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.String(80), nullable=False)

    def __init__(self, nome, plataforma, ano):
        self.nome = nome
        self.plataforma = plataforma
        self.ano = ano


@app.route("/")
def Index():
    all_data = Jogos.query.all()
    return render_template("index.html", employees=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        nome = request.form['nome']
        plataforma = request.form['plataforma']
        ano = request.form['ano']

        my_data = Jogos(nome, plataforma, ano)

        db.session.add(my_data)
        db.session.commit()

        flash("Jogo adicionado com sucesso")

        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Jogos.query.get(request.form.get('id'))
        my_data.nome = request.form['nome']
        my_data.plataforma = request.form['plataforma']
        my_data.ano = request.form['ano']

        db.session.commit()

        flash("Jogo atualizado com sucesso")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Jogos.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Jogo deletado com sucesso")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
