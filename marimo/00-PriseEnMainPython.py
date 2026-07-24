import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction au langage Python {#sec-chap00}

    Dans ce chapitre, nous présentons quelques éléments essentiels du langage Python qui nous seront utiles dans ce manuel. Python est un langage très riche et peut aboutir à des projets logiciels très sophistiqués. Il est important de comprendre que la programmation Python n'est pas ici une fin en soi, mais plutôt un outil de scriptage et de manipulation des données satellitaires.

    <div style="border:0.5px solid silver;border-left:.3rem solid #00796d;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2efec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADfUlEQVRYhb2XMXLbMBBFnzVKkSZ0ylRmJkVKMycwfQIrJzB9AVruMsNGLlCHwQVC3UC+AXUC02WKTOQ+hXGAjFNgIYIQZNkZxzvD4UhY7H7s/l0s9+7v73msJFWZAzmQAfvBcidPa5RePdbm3i4ASVWmwBQogOSRdpdAY5RuIvb2gX0H8kEASVXOxHkCGGAhT2uUvgt0M2x0CuBQ/r4BCqN05+m0wMQo3QKMtzjOgEYMGeAsdhpfxEkH1BK1GjhBUuU5H0RxIwKB4pWcYHDax0pSlalRehVxfiFghwACxQujdP0vjgMQ0ZOLfBt7ivvYsCc8EHLRy7GV4OQOy4su0C2wqYg5PzNKNz4HZticz7ewNxWd0xgw0bkFZt7+mHODTesCYCQbM+AcuMWyPjQ8websVHQugWPvOQPmwAE9CQFWEee5cw7CgaQqF1jGHrvy8JwXwHf5+SAvPMd32HI98pZvsOW3SqqyBmqj9Gokm06A24jzFBtGA3zaRUqvA7bifAm8xUYpF+c5NtozsH0gl00x4w09KdcEEyIW9O24M0ovAsbPjdKFB8iBbJOqNMDEAZjI2jov4iRzp/BJuY3ZSVX+AN4Bb5BUiY3CKB3yagGcJlWZjYAUMJELxAFbR0ZSsuYDfXh/Ah+B19ho1d7eczallXc2wpZeF1HKA2WQvAFTo3QtHbIAPgB/gFeB/p0AzxnKSt7pKOJ4IEEbTrHRasRwgy3NG+CLp+MkdrCB7ASwQ3Is03Pgd2R95x2yE4Aw3skKSKQxYZROjdK5RGnq6TgJh5YNGWPDl0XWWmwVTLDlCH0rbmRWWIiTGsulq4DMDmgb2E4d2JF3qjRQcmVZuD/E+Jn8/Ar8Aq7pm85aV4h3iL3SQ8nl3Y08RxNfQxrPEjiS2nf/N3KCC+ydcAl89lLhpA7eIQBjlO7G9GUzjSgX9FNO57qhOHroTmjoU9IGaxPspTUHGElY58BBWK+y5mbC66QqN27KwHiaVKW7NW/wUuKJs1FDfxtm2FzeAllk4HRETESnYdhwUmxY3awQHeW8m3VplM7XAGTRtU3/Ehmcjh0DiYDzB5JwfyeHeL8xlku9t9jcPctIFuxxtgczxUsMpb7zjej+77E8x5Z5OB9sByAbU9noPkymuz5MIvvdhwnApVF6FtN90U+zJwPwTvNsH6dPBhCAyXnmz/O/0JrtInNZu4wAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Objectifs d’apprentissage visés dans ce chapitre</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    À la fin de ce chapitre, vous devriez être en mesure de :

    <ul>
    <li>connaître les principales distributions de Python;</li>
    <li>installer un environnement d’exécution du code de cet ouvrage;</li>
    <li>comprendre les structures de base du langage Python (listes, tuples, ensembles, dictionnaires);</li>
    <li>écrire des boucles, des conditions et des fonctions;</li>
    <li>aborder la programmation orientée objet;</li>
    <li>manipuler un tableau <code>NumPy</code>.</li>
    </ul>
    </div>
    </div>

    Ce chapitre est aussi disponible sous la forme d'un notebook Python sur Google Colab :

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/00-PriseEnMainPython.ipynb)

    Python, créé par [Guido van Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum) en 1991, est un langage de programmation polyvalent et facile à apprendre, souvent comparé à un couteau suisse numérique pour sa simplicité et sa polyvalence. Comme un outil multifonction, Python peut être utilisé pour une variété de tâches, du développement web à l'analyse de données, en passant par l'intelligence artificielle.

    ## Les distributions

    Il existe plusieurs [distributions](https://wiki.python.org/moin/PythonDistributions) du langage Python, ces distributions sont comme différentes saveurs de votre glace préférée - chacune a ses propres caractéristiques uniques, mais elles sont toutes fondamentalement Python. Voici un aperçu des principales distributions :

    | Distribution | Description | Idéale pour |
    |---|---|---|
    | [CPython](https://www.python.org/downloads/) | L'implémentation officielle « vanille » | La compatibilité et la conformité aux standards |
    | [Anaconda](https://www.anaconda.com/download) | Livrée avec de nombreuses bibliothèques scientifiques | L'analyse de données et l'apprentissage automatique (*machine learning*) |
    | [Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) | Version légère ; on ajoute les bibliothèques au besoin | Un environnement minimal et contrôlé |
    | [PyPy](https://pypy.org/) | Implémentation optimisée pour la vitesse d'exécution | Les programmes gourmands en calcul |

    Chaque distribution a ses forces, que ce soit la simplicité, la vitesse ou des fonctionnalités spécifiques. Le choix dépend donc de vos besoins, comme choisir entre une glace simple ou une glace royale (banana split) élaborée.

    ## Les styles de programmation en Python

    Il existe plusieurs approches pour programmer en Python. La plus directe est en version interactive en tapant `python` et de rentrer des commandes ligne par ligne.

    ### Les outils de programmation

    Un code python prend la forme d'un simple fichier texte avec l'extension `.py` et peut être modifié avec un simple éditeur de texte. Cependant, il n'y aura pas de rétroactions immédiates de l'interpréteur Python, ce qui rend la correction d'erreurs (débogage) beaucoup plus laborieux.

    Un IDE (*Integrated Development Environment*) est comme une boîte à outils complète pour les programmeurs, vous trouverez :

    -   Un éditeur de texte amélioré pour écrire votre code, avec des fonctionnalités comme la coloration syntaxique qui rend le code plus lisible.

    -   Un interpréteur qui exécute votre code ligne par ligne.

    -   Un débogueur pour trouver et corriger les erreurs, tel un détective numérique.

    -   Des outils d'automatisation qui effectuent des tâches répétitives, comme un assistant virtuel pour le codage.

    -   L'accès à la documentation des différentes librairies.

    Ces outils intégrés permettent aux développeurs de travailler plus efficacement, en passant moins de temps à jongler entre différentes applications et plus de temps à produire du code.

    Voici quelques options populaires :

    | Outil | Type | Points forts |
    |---|---|---|
    | [PyCharm](https://www.jetbrains.com/pycharm/) | IDE complet | Autocomplétion, débogage intégré ; idéal pour les grands projets (gourmand en ressources) |
    | [Visual Studio Code](https://code.visualstudio.com/) | Éditeur extensible | Gratuit, léger, personnalisable par extensions |
    | [Spyder](https://www.spyder-ide.org/) | IDE scientifique | Libre et gratuit, orienté calcul scientifique |
    | [Jupyter](https://jupyter.org/) | Notebook | Mélange code, texte et visualisations ; gratuit sur Colab/Kaggle (reproductibilité limitée) |
    | [Marimo](https://marimo.io/) | Notebook réactif | Réexécute automatiquement les cellules dépendantes ; évite l'état caché |

    ## Bonnes pratiques

    Python est un langage très dynamique, qui évolue constamment. Cela pose certains défis pour la gestion du code à long terme. Il est fortement conseillé d'utiliser des environnements virtuels pour gérer vos différentes bibliothèques (*libraries*). Voici quelques bonnes pratiques à suivre :

    1.  **N'installez pas la toute dernière version de Python** : Il est recommandé d'installer 1 ou 2 version antérieure, par exemple si 3.13 est [la version plus récente](https://www.python.org/downloads/), installer plutôt la version 3.11. Les versions trop récentes peuvent être instables. La version de python désirée peut être spécifiée au moment de la création d'un environnement virtuel (voir plus bas). Vous pouvez afficher la liste des versions de python avec la commande `conda search --full-name python`.

    2.  **N'utilisez pas de version obsolète de Python**. Cela peut sembler contradictoire avec le point précédent mais c'est l'excès inverse. Si vous utilisez une version trop ancienne alors toutes vos librairies cesseront d'évoluer et peuvent devenir obsolètes.

    3.  **Utilisez des environnements virtuels**. Pensez-y comme à des compartiments séparés pour chaque projet. Cela évite les conflits entre les différentes versions de bibliothèques (*libraries*) et garde votre système propre. Par exemple, si vous souhaitez vérifier une nouvelle version de Python, utilisez un environnement : `conda create --name test python=3.11`

    4.  **Vérifiez l'installation**. Après l'installation, ouvrez un terminal et tapez `python --version` pour vous assurer que tout fonctionne correctement.

    ### Création d'un environnement virtuel {#sec-00-01}

    Il y a deux façons d'installer un environnement virtuel selon votre distribution de Python:

    1.  **Option 1**. Vous utilisez [Anaconda](https://www.anaconda.com/download) ou [Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/). La commande `conda` est utilisée pour créer un environnement test avec Python 3.10:

    ``` bash
    conda create -n test python=3.10
    conda activate test
    ```

    2.  **Option 2**. Vous utilisez [CPython](https://www.python.org/downloads/), sans `conda`. Le module `venv` de la bibliothèque standard crée l'environnement et `pip` installe ensuite les bibliothèques :

    ``` bash
    python -m venv test
    source test/bin/activate       # Windows : test\Scripts\activate
    pip install --upgrade pip
    ```

    ### Création d'un environnement de travail local (avancé)

    **Note**: les notebooks peuvent fonctionner localement uniquement sous Linux ou avec WSL2.

    Les notebooks Python fonctionnent par défaut dans l'environnement [Google Colab](https://colab.google/). Si vous souhaitez faire fonctionner ces notebook localement, vous pouvez installer un environnement local avec un serveur [Jupyter](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html). Il suffit de suivre les étapes suivantes:

    1\. Installer `WSL2` sous [Windows](https://learn.microsoft.com/en-us/windows/wsl/install)

    2\. Installer [vscode](https://code.visualstudio.com/docs/setup/windows)

    3\. Installer [Miniconda](https://docs.anaconda.com/miniconda/install/#quick-command-line-install)

    4\. Faire une installation du contenu du livre soit en utilisant une commande `git clone` ou en récupérant le `.zip` du livre

    5\. Ouvrir WSL2 et placer vous dans le répertoire du livre `TraitementImagesPythonVol1`. Assurez vous que vous avez accès à conda en tapant `conda --version`

    6\. Lancer la commande `conda env create -f jupyter_env.yaml`

    7\. Activer le nouvel environnement: `conda activate jupyter_env`

    8\. Le serveur jupyter peut ensuite être lancé avec la commande suivante: `jupyter lab --ip='*' --NotebookApp.token='' --NotebookApp.password=''`

    Une fenêtre devrait alors apparaître dans votre fureteur. Dans le menu de gauche vous pouvez accéder aux notebooks dans le répertoire `notebooks`:

    ![Fenêtre principale du serveur Jupyter Lab.](images/jupyter-accueil.png){#fig-jupyterlab fig-scap="Client Jupyter Lab" width="100%" fig-align="center"}

    ## Les structures de base en Python

    Python manipule quatre structures de données fondamentales : les listes, les tuples, les ensembles et les dictionnaires.

    ### Les listes

    Les listes sont comme des boites extensibles où vous pouvez ranger différents types d'objets:

    -   Représentées par des crochets : `[1, 2, 3, "python"]`.

    -   Ordonnées et modifiables (*mutable*), vous pouvez récupérer une valeur par sa position avec `[]`.

    -   Permettent les doublons (deux fois la même valeur).

    -   Idéales pour stocker des collections d'éléments que vous voulez modifier
    """)
    return


@app.cell
def _():
    # Une liste des bandes spectrales d'une image (analogie télédétection)
    _bandes = ['bleu', 'vert', 'rouge', 'PIR']
    print(_bandes[0])  # premier élément
    print(_bandes[-1])  # dernier élément
    print(_bandes[1:3])  # tranche (slice) : ['vert', 'rouge']
    _bandes.append('SWIR')
    print(len(_bandes), 'bandes :', _bandes)  # ajout en fin de liste
    # Compréhension de liste : transformer chaque élément
    print([b.upper() for b in _bandes])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Les tuples

    Les tuples sont similaires aux listes, mais les boîtes sont scellées:

    -   Représentés par des parenthèses : `(1, 2, 3, "python")`.

    -   Ordonnés mais non modifiables (*immutable*).

    -   Permettent les doublons.

    -   Souvent utilisés pour stocker des données qui ne doivent pas changer (comme des paramètres).
    """)
    return


@app.cell
def _():
    # Les dimensions (lignes, colonnes) d'une image : une donnée qui ne change pas
    dimensions = (512, 512)
    lignes, colonnes = dimensions        # dépaquetage (unpacking)
    print("Lignes :", lignes, "| Colonnes :", colonnes)

    # dimensions[0] = 1024   # -> TypeError : un tuple est immuable
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Les ensembles (Sets)

    Les ensembles sont comme des boites magiques qui ne gardent qu'un exemplaire de chaque objet:

    -   Représentés par des accolades : `{1, 2, 3}`.

    -   Non ordonnés et modifiables.

    -   N'autorisent pas les doublons.

    -   Utiles pour éliminer les doublons et effectuer des opérations mathématiques sur des ensembles.
    """)
    return


@app.cell
def _():
    # Éliminer les doublons d'une liste de classes d'occupation du sol
    classes = ["eau", "forêt", "eau", "urbain", "forêt"]
    uniques = set(classes)
    print(uniques)

    # Opérations ensemblistes
    a, b = {1, 2, 3}, {3, 4}
    print("intersection :", a & b, "| union :", a | b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dictionnaires

    Les dictionnaires sont comme des boites avec des étiquettes sur chacune d'elles :

    -   Représentés par des accolades avec des paires clé-valeur : `{"nom": "Python", "année": 1991}`.

    -   Non ordonnés et modifiables.

    -   Les clés doivent être uniques, mais les valeurs peuvent être dupliquées

    -   Utiles pour stocker des données associatives ou pour créer des tables de recherche rapide
    """)
    return


@app.cell
def _():
    # Un dictionnaire : les métadonnées d'une image satellite
    _image = {'capteur': 'Sentinel-2', 'bandes': 13, 'resolution_m': 10}
    print(_image['capteur'])  # accès par clé
    _image['date'] = '2024-07-01'
    for (cle, _valeur) in _image.items():  # ajout d'une paire clé-valeur
        print(f'{cle} : {_valeur}')  # parcours des paires clé-valeur
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Boucles et conditions

    Un programme prend des décisions (`if`) et répète des opérations (`for`, `while`). Ces structures de contrôle sont au cœur de tout traitement automatisé.
    """)
    return


@app.cell
def _():
    _bandes = ['bleu', 'vert', 'rouge', 'PIR']
    for (i, nom) in enumerate(_bandes):
    # Boucle for : parcourir chaque bande avec son indice
        print(i, nom)
    reflectance = 0.42
    if reflectance > 0.5:
    # Condition if / elif / else
        print('forte réflectance')
    elif reflectance > 0.3:
        print('réflectance moyenne')
    else:
        print('faible réflectance')
    (seuil, _valeur) = (0.5, 0.1)
    while _valeur < seuil:
        _valeur += 0.2
    # Boucle while : tant qu'une condition est vraie
    print('valeur finale :', round(_valeur, 1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Les fonctions

    Une fonction regroupe des instructions réutilisables sous un nom. On la définit avec `def` ; elle reçoit des *arguments* et renvoie un résultat avec `return`.
    """)
    return


@app.cell
def _():
    def ndvi(nir, rouge):
        """Indice de végétation NDVI = (PIR - Rouge) / (PIR + Rouge)."""
        return (nir - rouge) / (nir + rouge)
    print(round(ndvi(0.6, 0.2), 3))

    def normaliser(valeur, maximum=255):
    # Argument par défaut
        return _valeur / maximum
    print(normaliser(128))
    print(normaliser(1000, maximum=4095))  # image 12 bits
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Programmation objet

    La programmation orientée objet (POO) en Python est comme construire avec des blocs LEGO. Chaque objet est un bloc LEGO avec ses propres caractéristiques (attributs) et capacités (méthodes). Les classes sont les plans pour créer ces blocs. Par exemple, une classe "Voiture" pourrait avoir des attributs comme "couleur" et "vitesse", et des méthodes comme "démarrer" et "accélérer".

    Python rend la POO accessible avec des fonctionnalités conviviales:

    1.  **Encapsulation**: comme emballer un cadeau, elle cache les détails internes d'un objet.

    2.  **Héritage**: permet de créer de nouvelles classes basées sur des classes existantes, comme un enfant héritant des traits de ses parents.

    3.  **Polymorphisme**: permet à différents objets de répondre au même message de manière unique, comme si différents animaux répondaient différemment à "fais du bruit".

    Ces caractéristiques font de Python un excellent choix pour apprendre et appliquer les concepts de la POO, rendant le code plus organisé et réutilisable
    """)
    return


@app.cell
def _():
    class Image:
        """Une classe minimale décrivant une image satellite."""

        def __init__(self, capteur, bandes):  # constructeur
            self.capteur = capteur  # attributs
            self.bandes = _bandes

        def resume(self):  # méthode
            return f'{self.capteur} — {self.bandes} bandes'
    img = Image('Landsat-8', 11)
    print(img.resume())
    print(img.capteur)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Importer des bibliothèques

    Python possède une petite bibliothèque standard, mais toute sa puissance vient des *packages* externes (comme NumPy). On les installe une fois avec `pip`, puis on les charge dans un script avec `import`.

    ``` bash
    pip install numpy          # une seule fois par environnement
    ```
    """)
    return


@app.cell
def _():
    import numpy as np              # tout le module, sous l'alias np
    from math import pi, sqrt       # seulement certains éléments

    print(np.array([1, 2, 3]))
    print(round(pi, 4), sqrt(16))
    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Un avant-goût de NumPy {#sec-00-02}

    Dans ce manuel, une image est avant tout un tableau de nombres. La bibliothèque [NumPy](https://numpy.org/) fournit l'objet `ndarray` qui représente efficacement ces tableaux à plusieurs dimensions : c'est la brique de base de tous les chapitres suivants.
    """)
    return


@app.cell
def _(np):
    _image = np.array([[10, 12, 11, 9], [8, 20, 22, 7], [9, 21, 23, 8]])
    print('Forme (lignes, colonnes) :', _image.shape)
    print('Valeur maximale :', _image.max())
    print('Moyenne :', _image.mean().round(2))
    print(_image[:2, :2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Points clés

    <div style="border:0.5px solid silver;border-left:.3rem solid #357cc0;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#eef5fb;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IB2cksfwAAA/pJREFUWIXNl01sVFUYhp/vzLSlDTbiTCmpoEQT5SemQQNaFw12ftCQrtSmKxLiAmUp0UTsz51prcYFKxM10ZCwarCuiAlMWyQuICkQ7KKlmmBiqDWlc52m1jKkvedz0TuVInTujNH6rr6595z3ec89d+45RwioV/p+rVv0wruNyi4LuwV2Abv922MK4wbGrOi48bzxjLPlVhBfKdagpTf3eEi9bpTDQcP6zic9CaXOd2z6uawATSduVm/8fcN7CO+CVAFLwA8CowqjqjKq4aXvvUWRsIQaRbRRoFGhEXgaCIPeQfl4/qH8h5fe3nY7cICkk92hhgH/EVuB/iXxus531t8IMviWnuknwxpKK7QDBhgTy2sZJzpRNEA8fWuPYIaBTcB1i7wx3BW5FAR8r2Jpt8mgXwI7gZxiY0Ndm689MEDCmWnAyAjwKMg3G+ydtjNOw0I58IJanamavKk6DXoQ+AWr+waduqm/BXj9tIZmr/92HtFmhW9z9ZEDV4/I4j+BF/Tc51qxado9J/ASKt89vPORlq/axMOfHwBmJ9xjiDYDk0u2sq0YPJlyE4l0diSRzo4kU25irbZXj8jikq1sAyYRbZ6dcI8V7hmAZK+7DegGVIXDF5zabNFhiX4K7AX2+vWauuDUZlU4DCjQ7TOXA1hLB1CDSP9QZ3SoKLxMDXVGhxDpB2p8JibWNxcR9BBgrWedwG4qbwGXgct+HUg+wwp6KNY3F5FEauYIIp8B5wa7oi+XObiSlEhnzwIHUH3TIJIEUNWv/wv4KpZIMgy6B4SQmItBDeK97gvi2UYR2a7IdhHNZTqjR4P2D4m5aFFA94RBtgLMbVz4KaiBWJKIHFWoB0WVT4L2LbA2zlcDstUAFYA+aLG4nwa7ImlFPlq5oIyUEsBnKVBhArS/r0TYUahDRksKcLcMsAhI04mb1SX1VN3nV7mzHdEfS+nqswRYNKCTALXzNU8ENWh1pmqAZ/yflxHRUgL8xdJJA3INwFP7YlCD2+ENzy5vOEApbf5Xs+SaQTUDICKvBjUQ6xUeP0ZLn/8VlmrG2IqqASAPJGLOzFNBDFRYCeCFbUkBfEYCyNuKqgEzfLzWVeQUYEzIBFoLROV5lt+iG8Pv10+XEsBnGEVODR+vdQ2AMfQCC6i2x3uy8QA+m1me/4ZE2u1KpmYCBY/3ZOOotgMLPnN5Oc50RG4CKUBEObnfmYuuZaSiZ/xSQOtCar4oBt/vzEVFOen//VI+s8wtmaq0fDD7WLjqTjbzzpY/isHX2pKt+6Z01ad40KmbUmwrkAM9mDeVV2Jpt6lceCztNuVN5RUfnlNs691w/pcHk4LW9Wi2ajTrdTi9V//W8fxPxif/DjJKAKcAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>À retenir</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ul>
    <li>Installez Python via un <strong>environnement virtuel</strong> (<code>conda</code> ou <code>venv</code>) pour isoler chaque projet.</li>
    <li>Quatre structures de base : <strong>listes</strong> (ordonnées, modifiables), <strong>tuples</strong> (immuables), <strong>ensembles</strong> (sans doublons) et <strong>dictionnaires</strong> (paires clé-valeur).</li>
    <li><code>if</code>/<code>for</code>/<code>while</code> contrôlent le déroulement du programme ; les <strong>fonctions</strong> (<code>def</code>) regroupent du code réutilisable.</li>
    <li>Une image est avant tout un <strong>tableau <code>NumPy</code></strong> : c’est la structure centrale de tout le manuel.</li>
    </ul>
    </div>
    </div>

    ## Exercices

    <div style="border:0.5px solid silver;border-left:.3rem solid #e34692;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fbe8f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADP0lEQVRYha2XT3LaMBjFf3SyD91rBnqC0BOUbuJl6AkwB9CUnKD0BCXxAeKcIGSpVZ0bwAkKEx8ATkAXemoUgm0I/WY8smVJ7/n78yS3ttstp1iZZF0g1WNhnC3Un6o/N87mVfNbpxAQ+Bw4j7p/qv0R9Y2qSHx4N7q3scBvBLwS8A/dj4ANcCePvLFTPVAAX4yzraivDxCFogcUIvrGE6cSSIE74KdxdlIzrpLEqSGY4V2d1g0yzs6BPnvCcRIB4+waWAKdMsna7yHR2m63aPL4COzCOFuUSZYDQ+DeOJseMjEKB8bZduv58ratjosjCMSltgJ68gZlkg20+KyGRIrPndEZMBD4AuiHhSom9oHfeszxXusAkzLJ1vhc6GjsChjI9bs2UFt8ALp6GDeAt4GpHtfG2SUvMf2O90YHrwk3us/3rJMDV8CTcXZ5VgUYTehroY66NmFh4+w8kuI2r6X4OzthLZNsjM+ZBfJCLQF99Qxfvwu87E5iT+l+ujMvuPgp6kuBX/qAf6Fu8kBP4I/G2UHD2NjGAhpH4He74IcQCNYtk6xdlSNBfoGlcuMLPsbzPeCvkrL1fHk7wSfQ1xC/ncXnvMRyhU/Wmd7tK+ERPjmHwL3aveBwmBL2tdACn4gPSjzwyXchgEf1TXVtmsAPImCcXRtnU+NsT0QCMPgcQQADkTjHV0QgXgkOr3MglUzmu7HWF8dJ2I1keBMBFPgan4lk3vSBsQeG+DJZikgAT4E/ejeMxob7eA/J8aE6Bx7wqlm7x8QErqPJ8aSJ2nuNAV/f18DneG9XuHrAN172i+WhBMJ2CYqtsrwDLLTbBVevjbPTqtgaZ2d1B5QqAkHVFsCFYlxE5OL2qkyyWZlk46ZzwFEEZEHFhvgSW6kvEBwFEvi8KE4h8YaAxKgLfMWLU3dH+3PgIz7OG5FM30tgrxQLsKiapPcz7W53+Lr/fwSaTGU64KValjXDezXvjidQJtkUfwAJ9lj360WDd44iIEUM4Nf4A0ilzB5iZ0BIsJSauMu6am+Ms9O6gZGa1hJsPV/edvFSC14DKs+FeHeG0lzWc/13mPmkM8J+AvovGOC30E7VwHfYEw2/5gB/AcMlhsUeVwFpAAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>À vous de jouer</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ol type="1">
    <li>Créez un dictionnaire <code>metadonnees</code> décrivant une image (capteur, nombre de bandes, résolution) puis affichez chaque paire clé-valeur.
    </li>
    <li>À partir du tableau <code>image</code> de la <a href="#sec-00-02" class="quarto-xref"><span>Section 1.10</span></a>, calculez la valeur <strong>minimale</strong> et l’<strong>écart-type</strong> (<code>image.std()</code>), puis extrayez la dernière colonne.
    </li>
    <li>Écrivez une fonction <code>ratio(a, b)</code> renvoyant <code>(a - b) / (a + b)</code>, et utilisez-la pour un NDVI avec PIR = 0,55 et Rouge = 0,18.
    </li>
    </ol>
    </div>
    </div>

    <details>
    <summary>Afficher les solutions</summary>

    ``` python
    # 1. Dictionnaire de métadonnées
    metadonnees = {"capteur": "Sentinel-2", "bandes": 13, "resolution_m": 10}
    for cle, valeur in metadonnees.items():
        print(cle, ":", valeur)

    # 2. Statistiques et dernière colonne du tableau `image`
    print("min :", image.min(), "| écart-type :", round(image.std(), 2))
    print("dernière colonne :", image[:, -1])

    # 3. Fonction ratio et calcul du NDVI
    def ratio(a, b):
        return (a - b) / (a + b)

    print("NDVI :", round(ratio(0.55, 0.18), 3))
    ```

    </details>

    <div style="border:0.5px solid silver;border-left:.3rem solid #352c76;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2e1f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAABhUlEQVRYhe2Wv3HCMByFP3P0YYMwQHShiGrYgGSCsEFcRSWmVBWYIGYDNoDUashpAdiATOAUyMZnDvsiMKTwa2z9ud/7znqSFSRJQlFSqA1wfzRwnrbG6m6xMygCSKEiYAx8AauKoiP3jCvmDYA+MDFWRycBpFBdYO2aPWP1pqyqFGoFYKweVMw7WbdVmDsF7oBplflf5GpltfNjGYAUagAM2a9VdCnzHEQEbIGh8zoASKE6HNZxdGnznNLasfPMvkDIPvVzY/WqLndXe+68QoCWC8gY+Ek7a1bovMZSqG7w9PAeOYBbaNLONb6B3ZWMO8AjQB4grHP983K7YAnH58DV1a6aIIUa4b81Y2N17A0ghXoGPj3NAfpSqJ2xeuEFAPQAjNWBj7sUKnE1TgL8/wxAltqbAKS/0OUZHuuywVIAY/VCCvWCy4KPeVkAKwFSCEpCdK5uHsIGoAFoABqAPIDvceujzKvN4Wfx4a7odV9MO8Cbe18HSZIghYqB15qNi5oZq8Nf0ER+TJGyROAAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Liste des <em>packages</em> utilisés dans ce chapitre</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ul>
    <li>Pour importer et manipuler des fichiers géographiques :
    <ul>
    <li><code>numpy</code> pour manipuler des données matricielles.</li>
    <li><code>rasterio</code> pour importer et manipuler des données matricielles.</li>
    </ul></li>
    <li>Pour construire des cartes et des graphiques :
    <ul>
    <li><code>matplotlib</code> est certainement le <em>package</em> le plus complet pour l’affichage général.</li>
    <li><code>seaborn</code> pour construire des graphiques plus détaillés en particulier pour les statistiques.</li>
    </ul></li>
    </ul>
    </div>
    </div>

    ## Quiz

    ::: {.content-visible when-profile="production"}

    Utilisez la version html.
    :::
    """)
    return


@app.cell
def _():
    from code_complementaire.quizz_functions import Quiz, render_quizz
    Chap00Quiz = Quiz("quiz/Chap00.yml", "Chap00")
    render_quizz(Chap00Quiz)
    return


if __name__ == "__main__":
    app.run()
