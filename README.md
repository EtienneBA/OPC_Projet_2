# OPC_Projet_2

Déscription du projet:

Le but du projet est de récupérer des informations pour tous les livres présents sur le site : "http://books.toscrape.com/" dans un répértoire "Datas".

Les informations concernées sont les suivantes:
-product_page_url
-universal_ product_code (upc)
-title
-price_including_tax
-price_excluding_tax
-number_available
-product_description
-category
-review_rating
-image_url

Le scrip enregistre la liste des informations obtenues pour chaque livre par catégorie (ex: Travel, Mystery, Historical Fiction etc).
Il enregistre aussi l'image de tous les livres, toujours dans le dossier "Datas". 

Environement de développement: 

Placez vous dans votre répértoire de travail en utilisant le terminal et la commande "cd".
Créez un environnement virtuel en utilisant la commande "python -m venv env".
Activez l'environnement en utilisant la commande adapté à votre système d'exploitation.
Vous trouverez dans le répértoire GitHub un fichier "requirements.txt" qui contient la liste des paquets à installer pour configurer l'environnement virtuel. 
Vous pouvez installez les paquets contenus dans le fichier "requirements.txt" en entrant dans le terminal la commande "pip install -r requirements.txt" puis "Entrée". 

Instructions pour lancer le script:

Vous pouvez maintenant lancez le script de scraping en tapant, toujours dans le terminal, la commande suivante: "python Script_scraping.py" puis "Entrée". 
Le script se lance et génère les données dans le répértoire "Datas" qu'il va créer.

Il n'y a plus qu'à récupérer les données ! 
