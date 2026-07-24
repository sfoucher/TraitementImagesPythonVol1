import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams["image.aspect"]= 'equal'
    plt.rcParams['figure.dpi'] = 100
    import warnings
    warnings.filterwarnings('ignore')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Classifications d'images supervisées {#sec-chap05}

    ## Préambule

    Assurez-vous de lire ce préambule avant d'exécuter le reste du notebook.

    ### Objectifs

    Dans ce chapitre, nous ferons une introduction générale à l'apprentissage automatique et abordons quelques techniques fondamentales. La librairie centrale utilisée dans ce chapitre sera [`scikit-learn`](https://scikit-learn.org/). Ce chapitre est aussi disponible sous la forme d'un notebook Python sur Google Colab:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/05-ClassificationsSupervisees.ipynb)

    <div style="border:0.5px solid silver;border-left:.3rem solid #00796d;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2efec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADfUlEQVRYhb2XMXLbMBBFnzVKkSZ0ylRmJkVKMycwfQIrJzB9AVruMsNGLlCHwQVC3UC+AXUC02WKTOQ+hXGAjFNgIYIQZNkZxzvD4UhY7H7s/l0s9+7v73msJFWZAzmQAfvBcidPa5RePdbm3i4ASVWmwBQogOSRdpdAY5RuIvb2gX0H8kEASVXOxHkCGGAhT2uUvgt0M2x0CuBQ/r4BCqN05+m0wMQo3QKMtzjOgEYMGeAsdhpfxEkH1BK1GjhBUuU5H0RxIwKB4pWcYHDax0pSlalRehVxfiFghwACxQujdP0vjgMQ0ZOLfBt7ivvYsCc8EHLRy7GV4OQOy4su0C2wqYg5PzNKNz4HZticz7ewNxWd0xgw0bkFZt7+mHODTesCYCQbM+AcuMWyPjQ8websVHQugWPvOQPmwAE9CQFWEee5cw7CgaQqF1jGHrvy8JwXwHf5+SAvPMd32HI98pZvsOW3SqqyBmqj9Gokm06A24jzFBtGA3zaRUqvA7bifAm8xUYpF+c5NtozsH0gl00x4w09KdcEEyIW9O24M0ovAsbPjdKFB8iBbJOqNMDEAZjI2jov4iRzp/BJuY3ZSVX+AN4Bb5BUiY3CKB3yagGcJlWZjYAUMJELxAFbR0ZSsuYDfXh/Ah+B19ho1d7eczallXc2wpZeF1HKA2WQvAFTo3QtHbIAPgB/gFeB/p0AzxnKSt7pKOJ4IEEbTrHRasRwgy3NG+CLp+MkdrCB7ASwQ3Is03Pgd2R95x2yE4Aw3skKSKQxYZROjdK5RGnq6TgJh5YNGWPDl0XWWmwVTLDlCH0rbmRWWIiTGsulq4DMDmgb2E4d2JF3qjRQcmVZuD/E+Jn8/Ar8Aq7pm85aV4h3iL3SQ8nl3Y08RxNfQxrPEjiS2nf/N3KCC+ydcAl89lLhpA7eIQBjlO7G9GUzjSgX9FNO57qhOHroTmjoU9IGaxPspTUHGElY58BBWK+y5mbC66QqN27KwHiaVKW7NW/wUuKJs1FDfxtm2FzeAllk4HRETESnYdhwUmxY3awQHeW8m3VplM7XAGTRtU3/Ehmcjh0DiYDzB5JwfyeHeL8xlku9t9jcPctIFuxxtgczxUsMpb7zjej+77E8x5Z5OB9sByAbU9noPkymuz5MIvvdhwnApVF6FtN90U+zJwPwTvNsH6dPBhCAyXnmz/O/0JrtInNZu4wAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Objectifs d’apprentissage visés dans ce chapitre</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">

    </div>
    </div>

    ### Librairies

    Les librairies utilisées dans ce chapitre sont les suivantes :

    -   [SciPy](https://scipy.org/)

    -   [NumPy](https://numpy.org/)

    -   [opencv-python · PyPI](https://pypi.org/project/opencv-python/)

    -   [scikit-image](https://scikit-image.org/)

    -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

    -   [xarray](https://docs.xarray.dev/en/stable/)

    -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

    -   [geopandas](https://geopandas.org)

    -   [scikit-learn](https://scikit-learn.org/)

    Dans l'environnement Google Colab, seul `rioxarray` et `xrscipy` sont installés:
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # !pip install -qU matplotlib rioxarray xrscipy supertree
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifiez les importations nécessaires en premier:
    """)
    return


@app.cell
def _():
    import numpy as np
    import rioxarray as rxr
    from scipy import signal
    import xarray as xr
    import rasterio
    import xrscipy
    from matplotlib.colors import ListedColormap
    import geopandas
    from shapely.geometry import Point
    import pandas as pd
    from numba import jit
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
    from sklearn.preprocessing import StandardScaler
    from sklearn.inspection import DecisionBoundaryDisplay
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
    from sklearn.datasets import make_blobs, make_classification, make_gaussian_quantiles

    return (
        ConfusionMatrixDisplay,
        DecisionBoundaryDisplay,
        KNeighborsClassifier,
        ListedColormap,
        Pipeline,
        Point,
        QuadraticDiscriminantAnalysis,
        StandardScaler,
        classification_report,
        confusion_matrix,
        geopandas,
        jit,
        make_blobs,
        make_classification,
        make_gaussian_quantiles,
        np,
        pd,
        rasterio,
        rxr,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Images utilisées

    Nous utilisons les images suivantes dans ce chapitre:
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # import gdown
    # 
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6Ypg0g1Oy4AJt9XWKWfnR12NW1XhNg_', output= 'RGBNIR_of_S2A.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a4PQ68Ru8zBphbQ22j0sgJ4D2quw-Wo6', output= 'landsat7.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1dM6IVqjba6GHwTLmI7CpX8GP2z5txUq6', output= 'SAR.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1aAq7crc_LoaLC3kG3HkQ6Fv5JfG0mswg', output= 'carte.tif')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifiez que vous êtes capable de les lire :
    """)
    return


@app.cell
def _(rxr):
    with rxr.open_rasterio('berkeley.jpg', mask_and_scale= True) as img_rgb:
        print(img_rgb)
    with rxr.open_rasterio('RGBNIR_of_S2A.tif', mask_and_scale= True) as img_rgbnir:
        print(img_rgbnir)
    with rxr.open_rasterio('SAR.tif', mask_and_scale= True) as img_SAR:
        print(img_SAR)
    with rxr.open_rasterio('carte.tif', mask_and_scale= True) as img_carte:
        print(img_carte)
    return img_carte, img_rgbnir


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Principes généraux

    Une classification supervisée ou dirigée consiste à attribuer une étiquette (une classe) de manière automatique à chaque point d'un jeu de données. Cette classification peut se faire à l'aide d'une cascade de règles pré-établies (arbre de décision) ou à l'aide de techniques d'apprentissage automatique (*machine learning*). L'utilisation de règles pré-établies atteint vite une limite car ces règles doivent être fournies manuellement par un expert. Ainsi, l'avantage de l'apprentissage automatique est que les règles de décision sont dérivées automatiquement du jeu de données via une phase dite d’entraînement. On parle souvent de solutions générées par les données (*Data Driven Solutions*). Cet ensemble de règles est souvent appelé **modèle**. On visualise souvent ces règles sous la forme de *frontières de décisions* dans l'espace des données. Cependant, un des défis majeurs de ce type de technique est d'être capable de produire des règles qui soient généralisables au-delà du jeu d’entraînement.

    Les classifications supervisées ou dirigées présupposent donc que nous avons à disposition **un jeu d’entraînement** déjà étiqueté. Celui-ci va nous permettre de construire un modèle. Afin que ce modèle soit représentatif et robuste, il nous faut assez de données d’entraînement. Les algorithmes d'apprentissage automatique sont très nombreux et plus ou moins complexes pouvant produire des frontières de décision très complexes et non linéaires.

    ### Comportement d'un modèle

    Cet exemple tiré de [`scikit-learn`](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html#sphx-glr-auto-examples-model-selection-plot-underfitting-overfitting-py) illustre les problèmes d'ajustement insuffisant ou **sous-apprentissage** (*underfitting*) et d'ajustement excessif ou **sur-apprentissage** (*overfitting*) et montre comment nous pouvons utiliser la régression linéaire avec un modèle polynomiale pour approximer des fonctions non linéaires. La @fig-overfitting montre la fonction que nous voulons approximer, qui est une partie de la fonction cosinus (couleur orange). En outre, les échantillons de la fonction réelle et les approximations de différents modèles sont affichés en bleu. Les modèles ont des caractéristiques polynomiales de différents degrés. Nous pouvons constater qu'une fonction linéaire (polynôme de degré 1) n'est pas suffisante pour s'adapter aux échantillons d'apprentissage. C'est ce qu'on appelle un sous-ajustement (*underfitting*) qui produit un biais systématique quels que soient les points d’entraînement. Un polynôme de degré 4 se rapproche presque parfaitement de la fonction réelle. Cependant, pour des degrés plus élevés, le modèle s'adaptera trop aux données d'apprentissage, c'est-à-dire qu'il apprendra le bruit des données d'apprentissage. Nous évaluons quantitativement le sur-apprentissage et le sous-apprentissage à l'aide de la validation croisée. Nous calculons l'erreur quadratique moyenne (EQM) sur l'ensemble de validation. Plus elle est élevée, moins le modèle est susceptible de se généraliser correctement à partir des données d'apprentissage.
    """)
    return


@app.cell
def _(Pipeline, np, plt):
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import cross_val_score, cross_validate
    from sklearn.preprocessing import PolynomialFeatures

    def true_fun(X):
        return np.cos(1.5 * np.pi * X + np.pi / 2)
    np.random.seed(0)
    noise_level = 0.1
    _n_samples = 30
    degrees = [1, 4, 15]
    X = np.sort(np.random.rand(_n_samples))
    y = true_fun(X) + np.random.randn(_n_samples) * noise_level
    X_test = np.sort(np.random.rand(10))
    y_test = true_fun(X_test) + np.random.randn(int(10)) * noise_level
    plt.figure(figsize=(14, 5))
    results = []
    for _i in range(len(degrees)):
        _ax = plt.subplot(1, len(degrees), _i + 1)
        plt.setp(_ax, xticks=(), yticks=())
        polynomial_features = PolynomialFeatures(degree=degrees[_i], include_bias=False)
        linear_regression = LinearRegression()
        pipeline = Pipeline([('polynomial_features', polynomial_features), ('linear_regression', linear_regression)])
        pipeline.fit(X[:, np.newaxis], y)
        scores = cross_validate(pipeline, X[:, np.newaxis], y, scoring='neg_mean_squared_error', cv=10, return_train_score=True)
        X_true = np.linspace(0, 1, 100)
        plt.plot(X_true, pipeline.predict(X_true[:, np.newaxis]), label='Modèle')
        plt.plot(X_true, true_fun(X_true), label='Vraie fonction')
        plt.scatter(X, y, edgecolor='b', s=20, label='Entr.')
        plt.scatter(X_test, y_test, edgecolor='g', s=20, label='Test')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim((0, 1))
        plt.ylim((-2, 2))
        plt.legend(loc='best')
        plt.title('Degré {}\nErreur = {:.1e}(+/- {:.1e})'.format(degrees[_i], -scores['test_score'].mean(), scores['test_score'].std()), fontsize='small')
        results.append([degrees[_i], -scores['train_score'].mean(), -scores['test_score'].mean(), scores['train_score'].std(), scores['test_score'].std()])
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On constate aussi que sans les échantillons de validation, nous serions incapables de déterminer la situation de sur-apprentissage, l'erreur sur les points d’entraînement seuls étant excellente pour un degré 15.

    ### Pipeline

    La construction d'un modèle implique généralement toujours les mêmes étapes suivantes:

    1.  La préparation des données implique parfois un pré-traitement afin de normaliser les données.

    2.  Partage des données en trois groupes: entraînement, validation et test.

    3.  L'apprentissage du modèle sur l'ensemble d'entraînement. Cet apprentissage nécessite de déterminer les valeurs des hyper-paramètres du modèle par l'usager.

    4.  La validation du modèle sur l'ensemble de validation. Cette étape vise à vérifier que les hyper-paramètres du modèle sont adéquats.

    5.  Enfin le test du modèle sur un ensemble de données indépendant.

    ### Construction d'un ensemble d’entraînement {#sec-05.02.02}

    Les données d’entraînement permettent de construire un modèle. Elles peuvent prendre des formes très variées mais on peut voir cela sous la forme d'un tableau $N \times D$:

    1.  La taille $N$ du jeu de données.

    2.  Chaque entrée définit un échantillon ou un point dans un espace à plusieurs dimensions.

    3.  Chaque échantillon est décrit par $D$ dimensions ou caractéristiques (*features*).

    Une façon simple de construire un ensemble d’entraînement est d'échantillonner un produit existant. Nous utilisons une carte d'occupation des sols qui contient 12 classes différentes.
    """)
    return


@app.cell
def _():
    couleurs_classes= {'NoData': 'black', 'Commercial': 'yellow', 'Nuages': 'lightgrey', 
                        'Foret': 'darkgreen', 'Faible_végétation': 'green', 'Sol_nu': 'saddlebrown',
                      'Roche': 'dimgray', 'Route': 'red', 'Urbain': 'orange', 'Eau': 'blue', 'Tourbe': 'salmon', 'Végétation éparse': 'darkgoldenrod', 'Roche avec végétation': 'darkseagreen'}
    nom_classes= [*couleurs_classes.keys()]
    couleurs_classes= [*couleurs_classes.values()]
    return couleurs_classes, nom_classes


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut visualiser la carte de la façon suivante :
    """)
    return


@app.cell
def _(ListedColormap, couleurs_classes, img_carte, plt):
    cmap_classes = ListedColormap(couleurs_classes)
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    img_carte.squeeze().plot.imshow(cmap=cmap_classes, vmin=0, vmax=12)
    _ax.set_title("Carte d'occupation des sols", fontsize='small')
    return (cmap_classes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut facilement calculer la fréquence d’occurrences des 12 classes dans l'image à l'aide de `numpy`:
    """)
    return


@app.cell
def _(img_carte, np):
    img_carte_1 = img_carte.squeeze()  # nécessaire pour ignorer la dimension du canal
    compte_classe = np.unique(img_carte_1.data, return_counts=True)
    print(compte_classe)
    return compte_classe, img_carte_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La fréquence d'apparition de chaque classe varie grandement, on parle alors d'un **ensemble déséquilibré**. Ceci est très commun dans la plupart des ensembles d’entraînement, puisque les classes ont très rarement la même fréquence. Par exemple, à la lecture du graphique en barres verticales, on constate que la classe forêt est très présentes contrairement à plusieurs autres classes (notamment, tourbe, végétation éparse, roche, sol nu et nuages).
    """)
    return


@app.cell
def _(compte_classe, nom_classes, plt):
    valeurs, comptes = compte_classe

    # Create the histogram
    plt.figure(figsize=(5, 3))
    plt.bar(valeurs, comptes/comptes.sum()*100)
    plt.xlabel("Classes")
    plt.ylabel("%")
    plt.title("Fréquences des classes", fontsize="small")
    plt.xticks(range(len(nom_classes)), nom_classes, rotation=45, ha='right')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut échantillonner aléatoirement 100 points pour chaque classe:
    """)
    return


@app.cell
def _(cmap_classes, img_carte_1, np, plt, rasterio):
    img_carte_2 = img_carte_1.squeeze()
    class_counts = np.unique(img_carte_2.data, return_counts=True)
    sampled_points = []
    class_labels = []
    for class_label in range(1, 13):
        class_pixels = np.argwhere(img_carte_2.data == class_label)
        _n_samples = min(100, len(class_pixels))
        np.random.seed(0)
        sampled_indices = np.random.choice(len(class_pixels), _n_samples, replace=False)
        sampled_pixels = class_pixels[sampled_indices]
        sampled_points.extend(sampled_pixels)
        class_labels.extend(np.array([class_label] * _n_samples)[:, np.newaxis])
    sampled_points = np.array(sampled_points)
    class_labels = np.array(class_labels)
    transformer = rasterio.transform.AffineTransformer(img_carte_2.rio.transform())
    transform_sampled_points = transformer.xy(sampled_points[:, 0], sampled_points[:, 1])
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    img_carte_2.squeeze().plot.imshow(cmap=cmap_classes, vmin=0, vmax=12)
    _ax.scatter(transform_sampled_points[0], transform_sampled_points[1], c='w', s=1)
    _ax.set_title("Carte d'occupation des sols avec les points échantillonnés", fontsize='small')
    plt.show()
    return class_labels, img_carte_2, transform_sampled_points


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Une fois les points sélectionnés, on ajoute les valeurs des bandes provenant d'une image satellite. Pour cela, on utilise la méthode `sample()` de `rasterio`. Éventuellement, la librairie [`geopandas`](https://geopandas.org) permet de gérer les données d’entraînement sous la forme d'un tableau transportant aussi l'information de géoréférence. Afin de pouvoir classifier ces points, on ajoute les valeurs radiométriques provenant de l'image Sentinel-2 à 4 bandes `RGBNIR_of_S2A.tif`. Ces valeurs seront stockées dans la colonne `value` sous la forme d'un vecteur en format `string` :
    """)
    return


@app.cell
def _(
    Point,
    class_labels,
    geopandas,
    img_carte_2,
    rasterio,
    transform_sampled_points,
):
    points = [Point(xy) for xy in zip(transform_sampled_points[0], transform_sampled_points[1])]
    gdf = geopandas.GeoDataFrame(range(1, len(points) + 1), geometry=points, crs=img_carte_2.rio.crs)
    coord_list = [(x, y) for (x, y) in zip(gdf['geometry'].x, gdf['geometry'].y)]
    with rasterio.open('RGBNIR_of_S2A.tif') as src:
        gdf['value'] = [x for x in src.sample(coord_list)]
    gdf['class'] = class_labels
    gdf.to_csv('sampling_points.csv')  # sauvegarde sous forme d'un format csv
    gdf.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analyse préliminaire des données

    Une bonne pratique avant d'appliquer une technique d'apprentissage automatique est de regarder les caractéristiques de vos données:

    1.  Le nombre de dimensions (*features*).

    2.  Certaines dimensions sont informatives (discriminantes) et d'autres ne le sont pas.

    3.  Le nombre classes.

    4.  Le nombre de modes (*clusters*) par classes.

    5.  Le nombre d'échantillons par classe.

    6.  La forme des groupes.

    7.  La séparabilité des classes ou des groupes.

    Une manière d'évaluer la séparabilité de vos classes est d'appliquer des modèles Gaussiens sur chacune des classes. Le modèle Gaussien multivarié suppose que les données sont distribuées comme un nuage de points symétrique et unimodale. La distribution d'un point $x$ appartenant à la classe $i$ est la suivante:

    $$
    P(x | Classe=i) = \frac{1}{(2\pi)^{D/2} |\Sigma_i|^{1/2}}\exp\left(-\frac{1}{2} (x-m_i)^t \Sigma_k^{-1} (x-m_i)\right)
    $$

    La méthode [`QuadraticDiscriminantAnalysis`](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis.html) permet de calculer les paramètres des Gaussiennes multivariées pour chacune des classes.

    On peut calculer une distance entre deux nuages Gaussiens avec la distance dites de Jeffries-Matusita (JM) basée sur la distance de Bhattacharyya $B$ [@Jensen2016]:

    $$
    \begin{aligned}
    JM_{ij} &= 2(1 - e^{-B_{ij}}) \\
    B_{ij} &= \frac{1}{8}(m_i - m_j)^t \left( \frac{\Sigma_i + \Sigma_j}{2} \right)^{-1} (m_i - m_j) + \frac{1}{2} \ln \left( \frac{|(\Sigma_i + \Sigma_j)/2|}{|\Sigma_i|^{1/2} |\Sigma_j|^{1/2}} \right)
    \end{aligned}
    $$

    Cette distance présuppose que chaque classe $i$ est décrite par son centre $m_i$ et de sa dispersion dans l'espace à $D$ dimensions mesurée par la matrice de covariance $\Sigma_i$. On peut en faire facilement une fonction Python à l'aide de `numpy`:
    """)
    return


@app.cell
def _(np):
    def bhattacharyya_distance(m1, s1, m2, s2):
        # Calcul de la covariance moyenne
        s = (s1 + s2) / 2
    
        # Calcul du premier terme (différence des moyennes)
        m_diff = m1 - m2
        term1 = np.dot(np.dot(m_diff.T, np.linalg.inv(s)), m_diff) / 8
    
        # Calcul du second terme (différence de covariances)
        term2 = 0.5 * np.log(np.linalg.det(s) / np.sqrt(np.linalg.det(s1) * np.linalg.det(s2)))
    
        return term1 + term2

    def jeffries_matusita_distance(m1, s1, m2, s2):
        B = bhattacharyya_distance(m1, s1, m2, s2)
        return 2 * (1 - np.exp(-B))

    return (jeffries_matusita_distance,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La figure ci-dessous illustre différentes situations avec des données simulées ainsi que les distances JM correspondantes :
    """)
    return


@app.cell
def _(
    ListedColormap,
    QuadraticDiscriminantAnalysis,
    jeffries_matusita_distance,
    make_blobs,
    make_classification,
    make_gaussian_quantiles,
    np,
    plt,
):
    cmap_classes_1 = ListedColormap(['blue', 'yellow', 'red'])
    np.random.seed(42)
    plt.figure(figsize=(8, 8))
    plt.subplots_adjust(bottom=0.05, top=0.9, left=0.05, right=0.95)
    plt.subplot(321)
    (X1, Y1) = make_classification(n_features=2, n_redundant=0, n_informative=1, n_clusters_per_class=1)
    qda = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda.fit(X1, Y1)
    jm = jeffries_matusita_distance(qda.means_[0], qda.covariance_[0], qda.means_[1], qda.covariance_[1])
    plt.title(f'Une dimension informative, un mode par classe JM_12={jm:3.2f}', fontsize='small')
    plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=Y1, s=25, edgecolor='k', cmap=cmap_classes_1)
    plt.subplot(322)
    (X1, Y1) = make_classification(n_features=2, n_redundant=0, n_informative=2, n_clusters_per_class=1)
    qda = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda.fit(X1, Y1)
    jm = jeffries_matusita_distance(qda.means_[0], qda.covariance_[0], qda.means_[1], qda.covariance_[1])
    plt.title(f'Deux dimensions informatives, un mode par classe JM_12={jm:3.2f}', fontsize='small')
    plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=Y1, s=25, edgecolor='k', cmap=cmap_classes_1)
    plt.subplot(323)
    (X2, Y2) = make_classification(n_features=2, n_redundant=0, n_informative=2)
    qda = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda.fit(X2, Y2)
    jm = jeffries_matusita_distance(qda.means_[0], qda.covariance_[0], qda.means_[1], qda.covariance_[1])
    plt.title(f'Deux dimensions informatives, deux modes par classe JM_12={jm:3.2f}', fontsize='small')
    plt.scatter(X2[:, 0], X2[:, 1], marker='o', c=Y2, s=25, edgecolor='k', cmap=cmap_classes_1)
    plt.subplot(324)
    (X1, Y1) = make_classification(n_features=2, n_redundant=0, n_informative=2, n_clusters_per_class=1, n_classes=3)
    qda = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda.fit(X1, Y1)
    jm = jeffries_matusita_distance(qda.means_[0], qda.covariance_[0], qda.means_[1], qda.covariance_[1])
    plt.title(f'Trois classes, deux dimensions informatives, un mode JM_12={jm:3.2f}', fontsize='small')
    plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=Y1, s=25, edgecolor='k', cmap=cmap_classes_1)
    plt.subplot(325)
    (X1, Y1) = make_blobs(n_features=2, centers=3)
    qda = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda.fit(X1, Y1)
    jm = jeffries_matusita_distance(qda.means_[0], qda.covariance_[0], qda.means_[1], qda.covariance_[1])
    plt.title(f'Trois classes JM_12={jm:3.2f}', fontsize='small')
    plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=Y1, s=25, edgecolor='k', cmap=cmap_classes_1)
    plt.subplot(326)
    (X1, Y1) = make_gaussian_quantiles(n_features=2, n_classes=3)
    qda = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda.fit(X1, Y1)
    jm = jeffries_matusita_distance(qda.means_[0], qda.covariance_[0], qda.means_[1], qda.covariance_[1])
    plt.title(f'Trois classes, Gaussiennes superposées JM_12={jm:3.2f}', fontsize='small')
    plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=Y1, s=25, edgecolor='k', cmap=cmap_classes_1)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On forme notre ensemble d'entrainement à partir du fichier `csv` de la section @sec-05.02.02.
    """)
    return


@app.cell
def _(ListedColormap, couleurs_classes, nom_classes, np, pd):
    _df = pd.read_csv('sampling_points.csv')
    X_1 = _df['value'].apply(lambda x: np.fromstring(x[1:-1], dtype=float, sep=' ')).to_list()
    X_1 = np.array([row.tolist() for row in X_1])
    _idx = X_1.sum(axis=-1) > 0
    X_1 = X_1[_idx, ...]
    y_1 = _df['class'].to_numpy()
    y_1 = y_1[_idx]
    class_labels_1 = np.unique(y_1).tolist()
    _n_classes = len(class_labels_1)
    if max(class_labels_1) > _n_classes:
        y_new = []
        for (_i, _l) in enumerate(class_labels_1):
            y_new.extend([_i] * sum(y_1 == _l))
        y_new = np.array(y_new)
    _couleurs_classes2 = [couleurs_classes[c] for c in np.unique(y_1).tolist()]
    nom_classes2 = [nom_classes[c] for c in np.unique(y_1).tolist()]
    cmap_classes2 = ListedColormap(_couleurs_classes2)
    return X_1, cmap_classes2, nom_classes2, y_1, y_new


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut faire une analyse de séparabilité sur notre ensemble d'entrainement de 10 classes. On obtient un tableau symétrique de 10x10 valeurs. On observe des valeurs inférieures à 1, indiquant des séparabilités faibles entre ces classes sous l'hypothèse du modèle Gaussien:
    """)
    return


@app.cell
def _(
    QuadraticDiscriminantAnalysis,
    X_1,
    jeffries_matusita_distance,
    np,
    pd,
    y_new,
):
    qda_1 = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda_1.fit(X_1, y_new)  # calcul des paramètres des distributions Gaussiennes
    JM = []
    classes = np.unique(y_new).tolist()  # étiquettes uniques des classes
    for cl1 in classes:
        for cl2 in classes:
            JM.append(jeffries_matusita_distance(qda_1.means_[cl1], qda_1.covariance_[cl1], qda_1.means_[cl2], qda_1.covariance_[cl2]))
    JM = np.array(JM).reshape(len(classes), len(classes))
    JM = pd.DataFrame(JM, index=classes, columns=classes)
    JM.head(10)
    return (JM,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Afin d'évaluer chaque classe, on peut calculer la séparabilité minimale, ce qui nous permet de constater que la classe eau a le maximum de séparabilité avec les autres classes.
    """)
    return


@app.cell
def _(JM, nom_classes2, np, plt):
    plt.figure(figsize=(5, 3))
    plt.bar(range(JM.shape[0]), np.min(JM[JM>0],axis=1))
    plt.xlabel("Classes")
    plt.ylabel("JM")
    plt.title("Séparabilité minimale", fontsize="small")
    plt.xticks(range(len(nom_classes2)), nom_classes2, rotation=45, ha='right')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mesures de performance d'une méthode de classification

    Lorsque que l'on cherche à établir la performance d'un modèle, il convient de mesurer la performance du classificateur utilisé. Il existe de nombreuses mesures de performance qui sont toutes dérivées de la matrice de confusion. Cette matrice compare les étiquettes provenant de l'annotation (la vérité terrain) et les étiquettes prédites par un modèle. On peut définir $C(i,j)$ comme étant le nombre de prédictions dont la vérité terrain indique la classe $i$ qui sont prédites dans la classe $j$. La fonction [confusion_matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html) permet de faire ce calcul, voici un exemple très simple:
    """)
    return


@app.cell
def _(confusion_matrix):
    _y_true = ['cat', 'ant', 'cat', 'cat', 'ant', 'bird', 'bird']
    y_pred = ['ant', 'ant', 'cat', 'cat', 'ant', 'cat', 'bird']
    confusion_matrix(_y_true, y_pred, labels=['ant', 'bird', 'cat'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La fonction [classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report) permet de générer quelques métriques:
    """)
    return


@app.cell
def _(classification_report):
    _y_true = ['cat', 'ant', 'cat', 'cat', 'ant', 'bird', 'bird']
    y_pred_1 = ['ant', 'ant', 'cat', 'cat', 'ant', 'cat', 'bird']
    print(classification_report(_y_true, y_pred_1, target_names=['ant', 'bird', 'cat']))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le rappel (*recall*) pour une classe donnée est la proportion de la vérité terrain qui a été correctement identifiée et est sensible aux confusions entre classes (erreurs d'omission). Les valeurs de rappels correspondent à une normalisation de la matrice de confusion par rapport aux lignes.

    $$
    Recall_i= C_{ii} / \sum_j C_{ij}
    $$ Une faible valeur de rappel signifie que le classificateur confond facilement la classe concernée avec d'autres classes.

    La précision est la portion des prédictions qui ont été bien classifiées et est sensible aux fausses alarmes (erreurs de commission). Les valeurs de précision correspondent à une normalisation de la matrice de confusion par rapport aux colonnes. $$
    Precision_i= C_{ii} / \sum_j C_{ji}
    $$ Une faible valeur de précision signifie que le classificateur trouve facilement la classe concernée dans d'autres classes.

    Le `f1-score` calcul une moyenne des deux métriques précédentes: $$
    \text{f1-score}_i=2\frac{Recall_i \times Precision_i}{Recall_i + Precision_i}
    $$

    ## Méthodes non paramétriques

    Les méthodes non paramétriques ne font pas d'hypothèses particulières sur les données. Un des inconvénients de ces modèles est que le nombre de paramètres du modèle augmente avec la taille des données.

    ### Méthode des parallélépipèdes {#sec-0511}

    La méthode du parallélépipède est probablement la plus simple et consiste à délimiter directement le domaine des points d'une classe par une boite (un parallélépipède) à $D$ dimensions. Les limites de ces parallélépipèdes forment alors des frontières de décision manuelles qui permettent d'attribuer une classe d'appartenance à un nouveau point. Un des avantages de cette technique est que si un point n'est dans aucun parallélépipède alors il est non classifié. Par contre, la construction de ces parallélépipèdes se complexifient grandement avec le nombre de bandes. À une dimension, deux paramètres, équivalents à un seuillage d'histogramme, sont suffisants. À deux dimensions, vous devez définir 4 segments par classe. Avec trois bandes, vous devez définir six plans par classes et à D dimensions, D hyperplans à D-1 dimensions par classe. Le modèle ici est donc une suite de valeurs `min` et `max` pour chacune des bandes et des classes:
    """)
    return


@app.cell
def _(X_1, np, y_new):
    def parrallepiped_train(X_train, y_train):
        classes = np.unique(y_train).tolist()
        clf = []
        for cl in classes:
            data_cl = X_train[y_train == cl, ...]  # on cherche les données pour la classe courante
            limits = []
            for b in range(data_cl.shape[1]):
                limits.append([data_cl[:, b].min(), data_cl[:, b].max()])
            clf.append(np.array(limits))  # on calcul le min et max pour chaque bande
        return clf
    clf = parrallepiped_train(X_1, y_new)
    return (clf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La prédiction consiste à trouver pour chaque point la première limite qui est satisfaite. Notez qu'il n'y a aucun moyen de décider quelle est la meilleure classe si le point appartient à plusieurs classes.
    """)
    return


@app.cell
def _(jit, np):
    @jit(nopython=True)
    def parrallepiped_predict(clf, X_test):
      y_pred= []
      for data in X_test:
        y_pred.append(np.nan)
        for cl, limits in enumerate(clf):
          inside= True
          for b,limit in enumerate(limits):
            inside = inside and (data[b] >= limit[0]) & (data[b] <= limit[1])
            if ~inside:
              break
          if inside:
            y_pred[-1]=cl
      return np.array(y_pred)

    return (parrallepiped_predict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut appliquer ensuite le modèle sur l'image au complet. Les résultats sont assez mauvais, puisque seule la classe eau en bleu semble être bien classifiée.
    """)
    return


@app.cell
def _(clf, cmap_classes2, img_rgbnir, parrallepiped_predict, plt):
    _data_image = img_rgbnir.to_numpy().transpose(1, 2, 0).reshape(img_rgbnir.shape[1] * img_rgbnir.shape[2], 4)
    y_image = parrallepiped_predict(clf, _data_image)
    y_image = y_image.reshape(img_rgbnir.shape[1], img_rgbnir.shape[2])
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    plt.imshow(y_image, cmap=cmap_classes2)
    _ax.set_title('Méthode des parrallélépipèdes', fontsize='small')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut calculer quelques mesures de performance sur l'ensemble d'entrainement :
    """)
    return


@app.cell
def _(
    X_1,
    classification_report,
    clf,
    nom_classes,
    np,
    parrallepiped_predict,
    y_1,
    y_new,
):
    y_pred_2 = parrallepiped_predict(clf, X_1)
    nom_classes2_1 = [nom_classes[c] for c in np.unique(y_1).tolist()]
    print(classification_report(y_new, y_pred_2, target_names=nom_classes2_1, zero_division=np.nan))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### La malédiction de la haute dimension

    Augmenter le nombre de dimension ou de caractéristiques des données permet de résoudre des problèmes complexes comme la classification d'image. Cependant, cela amène beaucoup de contraintes sur le volume des données. Supposons que nous avons N points occupant un segment linéaire de taille d. La densité de points est $N/d$. Si nous augmentons le nombre de dimension D, la densité de points va diminuer exponentiellement en $1/d^D$. Par conséquent, pour garder une densité constante et donc une bonne estimation des parallélépipèdes, il nous faudrait augmenter le nombre de points en puissance de D. Ceci porte le nom de la malédiction de la dimensionnalité (*dimensionality curse*). En résumé, l'espace vide augmente plus rapidement que le nombre de données d'entraînement et l'espace des données devient de plus en plus parcimonieux (*sparse*). Pour contrecarrer ce problème, on peut sélectionner les meilleures caractéristiques ou appliquer une réduction de dimension comme une ACP (Analyse en composantes principales).

    ### Plus proches voisins

    La méthode des plus proches voisins (*K-Nearest-Neighbors*) est certainement la plus simple des méthodes pour classifier des données. Elle consiste à comparer une nouvelle donnée avec ses voisins les plus proches en fonction d'une simple distance Euclidienne. Si une majorité de ces $K$ voisins appartiennent à une classe majoritaire alors cette classe est sélectionnée. Afin de permettre un vote majoritaire, on choisira un nombre impair pour la valeur de $K$. Malgré sa simplicité, cette technique peut devenir assez demandante en temps de calcul pour un nombre important de points et un nombre élevé de dimensions.

    Reprenons l'ensemble d’entraînement formé à partir de notre image RGBNIR précédente :
    """)
    return


@app.cell
def _(nom_classes, np, pd):
    _df = pd.read_csv('sampling_points.csv')
    X_2 = _df['value'].apply(lambda x: np.fromstring(x[1:-1], dtype=float, sep=' ')).to_list()
    X_2 = np.array([row.tolist() for row in X_2])
    _idx = X_2.sum(axis=-1) > 0
    X_2 = X_2[_idx, ...]
    y_2 = _df['class'].to_numpy()
    y_2 = y_2[_idx]
    class_labels_2 = np.unique(y_2).tolist()
    _n_classes = len(class_labels_2)
    if max(class_labels_2) > _n_classes:
        y_new_1 = []
        for (_i, _l) in enumerate(class_labels_2):
            y_new_1.extend([_i] * sum(y_2 == _l))
        y_new_1 = np.array(y_new_1)
    nom_classes2_2 = [nom_classes[c] for c in np.unique(y_2).tolist()]
    return X_2, y_2, y_new_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Il importe de préalablement centrer (moyenne = 0) et de réduire (variance = 1) les données avant d’appliquer la méthode K-NN; avec cette méthode de normalisation, on dit parfois que l’on blanchit les données. Puisque la variance de chaque dimension est égale à 1 (et donc l’inertie totale est égale au nombre de bandes), on s’assure qu’elle ait le même poids dans le calcul des distances entre points. Cette opération porte le nom de `StandardScaler` dans `scikit-learn`. On peut alors former un pipeline de traitement combinant les deux opérations :
    """)
    return


