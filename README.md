
![alt logo](img/logo.png)


# Prérequis:

Disposer de python 3.x de préférence la version maj.

## 1. Installation:

* Cloner le depot github:

* `git clone https://github.com/lou57810/SoftDesk.git`

* Le dossier SoftDesk est créé.

## 2. Installer un environnement virtuel env:

### Windows:

* Dans la console git bash(MINGW64)

* `python -m venv env` 
 
* `source env/scripts/activate`

### Linux:

* `python3 -m venv env` 
 
* `source env/bin/activate`

## 3. Installer les modules nécéssaires:

* `pip install -r requirements.txt`

## 4. Demarrage du serveur:

`python manage.py runserver`

### * Visualisation administration de django dans le navigateur:

* `http://127.0.0.1:8000/admin/`

* username: ben

* password: ben


## 5. Test des endpoints:

### Télécharger et installer Postman:

* Création d'utilisateur (POST) `http://127.0.0.1:8000/signup/`

* Login utilisateur (POST) `http://127.0.0.1:8000/login/`

* Copier l'access Token et le recopier dans l'autorisation de la collection,

* ce qui généralisera l'accès à tous les endpoints de la collection.

* Voir la documentation jointe de postman pour les endpoints.

* [Lien Doc](https://documenter.getpostman.com/view/22746423/2s946idsAF)




 
	 
					