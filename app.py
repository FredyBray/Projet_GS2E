from flask import Flask, render_template,request,redirect, url_for
import sqlite3
#importation de module pour la gestion des authentifications 
from werkzeug.security import generate_password_hash, check_password_hash
#importation des modules pour la gestion des session de connexion
#from flask_login import LoginManager, login_user, logout_user, login_required, current_user
#from ecoindex.compute import compute_ecoindex
#from ecoindex.analyzer import analyze_page


app = Flask(__name__)

# Définition de la clé secrète pour sécuriser les sessions
app.secret_key = 'votre_secret_key'

'''
login_manager = LoginManager()
login_manager.init_app(app)
'''



# Fonction pour attribuer un rôle par défaut à un nouvel utilisateur
def attribuer_role_par_defaut(nom, prenom, contact, email, password, role_nom='Utilisateur'):
    # Connexion à la base de données
    conn = sqlite3.connect('mabase.db')
    cursor = conn.cursor()

    # Récupération de l'ID du rôle par défaut (par exemple, l'ID de l'utilisateur simple)
    cursor.execute("SELECT id FROM Roles WHERE nom = ?", (role_nom,))
    # role = cursor.fetchone()[0]

    # Hashage du mot de passe
    password_hash = generate_password_hash(password)

    # Ajout du nouvel utilisateur avec le rôle par défaut
    cursor.execute("INSERT INTO utilisateurs (nom,prenom,contact,email,password,role) VALUES (?, ?, ?, ?, ?, ?)",
                   (nom, prenom, contact, email, password_hash, role_nom))

    # Commit des changements et fermeture de la connexion
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=['GET'])
def afficher_formulaire():
    return render_template("signup.html")


@app.route("/signup", methods=['POST'])
def inscription():
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    password = request.form['password']
    verification = request.form['verification']
    contact = request.form['contact']

    if password != verification:
        return "Les mots de passe ne correspondent pas"

    # Appel de la fonction pour attribuer le rôle par défaut
    attribuer_role_par_defaut(nom, prenom, contact, email, password,)
    

    return render_template("signin.html")


@app.route("/signin", methods=['GET'])
def afficher_form():
    return render_template("signin.html")


@app.route("/signin", methods=['POST'])
def login():
    email = request.form['email']

    password = request.form['password']

    # Vérification du mot de passe
    conn = sqlite3.connect('mabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM utilisateurs WHERE email = ?", (email,))
    result = cursor.fetchone()
#ne pas oublier d'ajoueter se paramètre dans la partie verification du mot de passe 
#role 
    conn.commit()
    conn.close()
   
      
    if result:
        password_hash = result[0]
        if check_password_hash(password_hash, password):
            return render_template('user.html')
        else:
            error = 'Mot de passe incorrect.'
            return render_template('signin.html', error=error)

    error = 'Vous vous êtes soit trompé d\'adresse email soit de mot de passe.'
    return render_template('signin.html', error=error)

@app.route("/formu", methods=['GET'])
def afficher_formu():
    return render_template("formu.html")

@app.route('/formu', methods=['POST'])
def save_site():
    # Récupération des valeurs du formulaire
    nom = request.form['nom']
    types = request.form['types']
    score = request.form['score']
    commentaire = request.form['commentaire']
    
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('mabase.db')
    cursor = conn.cursor()
    
    # Insertion des données dans la table "Sites"
    cursor.execute("INSERT INTO Sites (nom, types, score, commentaire) VALUES (?, ?, ?, ?)", 
                   (nom, types, score, commentaire))
    
    conn.commit()
    conn.close()
    
    # Redirection vers la page de liste des sites
    return render_template('user.html')

@app.route('/test')
def test():
    conn = sqlite3.connect('mabase.db')
    cursor = conn.cursor()
    
    # Récupérer les données de la table "Sites"
    cursor.execute("SELECT * FROM Sites")
    sites = cursor.fetchall()
    conn.commit()
    conn.close()
    
    return render_template('test.html', sites=sites)



    
    #return render_template("test.html")

'''
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('mabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user
    return None

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
'''
@app.route("/user")
def after_login():
    # Logique pour la page après la connexion
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)