@app.cell
def _(KNeighborsClassifier, Pipeline, StandardScaler):
    clf_1 = Pipeline(steps=[('scaler', StandardScaler()), ('knn', KNeighborsClassifier(n_neighbors=1))])
    return (clf_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Avant d'effectuer un entraînement, on met généralement une portion des données pour valider les performances :
    """)
    return


@app.cell
def _(X_2, train_test_split, y_new_1):
    (X_train, X_test_1, y_train, y_test_1) = train_test_split(X_2, y_new_1, test_size=0.2, random_state=0)
    return X_test_1, X_train, y_test_1, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut visualiser les frontières de décision du K-NN pour différentes valeurs de $K$ lorsque seulement deux bandes sont utilisées (Rouge et proche infra-rouge ici) :
    """)
    return


@app.cell
def _(
    DecisionBoundaryDisplay,
    ListedColormap,
    X_2,
    X_test_1,
    X_train,
    clf_1,
    couleurs_classes,
    np,
    plt,
    y_2,
    y_test_1,
    y_train,
):
    (_, _axs) = plt.subplots(nrows=2, ncols=2, figsize=(9, 9))
    _couleurs_classes2 = [couleurs_classes[c] for c in np.unique(y_2).tolist()]
    cmap_classes2_1 = ListedColormap(_couleurs_classes2)
    for (_ax, _K) in zip(_axs.flatten(), [1, 3, 7, 15]):
        clf_1.set_params(knn__weights='distance', knn__n_neighbors=_K).fit(X_train[:, 2:4], y_train)
        y_pred_3 = clf_1.predict(X_test_1[:, 2:4])
        print('Number of mislabeled points out of a total %d points : %d' % (X_test_1.shape[0], (y_test_1 != y_pred_3).sum()))
        _disp = DecisionBoundaryDisplay.from_estimator(clf_1, X_2[:, 2:4], response_method='predict', plot_method='contourf', shading='auto', alpha=0.5, ax=_ax, cmap=cmap_classes2_1)
        _scatter = _disp.ax_.scatter(X_test_1[:, 2], X_test_1[:, 3], c=y_test_1, edgecolors='k', cmap=cmap_classes2_1)
        _disp.ax_.set_xlabel('Rouge', fontsize='small')
        _disp.ax_.set_ylabel('Proche infra-rouge', fontsize='small')
        _ = _disp.ax_.set_title(f'K={clf_1[-1].n_neighbors} erreur={(y_test_1 != y_pred_3).sum() / X_test_1.shape[0] * 100:3.1f}%', fontsize='small')
    plt.show()
    return (cmap_classes2_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut voir comment les différentes frontières de décision se forment dans l'espace des bandes Rouge-NIR. L'augmentation de K rend ces frontières plus complexes et le calcul plus long.
    """)
    return


@app.cell
def _(X_test_1, X_train, clf_1, y_test_1, y_train):
    clf_1.set_params(knn__weights='distance', knn__n_neighbors=7).fit(X_train, y_train)
    y_pred_4 = clf_1.predict(X_test_1)
    print('Nombre de points misclassifiés sur %d points : %d' % (X_test_1.shape[0], (y_test_1 != y_pred_4).sum()))
    return (y_pred_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le rapport de performance est le suivant :
    """)
    return


