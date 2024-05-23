import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('mabase.db')
cursor = conn.cursor()

# Création de la table Utilisateurs avec contraintes uniques
cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        contact TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role INTEGER NOT NULL,
        FOREIGN KEY(role) REFERENCES Roles(id)
    )
''')

# Création de la table Roles avec contraintes uniques
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL UNIQUE
    )
''')

# Ajout des rôles par défaut si ils n'existent pas
cursor.execute("INSERT OR IGNORE INTO Roles (nom) VALUES ('Admin')")
cursor.execute("INSERT OR IGNORE INTO Roles (nom) VALUES ('Utilisateur')")

# Création de la table Sites avec contraintes uniques
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sites (
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL,
        types TEXT NOT NULL,
        score INTEGER,
        commentaire TEXT,
        id_Formulaire INTEGER,
        FOREIGN KEY (id_Formulaire) REFERENCES Formulaire(id),
        UNIQUE(nom, types)
    )
''')

# Création de la table Formulaire avec contraintes uniques
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Formulaire (
        id INTEGER PRIMARY KEY,
        Contenu TEXT NOT NULL,
        Date DATETIME NOT NULL,
        UNIQUE(Contenu)
    )
''')

# Création de la table Tester avec clés étrangères
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tester (
        id_utilisateur INTEGER,
        id_Sites INTEGER,
        PRIMARY KEY (id_utilisateur, id_Sites),
        FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id),
        FOREIGN KEY (id_Sites) REFERENCES Sites(id)
    )
''')

# Commit des changements et fermeture de la connexion
conn.commit()
conn.close()
