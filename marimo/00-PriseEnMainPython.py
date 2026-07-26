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
    <li>organiser du code en modules et packages;</li>
    <li>manipuler un tableau <code>NumPy</code>.</li>
    </ul>
    </div>
    </div>

    Ce chapitre est aussi disponible sous la forme d'un notebook Python sur Google Colab :

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/00-PriseEnMainPython.ipynb)

    Python, créé par [Guido van Rossum](https://en.wikipedia.org/wiki/Guido_van_Rossum) en 1991, est un langage de programmation polyvalent et facile à apprendre, souvent comparé à un couteau suisse numérique pour sa simplicité et sa polyvalence. Comme un outil multifonction, Python peut être utilisé pour une variété de tâches, du développement web à l'analyse de données, en passant par l'intelligence artificielle.

    ## Les distributions

    Il existe plusieurs [distributions](https://wiki.python.org/moin/PythonDistributions) du langage Python, ces distributions sont des variantes plus ou moins volumineuses - chacune a ses propres caractéristiques uniques, mais elles sont toutes fondamentalement Python. Voici un aperçu des principales distributions :

    | Distribution | Description | Idéale pour |
    |------------------------|------------------------|------------------------|
    | [CPython](https://www.python.org/downloads/) | L'implémentation officielle « vanille » | La compatibilité et la conformité aux standards |
    | [Anaconda](https://www.anaconda.com/download) | Livrée avec de nombreuses bibliothèques scientifiques | L'analyse de données et l'apprentissage automatique (*machine learning*) |
    | [Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) | Version légère ; on ajoute les bibliothèques au besoin | Un environnement minimal et contrôlé |
    | [PyPy](https://pypy.org/) | Implémentation optimisée pour la vitesse d'exécution | Les programmes gourmands en calcul |

    Chaque distribution a ses forces, que ce soit la simplicité, la vitesse ou des fonctionnalités spécifiques. Le choix dépend donc de vos besoins, la version Anaconda est par exemple très volumineuse et contiendra la plupart des librairies de base (Numpy, Scikit, etc.). Au contraire, Miniconda ne contient que le cœur de Python et les librairies seront ajoutées une par une au besoin.

    ## Les styles de programmation en Python

    Il existe plusieurs approches pour programmer en Python. La plus directe est en version interactive en tapant `python` et de rentrer des commandes ligne par ligne. On parle de mode REPL (“Read-Eval-Print Loop”) ou l'interpréteur Python vous donne une rétroaction immédiate commande par commande.

    ### Les outils de programmation

    Un code python prend la forme d'un simple fichier texte avec l'extension `.py` et peut être modifié avec un simple éditeur de texte. On parle alors de *script* Python. Cependant, il n'y aura pas de rétroactions immédiates de l'interpréteur Python, ce qui rend la correction d'erreurs (débogage) beaucoup plus laborieux.

    Un IDE (*Integrated Development Environment*) est comme une boîte à outils complète pour les programmeurs, vous trouverez :

    -   Un éditeur de texte amélioré pour écrire votre code, avec des fonctionnalités comme la coloration syntaxique qui rend le code plus lisible.

    -   Un interpréteur qui exécute votre code ligne par ligne.

    -   Un débogueur pour trouver et corriger les erreurs, tel un détective numérique.

    -   Des outils d'automatisation qui effectuent des tâches répétitives, comme un assistant virtuel pour le codage.

    -   L'accès à la documentation des différentes librairies.

    Ces outils intégrés permettent aux développeurs de travailler plus efficacement, en passant moins de temps à jongler entre différentes applications et plus de temps à produire du code.

    Voici quelques options populaires :

    | Outil | Type | Points forts |
    |------------------------|------------------------|------------------------|
    | [PyCharm](https://www.jetbrains.com/pycharm/) | IDE complet | Autocomplétion, débogage intégré ; idéal pour les grands projets (gourmand en ressources) |
    | [Visual Studio Code](https://code.visualstudio.com/) | Éditeur extensible | Gratuit, léger, personnalisable par extensions |
    | [Spyder](https://www.spyder-ide.org/) | IDE scientifique | Libre et gratuit, orienté calcul scientifique |
    | [Jupyter](https://jupyter.org/) | Notebook | Mélange code, texte et visualisations ; gratuit sur Colab/Kaggle (reproductibilité limitée) |
    | [Marimo](https://marimo.io/) | Notebook réactif | Réexécute automatiquement les cellules dépendantes ; évite l'état caché |

    ### Le principe du serveur Jupyter et des notebooks

    Les chapitres de ce livre sont fournis sous forme de *notebooks* (carnets), le format le plus répandu pour l'analyse de données scientifiques. Un **notebook** est un fichier (extension `.ipynb`) organisé en **cellules** que l'on exécute une à une :

    -   des cellules de **code** Python, dont le résultat (texte, tableau, figure) s'affiche juste en dessous ;
    -   des cellules de **texte** (Markdown) pour la documentation, les titres et les équations.

    On peut ainsi entrelacer le code, les explications et les résultats dans un même document, ce qui en fait un excellent outil pédagogique et un support d'analyse reproductible.

    Un notebook repose sur une **architecture client-serveur** en trois pièces :

    1.  Le **serveur Jupyter** est un programme lancé sur votre machine (ou dans le nuage). Il gère les fichiers de notebooks et fait le pont entre l'interface et le moteur de calcul.
    2.  L'**interface** s'affiche dans un simple navigateur web : c'est là que vous éditez et lancez les cellules. Aucune installation supplémentaire n'est requise côté affichage.
    3.  Le **noyau** (*kernel*) est le processus Python qui exécute réellement le code. Il **conserve l'état en mémoire** entre les cellules : une variable définie dans une cellule reste disponible dans les suivantes.

    Quand vous exécutez une cellule, l'interface envoie le code au serveur, qui le transmet au noyau ; le noyau calcule puis renvoie le résultat, affiché sous la cellule. Comme le noyau garde l'état, l'**ordre d'exécution** des cellules compte : réexécuter des cellules dans le désordre peut mener à un état incohérent. En cas de doute, on redémarre le noyau et on réexécute tout depuis le début (menu *Kernel*, puis *Restart & Run All*).

    Le service [Google Colab](https://colab.google/) fournit gratuitement ce trio (serveur, interface, noyau) dans le nuage : c'est la façon la plus simple d'ouvrir les notebooks du livre sans rien installer. Pour travailler localement, il faut lancer soi-même un serveur Jupyter (voir @sec-00-jupyter-local plus bas).

    ## Bonnes pratiques

    Python est un langage très dynamique, qui évolue constamment. Cela pose certains défis pour la gestion du code à long terme. Il est fortement conseillé d'utiliser des environnements virtuels pour gérer vos différentes bibliothèques (*libraries*). Voici quelques bonnes pratiques à suivre :

    1.  **N'installez pas la toute dernière version de Python** : Il est recommandé d'installer 1 ou 2 version antérieure, par exemple si 3.13 est [la version plus récente](https://www.python.org/downloads/), installer plutôt la version 3.11. Les versions trop récentes peuvent être instables surtout au niveau des librairies. La version de python désirée peut être spécifiée au moment de la création d'un environnement virtuel (voir plus bas). Vous pouvez afficher la liste des versions de python avec la commande `conda search --full-name python`.

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

    ### Création d'un environnement de travail local (avancé) {#sec-00-jupyter-local}

    **Note**: les notebooks peuvent fonctionner localement sous Windows ou sous Linux avec WSL2.

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
    image = {'capteur': 'Sentinel-2', 'bandes': 13, 'resolution_m': 10}
    print(image['capteur'])  # accès par clé
    image['date'] = '2024-07-01'
    for (cle, _valeur) in image.items():  # ajout d'une paire clé-valeur
        print(f'{cle} : {_valeur}')  # parcours des paires clé-valeur
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div style="border:0.5px solid silver;border-left:.3rem solid #eb5f23;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fef4ec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADSElEQVRYhbWX0W3bMBCGPwd5jwvwPUY1QNQJokxQL1DVmSDuBHEnqDNBFS7QdIJKE9QdgIDzXAFRJnAfeIzPDC05TXuAIZu64//z7ueRHm02G/63tWU2BvLUu+P/BFbIJwfO+/z/GYG2zApgBnyMXjXAWj7aZsDpqwkI8ILtSu+BCrgz1q0G4l5HoC2zJXAlPxtgYayrDwzPgaaXQFtmE2AKpFayBM7wK55p4LbMpmxFV8ekRCcnQLeXQFtmOVCL4z77LuCdiqvY1cF1W2Y3xrq5GivkuTraA14o8E/AhTxvlNutsW4agRcCfi/kGuARuJIFxQTqZxloy2wGfJWfl8a6SsZXQiqAzxLcw8RrY91U4mq8QHUppwDGul0CCvwRmEa1q/A13wc+ZJ1g5MApPkPbPqBq9wgUegu1ZTYH3gPNAPgdcA2ct2W2xu/9XL0DCFqoAEabzUaD/8KLSoNP2KZuomuesqiEyILmxrpK1L8GOmPdBOA4Um0NTGUb1YrxCV4PSXBJa2esWwtQjRKasW4t3xcy1zLEjn5/eNvRv9UA7gPjBPgCn/bPxrrFvgmE5M94rmNj3Vg5jKO4UPslCYt0c5fyEb8xUnO2GvAEwpdU35Z9/Z7oIJEJl2x1UwxoI3TNW2PdDtFkI1IWSFWhkQh4fSi4FnhqB42GLiRRb8jxqT4DbvHq3ifMsfie9xFNElA3mJWxrlNCC9bbjCRblRAFeLOP6LMSqBT/4HkTAdnXPeBziQ/g9JVoh4AwX0lwA6ykBLW4NET7WMfK/v8iQ5fif78PHFQJouP3KcVtmW3YrvpOre5Wxgp5hhtRg++maznAOmNdcUgGdsClFACf8QKqJJUFXlQfgQfgm4A3wIWxrlCd74wBO1Kr7/Bpmwvzh7bMCulueVtm67bMZopEI0QAbgS4DhNLOx+0Y3hqQhMlwDOZfNXuHi6d+HdAIY3qRxhX4Dom2UV3MqCyoAVY4A+P0AMu4y6WsqhvvBuKiTVwitdAAL9iez+oDgCvFHiRau9JArL6E3wtZ/JOgw9NVEd3ivwQcNjVwCh69w5/t+s7ZAp5VvjsHXIwPSeQskNXIBbueLOXgPcSeKH97UX11QSWJP75vMT+AHO9uY9+8Go9AAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>Les opérateurs <code>*</code> et <code>**</code> sur un dictionnaire</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    Les opérateurs de <em>déballage</em> (<em>unpacking</em>) donnent accès au contenu d’un dictionnaire sans écrire de boucle. La règle est simple : <code>**</code> déballe les <strong>paires clé-valeur</strong>, tandis que <code>*</code> (une seule étoile) ne déballe que les <strong>clés</strong>.

    <div class="code-copy-outer-scaffold"><div class="sourceCode" id="cb11"><pre class="sourceCode python code-with-copy"><code class="sourceCode python"><span id="cb11-1"><a href="#cb11-1" aria-hidden="true" tabindex="-1"></a>image <span class="op">=</span> {<span class="st">"capteur"</span>: <span class="st">"Sentinel-2"</span>, <span class="st">"bandes"</span>: <span class="dv">13</span>, <span class="st">"resolution_m"</span>: <span class="dv">10</span>}</span>
    <span id="cb11-2"><a href="#cb11-2" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb11-3"><a href="#cb11-3" aria-hidden="true" tabindex="-1"></a><span class="co"># ** : fusionner ou copier des dictionnaires</span></span>
    <span id="cb11-4"><a href="#cb11-4" aria-hidden="true" tabindex="-1"></a>complet <span class="op">=</span> {<span class="op">**</span>image, <span class="st">"date"</span>: <span class="st">"2024-07-01"</span>}   <span class="co"># copie + une paire en plus</span></span>
    <span id="cb11-5"><a href="#cb11-5" aria-hidden="true" tabindex="-1"></a>fusion  <span class="op">=</span> {<span class="op">**</span>image, <span class="st">"bandes"</span>: <span class="dv">4</span>}            <span class="co"># en cas de collision, la dernière clé gagne</span></span>
    <span id="cb11-6"><a href="#cb11-6" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb11-7"><a href="#cb11-7" aria-hidden="true" tabindex="-1"></a><span class="co"># ** : passer un dictionnaire comme arguments nommés d'une fonction</span></span>
    <span id="cb11-8"><a href="#cb11-8" aria-hidden="true" tabindex="-1"></a><span class="kw">def</span> resume(capteur, bandes, resolution_m):</span>
    <span id="cb11-9"><a href="#cb11-9" aria-hidden="true" tabindex="-1"></a>    <span class="cf">return</span> <span class="ss">f"</span><span class="sc">{</span>capteur<span class="sc">}</span><span class="ss"> : </span><span class="sc">{</span>bandes<span class="sc">}</span><span class="ss"> bandes à </span><span class="sc">{</span>resolution_m<span class="sc">}</span><span class="ss"> m"</span></span>
    <span id="cb11-10"><a href="#cb11-10" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb11-11"><a href="#cb11-11" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(resume(<span class="op">**</span>image))          <span class="co"># équivaut à resume(capteur="Sentinel-2", bandes=13, ...)</span></span>
    <span id="cb11-12"><a href="#cb11-12" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb11-13"><a href="#cb11-13" aria-hidden="true" tabindex="-1"></a><span class="co"># * : ne déballe que les clés</span></span>
    <span id="cb11-14"><a href="#cb11-14" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>([<span class="op">*</span>image])                 <span class="co"># ['capteur', 'bandes', 'resolution_m']</span></span>
    <span id="cb11-15"><a href="#cb11-15" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(<span class="op">*</span>image, sep<span class="op">=</span><span class="st">", "</span>)         <span class="co"># capteur, bandes, resolution_m</span></span>
    <span id="cb11-16"><a href="#cb11-16" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb11-17"><a href="#cb11-17" aria-hidden="true" tabindex="-1"></a><span class="co"># Côté définition d'une fonction : **kwargs collecte les arguments nommés dans un dict</span></span>
    <span id="cb11-18"><a href="#cb11-18" aria-hidden="true" tabindex="-1"></a><span class="kw">def</span> info(<span class="op">**</span>meta):               <span class="co"># meta est un dictionnaire</span></span>
    <span id="cb11-19"><a href="#cb11-19" aria-hidden="true" tabindex="-1"></a>    <span class="cf">for</span> cle, valeur <span class="kw">in</span> meta.items():</span>
    <span id="cb11-20"><a href="#cb11-20" aria-hidden="true" tabindex="-1"></a>        <span class="bu">print</span>(cle, <span class="st">":"</span>, valeur)</span>
    <span id="cb11-21"><a href="#cb11-21" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb11-22"><a href="#cb11-22" aria-hidden="true" tabindex="-1"></a>info(capteur<span class="op">=</span><span class="st">"SPOT"</span>, bandes<span class="op">=</span><span class="dv">4</span>)</span></code></pre></div><button title="Copier vers le presse-papier" class="code-copy-button"><i class="bi"></i></button></div>
    À retenir : <code>**d</code> sert à <em>fournir</em> ou <em>fusionner</em> des paires clé-valeur (appels de fonction, construction de dictionnaires), alors que <code>**kwargs</code> dans une <strong>définition</strong> de fonction fait l’inverse — il <em>collecte</em> les arguments nommés dans un dictionnaire. À partir de Python 3.9, <code>a | b</code> fusionne aussi deux dictionnaires, en équivalent plus lisible de <code>{**a, **b}</code>.

    </div>
    </div>

    <div style="border:0.5px solid silver;border-left:.3rem solid #eb5f23;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fef4ec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADSElEQVRYhbWX0W3bMBCGPwd5jwvwPUY1QNQJokxQL1DVmSDuBHEnqDNBFS7QdIJKE9QdgIDzXAFRJnAfeIzPDC05TXuAIZu64//z7ueRHm02G/63tWU2BvLUu+P/BFbIJwfO+/z/GYG2zApgBnyMXjXAWj7aZsDpqwkI8ILtSu+BCrgz1q0G4l5HoC2zJXAlPxtgYayrDwzPgaaXQFtmE2AKpFayBM7wK55p4LbMpmxFV8ekRCcnQLeXQFtmOVCL4z77LuCdiqvY1cF1W2Y3xrq5GivkuTraA14o8E/AhTxvlNutsW4agRcCfi/kGuARuJIFxQTqZxloy2wGfJWfl8a6SsZXQiqAzxLcw8RrY91U4mq8QHUppwDGul0CCvwRmEa1q/A13wc+ZJ1g5MApPkPbPqBq9wgUegu1ZTYH3gPNAPgdcA2ct2W2xu/9XL0DCFqoAEabzUaD/8KLSoNP2KZuomuesqiEyILmxrpK1L8GOmPdBOA4Um0NTGUb1YrxCV4PSXBJa2esWwtQjRKasW4t3xcy1zLEjn5/eNvRv9UA7gPjBPgCn/bPxrrFvgmE5M94rmNj3Vg5jKO4UPslCYt0c5fyEb8xUnO2GvAEwpdU35Z9/Z7oIJEJl2x1UwxoI3TNW2PdDtFkI1IWSFWhkQh4fSi4FnhqB42GLiRRb8jxqT4DbvHq3ifMsfie9xFNElA3mJWxrlNCC9bbjCRblRAFeLOP6LMSqBT/4HkTAdnXPeBziQ/g9JVoh4AwX0lwA6ykBLW4NET7WMfK/v8iQ5fif78PHFQJouP3KcVtmW3YrvpOre5Wxgp5hhtRg++maznAOmNdcUgGdsClFACf8QKqJJUFXlQfgQfgm4A3wIWxrlCd74wBO1Kr7/Bpmwvzh7bMCulueVtm67bMZopEI0QAbgS4DhNLOx+0Y3hqQhMlwDOZfNXuHi6d+HdAIY3qRxhX4Dom2UV3MqCyoAVY4A+P0AMu4y6WsqhvvBuKiTVwitdAAL9iez+oDgCvFHiRau9JArL6E3wtZ/JOgw9NVEd3ivwQcNjVwCh69w5/t+s7ZAp5VvjsHXIwPSeQskNXIBbueLOXgPcSeKH97UX11QSWJP75vMT+AHO9uY9+8Go9AAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>Les compréhensions de liste et de dictionnaire</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    Une <strong>compréhension</strong> construit une collection en une seule ligne, à la place d’une boucle <code>for</code> suivie d’un <code>append</code>. Le code est plus court, plus lisible et souvent plus rapide. Le patron est toujours le même : une <strong>expression</strong>, un parcours (<code>for</code>), et un <strong>filtre</strong> optionnel (<code>if</code>).

    <div class="code-copy-outer-scaffold"><div class="sourceCode" id="cb12"><pre class="sourceCode python code-with-copy"><code class="sourceCode python"><span id="cb12-1"><a href="#cb12-1" aria-hidden="true" tabindex="-1"></a>bandes <span class="op">=</span> [<span class="st">"bleu"</span>, <span class="st">"vert"</span>, <span class="st">"rouge"</span>, <span class="st">"PIR"</span>]</span>
    <span id="cb12-2"><a href="#cb12-2" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb12-3"><a href="#cb12-3" aria-hidden="true" tabindex="-1"></a><span class="co"># Compréhension de LISTE : [expression for élément in itérable if condition]</span></span>
    <span id="cb12-4"><a href="#cb12-4" aria-hidden="true" tabindex="-1"></a>majuscules <span class="op">=</span> [b.upper() <span class="cf">for</span> b <span class="kw">in</span> bandes]           <span class="co"># transforme chaque élément</span></span>
    <span id="cb12-5"><a href="#cb12-5" aria-hidden="true" tabindex="-1"></a>courtes    <span class="op">=</span> [b <span class="cf">for</span> b <span class="kw">in</span> bandes <span class="cf">if</span> <span class="bu">len</span>(b) <span class="op"><=</span> <span class="dv">4</span>]    <span class="co"># ne garde que certains éléments</span></span>
    <span id="cb12-6"><a href="#cb12-6" aria-hidden="true" tabindex="-1"></a><span class="co"># équivalent avec une boucle classique :</span></span>
    <span id="cb12-7"><a href="#cb12-7" aria-hidden="true" tabindex="-1"></a>courtes <span class="op">=</span> []</span>
    <span id="cb12-8"><a href="#cb12-8" aria-hidden="true" tabindex="-1"></a><span class="cf">for</span> b <span class="kw">in</span> bandes:</span>
    <span id="cb12-9"><a href="#cb12-9" aria-hidden="true" tabindex="-1"></a>    <span class="cf">if</span> <span class="bu">len</span>(b) <span class="op"><=</span> <span class="dv">4</span>:</span>
    <span id="cb12-10"><a href="#cb12-10" aria-hidden="true" tabindex="-1"></a>        courtes.append(b)</span>
    <span id="cb12-11"><a href="#cb12-11" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb12-12"><a href="#cb12-12" aria-hidden="true" tabindex="-1"></a><span class="co"># Compréhension de DICTIONNAIRE : {clé: valeur for ...}</span></span>
    <span id="cb12-13"><a href="#cb12-13" aria-hidden="true" tabindex="-1"></a>indices <span class="op">=</span> {nom: i <span class="cf">for</span> i, nom <span class="kw">in</span> <span class="bu">enumerate</span>(bandes)}  <span class="co"># {'bleu': 0, 'vert': 1, ...}</span></span>
    <span id="cb12-14"><a href="#cb12-14" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb12-15"><a href="#cb12-15" aria-hidden="true" tabindex="-1"></a>image <span class="op">=</span> {<span class="st">"capteur"</span>: <span class="st">"Sentinel-2"</span>, <span class="st">"bandes"</span>: <span class="dv">13</span>, <span class="st">"resolution_m"</span>: <span class="dv">10</span>}</span>
    <span id="cb12-16"><a href="#cb12-16" aria-hidden="true" tabindex="-1"></a>inverse <span class="op">=</span> {valeur: cle <span class="cf">for</span> cle, valeur <span class="kw">in</span> image.items()}   <span class="co"># échange clés et valeurs</span></span>
    <span id="cb12-17"><a href="#cb12-17" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb12-18"><a href="#cb12-18" aria-hidden="true" tabindex="-1"></a><span class="co"># Compréhension d'ENSEMBLE : {expression for ...} -> doublons éliminés</span></span>
    <span id="cb12-19"><a href="#cb12-19" aria-hidden="true" tabindex="-1"></a>classes <span class="op">=</span> [<span class="st">"eau"</span>, <span class="st">"forêt"</span>, <span class="st">"eau"</span>, <span class="st">"urbain"</span>]</span>
    <span id="cb12-20"><a href="#cb12-20" aria-hidden="true" tabindex="-1"></a>uniques <span class="op">=</span> {c <span class="cf">for</span> c <span class="kw">in</span> classes}                      <span class="co"># {'eau', 'forêt', 'urbain'}</span></span></code></pre></div><button title="Copier vers le presse-papier" class="code-copy-button"><i class="bi"></i></button></div>
    On peut aussi choisir la valeur selon une condition, en plaçant un <code>if</code>/<code>else</code> dans l’<strong>expression</strong> (et non comme filtre en fin) : <code>["vég." if b == "PIR" else "visible" for b in bandes]</code>.

    </div>
    </div>

    <div style="border:0.5px solid silver;border-left:.3rem solid #f0ae4e;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fef4ec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IB2cksfwAAA+5JREFUWIXlll1Mm1UYx3/P+1bKAtiWGT/2cUN0XizEAH4k0yzeQLKMtmtpMU4TvdDscpp54YbJYLpENuNmpzNZXDZJ3EVLW2hhF1NjvCKwuPnBNLoYxQvG2ActJmMM+z5eFJBiZ1uYxMTn6v+e5/z/z/885805B/7vIUslTkQ9m0W1AxFR0b0uf/LLFTMwEWt+RNQ4v4CvqjS4AonzpWoZpRJUEVEjBIgI7wkcBsQQQqqlL6hkQrrb/ayKnALGrYx9A4BhTv8I3CfC8w5/4pNS9ErqwFhXU4WKHCDbid3VrZF0dWskrSK7Z8c6x8PByn/NQHnFqj3AOtAh53D9yblx57d1HwODwNoy2822UjSL3oJ02POgmgwDd4nKJkegdzAnH9/2uFrWADAjatU6An0Xi9EtvgOmvgvYBelaXBzA4esZQjkJ2C0xDhUrW1QH0nH3FrXkNJC22Xi40pu4nO72PqGipwBEZbsj0Dv4e8x3b0YzPwEOgWZHS6K/kHbBDmg4WKaWHCb7k+2r9CYuAyi6F6gBamYxVf74uKLt2TyH9PQW+7INpM3pV4ANoD84r91/ZIG1Vfmw8+oDH4jyPfBQ+kbZq8sycKXXswZ4AwCRnbLj2MxfTLmUD8uOYzMqsjP7oW1Xw81rl2zAlqETqALiTn/i05ykMpoXA86W3s9QYkClaRqdSzIwGfFuEuU5gZtkdNfivMKlfHh+zDR2AVMC26/H3E+VZEDb2w3L0COAWHDQ2Zr85W9E1dF8eC5cvp5fBQ4AYqiENBw0izaQrj33ElAP/DZVpm/nm2OpeSkfXhiTGXsnyAhQl7ZNv1yUgVTfVhewHwDhtTXu5I18RNOU0Xx4YaxvjUyhVnb7lLfS4WB1QQM6be4D7gG+cPoTkXzCAFW++EVRDYlqqMoXv+2x6wwko4h8DqxW89abi/M5J+H1Hm+tkdFzAJZk6qr9/cO3Ey4lrnW7N5oiX2cPTavB5e/7Zi6X0wHjDysE2ET16J0qDrA6kLwg8D5giho5D5d5A6ludysiTwNXtNxqLySainkaU1HPUCrqOZuKuJsKzbcMowMYBzZPxj3P5BgY62qqQOQdAJQ2Z3P/RMFlKUeBx4BHMeTDQtNdvp4U6B6yd8rBsa6minkD9ory14H1wFeO4frjBYsvMRzfNZwAzgLrZh83SCq6tUYwLyjYDbGevNvfN1CMWCrmaUTZDwiWtjmDyTPF8Gav8QHgFoaxUVJRTxgICnQ5WhIvLHeVRZmIek8o+iJI1AAaAZRMx0oUB7AMydZSbbQBI4ATzJ9TUc8KObDm0IhBRn2gH4HM/DPrTobMAMeRzLaVq/lfjT8B9MWCOfMxlGMAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Types de variables et copie</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    En Python, une variable est une <strong>étiquette</strong> qui pointe vers un objet, et non une boîte qui contient une valeur. Cette distinction est source d’erreurs fréquentes.

    Les types <strong>immuables</strong> (<code>int</code>, <code>float</code>, <code>str</code>, <code>tuple</code>) ne peuvent pas être modifiés sur place : les réaffecter crée un <strong>nouvel</strong> objet. Les types <strong>muables</strong> (<code>list</code>, <code>dict</code>, <code>set</code>) peuvent, eux, être modifiés en place — et une simple affectation <code>b = a</code> ne fait que créer une <strong>seconde étiquette sur le même objet</strong> :

    <div class="code-copy-outer-scaffold"><div class="sourceCode" id="cb13"><pre class="sourceCode python code-with-copy"><code class="sourceCode python"><span id="cb13-1"><a href="#cb13-1" aria-hidden="true" tabindex="-1"></a>a <span class="op">=</span> [<span class="dv">1</span>, <span class="dv">2</span>, <span class="dv">3</span>]</span>
    <span id="cb13-2"><a href="#cb13-2" aria-hidden="true" tabindex="-1"></a>b <span class="op">=</span> a                 <span class="co"># b et a désignent le MÊME objet</span></span>
    <span id="cb13-3"><a href="#cb13-3" aria-hidden="true" tabindex="-1"></a>b.append(<span class="dv">4</span>)</span>
    <span id="cb13-4"><a href="#cb13-4" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(a)              <span class="co"># [1, 2, 3, 4]  <- a est modifiée aussi !</span></span>
    <span id="cb13-5"><a href="#cb13-5" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(a <span class="kw">is</span> b)         <span class="co"># True (même objet en mémoire)</span></span>
    <span id="cb13-6"><a href="#cb13-6" aria-hidden="true" tabindex="-1"></a></span>
    <span id="cb13-7"><a href="#cb13-7" aria-hidden="true" tabindex="-1"></a>c <span class="op">=</span> a.copy()          <span class="co"># copie superficielle : un nouvel objet</span></span>
    <span id="cb13-8"><a href="#cb13-8" aria-hidden="true" tabindex="-1"></a>c.append(<span class="dv">5</span>)</span>
    <span id="cb13-9"><a href="#cb13-9" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(a, a <span class="kw">is</span> c)      <span class="co"># [1, 2, 3, 4] False  (a reste inchangée)</span></span></code></pre></div><button title="Copier vers le presse-papier" class="code-copy-button"><i class="bi"></i></button></div>
    Pour un tableau <code>NumPy</code>, c’est la méthode <code>.copy()</code> qui joue ce rôle (le découpage renvoie une <strong>vue</strong>, pas une copie). Attention enfin à la <strong>copie superficielle</strong> : elle duplique le conteneur mais <strong>partage</strong> les objets imbriqués. Pour une indépendance totale, on utilise <code>copy.deepcopy</code> :

    <div class="code-copy-outer-scaffold"><div class="sourceCode" id="cb14"><pre class="sourceCode python code-with-copy"><code class="sourceCode python"><span id="cb14-1"><a href="#cb14-1" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> copy</span>
    <span id="cb14-2"><a href="#cb14-2" aria-hidden="true" tabindex="-1"></a>grille <span class="op">=</span> [[<span class="dv">0</span>, <span class="dv">0</span>], [<span class="dv">0</span>, <span class="dv">0</span>]]</span>
    <span id="cb14-3"><a href="#cb14-3" aria-hidden="true" tabindex="-1"></a>sup <span class="op">=</span> grille.copy()             <span class="co"># copie superficielle : sous-listes PARTAGÉES</span></span>
    <span id="cb14-4"><a href="#cb14-4" aria-hidden="true" tabindex="-1"></a>sup[<span class="dv">0</span>][<span class="dv">0</span>] <span class="op">=</span> <span class="dv">9</span></span>
    <span id="cb14-5"><a href="#cb14-5" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span>(grille)                   <span class="co"># [[9, 0], [0, 0]]  <- affectée malgré la copie !</span></span>
    <span id="cb14-6"><a href="#cb14-6" aria-hidden="true" tabindex="-1"></a>prof <span class="op">=</span> copy.deepcopy(grille)    <span class="co"># copie profonde : totalement indépendante</span></span></code></pre></div><button title="Copier vers le presse-papier" class="code-copy-button"><i class="bi"></i></button></div>
    À retenir : <code>is</code> compare l’<strong>identité</strong> (le même objet), <code>==</code> compare la <strong>valeur</strong>. En cas de doute sur un objet muable, copiez avant de modifier.

    </div>
    </div>

    ## Boucles et conditions

    Un programme prend des décisions (`if`) et répète des opérations (`for`, `while`). Ces structures de contrôle sont au cœur de tout traitement automatisé.
    """)
    return


@app.cell
def _():
    _bandes = ['bleu', 'vert', 'rouge', 'PIR']
    for (i, nom) in enumerate(_bandes):
        print(i, nom)
    _reflectance = 0.42
    if _reflectance > 0.5:
        print('forte réflectance')
    elif _reflectance > 0.3:
        print('réflectance moyenne')
    else:
        print('faible réflectance')
    (seuil, _valeur) = (0.5, 0.1)
    while _valeur < seuil:
        _valeur = _valeur + 0.2
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
    def _ndvi(nir, rouge):
        """Indice de végétation NDVI = (PIR - Rouge) / (PIR + Rouge)."""
        return (nir - rouge) / (nir + rouge)
    print(round(_ndvi(0.6, 0.2), 3))

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
    _img = Image('Landsat-8', 11)
    print(_img.resume())
    print(_img.capteur)
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
    ## Modules et packages

    Jusqu'ici, nous avons *importé* des bibliothèques existantes. Comprendre comment le code Python est **organisé** permet de structurer ses propres projets et de réutiliser du code.

    -   Un **module** est simplement un fichier `.py` contenant des fonctions, des classes ou des variables. Le nom du module est celui du fichier, sans l'extension.
    -   Un **package** (ou paquet) est un **dossier** regroupant plusieurs modules. Ce dossier contient un fichier spécial `__init__.py` qui indique à Python qu'il s'agit d'un package.

    Par exemple, un package `teledetection` pourrait s'organiser ainsi :

    ```
    teledetection/
        __init__.py       # marque le dossier comme un package
        indices.py        # fonctions d'indices spectraux (ndvi, ...)
        filtres.py        # fonctions de filtrage spatial
    ```

    On accède au contenu avec la notation pointée `package.module.fonction` :
    """)
    return


@app.cell
def _():
    import teledetection.indices  # importe le module
    from teledetection import filtres as f  # importe une fonction précise
    resultat = teledetection.indices.ndvi(0.6, 0.2)  # importe un module sous un alias
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Le fichier `__init__.py`

    Le fichier `__init__.py` est exécuté **automatiquement** la première fois que le package est importé. Souvent vide, il peut aussi :

    -   exposer une **interface simplifiée**. Si `__init__.py` contient `from .indices import ndvi`, on peut alors écrire directement `from teledetection import ndvi` au lieu de `from teledetection.indices import ndvi`. Le point (`.`) dans `from .indices` désigne le package courant : c'est un **import relatif**.
    -   initialiser des données ou vérifier des dépendances au chargement du package.

    Ce mécanisme n'est pas qu'une abstraction : ce manuel l'utilise lui-même. Les quiz de fin de chapitre proviennent d'un package local `code_complementaire`, importé exactement de cette façon :
    """)
    return


@app.cell
def _():
    from code_complementaire.quizz_functions import Quiz, render_quizz

    return Quiz, render_quizz


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Enfin, un module peut contenir un bloc `if __name__ == "__main__":` dont le code ne s'exécute **que** si le fichier est lancé directement (`python indices.py`), et **pas** lorsqu'il est importé. C'est la façon habituelle de séparer le code exécutable des fonctions réutilisables. La variable `__name__` vaut `"__main__"` dans le premier cas, et le nom du module dans le second :
    """)
    return


@app.cell
def _():
    print("Nom du contexte courant :", __name__)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Créer un exécutable Python {#sec-00-executable}

    Un *notebook* est idéal pour explorer, mais pour une tâche répétitive — appliquer le même traitement à des centaines d'images — on préfère un **script exécutable** lancé depuis un terminal. Nous construisons ici, en trois étapes, un petit programme qui calcule un NDVI à partir d'une image à quatre bandes (B, V, R, PIR).

    ### 1. La solution la plus simple

    Un script est un simple fichier `.py` que l'on exécute avec `python`. Le code utile est placé dans le bloc `if __name__ == "__main__":` vu plus haut. Enregistrons ce fichier sous le nom `ndvi.py` :
    """)
    return


@app.cell
def _():
    # ndvi.py
    import rioxarray as rxr
    if __name__ == '__main__':
        _img = rxr.open_rasterio('RGBNIR_of_S2A.tif')
        rouge = _img.sel(band=3).astype('float32')
        pir = _img.sel(band=4).astype('float32')
        _ndvi = (pir - rouge) / (pir + rouge)
        _ndvi.rio.to_raster('ndvi.tif')
        print('NDVI enregistré dans ndvi.tif')
    return (rxr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On le lance depuis un terminal :

    ``` bash
    python ndvi.py
    ```

    Sur Linux ou macOS, on peut aussi rendre le fichier directement exécutable. Il suffit d'ajouter une ligne *shebang* en tête (`#!/usr/bin/env python3`), puis de donner le droit d'exécution avec `chmod +x ndvi.py` ; le script se lance alors avec `./ndvi.py`.

    Cette version fonctionne, mais tout est **figé** : les noms de fichiers et les numéros de bandes sont écrits en dur dans le code. Pour traiter une autre image, il faut éditer le script.

    ### 2. Bonnes pratiques : fonction `main` et paramètres

    On sépare le **traitement** (une fonction réutilisable, avec des **valeurs par défaut**) de l'**interface en ligne de commande**, gérée par le module `argparse` de la bibliothèque standard. Les valeurs par défaut rendent la plupart des arguments optionnels ; `argparse` génère aussi automatiquement une aide (`-h`).
    """)
    return


@app.cell
def _(rxr):
    """Calcule un NDVI à partir d'une image à quatre bandes (B, V, R, PIR)."""
    import argparse

    def _calcule_ndvi(entree, sortie='ndvi.tif', bande_rouge=3, bande_pir=4):
        """Le traitement : réutilisable, avec des valeurs par défaut."""
        _img = rxr.open_rasterio(entree)
        rouge = _img.sel(band=bande_rouge).astype('float32')
        pir = _img.sel(band=bande_pir).astype('float32')
        _ndvi = (pir - rouge) / (pir + rouge)
        _ndvi.rio.to_raster(sortie)
        return sortie

    def _main():
        p = argparse.ArgumentParser(description=__doc__)
        p.add_argument('entree', help="image d'entrée (GeoTIFF)")
        p.add_argument('-o', '--sortie', default='ndvi.tif', help='fichier de sortie')
        p.add_argument('--bande-rouge', type=int, default=3, help='indice de la bande rouge')
        p.add_argument('--bande-pir', type=int, default=4, help='indice de la bande PIR')
        args = p.parse_args()
        chemin = _calcule_ndvi(args.entree, args.sortie, args.bande_rouge, args.bande_pir)
        print('NDVI enregistré dans', chemin)
    if __name__ == '__main__':
        _main()
    return (argparse,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Grâce aux valeurs par défaut, seul le fichier d'entrée est requis :

    ``` bash
    python ndvi.py RGBNIR_of_S2A.tif                 # utilise tous les défauts
    python ndvi.py RGBNIR_of_S2A.tif -o mon_ndvi.tif --bande-pir 4
    python ndvi.py -h                                # affiche l'aide générée
    ```

    ### 3. Gérer les paramètres avec un fichier YAML

    Dès que les paramètres se multiplient, les passer un à un devient pénible et difficile à **reproduire**. On les regroupe alors dans un fichier de configuration **YAML**, lisible et versionnable. Créons `config.yaml` :

    ``` yaml
    entree: RGBNIR_of_S2A.tif
    sortie: ndvi.tif
    bande_rouge: 3
    bande_pir: 4
    ```

    Le script lit ce fichier avec le module `yaml` (`safe_load` — jamais `load`, qui peut exécuter du code arbitraire). On fusionne les valeurs lues avec un dictionnaire de **défauts** grâce au déballage `**` (voir l'encadré plus haut) : ce qui est absent du YAML prend sa valeur par défaut.
    """)
    return


@app.cell
def _(argparse, rxr):
    """Calcule un NDVI, paramétré par un fichier YAML."""
    import yaml
    DEFAUTS = {'sortie': 'ndvi.tif', 'bande_rouge': 3, 'bande_pir': 4}

    def _calcule_ndvi(entree, sortie, bande_rouge, bande_pir):
        _img = rxr.open_rasterio(entree)
        rouge = _img.sel(band=bande_rouge).astype('float32')
        pir = _img.sel(band=bande_pir).astype('float32')
        ((pir - rouge) / (pir + rouge)).rio.to_raster(sortie)

    def _main():
        p = argparse.ArgumentParser(description=__doc__)
        p.add_argument('config', help='fichier de configuration YAML')
        args = p.parse_args()
        with open(args.config) as f:
            params = {**DEFAUTS, **yaml.safe_load(f)}
        _calcule_ndvi(**params)
        print('NDVI enregistré dans', params['sortie'])
    if __name__ == '__main__':
        _main()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le programme se lance alors simplement avec sa configuration, et rejouer exactement le même traitement ne demande que de conserver le fichier YAML :

    ``` bash
    python ndvi.py config.yaml
    ```

    Pour aller plus loin, un script peut être transformé en **commande installable** (accessible partout, sans préciser `python ...`) en déclarant un *point d'entrée* (`entry point`) dans le fichier `pyproject.toml` du package — le mécanisme utilisé par des outils comme `quarto` ou `jupyter`.

    ## Un avant-goût de NumPy {#sec-00-02}

    Dans ce manuel, une image est avant tout un tableau de nombres. La bibliothèque [NumPy](https://numpy.org/) fournit l'objet `ndarray` qui représente efficacement ces tableaux à plusieurs dimensions : c'est la brique de base de tous les chapitres suivants.
    """)
    return


@app.cell
def _(np):
    image_1 = np.array([[10, 12, 11, 9], [8, 20, 22, 7], [9, 21, 23, 8]])
    print('Forme (lignes, colonnes) :', image_1.shape)
    # Une petite image à une bande : 3 lignes x 4 colonnes
    print('Valeur maximale :', image_1.max())
    print('Moyenne :', image_1.mean().round(2))
    # Découpage d'une sous-image (2 premières lignes, 2 premières colonnes)
    print(image_1[:2, :2])
    return (image_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Attributs et type de données

    Au-delà de la forme (`shape`), un tableau expose son nombre de dimensions (`ndim`), son nombre total d'éléments (`size`) et surtout son **type de données** (`dtype`). Ce dernier encode la *profondeur radiométrique* de l'image : un capteur 8 bits produit des entiers `uint8` (0 à 255), tandis qu'une réflectance se stocke en `float32`. La méthode `astype` convertit d'un type à l'autre.
    """)
    return


@app.cell
def _(image_1):
    print('Dimensions (ndim) :', image_1.ndim)
    print('Nombre de pixels  :', image_1.size)
    print('Type de données   :', image_1.dtype)
    _reflectance = (image_1 / image_1.max()).astype('float32')
    print('Nouveau type      :', _reflectance.dtype)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Créer des tableaux

    On construit souvent un tableau sans l'écrire à la main : un masque rempli de zéros, une bande constante, un axe régulier de longueurs d'onde. NumPy fournit `zeros`, `ones`, `arange` (pas fixe) et `linspace` (nombre de points fixe).
    """)
    return


@app.cell
def _(np):
    print(np.zeros((2, 3)))                 # masque vide (2 x 3)
    print(np.ones(4, dtype="uint8"))        # bande constante
    print(np.arange(0, 10, 2))              # 0, 2, 4, 6, 8
    print(np.linspace(490, 2190, 6))        # 6 longueurs d'onde (nm)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Le *broadcasting*

    Le *broadcasting* applique une opération entre tableaux de formes différentes sans boucle : NumPy « étire » automatiquement la plus petite forme. C'est le mécanisme derrière presque tous les calculs vectorisés du manuel — appliquer un gain scalaire à toute l'image, ou un gain **par bande**.
    """)
    return


@app.cell
def _(image_1, np):
    # Un petit cube à 2 bandes : (bandes, lignes, colonnes)
    cube = np.array([[[10, 12, 11, 9], [8, 20, 22, 7], [9, 21, 23, 8]], [[30, 35, 33, 28], [25, 60, 66, 22], [27, 63, 69, 24]]])
    print('Forme du cube :', cube.shape)
    print((image_1 / 10000).round(4)[0])
    gains = np.array([1.0, 0.5]).reshape(2, 1, 1)
    # Scalaire : convertir des comptes numériques en réflectance
    # Par bande : un gain différent par bande via une forme (bandes, 1, 1)
    print((cube * gains)[:, 0, 0])  # (2, 3, 4)  # applique 1.0 et 0.5 aux 2 bandes
    return (cube,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Remodeler et réordonner les axes

    Deux opérations reviennent constamment sur les images. `reshape` change la forme sans toucher aux données (le nombre total d'éléments est conservé) : c'est ainsi qu'on aplatit une image en une table `pixels × bandes` pour l'entrée d'un classificateur (chapitre 5). `transpose` réordonne les axes : les rasters se chargent en `(bandes, lignes, colonnes)` mais l'affichage attend `(lignes, colonnes, bandes)`.
    """)
    return


@app.cell
def _(cube, image_1):
    # reshape : aplatir puis restaurer une image à une bande
    plat = image_1.reshape(-1)  # 1D : 12 valeurs
    print(plat.shape, '->', plat.reshape(3, 4).shape)
    image_hwc = cube.transpose(1, 2, 0)
    # transpose : (bandes, lignes, colonnes) -> (lignes, colonnes, bandes)
    print('Ordre affichage :', image_hwc.shape)
    table = cube.transpose(1, 2, 0).reshape(-1, 2)  # (3, 4, 2)
    # Aplatir un cube en table (pixels x bandes) pour un classificateur
    print('Table pixels x bandes :', table.shape)  # (12, 2)
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
    <li>Le code s’organise en <strong>modules</strong> (fichiers <code>.py</code>) et <strong>packages</strong> (dossiers avec <code>__init__.py</code>), accessibles par la notation pointée (<code>package.module.fonction</code>).</li>
    <li>Une image est avant tout un <strong>tableau <code>NumPy</code></strong> : c’est la structure centrale de tout le manuel.</li>
    <li>Un tableau se caractérise par sa <strong>forme</strong> (<code>shape</code>) et son <strong>type</strong> (<code>dtype</code>, la profondeur radiométrique) ; le <strong><em>broadcasting</em></strong>, <code>reshape</code> et <code>transpose</code> permettent de calculer et de réorganiser les axes sans boucle.</li>
    </ul>
    </div>
    </div>

    ## Exercices

    <div style="border:0.5px solid silver;border-left:.3rem solid #e34692;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fbe8f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADP0lEQVRYha2XT3LaMBjFf3SyD91rBnqC0BOUbuJl6AkwB9CUnKD0BCXxAeKcIGSpVZ0bwAkKEx8ATkAXemoUgm0I/WY8smVJ7/n78yS3ttstp1iZZF0g1WNhnC3Un6o/N87mVfNbpxAQ+Bw4j7p/qv0R9Y2qSHx4N7q3scBvBLwS8A/dj4ANcCePvLFTPVAAX4yzraivDxCFogcUIvrGE6cSSIE74KdxdlIzrpLEqSGY4V2d1g0yzs6BPnvCcRIB4+waWAKdMsna7yHR2m63aPL4COzCOFuUSZYDQ+DeOJseMjEKB8bZduv58ratjosjCMSltgJ68gZlkg20+KyGRIrPndEZMBD4AuiHhSom9oHfeszxXusAkzLJ1vhc6GjsChjI9bs2UFt8ALp6GDeAt4GpHtfG2SUvMf2O90YHrwk3us/3rJMDV8CTcXZ5VgUYTehroY66NmFh4+w8kuI2r6X4OzthLZNsjM+ZBfJCLQF99Qxfvwu87E5iT+l+ujMvuPgp6kuBX/qAf6Fu8kBP4I/G2UHD2NjGAhpH4He74IcQCNYtk6xdlSNBfoGlcuMLPsbzPeCvkrL1fHk7wSfQ1xC/ncXnvMRyhU/Wmd7tK+ERPjmHwL3aveBwmBL2tdACn4gPSjzwyXchgEf1TXVtmsAPImCcXRtnU+NsT0QCMPgcQQADkTjHV0QgXgkOr3MglUzmu7HWF8dJ2I1keBMBFPgan4lk3vSBsQeG+DJZikgAT4E/ejeMxob7eA/J8aE6Bx7wqlm7x8QErqPJ8aSJ2nuNAV/f18DneG9XuHrAN172i+WhBMJ2CYqtsrwDLLTbBVevjbPTqtgaZ2d1B5QqAkHVFsCFYlxE5OL2qkyyWZlk46ZzwFEEZEHFhvgSW6kvEBwFEvi8KE4h8YaAxKgLfMWLU3dH+3PgIz7OG5FM30tgrxQLsKiapPcz7W53+Lr/fwSaTGU64KValjXDezXvjidQJtkUfwAJ9lj360WDd44iIEUM4Nf4A0ilzB5iZ0BIsJSauMu6am+Ms9O6gZGa1hJsPV/edvFSC14DKs+FeHeG0lzWc/13mPmkM8J+AvovGOC30E7VwHfYEw2/5gB/AcMlhsUeVwFpAAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>À vous de jouer</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <strong>Structures de données</strong>

    <ol type="1">
    <li><em>(listes)</em> Créez <code>bandes = ["bleu", "vert", "rouge", "PIR"]</code>, ajoutez <code>"SWIR"</code>, inversez l’ordre de la liste, puis affichez ses deux premiers éléments.
    </li>
    <li><em>(dictionnaires)</em> Créez un dictionnaire <code>metadonnees</code> décrivant une image (capteur, nombre de bandes, résolution), ajoutez-y une date, puis affichez chaque paire clé-valeur.
    </li>
    <li><em>(ensembles)</em> À partir de <code>["eau", "forêt", "eau", "urbain", "forêt"]</code>, trouvez les classes uniques et affichez leur nombre.
    </li>
    <li><em>(tuples)</em> Stockez les dimensions <code>(512, 512)</code> d’une image dans un tuple, dépaquetez-les en <code>lignes</code> et <code>colonnes</code>, puis calculez le nombre total de pixels.
    </li>
    </ol>
    <strong>Boucles et conditions</strong>

    <ol start="5" type="1">
    <li>Parcourez une liste de valeurs de réflectance et comptez combien dépassent <code>0.3</code>.
    </li>
    <li>Dans une boucle, classez chaque valeur de réflectance en <code>"eau"</code>, <code>"végétation"</code> ou <code>"autre"</code> selon des seuils (<code>if</code>/<code>elif</code>/<code>else</code>).
    </li>
    </ol>
    <strong>Fonctions</strong>

    <ol start="7" type="1">
    <li>Écrivez une fonction <code>ratio(a, b)</code> renvoyant <code>(a - b) / (a + b)</code>, et utilisez-la pour un NDVI avec PIR = 0,55 et Rouge = 0,18.
    </li>
    <li>Écrivez <code>normaliser(valeur, maximum=255)</code> avec un argument par défaut ; testez-la en 8 bits, puis en 12 bits (<code>maximum=4095</code>).
    </li>
    <li><em>(avancé)</em> Écrivez une fonction qui reçoit une liste de bandes et renvoie un dictionnaire <code>{nom_bande: indice}</code> (indice <code>enumerate</code>).
    </li>
    </ol>
    <strong>NumPy</strong>

    <ol start="10" type="1">
    <li>À partir du tableau <code>image</code> de la <a href="#sec-00-02" class="quarto-xref"><span>Section 1.12</span></a>, calculez la valeur <strong>minimale</strong> et l’<strong>écart-type</strong> (<code>image.std()</code>), puis extrayez la dernière colonne.
    </li>
    <li>Créez un tableau NumPy 4 × 4 et, par <strong>masquage booléen</strong>, remplacez par <code>0</code> toutes les valeurs inférieures à 10.
    </li>
    <li>Sur le tableau <code>image</code>, calculez la moyenne <strong>par ligne</strong> puis <strong>par colonne</strong> (paramètre <code>axis</code>).
    </li>
    <li><em>(attributs)</em> Sur <code>image</code>, affichez <code>ndim</code>, <code>size</code> et <code>dtype</code>. Convertissez-le en réflectance <code>float32</code> (divisez par le maximum) et vérifiez le nouveau <code>dtype</code>.
    </li>
    <li><em>(création)</em> Avec <code>np.linspace</code>, construisez un axe de 6 longueurs d’onde entre 490 et 2190 nm. Créez ensuite un masque <code>np.zeros((3, 4))</code> et mettez sa <strong>première ligne</strong> à <code>1</code>.
    </li>
    <li><em>(broadcasting)</em> Sur le <code>cube</code> à 2 bandes de la <a href="#sec-00-02" class="quarto-xref"><span>Section 1.12</span></a>, multipliez chaque bande par un gain différent <code>[1.0, 0.8]</code> à l’aide d’une forme <code>(2, 1, 1)</code>.
    </li>
    <li><em>(reshape/transpose)</em> Transformez le <code>cube</code> <code>(2, 3, 4)</code> en une table <code>(12, 2)</code> (pixels × bandes), puis revenez à la forme d’origine <code>(2, 3, 4)</code>.
    </li>
    </ol>
    <strong>Programmation objet</strong>

    <ol start="17" type="1">
    <li><em>(avancé)</em> Ajoutez à la classe <code>Image</code> une méthode <code>est_multispectrale()</code> qui renvoie <code>True</code> si l’image possède plus de 3 bandes.</li>
    </ol>
    </div>
    </div>

    <details>

    <summary>Afficher les solutions</summary>

    ``` python
    import numpy as np

    # --- Structures de données ---
    # 1. Listes
    bandes = ["bleu", "vert", "rouge", "PIR"]
    bandes.append("SWIR")
    bandes.reverse()
    print(bandes[:2])

    # 2. Dictionnaire de métadonnées
    metadonnees = {"capteur": "Sentinel-2", "bandes": 13, "resolution_m": 10}
    metadonnees["date"] = "2024-07-01"
    for cle, valeur in metadonnees.items():
        print(cle, ":", valeur)

    # 3. Ensembles : classes uniques
    classes = ["eau", "forêt", "eau", "urbain", "forêt"]
    uniques = set(classes)
    print(uniques, "->", len(uniques), "classes")

    # 4. Tuples : dépaquetage et nombre de pixels
    dimensions = (512, 512)
    lignes, colonnes = dimensions
    print("pixels :", lignes * colonnes)

    # --- Boucles et conditions ---
    reflectances = [0.12, 0.45, 0.33, 0.28, 0.51]
    # 5. Compter les valeurs > 0.3
    print(sum(1 for r in reflectances if r > 0.3))

    # 6. Classer selon des seuils
    for r in reflectances:
        if r < 0.15:
            print(r, "-> eau")
        elif r > 0.3:
            print(r, "-> végétation")
        else:
            print(r, "-> autre")

    # --- Fonctions ---
    # 7. ratio / NDVI
    def ratio(a, b):
        return (a - b) / (a + b)
    print("NDVI :", round(ratio(0.55, 0.18), 3))

    # 8. normaliser avec argument par défaut
    def normaliser(valeur, maximum=255):
        return valeur / maximum
    print(normaliser(128))
    print(normaliser(1000, maximum=4095))   # 12 bits

    # 9. dict {nom_bande: indice}
    def indexer(bandes):
        return {nom: i for i, nom in enumerate(bandes)}
    print(indexer(["bleu", "vert", "rouge", "PIR"]))

    # --- NumPy ---
    image = np.array([[10, 12, 11,  9],
                      [ 8, 20, 22,  7],
                      [ 9, 21, 23,  8]])
    cube = np.array([[[10, 12, 11,  9],
                      [ 8, 20, 22,  7],
                      [ 9, 21, 23,  8]],
                     [[30, 35, 33, 28],
                      [25, 60, 66, 22],
                      [27, 63, 69, 24]]])
    # 10. min, écart-type, dernière colonne
    print("min :", image.min(), "| écart-type :", round(image.std(), 2))
    print("dernière colonne :", image[:, -1])

    # 11. Masquage booléen : valeurs < 10 -> 0
    arr = np.array([[ 3, 12,  8, 15],
                    [20,  5,  9, 11],
                    [ 7, 14,  2, 18],
                    [10,  6, 13,  4]])
    arr[arr < 10] = 0
    print(arr)

    # 12. Moyennes par axe
    print("par ligne   :", image.mean(axis=1).round(1))
    print("par colonne :", image.mean(axis=0).round(1))

    # 13. Attributs et dtype
    print(image.ndim, image.size, image.dtype)
    refl = (image / image.max()).astype("float32")
    print(refl.dtype)

    # 14. Création : axe de longueurs d'onde et masque
    print(np.linspace(490, 2190, 6))
    masque = np.zeros((3, 4))
    masque[0] = 1
    print(masque)

    # 15. Broadcasting par bande
    gains = np.array([1.0, 0.8]).reshape(2, 1, 1)
    print((cube * gains)[:, 0, 0])

    # 16. reshape / transpose
    table = cube.transpose(1, 2, 0).reshape(-1, 2)
    print(table.shape)                      # (12, 2)
    retour = table.reshape(3, 4, 2).transpose(2, 0, 1)
    print(retour.shape)                     # (2, 3, 4)

    # --- Programmation objet ---
    # 17. Méthode est_multispectrale
    class Image:
        def __init__(self, capteur, bandes):
            self.capteur = capteur
            self.bandes = bandes
        def est_multispectrale(self):
            return self.bandes > 3
    print(Image("Landsat-8", 11).est_multispectrale())
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
def _(Quiz, render_quizz):
    Chap00Quiz = Quiz('quiz/Chap00.yml', 'Chap00')
    render_quizz(Chap00Quiz)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Revise the slides, make sure: 1) one slide per concept 2) make sure that all the sections are mapped on at least one slide 3) explain the concept in a few bullet point 4) include a code exemple if possible
    """)
    return


if __name__ == "__main__":
    app.run()
