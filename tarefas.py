from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200))
    feita = db.Column(db.Boolean)

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET'])
def home():
    todas_tarefas = Tarefa.query.all()
    return render_template("index.html", lista_tarefas=todas_tarefas)

@app.route('/criar-tarefa', methods=['POST'])
def criar():
    tarefa = Tarefa(conteudo=request.form['conteudo_tarefa'], feita=False)
    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/tarefa-feita/<id>')
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()
    tarefa.feita = not(tarefa.feita) # troca o estado booleano da tarefa selecionada
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