@app.cell
def _(classification_report, nom_classes, np, y_2, y_pred_4, y_test_1):
    nom_classes2_3 = [nom_classes[c] for c in np.unique(y_2).tolist()]
    print(classification_report(y_test_1, y_pred_4, target_names=nom_classes2_3, zero_division=np.nan))
    return (nom_classes2_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La matrice de confusion peut-être affichée de manière graphique :
    """)
    return


@app.cell
def _(ConfusionMatrixDisplay, nom_classes2_3, y_pred_4, y_test_1):
    _disp = ConfusionMatrixDisplay.from_predictions(y_test_1, y_pred_4, display_labels=nom_classes2_3, xticks_rotation='vertical')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'application du modèle (la prédiction) peut se faire sur toute l'image en transposant l'image sous forme d'une matrice avec Largeur x Hauteur lignes et 4 colonnes :
    """)
    return


@app.cell
def _(clf_1, img_rgbnir):
    _data_image = img_rgbnir.to_numpy().transpose(1, 2, 0).reshape(img_rgbnir.shape[1] * img_rgbnir.shape[2], 4)
    y_classe = clf_1.predict(_data_image)
    y_classe = y_classe.reshape(img_rgbnir.shape[1], img_rgbnir.shape[2])
    return (y_classe,)


@app.cell
def _(cmap_classes2_1, plt, y_classe):
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    plt.imshow(y_classe, cmap=cmap_classes2_1)
    _ax.set_title("Carte d'occupation des sols avec K-NN", fontsize='small')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Méthodes par arbre de décision

    La méthode par arbre de décision consiste à construire une cascade de règles de décision sur chaque caractéristique du jeu de donnée [@Breiman1984]. On pourra trouver plus de détails dans la documentation de `scikit-learn` ([Decision Trees](https://scikit-learn.org/stable/modules/tree.html)). Les arbres de décision on tendance à surapprendre surtout si le nombre de dimensions est élevé. Il est donc conseillé d'avoir un bon ratio entre le nombre d'échantillons et le nombre de dimensions.
    """)
    return


@app.cell
def _(X_2, train_test_split, y_new_1):
    (X_train_1, X_test_2, y_train_1, y_test_2) = train_test_split(X_2, y_new_1, test_size=0.2, random_state=0)
    return X_test_2, X_train_1, y_test_2, y_train_1


@app.cell
def _(
    DecisionBoundaryDisplay,
    ListedColormap,
    X_2,
    X_test_2,
    X_train_1,
    couleurs_classes,
    np,
    plt,
    y_2,
    y_test_2,
    y_train_1,
):
    from sklearn import tree
    (_, _axs) = plt.subplots(nrows=2, ncols=2, figsize=(9, 9))
    _couleurs_classes2 = [couleurs_classes[c] for c in np.unique(y_2).tolist()]
    cmap_classes2_2 = ListedColormap(_couleurs_classes2)
    clf_2 = tree.DecisionTreeClassifier()
    for (_ax, _K) in zip(_axs.flatten(), [1, 2, 3, 4]):
        clf_2.set_params(max_depth=_K).fit(X_train_1[:, 2:4], y_train_1)
        y_pred_5 = clf_2.predict(X_test_2[:, 2:4])
        print('Number of mislabeled points out of a total %d points : %d' % (X_test_2.shape[0], (y_test_2 != y_pred_5).sum()))
        _disp = DecisionBoundaryDisplay.from_estimator(clf_2, X_2[:, 2:4], response_method='predict', plot_method='contourf', shading='auto', alpha=0.5, ax=_ax, cmap=cmap_classes2_2)
        _scatter = _disp.ax_.scatter(X_test_2[:, 2], X_test_2[:, 3], c=y_test_2, edgecolors='k', cmap=cmap_classes2_2)
        _disp.ax_.set_xlabel('Rouge', fontsize='small')
        _disp.ax_.set_ylabel('Proche infra-rouge', fontsize='small')
        _ = _disp.ax_.set_title(f'max_depth={_K} erreur={(y_test_2 != y_pred_5).sum() / X_test_2.shape[0] * 100:3.1f}%', fontsize='small')
    plt.show()
    return cmap_classes2_2, tree


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut observer que les frontières de décision sont formées d'un ensemble de plans simple. Chaque plan étant issu d'une règle de décison formé d'un seuil sur chacune des dimensions. On entraine un arbre de décision avec une profondeur maximale de 5:
    """)
    return


@app.cell
def _(X_test_2, X_train_1, tree, y_test_2, y_train_1):
    clf_3 = tree.DecisionTreeClassifier(max_depth=5)
    clf_3.fit(X_train_1, y_train_1)
    y_pred_6 = clf_3.predict(X_test_2)
    print('Nombre de points misclassifiés sur %d points : %d' % (X_test_2.shape[0], (y_test_2 != y_pred_6).sum()))
    return clf_3, y_pred_6


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le rapport de performance et la matrice de confusion:
    """)
    return


@app.cell
def _(classification_report, nom_classes2_3, np, y_pred_6, y_test_2):
    print(classification_report(y_test_2, y_pred_6, target_names=nom_classes2_3, zero_division=np.nan))
    return


@app.cell
def _(ConfusionMatrixDisplay, nom_classes2_3, y_pred_6, y_test_2):
    _disp = ConfusionMatrixDisplay.from_predictions(y_test_2, y_pred_6, display_labels=nom_classes2_3, xticks_rotation='vertical')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'application du modèle (la prédiction) peut se faire sur toute l'image en transposant l'image sous forme d'une matrice avec Largeur x Hauteur lignes et 4 colonnes:
    """)
    return


