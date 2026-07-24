import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    return (subprocess,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['image.aspect'] = 'equal'
    plt.rcParams['image.cmap'] = 'gray'
    plt.rcParams['figure.dpi'] = 100
    import warnings
    warnings.filterwarnings('ignore')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Réhaussement et visualisation d'images {#sec-chap02}

    Assurez-vous de lire ce préambule avant d'exécutez le reste du notebook.

    ## Préambule

    ### Objectifs

    Dans ce chapitre, nous abordons quelques techniques de réhaussement et de visualisation d'images. Ce chapitre est aussi disponible sous la forme d'un notebook Python:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/02-RehaussementVisualisationImages.ipynb)

    <div style="border:0.5px solid silver;border-left:.3rem solid #00796d;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2efec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADfUlEQVRYhb2XMXLbMBBFnzVKkSZ0ylRmJkVKMycwfQIrJzB9AVruMsNGLlCHwQVC3UC+AXUC02WKTOQ+hXGAjFNgIYIQZNkZxzvD4UhY7H7s/l0s9+7v73msJFWZAzmQAfvBcidPa5RePdbm3i4ASVWmwBQogOSRdpdAY5RuIvb2gX0H8kEASVXOxHkCGGAhT2uUvgt0M2x0CuBQ/r4BCqN05+m0wMQo3QKMtzjOgEYMGeAsdhpfxEkH1BK1GjhBUuU5H0RxIwKB4pWcYHDax0pSlalRehVxfiFghwACxQujdP0vjgMQ0ZOLfBt7ivvYsCc8EHLRy7GV4OQOy4su0C2wqYg5PzNKNz4HZticz7ewNxWd0xgw0bkFZt7+mHODTesCYCQbM+AcuMWyPjQ8websVHQugWPvOQPmwAE9CQFWEee5cw7CgaQqF1jGHrvy8JwXwHf5+SAvPMd32HI98pZvsOW3SqqyBmqj9Gokm06A24jzFBtGA3zaRUqvA7bifAm8xUYpF+c5NtozsH0gl00x4w09KdcEEyIW9O24M0ovAsbPjdKFB8iBbJOqNMDEAZjI2jov4iRzp/BJuY3ZSVX+AN4Bb5BUiY3CKB3yagGcJlWZjYAUMJELxAFbR0ZSsuYDfXh/Ah+B19ho1d7eczallXc2wpZeF1HKA2WQvAFTo3QtHbIAPgB/gFeB/p0AzxnKSt7pKOJ4IEEbTrHRasRwgy3NG+CLp+MkdrCB7ASwQ3Is03Pgd2R95x2yE4Aw3skKSKQxYZROjdK5RGnq6TgJh5YNGWPDl0XWWmwVTLDlCH0rbmRWWIiTGsulq4DMDmgb2E4d2JF3qjRQcmVZuD/E+Jn8/Ar8Aq7pm85aV4h3iL3SQ8nl3Y08RxNfQxrPEjiS2nf/N3KCC+ydcAl89lLhpA7eIQBjlO7G9GUzjSgX9FNO57qhOHroTmjoU9IGaxPspTUHGElY58BBWK+y5mbC66QqN27KwHiaVKW7NW/wUuKJs1FDfxtm2FzeAllk4HRETESnYdhwUmxY3awQHeW8m3VplM7XAGTRtU3/Ehmcjh0DiYDzB5JwfyeHeL8xlku9t9jcPctIFuxxtgczxUsMpb7zjej+77E8x5Z5OB9sByAbU9noPkymuz5MIvvdhwnApVF6FtN90U+zJwPwTvNsH6dPBhCAyXnmz/O/0JrtInNZu4wAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Objectifs d’apprentissage visés dans ce chapitre</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">

    </div>
    </div>

    ###

    ### Bibliothèques

    Les bibliothèques qui vont être explorées dans ce chapitre sont les suivantes:

    -   [SciPy](https://scipy.org/)

    -   [NumPy](https://numpy.org/)

    -   [opencv-python · PyPI](https://pypi.org/project/opencv-python/)

    -   [scikit-image](https://scikit-image.org/)

    -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

    -   [Xarray](https://docs.xarray.dev/en/stable/)

    -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

    Dans l'environnement Google Colab, seul `rioxarray` et GDAL doivent être installés:
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # !apt-get update
    # !apt-get install gdal-bin libgdal-dev
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Dans l'environnement [Google Colab](https://colab.research.google.com/), il convient de s'assurer que les librairies sont installées:
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # !pip install -qU matplotlib rioxarray xrscipy scikit-image
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifier les importations:
    """)
    return


@app.cell
def _():
    import numpy as np
    import rioxarray as rxr
    from scipy import signal
    import xarray as xr
    import xrscipy

    return np, rxr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Données

    Nous utiliserons les images suivantes dans ce chapitre:
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # import gdown
    # 
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6Ypg0g1Oy4AJt9XWKWfnR12NW1XhNg_', output= 'RGBNIR_of_S2A.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6O3L_abOfU7h94K22At8qtBuLMGErwo', output= 'sentinel2.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1dM6IVqjba6GHwTLmI7CpX8GP2z5txUq6', output= 'SAR.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a4PQ68Ru8zBphbQ22j0sgJ4D2quw-Wo6', output= 'landsat7.tif')
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
    with rxr.open_rasterio('sentinel2.tif', mask_and_scale= True) as img_s2:
        print(img_s2)
    with rxr.open_rasterio('RGBNIR_of_S2A.tif', mask_and_scale= True) as img_rgbnir:
        print(img_rgbnir)
    with rxr.open_rasterio('SAR.tif', mask_and_scale= True) as img_SAR:
        print(img_SAR)
    return img_SAR, img_rgbnir, img_s2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Visualisation en Python

    D'emblée, il faut mentionner que Python n'est pas vraiment fait pour visualiser de la donnée de grande taille, le niveau d'interactivité est aussi assez limité. Pour une visualisation interactives, il est plutôt conseillé d'utiliser un outil comme [QGIS](https://qgis.org/). Néanmoins, il est possible de visualiser de petites images avec la librairie [`matplotlib`](https://matplotlib.org/stable/) qui est la librairie principale de visualisation en Python. Cette librairie est extrêmement riche et versatile, nous ne présenterons que les bases nécessaires pour démarrer. Le lecteur désirant aller plus loin pourra consulter les nombreux tutoriels disponibles comme [celui-ci](https://matplotlib.org/stable/tutorials/index.html).

    La fonction de base pour créer une figure est `subplots`, la largeur et la hauteur en pouces de la figure peuvent être contrôlées via le paramètre `figsize`:
    """)
    return


@app.cell
def _(plt):
    (_fig, _ax) = plt.subplots(figsize=(5, 4))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour l'affichage des images, la fonction `imshow` permet d'afficher une matrice 2D à une dimension en format *float* ou une matrice RVB avec 3 bandes. Il est important que les dimensions de la matrice soient dans l'ordre hauteur, largeur et bande.
    """)
    return


@app.cell
def _(img_rgbnir, plt):
    (_fig, _ax) = plt.subplots(figsize=(6, 5))
    plt.imshow(img_rgbnir[0].data)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour un affichage à trois bandes, les valeurs seront ramenées sur une échelle de 0 à 1, il est donc nécessaire de normaliser les valeurs avant l'affichage:
    """)
    return


@app.cell
def _(img_rgbnir, plt):
    (_fig, _ax) = plt.subplots(figsize=(6, 5))
    plt.imshow(img_rgbnir.data[0:3].transpose(1, 2, 0) / 2500.0)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On remarquera les valeurs des axes `x` et `y` avec une origine en haut à gauche. Ceci est un référentiel purement matriciel (lignes et colonnes); autrement dit, il n'y a pas ici de géoréférence. Pour pallier à cette limitation, les librairies `rasterio` et `xarray` proposent une extension de la fonction `imshow` permettant d'afficher les coordonnées cartographiques ainsi qu'un contrôle la dynamique de l'image:
    """)
    return


@app.cell
def _(img_rgbnir, plt):
    (_fig, _ax) = plt.subplots(figsize=(6, 5))
    img_rgbnir.sel(band=[1, 2, 3]).plot.imshow(vmin=86, vmax=5000)
    _ax.set_title('Imshow avec rioxarray')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Réhaussements visuels

    Le réhaussement visuel d'une image vise principalement à améliorer la qualité visuelle d'une image en améliorant le contraste, la dynamique ou la texture d'une image. De manière générale, ce réhaussement ne modifie pas la donnée d'origine mais il est appliquée dynamiquement à l'affichage pour des fins d'inspection visuelle. Le réhaussement nécessite généralement une connaissance des caractéristiques statistiques d'une image. Ces statistiques sont ensuite exploitées pour appliquer diverses transformations linéaires ou non linéaires.

    ### Statistiques d'une image

    On peut considérer un ensemble de statistique pour chacune des bandes d'une image:

    -   valeurs minimales et maximales

    -   valeurs moyennes,

    -   Quartiles (1er quartile, médiane et 3ième quartile), quantiles et percentiles.

    -   écart-type, et coefficients d'asymétrie (*skewness*) et d'applatissement (*kurtosis*)

    Ces statistiques doivent être calculées pour chaque bande d'une image multispectrale.

    En ligne de commande, `gdalinfo` permet d'interroger rapidement un fichier image pour connaitre ces statistiques univariées de base:
    """)
    return


@app.cell
def _(subprocess):
    #! gdalinfo -stats landsat7.tif
    subprocess.call(['gdalinfo', '-stats', 'landsat7.tif'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les librairies de base comme `rasterio` et `xarray` produisent facilement un sommaire des statistiques de base avec la fonction [stats](https://rasterio.readthedocs.io/en/stable/api/rasterio.io.html#rasterio.io.BufferedDatasetWriter.stats):
    """)
    return


@app.cell
def _():
    import rasterio as rio
    with rio.open('landsat7.tif') as _src:
        stats = _src.stats()
        print(stats)
    return (rio,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La librairie `xarray` donne accès à des fonctionnalités plus sophistiquées comme le calcul des quantiles:
    """)
    return


@app.cell
def _():
    import rioxarray as riox
    with riox.open_rasterio('landsat7.tif', masked=True) as _src:
        print(_src)
    quantiles = _src.quantile(dim=['x', 'y'], q=[0.025, 0.25, 0.5, 0.75, 0.975])
    quantiles
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Calcul de l'histogramme

    Le calcul d'un histogramme pour une image (une bande) permet d'avoir une vue plus détaillée de la répartition des valeurs radiométriques. Le calcul d'un histogramme nécessite minimalement de faire le choix du nombre de barre ( *bins* ou de la largeur ). Un *bin* est un intervalle de valeurs pour lequel on peut calculer le nombre de valeurs observées dans l'image. La fonction de base pour ce type de calcul est la fonction `numpy.histogram()`:
    """)
    return


@app.cell
def _(np):
    array = np.random.randint(0, 10, 100)
    (hist, bin_limites) = np.histogram(array, density=True)  # 100 valeurs aléatoires entre 0 et 10
    print('valeurs :', hist)
    print('limites :', bin_limites)
    return bin_limites, hist


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le calcul se fait avec 10 intervalles par défaut.
    """)
    return


@app.cell
def _(bin_limites, hist, plt):
    (_fig, _ax) = plt.subplots(figsize=(5, 4))
    plt.bar(bin_limites[:-1], hist)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour des besoins de visualisation, le calcul des valeurs extrêmes de l'histogramme peut aussi se faire via les quantiles comme discutés auparavant.

    ##### Visualisation des histogrammes

    La librarie `rasterio` est probablement l'outil le plus simples pour visualiser rapidement des histogrammes sur une image multi-spectrale:
    """)
    return


@app.cell
def _(rio):
    from rasterio.plot import show_hist
    with rio.open('RGBNIR_of_S2A.tif') as _src:
        show_hist(_src, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', title='Histogram')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Réhaussements linéaires

    Le réhaussement linéaire (*linear stretch*) d'une image est la forme la plus simple de réhaussement, elle consiste à 1) optimiser les valeurs des pixels d'une image afin de maximiser la dynamique disponibles à l'affichage, ou 2) à changer le format de stockage des valeurs (de 8 bits à 16 bits):

    $$ \text{nouvelle valeur d'un pixel} = \frac{\text{valeur d'un pixel} - min_0}{max_0 - min_0}\times (max_1 - min_1)+min_1$$ {#eq-rehauss-lin}

    Par cette opération, on passe de la dynamique de départ ($max_0 - min_0$) vers la dynamique cible ($max_1 - min_1$). Bien que cette opération semble triviale, il est important d'être conscient des trois contraintes suivantes:

    1.  **Faire attention à la dynamique cible**, ainsi, pour sauvegarder une image en format 8 bit, on utilisera alors $max_1=255$ et $min_1=0$.

    2\. **Préservation de la valeur de no data** : il faut faire attention à la valeur $min_1$ dans le cas d'une valeur présente pour *no_data*. Par exemple, si *no_data=0* alors il faut s'assurer que $min_1>0$.

    3\. **Précision du calcul** : si possible réaliser la division ci-dessus en format *float*

    #### Cas des histogrammes asymétriques

    Dans certains cas, la distribution de valeurs est très asymétrique et présente une longue queue avec des valeurs extrêmes élevées (à droite ou à gauche de l'histogramme). Le cas des images SAR est particulièrement représentatif de ce type de données. En effet, celles-ci peuvent présenter une distribution de valeurs de type exponentiel. Il est alors préférable d'utiliser des [percentiles](https://fr.wikipedia.org/wiki/Centile) au préalable afin d'explorer la forme de l'histogramme et la distribution des valeurs:
    """)
    return


@app.cell
def _(img_SAR, np):
    NO_DATA_FLOAT = -999.0
    # on prend tous les pixels de la première bande
    values = img_SAR[0].values.flatten().astype(float)
    # on exclut les valeurs invalides
    values = values[~np.isnan(values)]
    # on exclut le no data
    values = values[values != NO_DATA_FLOAT]
    # calcul des percentiles
    _percentiles_position = (0, 0.1, 1, 2, 50, 98, 99, 99.9, 100)
    percentiles = dict(zip(_percentiles_position, np.percentile(values, _percentiles_position)))
    print(percentiles)
    return NO_DATA_FLOAT, percentiles, values


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On constate que la valeur médiane (`0.012`) est très faible, ce qui signifie que 50% des valeurs sont inférieures à cette valeur alors que la valeur maximale (`483`) est 10 000 fois plus élevée! Une manière de visualiser cette distribution de valeurs est d'utiliser [`boxplot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html) et [`violinplot`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.violinplot.html) de la librairie `matplotlib`:
    """)
    return


@app.cell
def _(plt, values):
    (_fig, _ax) = plt.subplots(nrows=2, ncols=1, figsize=(6, 4), sharex=True)
    _ax[0].set_title('Distribution de la bande 0 de img_SAR', fontsize='small')
    _ax[0].grid(True)
    _ax[0].violinplot(values, orientation='horizontal', quantiles=(0.01, 0.02, 0.5, 0.98, 0.99), showmeans=False, showmedians=True)
    _ax[1].set_xlabel('Valeur des pixels')
    _ax[1].grid(True)
    _bplot = _ax[1].boxplot(values, notch=True, orientation='horizontal')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Afin de visualiser correctement l'histogramme, il faut se limiter à un intervalle de valeurs plus réduit. Dans le code ci-dessous, on impose à la fonction `np.histogramme` de compter les valeurs de pixels dans des intervalles de valeurs fixés par la fonction `np.linspace(percentiles[0.1],percentiles[99.9], 50)` où `percentiles[0.1]` et `percentiles[99.9]` sont les $0.1\%$ et $99.9\%$ percentiles respectivement:
    """)
    return


@app.cell
def _(np, percentiles, plt, values):
    (hist_1, bin_edges) = np.histogram(values, bins=np.linspace(percentiles[0.1], percentiles[99.9], 50), density=True)
    (_fig, _ax) = plt.subplots(nrows=2, ncols=1, figsize=(6, 5), sharex=True)
    _ax[0].bar(bin_edges[:-1], hist_1 * (bin_edges[1] - bin_edges[0]), width=bin_edges[1] - bin_edges[0], edgecolor='w')
    _ax[0].set_title('Distribution de probabilité (PDF)')
    _ax[0].set_ylabel('Densité de probabilité')
    _ax[0].grid(True)
    _ax[1].plot(bin_edges[:-1], hist_1.cumsum() * (bin_edges[1] - bin_edges[0]))
    _ax[1].set_title('Distribution de probabilité cumulée (CDF)')
    _ax[1].set_xlabel('Valeur du pixel')
    _ax[1].set_ylabel('Probabilité cumulée')
    _ax[1].grid(True)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Au niveau de l'affichage avec `matplotlib`, la dynamique peut être contrôlée directement avec les paramètres `vmin` et `vmax` comme ceci:
    """)
    return


@app.cell
def _(img_SAR, percentiles, plt):
    (_fig, _ax) = plt.subplots(nrows=2, ncols=2, figsize=(6, 5), sharex=True, sharey=True)
    [a.axis('off') for a in _ax.flatten()]
    _ax[0, 0].imshow(img_SAR[0].values, vmin=percentiles[0], vmax=percentiles[100])
    _ax[0, 0].set_title(f'0% - 100%={percentiles[0]:2.1f} - {percentiles[100]:2.1f}')
    _ax[0, 1].imshow(img_SAR[0].values, vmin=percentiles[0.1], vmax=percentiles[99.9])
    _ax[0, 1].set_title(f'0.1% - 99.9%={percentiles[0.1]:2.1f} - {percentiles[99.9]:2.1f}')
    _ax[1, 0].imshow(img_SAR[0].values, vmin=percentiles[1], vmax=percentiles[99])
    _ax[1, 0].set_title(f'1% - 99%={percentiles[1]:2.1f} - {percentiles[99]:2.1f}')
    _ax[1, 1].imshow(img_SAR[0].values, vmin=percentiles[2], vmax=percentiles[98])
    _ax[1, 1].set_title(f'2% - 98%={percentiles[2]:2.1f} - {percentiles[98]:2.1f}')
    plt.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Réhaussements non linéaires

    #### Réhaussement par fonctions

    Le réhaussenent par fonction consiste à appliquer une fonction non linéaire afin de modifier la dynamique de l'image. Par exemple, pour une image radar, une transformation populaire est d'afficher les valeurs de rétrodiffusion en décibel (`dB`) avec la fonction `log10()`.
    """)
    return


