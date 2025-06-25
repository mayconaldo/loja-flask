from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loja.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text)
    imagem_url = db.Column(db.String(255))

#class Produto(db.Model):
    
#id = db.Column(db.Integer, primary_key=True)
   # nome = db.Column(db.String(100), nullable=False)
    #preco = db.Column(db.Float, nullable=False)
    #descricao = db.Column(db.String(200), nullable=False)

# Criar o banco de dados (executar 1x)
#@app.before_first_request

#def criar_tabelas():
with app.app_context():
    db.create_all()
    if not Produto.query.first():
        db.session.add_all([
        Produto(nome="Camiseta", preco=49.90, descricao="Camiseta 100% algodão"),
        Produto(nome="Tênis", preco=199.90, descricao="Tênis esportivo confortável"),
        Produto(nome="Boné", preco=29.90, descricao="Boné com estampa"),
        Produto(nome="Calça Jeans", preco=119.90, descricao="Calça jeans masculina"),
        Produto(nome="Jaqueta", preco=239.90, descricao="Jaqueta de couro sintético"),
        Produto(nome="Meias", preco=19.90, descricao="Par de meias tamanho único"),
    ])
    db.session.commit()
@app.route("/")
def index():
    produtos = Produto.query.all()
    return render_template("index.html", produtos=produtos)

@app.route("/produto/<int:produto_id>", methods=["GET", "POST"])
def produto(produto_id):
    produto_atual = Produto.query.get_or_404(produto_id)

    if request.method == "POST":
        nome = request.form["nome"]
        preco = float(request.form["preco"])
        descricao = request.form["descricao"]

        novo = Produto(nome=nome, preco=preco, descricao=descricao)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("produto", produto_id=produto_id))

    # Lista todos os produtos
    todos_produtos = Produto.query.all()

    return render_template(
        "produto_com_form.html",
        produto=produto_atual,
        todos_produtos=todos_produtos
    )

#@app.route("/produto/<int:produto_id>")
#def produto(produto_id):
    #produto = Produto.query.get_or_404(produto_id)
    #return render_template("produto.html", produto=produto)

# Simulação de carrinho simples (em memória)
carrinho = []

@app.route("/adicionar_ao_carrinho/<int:produto_id>")
def adicionar_ao_carrinho(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    carrinho.append(produto)
    return redirect(url_for("index"))

@app.route("/carrinho")
def ver_carrinho():
    total = sum(p.preco for p in carrinho)
    return f"<h1>Carrinho</h1>" + \
           "<ul>" + "".join(f"<li>{p.nome} - R$ {p.preco}</li>" for p in carrinho) + "</ul>" + \
           f"<strong>Total: R$ {total:.2f}</strong>"

@app.route("/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        nome = request.form["nome"]
        preco = float(request.form["preco"])
        descricao = request.form["descricao"]

        novo = Produto(nome=nome, preco=preco, descricao=descricao)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("novo.html")

@app.route("/")
def home():
    return render_template("meusite.html")



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
