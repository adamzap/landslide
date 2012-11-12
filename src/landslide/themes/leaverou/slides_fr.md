#Présentation de Landslide <br/> avec le modèle Lea Verou
Jean-Philippe ZIMMER - IUT Dijon-Auxerre
{: .attribution}

---

# Landslide

Lanslide permet de générer un diaporama en utilisant des diapositives simples à écrire.
La version de base utilise le modèle de diapos google.

Cette version utilise le modèle de [présentation de Lea Verou](http://leaverou.github.com/CSSS/).

Landslide a besoin du langage **python** avec les modules *jinja2*, *markdown*, et *pygments* pour fonctionner.

Sous **debian** et **ubuntu**, l'installation est réalisée avec `apt-get install landslide`. Néanmoins, la
version de l'application landslide contenue dans les dépots ne contient pas les dernières améliorations. Pour
y avoir accès vous devez suivre la procédure d'installation comme indiquée sur la page principale du dépot GitHub.

## Comment faire votre diaporama ?

- Elaborez vos diapos avec des balises simples dans le fichier *slides.md*,
- Lancez la commande `landslide leaverou.cfg`,
- Visualisez le résultat de *presentation.html*.

---

# Pourquoi utiliser la présentation Lea Verou ?

- Elle est basée sur HTML5/CSS3 et prend en compte les dernières avancées de ces standards.
- Elle a un design propre, efficace et est agréable à regarder.
- Elle est Open Source et téléchargeable sur [GitHub](https://github.com/LeaVerou/csss).
- Les déplacements sont faciles :
    - les fléches pour avancer ou reculer finement
    - CTRL fléche pour avancer ou reculer de diapo en diapo
    - HOME pour aller à la première diapo, END pour la dernière
    - CTRL G pour aller à la diapo indiquée
- La taille des contenus des pages est dynamique
- Le titre de page prend le titre de la diapo
- ...
 
---

# Pourquoi la présentation Lea Verou avec Landslide

Dans le but de réaliser une application de présentation qui pourrait remplacer des applications
classiques comme MS Powerpoint ou OO Impress, j'ai rechercher des présentations qui serait visualisables
par un navigateur.

J'ai trouvé cette présentation (et d'autre aussi disponible) basée sur HTML5/CSS3.
Cette présentation est assez simple a utiliser pour quelqu'un qui sait un peu coder en HTML. 
Néanmoins, pour un novice ou une personne réticente à la programmation, j'ai cherché une meilleure
solution pour composer les diapositives d'une présentation. 

Après avoir fait différents essais et recherches, j'ai tester avec bonheur l'application landslide.
C'est réellement l'application qu'il me fallait pour mener à bien ma réalisation. 

Le reste est un peu d'adaptation et de codage pour présenter une application simple, facile a utiliser
et réfléchir à quelques améliorations.

---

# Instructions pour le formatage Markdown

- Les instructions suivantes sont succinctes. Vous pouvez trouver [sur ce site](http://daringfireball.net/projects/markdown/syntax)
des instructions plus détaillées.
- Séparez vos diapositives avec une ligne horizontale (--- en markdown).
    - La première diapositive sera utilisée comme titre de la présentation.
    - Les autres diapositives peuvent avoir un titre.
- Les titres principaux sont marqués avec un #, les secondaires avec ##, ... 

---

# Instructions pour le formatage Markdown - 2

- Un paragraphe est composé d'une ou plusieurs phrases consécutives, 
    - Pour séparer les paragraphes, vous devez insérer une ligne blanche entre eux,
    - Pour forcer un retour à la ligne vous devez insérer au moins deux espaces à la fin de la ligne. 
- Un mot entouré de :
    - \* est affiché *gras*,
    - \*\* est affiché **italique**.
    - \` est affiché `surligné`. 
- Pour afficher des caractères de marquage ( \* , \` , \- ,... ), vous devez les précéder de \\ (AltGr-8).

---

# Instructions pour le formatage Markdown - 3

Pour surligner du code, vous devez insérer 4 espaces ou 1 tabulation en début de ligne. 

Vous pouvez aussi insérer \!lelangage avant la première ligne de code.

Premier bloc de code (\!python):

    !python
    while True:
        print "Everything's gonna be allright"

Second bloc de code (\!php):

    !php
    <?php exec('python render.py --help'); ?>

---

# Les liens avec Markdown

Un hyperlien est facilement réalisé en mettant le texte du lien entre crochets (\[ et \]) suivi
de l'adresse de l'URL entre parenthèses () . 

Par exemple : 

\[MySafeKey vous aide a sécuriser votre PC\](http://www.mysafekey.org) donne : 

[MySafeKey vous aide a sécuriser votre PC](http://www.mysafekey.org).

En suivant ce principe et en précédent d'un \! on peut aussi facilement insérer une image :

Par exemple :
\!\[MySafeKey \](./img/logomysafekey3.png) donne : ![MySafeKey](./img/logomysafekey3.png)

---

# Les listes avec Markdown

## Listes simples

Faire des listes est très simple : elles utilisent les marques \- ,\+ ou \* .
Par exemple :

    - Elément 1
    - Elément 2
        - Sous élément 2.1 (4 caractères espace à gauche de la marque)
            - Sous élément 2.1.1 (8 caractères espace à gauche de la marque)
    - Elément 3 (retour au début de ligne)


apparait :

- Elément 1
- Elément 2
    - Sous élément 2.1 (4 caractères espace à gauche de la marque)
        - Sous élément 2.1.1 (8 caractères espace à gauche de la marque)
- Elément 3 (retour au début de ligne)

---

# Les listes avec Markdown - 2
## Un ajout des styles Lea Verou

Les éléments apparaissent l'un après l'autre :

- Elément
{: .delayed}
    - Sous élément
{: .delayed}
         - Sous sous élément
{: .delayed}
- Ceci est rendu possible grâce aux extensions Markdown.
{: .delayed}
    - en insérant {: .delayed} juste sous la ligne de l'élément.
{: .delayed}

---

# Markdown est magique !

.fx: foo bar

Markdown a des extensions très puissantes et intéressantes. Vous pouvez en consulter
la liste des extensions de [Markdown sous Python](http://packages.python.org/Markdown/extensions/index.html).

Les extensions peuvent être utilisées avec Landslide grâce à l'option \-x.

## Extension attr_list

Elle permet, avec sa syntaxe, d'ajouter des attributs aux différents éléments HTML. Par exemple :

	Ceci est un paragraphe.
	{: #un_id .une_class }
	
devient

	<p id="un_id" class="une_class">Ceci est un paragraphe.</p>
	
C'est grâce à cette option que la classe "delayed" de Lea Verou vue dans la diapo précédente ou que la 
classe "attribution" de la page de titre de présentation sont utilisées.
 
Bien d'autres extensions sont possibles, vous ouvez vous reporter à la page précédemment citée.