@app.cell
def _(clf_3, img_rgbnir):
    _data_image = img_rgbnir.to_numpy().transpose(1, 2, 0).reshape(img_rgbnir.shape[1] * img_rgbnir.shape[2], 4)
    y_classe_1 = clf_3.predict(_data_image)
    y_classe_1 = y_classe_1.reshape(img_rgbnir.shape[1], img_rgbnir.shape[2])
    return (y_classe_1,)


@app.cell
def _(cmap_classes2_2, plt, y_classe_1):
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    plt.imshow(y_classe_1, cmap=cmap_classes2_2)
    _ax.set_title("Carte d'occupation des sols avec un arbre de décision", fontsize='small')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Il est possible de visualiser l'arbre avec l'outil [SuperTree](https://github.com/mljar/supertree?tab=readme-ov-file) mais cela contient beaucoup d'information
    """)
    return


@app.cell
def _(X_train_1, clf_3, nom_classes2_3, y_train_1):
    from supertree import SuperTree  # <- import supertree :)
    super_tree = SuperTree(clf_3, X_train_1, y_train_1, ['Bleu', 'Vert', 'Rouge', 'NIR'], nom_classes2_3)
    super_tree.show_tree()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut voir que le nœud le plus haut utilise la bande proche-infrarouge pour séparer l'eau de la forêt comme première décision.

    ## Méthodes paramétriques

    Les méthodes paramétriques se basent sur des modélisations statistiques des données pour permettre une classification. Contrairement au méthodes non paramétriques, elles ont un nombre fixe de paramètres qui ne dépend pas de la taille du jeu de données. Par contre, des hypothèses sont faites a priori sur le comportement statistique des données. La classification consiste alors à trouver la classe la plus vraisemblable dont le modèle statistique décrit le mieux les valeurs observées. L'ensemble d’entraînement permettra alors de calculer les paramètres de chaque Gaussienne pour chacune des classes d'intérêt.

    ### Méthode Bayésienne naïve

    La méthode Bayésienne naïve Gaussienne consiste à poser des hypothèses simplificatrices sur les données, en particulier l'indépendance des données et des dimensions. Ceci permet un calcul plus simple.
    """)
    return