@app.cell
def _(NO_DATA_FLOAT, img_SAR, np):
    _percentiles_position = (0, 0.1, 1, 2, 50, 98, 99, 99.9, 100)
    _sar = img_SAR[0].data
    _valid = (_sar != NO_DATA_FLOAT) & (_sar > 0)
    values_1 = 10 * np.log10(np.where(_valid, _sar, np.nan))
    percentiles_db = dict(zip(_percentiles_position, np.nanpercentile(values_1, _percentiles_position)))
    print(percentiles_db)
    return percentiles_db, values_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les boites à moustache (*boxplots*) ont une bien meilleure distribution qui est en effet très proche d'une distribution normale gaussienne:
    """)
    return


@app.cell
def _(np, plt, values_1):
    values_valid = values_1.flatten()
    values_valid = values_valid[np.isfinite(values_valid)]
    (_fig, _ax) = plt.subplots(nrows=2, ncols=1, figsize=(6, 4), sharex=True)
    _ax[0].set_title('Distribution de la bande 0 de img_SAR en dB', fontsize='small')
    _ax[0].grid(True)
    _ax[0].violinplot(values_valid, orientation='horizontal', quantiles=(0.01, 0.02, 0.5, 0.98, 0.99), showmeans=False, showmedians=True, showextrema=True)
    _ax[1].set_xlabel('Valeur des pixels')
    _ax[1].grid(True)
    _bplot = _ax[1].boxplot(values_valid, notch=True, orientation='horizontal')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On obtient ainsi les images suivantes:
    """)
    return


