#Présentation de Landslide <br/> avec le modèle Lea Verou
Jean-Philippe ZIMMER - IUT Dijon-Auxerre - jean-philippe.zimmer@u-bourgogne.fr
{: .attribution}

---

# Landslide

Lanslide permet de générer un diaporama en utilisant des diapositives simples à écrire.
La version de base utilise le modèle de diapos google.

Cette version utilise le modèle de [présentation de Lea Verou](http://leaverou.github.com/CSSS/).

Landslide a besoin du langage **python** avec les modules *jinja2*, *markdown*, et *pygments* pour fonctionner.

Sous **debian** et **ubuntu**, l'installation est réalisée avec `apt-get install landslide`. 

## Comment faire votre diaporama ?

- Elaborez vos diapos avec des balises simples dans le fichier *slides.md*,
- Lancez la commande `landslide leaverou.cfg`,
- Visualisez le résultat de *presentation.html*.

---

# Instructions pour le formatage Markdown

- Les instructions suivantes sont succinctes. Vous pouvez trouver [sur ce site](http://daringfireball.net/projects/markdown/syntax)
des instructions plus détaillées.
- Séparez vos diapositives avec une ligne horizontale (--- en markdown).
    - Your first slide (title slide) should not have a heading, only `<p>`s
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
	
C'est grâce à cette option que la classe "delayed" de Lea Verou vue précemment est utilisée.

Bien d'autres extensions sont possibles, vous ouvez vous reporter à la page précédemment citée.