@app.cell
def _(X_test_2, X_train_1, y_test_2, y_train_1):
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    y_pred_7 = gnb.fit(X_train_1, y_train_1).predict(X_test_2)
    print('Nombre de points erronés sur %d points : %d' % (X_test_2.shape[0], (y_test_2 != y_pred_7).sum()))
    return (gnb,)


@app.cell
def _(
    DecisionBoundaryDisplay,
    ListedColormap,
    X_2,
    X_test_2,
    X_train_1,
    couleurs_classes,
    gnb,
    np,
    plt,
    y_2,
    y_test_2,
    y_train_1,
):
    (_, _axs) = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
    _couleurs_classes2 = [couleurs_classes[c] for c in np.unique(y_2).tolist()]
    cmap_classes2_3 = ListedColormap(_couleurs_classes2)
    gnb_1 = gnb.fit(X_train_1[:, 2:4], y_train_1)
    _disp = DecisionBoundaryDisplay.from_estimator(gnb_1, X_2[:, 2:4], response_method='predict', plot_method='contourf', shading='auto', alpha=0.5, ax=_axs, cmap=cmap_classes2_3)
    _scatter = _disp.ax_.scatter(X_test_2[:, 2], X_test_2[:, 3], c=y_test_2, edgecolors='k', cmap=cmap_classes2_3)
    _disp.ax_.set_xlabel('Rouge', fontsize='small')
    _disp.ax_.set_ylabel('NIR', fontsize='small')
    _ = _disp.ax_.set_title(f'Bayésien naif', fontsize='small')
    plt.show()
    return cmap_classes2_3, gnb_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On observe que les frontières de décision sont beaucoup plus régulières que pour K-NN.
    """)
    return


@app.cell
def _(X_test_2, X_train_1, gnb_1, y_test_2, y_train_1):
    gnb_1.fit(X_train_1, y_train_1)
    y_pred_8 = gnb_1.predict(X_test_2)
    print('Nombre de points misclassifiés sur %d points : %d' % (X_test_2.shape[0], (y_test_2 != y_pred_8).sum()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    De la même manière, la prédiction peut s'appliquer sur toute l'image:
    """)
    return