@app.cell
def _(percentiles_db, plt, values_1):
    (_fig, _ax) = plt.subplots(nrows=2, ncols=2, figsize=(6, 5), sharex=True, sharey=True)
    [a.axis('off') for a in _ax.flatten()]
    _ax[0, 0].imshow(values_1, vmin=percentiles_db[0], vmax=percentiles_db[100])
    _ax[0, 0].set_title(f'0% - 100%={percentiles_db[0]:2.1f} - {percentiles_db[100]:2.1f}')
    _ax[0, 1].imshow(values_1, vmin=percentiles_db[0.1], vmax=percentiles_db[99.9])
    _ax[0, 1].set_title(f'0.1% - 99.9%={percentiles_db[0.1]:2.1f} - {percentiles_db[99.9]:2.1f}')
    _ax[1, 0].imshow(values_1, vmin=percentiles_db[1], vmax=percentiles_db[99])
    _ax[1, 0].set_title(f'1% - 99%={percentiles_db[1]:2.1f} - {percentiles_db[99]:2.1f}')
    _ax[1, 1].imshow(values_1, vmin=percentiles_db[2], vmax=percentiles_db[98])
    _ax[1, 1].set_title(f'2% - 98%={percentiles_db[2]:2.1f} - {percentiles_db[98]:2.1f}')
    plt.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Égalisation d'histogramme

    L'égalisation d'histogramme consiste à modifier les valeurs des pixels d'une image source afin que la distribution cumulée des valeurs (CDF) devienne similaire à celle d'une image cible. La CDF (*Cumulative Distribution Function*) est simplement la somme cumulée des valeurs de l'histogramme:

    $$
    CDF_{source}(i)= \frac{1}{K}\sum_{j=0}^{j \leq i} hist_{source}(j)
    $$ avec $K$ choisit de façon à ce que la dernière valeur soit égale à 1 ($CDF_{source}(i_{max})=1$). De la même manière, $CDF_{cible}$ est la CDF d'une image cible. La formule générale pour l'égalisation d'histogramme est la suivante: $$
    j = CDF_{cible}^{-1}(CDF_{source}(i))
    $$

    On peut choisir $CDF_{cible}$ comme correspondant à une image où chaque valeur de pixel est équiprobable (d'où le terme *égalisation*), ce qui veut dire $hist_{cible}(j)=1/L$ avec $L$ égale au nombre de valeurs possibles dans l'image (par exemple $L=256$). $$
    j = L \times CDF_{source}(i)
    $$ On peut appliquer cette procédure sur l'image SAR en dB de la façon suivante:
    """)
    return


@app.cell
def _(NO_DATA_FLOAT, img_SAR, np, plt):
    _sar = img_SAR[0].data
    _valid = (_sar != NO_DATA_FLOAT) & (_sar > 0)
    sar_db = 10 * np.log10(np.where(_valid, _sar, np.nan))
    values_2 = np.sort(sar_db[_valid].flatten())
    cdf_x = np.linspace(values_2[0], values_2[-1], 1000)
    cdf_source = np.interp(cdf_x, values_2, np.arange(len(values_2)) / len(values_2) * 255)
    values_eq = np.interp(sar_db, cdf_x, cdf_source)
    values_eq = np.where(_valid, values_eq, 0).astype('uint8')
    plt.imshow(values_eq)
    plt.axis('off')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Palettes de couleur

    Les palettes de couleurs sont appliquées dynamiquement à l'affichage sur une image à une seule bande. La librairie `matplotlib` contient un nombre considérable de [palettes](https://matplotlib.org/stable/users/explain/colors/colormaps.html).
    """)
    return


@app.cell
def _():
    # | output: false
    from matplotlib import colormaps
    list(colormaps)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Voici quelques exemples ci-dessous, les valeurs de l'image doivent être normalisées entre 0 et 1 ou entre 0 et 255 sinon les paramètres `vmin` et `vmax` doivent être spécifiés. On peut observer comment ces palettes révèlent les détails de l'image malgré une image originalement très sombre.
    """)
    return


@app.cell
def _(img_SAR, percentiles, plt):
    (_fig, _ax) = plt.subplots(nrows=2, ncols=2, figsize=(6, 5), sharex=True, sharey=True)
    [a.axis('off') for a in _ax.flatten()]
    _ax[0, 0].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='jet')
    _ax[0, 0].set_title(f'jet')
    _ax[0, 1].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='hot')
    _ax[0, 1].set_title(f'hot')
    _ax[1, 0].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='hsv')
    _ax[1, 0].set_title(f'hsv')
    _ax[1, 1].imshow(img_SAR[0].data, vmin=percentiles[2], vmax=percentiles[98], cmap='terrain')
    _ax[1, 1].set_title(f'terrain')
    plt.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Il peut être utile d'ajouter une barre de couleurs afin d'indiquer la correspondance entre les couleurs et les valeurs numériques:
    """)
    return