@app.cell
def _(cmap_classes2_3, gnb_1, img_rgbnir, plt):
    _data_image = img_rgbnir.to_numpy().transpose(1, 2, 0).reshape(img_rgbnir.shape[1] * img_rgbnir.shape[2], 4)
    y_classe_2 = gnb_1.predict(_data_image)
    y_classe_2 = y_classe_2.reshape(img_rgbnir.shape[1], img_rgbnir.shape[2])
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    plt.imshow(y_classe_2, cmap=cmap_classes2_3)
    _ax.set_title("Carte d'occupation des sols avec la méthode Bayésienne naive", fontsize='small')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Analyse discriminante quadratique (ADQ)

    L'analyse discriminante quadratique peut-être vue comme une généralisation de l'approche Bayésienne naive qui suppose des modèles Gaussiens indépendants pour chaque dimension et chaque point. Ici, on va considérer un modèle Gaussien multivarié.
    """)
    return


@app.cell
def _(QuadraticDiscriminantAnalysis, X_test_2, X_train_1, y_test_2, y_train_1):
    qda_2 = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda_2.fit(X_train_1, y_train_1)
    y_pred_9 = qda_2.predict(X_test_2)
    print('Nombre de points misclassifiés sur %d points : %d' % (X_test_2.shape[0], (y_test_2 != y_pred_9).sum()))
    return (qda_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les Gaussiennes multivariées peuvent être visualiser sous forme d'éllipses décrivant le domaine des valeurs de chaque classe:
    """)
    return