@app.cell
def _(img_SAR, percentiles, plt):
    import matplotlib as mpl
    (_fig, _ax) = plt.subplots(figsize=(6, 6))
    cmap = mpl.colormaps.get_cmap('jet').with_extremes(under='white', over='magenta')
    h = plt.imshow(img_SAR[0].data, norm=mpl.colors.LogNorm(vmin=percentiles[2], vmax=percentiles[98]), cmap=cmap)
    _fig.colorbar(h, ax=_ax, orientation='horizontal', label='Intensité', extend='both')
    _ax.axis('off')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Composés colorés

    Le système visuel humain est sensible seulement à la partie visible du spectre électromagnétique qui compose les couleurs de l'arc-en-ciel du bleu au rouge. L'ensemble des couleurs du spectre visible peut être obtenu à partir du mélange de trois couleurs primaires (rouge, vert et bleu). Ce système de décomposition à trois couleurs est à la base de la plupart des systèmes de visualisation ou de représentation de l'information de couleur. Si on prend le cas des images Sentinel-2, 12 bandes sont disponibles, plusieurs composés couleurs sont donc possibles (voir le site de [Copernicus](https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/composites/)). Voici quelques exemples possibles, chaque composé mettant en valeur des propriétés différentes de la surface.
    """)
    return


@app.cell
def _(img_s2, plt):
    (_fig, _ax) = plt.subplots(nrows=2, ncols=2, figsize=(8, 6), sharex=True, sharey=True)
    img_s2.sel(band=[4, 3, 2]).plot.imshow(vmin=86, vmax=4000, ax=_ax[0, 0])
    _ax[0, 0].set_title('RVB')
    img_s2.sel(band=[8, 3, 2]).plot.imshow(vmin=86, vmax=4000, ax=_ax[0, 1])
    _ax[0, 1].set_title('NIR,V,B')
    img_s2.sel(band=[12, 8, 4]).plot.imshow(vmin=86, vmax=4000, ax=_ax[1, 0])
    _ax[1, 0].set_title('SWIR2,NIR,R')
    img_s2.sel(band=[12, 11, 4]).plot.imshow(vmin=86, vmax=4000, ax=_ax[1, 1])
    _ax[1, 1].set_title('SWIR2,SWIR1,NIR')
    plt.tight_layout()
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
    <li>Le réhaussement visuel améliore l’affichage (contraste, dynamique) <strong>sans modifier la donnée</strong> d’origine : il est appliqué dynamiquement à l’affichage.</li>
    <li>Les <strong>statistiques</strong> d’une image (min/max, moyenne, quantiles, écart-type) guident le choix de la transformation.</li>
    <li>Le <strong>stretch linéaire</strong> remappe la dynamique ; pour les histogrammes <strong>asymétriques</strong> (images SAR), les <strong>percentiles</strong> (p. ex. 2 %–98 %) fournissent des bornes d’affichage robustes.</li>
    <li>Les transformations <strong>non linéaires</strong> — passage en <strong>dB</strong> (<code>10·log10</code>) et <strong>égalisation d’histogramme</strong> — rétablissent une distribution exploitable.</li>
    <li>Les <strong>palettes de couleur</strong> et les <strong>composés colorés</strong> (choix des bandes) révèlent des propriétés différentes de la surface ; <code>vmin</code>/<code>vmax</code> contrôlent la dynamique affichée.</li>
    </ul>
    </div>
    </div>

    ## Exercices

    <div style="border:0.5px solid silver;border-left:.3rem solid #e34692;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fbe8f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADP0lEQVRYha2XT3LaMBjFf3SyD91rBnqC0BOUbuJl6AkwB9CUnKD0BCXxAeKcIGSpVZ0bwAkKEx8ATkAXemoUgm0I/WY8smVJ7/n78yS3ttstp1iZZF0g1WNhnC3Un6o/N87mVfNbpxAQ+Bw4j7p/qv0R9Y2qSHx4N7q3scBvBLwS8A/dj4ANcCePvLFTPVAAX4yzraivDxCFogcUIvrGE6cSSIE74KdxdlIzrpLEqSGY4V2d1g0yzs6BPnvCcRIB4+waWAKdMsna7yHR2m63aPL4COzCOFuUSZYDQ+DeOJseMjEKB8bZduv58ratjosjCMSltgJ68gZlkg20+KyGRIrPndEZMBD4AuiHhSom9oHfeszxXusAkzLJ1vhc6GjsChjI9bs2UFt8ALp6GDeAt4GpHtfG2SUvMf2O90YHrwk3us/3rJMDV8CTcXZ5VgUYTehroY66NmFh4+w8kuI2r6X4OzthLZNsjM+ZBfJCLQF99Qxfvwu87E5iT+l+ujMvuPgp6kuBX/qAf6Fu8kBP4I/G2UHD2NjGAhpH4He74IcQCNYtk6xdlSNBfoGlcuMLPsbzPeCvkrL1fHk7wSfQ1xC/ncXnvMRyhU/Wmd7tK+ERPjmHwL3aveBwmBL2tdACn4gPSjzwyXchgEf1TXVtmsAPImCcXRtnU+NsT0QCMPgcQQADkTjHV0QgXgkOr3MglUzmu7HWF8dJ2I1keBMBFPgan4lk3vSBsQeG+DJZikgAT4E/ejeMxob7eA/J8aE6Bx7wqlm7x8QErqPJ8aSJ2nuNAV/f18DneG9XuHrAN172i+WhBMJ2CYqtsrwDLLTbBVevjbPTqtgaZ2d1B5QqAkHVFsCFYlxE5OL2qkyyWZlk46ZzwFEEZEHFhvgSW6kvEBwFEvi8KE4h8YaAxKgLfMWLU3dH+3PgIz7OG5FM30tgrxQLsKiapPcz7W53+Lr/fwSaTGU64KValjXDezXvjidQJtkUfwAJ9lj360WDd44iIEUM4Nf4A0ilzB5iZ0BIsJSauMu6am+Ms9O6gZGa1hJsPV/edvFSC14DKs+FeHeG0lzWc/13mPmkM8J+AvovGOC30E7VwHfYEw2/5gB/AcMlhsUeVwFpAAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>À vous de jouer</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ol type="1">
    <li>Proposez une autre transformation non linéaire pour l’image SAR (p. ex. la racine carrée ou <code>np.arcsinh</code>) et comparez son histogramme à celui obtenu en décibels.
    </li>
    <li>Reprenez l’égalisation d’histogramme en remplaçant la CDF cible équiprobable par une <strong>CDF gaussienne</strong> (avec <code>scipy.stats.norm.cdf</code>), puis observez l’effet sur l’image SAR.
    </li>
    <li>À partir de <code>img_s2</code>, construisez un nouveau composé coloré (p. ex. <code>[11, 8, 4]</code> ou <code>[8, 4, 3]</code>) et décrivez les surfaces qu’il met en valeur.
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
    Chap02Quiz = Quiz("quiz/Chap02.yml", "Chap02")
    render_quizz(Chap02Quiz)
    return


if __name__ == "__main__":
    app.run()