@app.cell
def _(X_2, couleurs_classes, np, plt, qda_2, y_2, y_new_1):
    import matplotlib as mpl
    colors = [couleurs_classes[c] for c in np.unique(y_2).tolist()]

    def make_ellipses(gmm, bands, ax):
        for (n, color) in enumerate(colors):
            covariances = gmm.covariance_[n][np.ix_(bands, bands)]
            (v, w) = np.linalg.eigh(covariances)
            u = w[0] / np.linalg.norm(w[0])
            angle = np.arctan2(u[1], u[0])
            angle = 180 * angle / np.pi
            v = 2.0 * np.sqrt(2.0) * np.sqrt(v)
            ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1], angle=180 + angle, color=color)
            ell.set_clip_box(_ax.bbox)
            ell.set_alpha(0.5)
            _ax.add_artist(ell)
            _ax.set_aspect('equal', 'datalim')
    (_fig, _ax) = plt.subplots(nrows=1, ncols=3, figsize=(9, 3), sharey=True)
    noms_bandes = ['Bleu', 'Vert', 'Rouge', 'NIR']
    for (index, b) in enumerate([0, 1, 3]):
        bands = [2, b]
        make_ellipses(qda_2, bands, _ax[index])
        for (n, color) in enumerate(colors):
            data = X_2[y_new_1 == n, ...]
            plt.scatter(data[:, bands[0]], data[:, bands[1]], s=0.8, color=color)
        _ax[index].set_xlabel(noms_bandes[2], fontsize='small')
        _ax[index].set_ylabel(noms_bandes[b], fontsize='small')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    De la même manière, la prédiction peut s'appliquer sur toute l'image:
    """)
    return


@app.cell
def _(cmap_classes2_3, img_rgbnir, plt, qda_2):
    _data_image = img_rgbnir.to_numpy().transpose(1, 2, 0).reshape(img_rgbnir.shape[1] * img_rgbnir.shape[2], 4)
    y_classe_3 = qda_2.predict(_data_image)
    y_classe_3 = y_classe_3.reshape(img_rgbnir.shape[1], img_rgbnir.shape[2])
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    plt.imshow(y_classe_3, cmap=cmap_classes2_3)
    _ax.set_title("Carte d'occupation des sols avec la méthode ADQ", fontsize='small')
    plt.show()
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
    <li>La <strong>classification supervisée</strong> attribue une classe à chaque pixel à partir d’un <strong>jeu d’entraînement étiqueté</strong> ; le modèle apprend des <strong>frontières de décision</strong>.</li>
    <li>Séparer les données en <strong>entraînement / validation / test</strong> est essentiel pour détecter le <strong>sur-apprentissage</strong> — l’erreur d’entraînement seule est trompeuse.</li>
    <li>Les ensembles réels sont souvent <strong>déséquilibrés</strong> ; la <strong>séparabilité</strong> (distance JM) et les statistiques par classe guident l’analyse préliminaire.</li>
    <li>La performance se lit dans la <strong>matrice de confusion</strong> : <strong>rappel</strong> (omission, lignes), <strong>précision</strong> (fausses alarmes, colonnes), <strong>f1-score</strong>.</li>
    <li>Méthodes <strong>non paramétriques</strong> (parallélépipèdes, K-NN, arbres) vs <strong>paramétriques</strong> (Bayésien naïf, ADQ) ; le K-NN exige une <strong>normalisation</strong> (<code>StandardScaler</code>).</li>
    <li>La <strong>malédiction de la dimensionnalité</strong> : le nombre de points requis croît exponentiellement avec le nombre de dimensions <span class="math inline">\(D\)</span>.</li>
    </ul>
    </div>
    </div>

    ## Exercices

    <div style="border:0.5px solid silver;border-left:.3rem solid #e34692;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fbe8f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADP0lEQVRYha2XT3LaMBjFf3SyD91rBnqC0BOUbuJl6AkwB9CUnKD0BCXxAeKcIGSpVZ0bwAkKEx8ATkAXemoUgm0I/WY8smVJ7/n78yS3ttstp1iZZF0g1WNhnC3Un6o/N87mVfNbpxAQ+Bw4j7p/qv0R9Y2qSHx4N7q3scBvBLwS8A/dj4ANcCePvLFTPVAAX4yzraivDxCFogcUIvrGE6cSSIE74KdxdlIzrpLEqSGY4V2d1g0yzs6BPnvCcRIB4+waWAKdMsna7yHR2m63aPL4COzCOFuUSZYDQ+DeOJseMjEKB8bZduv58ratjosjCMSltgJ68gZlkg20+KyGRIrPndEZMBD4AuiHhSom9oHfeszxXusAkzLJ1vhc6GjsChjI9bs2UFt8ALp6GDeAt4GpHtfG2SUvMf2O90YHrwk3us/3rJMDV8CTcXZ5VgUYTehroY66NmFh4+w8kuI2r6X4OzthLZNsjM+ZBfJCLQF99Qxfvwu87E5iT+l+ujMvuPgp6kuBX/qAf6Fu8kBP4I/G2UHD2NjGAhpH4He74IcQCNYtk6xdlSNBfoGlcuMLPsbzPeCvkrL1fHk7wSfQ1xC/ncXnvMRyhU/Wmd7tK+ERPjmHwL3aveBwmBL2tdACn4gPSjzwyXchgEf1TXVtmsAPImCcXRtnU+NsT0QCMPgcQQADkTjHV0QgXgkOr3MglUzmu7HWF8dJ2I1keBMBFPgan4lk3vSBsQeG+DJZikgAT4E/ejeMxob7eA/J8aE6Bx7wqlm7x8QErqPJ8aSJ2nuNAV/f18DneG9XuHrAN172i+WhBMJ2CYqtsrwDLLTbBVevjbPTqtgaZ2d1B5QqAkHVFsCFYlxE5OL2qkyyWZlk46ZzwFEEZEHFhvgSW6kvEBwFEvi8KE4h8YaAxKgLfMWLU3dH+3PgIz7OG5FM30tgrxQLsKiapPcz7W53+Lr/fwSaTGU64KValjXDezXvjidQJtkUfwAJ9lj360WDd44iIEUM4Nf4A0ilzB5iZ0BIsJSauMu6am+Ms9O6gZGa1hJsPV/edvFSC14DKs+FeHeG0lzWc/13mPmkM8J+AvovGOC30E7VwHfYEw2/5gB/AcMlhsUeVwFpAAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>À vous de jouer</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ol type="1">
    <li>Comparez les rapports de performance (<code>classification_report</code>) du K-NN, de l’arbre de décision et de l’ADQ sur le même ensemble de test : quelle méthode l’emporte, et pour quelles classes ?
    </li>
    <li>Faites varier <code>test_size</code> (0.1, 0.3, 0.5) dans <code>train_test_split</code> et observez l’effet sur l’erreur de test du K-NN.
    </li>
    <li>Entraînez un arbre de décision avec plusieurs <code>max_depth</code> (3, 5, 10, <code>None</code>) et repérez à partir de quelle profondeur le sur-apprentissage apparaît.
    </li>
    <li>Utilisez les <strong>4 bandes</strong> (au lieu de Rouge–NIR) pour l’ADQ et comparez la carte d’occupation des sols obtenue.
    </li>
    </ol>
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
    Chap05Quiz = Quiz("quiz/Chap05.yml", "Chap05")
    render_quizz(Chap05Quiz)
    return


if __name__ == "__main__":
    app.run()
