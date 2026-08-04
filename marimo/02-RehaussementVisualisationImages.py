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
    # Réhaussement et visualisation d'images

    Assurez-vous de lire ce préambule avant d'exécutez le reste du notebook.

    ## Préambule

    ### Objectifs

    Dans ce chapitre, nous abordons quelques techniques de réhaussement et de visualisation d'images. Ce chapitre est aussi disponible sous la forme d'un notebook Python:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/02-RehaussementVisualisationImages.ipynb)

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
    # %%capture --no-stderr
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
    # %%capture --no-stderr
    # !pip install -qU matplotlib rioxarray xrscipy scikit-image leafmap localtileserver
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
    # %%capture --no-stderr
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
    return img_SAR, img_rgb, img_rgbnir, img_s2


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
    Pour un affichage à trois bandes, les valeurs seront ramenées sur une dynamique de 0 à 1, il est donc nécessaire de normaliser les valeurs avant l'affichage:
    """)
    return


@app.cell
def _(img_rgbnir, plt):
    (_fig, _ax) = plt.subplots(figsize=(6, 5))
    plt.imshow(img_rgbnir.sel(band=[3, 2, 1]).data.transpose(1, 2, 0) / 2500.0)
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
    img_rgbnir.sel(band=[3, 2, 1]).plot.imshow(vmin=86, vmax=5000)
    _ax.set_title('Imshow avec rioxarray')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Visualisation sur le Web

    Les affichages `matplotlib` précédents sont **statiques**. Pour explorer une image de manière **interactive** — zoomer, se déplacer, superposer un fond de carte, comparer deux visualisations — on peut la placer sur une carte web. La librairie [`leafmap`](https://leafmap.org/) offre une interface Python unifiée au-dessus de `folium` et `ipyleaflet` et permet, en quelques lignes, d'afficher un GeoTIFF géoréférencé sur une carte glissante (*slippy map*).

    On crée une carte, puis on ajoute directement notre image locale. Comme les bandes sont stockées dans l'ordre B, V, R, PIR, on demande les indices `[3, 2, 1]` pour un composé **vraie couleur** :
    """)
    return


@app.cell
def _():
    import leafmap
    _m = leafmap.Map()
    _m.add_raster('RGBNIR_of_S2A.tif', indexes=[3, 2, 1], layer_name='Vraie couleur')
    _m
    return (leafmap,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Cette carte est **interactive** : elle ne s'affiche que dans un notebook. Pour le livre, nous en produisons une **capture statique** hors ligne avec `matplotlib` et [`contextily`](https://contextily.readthedocs.io/) (qui télécharge le fond OpenStreetMap). L'image Sentinel-2 est reprojetée en Web Mercator (`EPSG:3857`), chaque bande est étirée entre ses centiles 2 % et 98 %, et les pixels *no data* (valeur `65535` après reprojection) sont rendus transparents pour laisser voir le fond de carte :
    """)
    return


@app.cell
def _(np, plt, rxr):
    import contextily as cx
    _src = rxr.open_rasterio('RGBNIR_of_S2A.tif').rio.reproject('EPSG:3857')
    nd = _src.rio.nodata
    (x, y) = (_src.x.values, _src.y.values)
    extent = [x.min(), x.max(), y.min(), y.max()]

    def composite(bandes):
        raw = _src.isel(band=[b - 1 for b in _bandes]).to_numpy().astype('float32')
        rgba = np.zeros(raw.shape[1:] + (4,), 'float32')
        for i in range(3):
            canal = raw[i]
            valide = canal != nd
            (p2, p98) = np.percentile(canal[valide], [2, 98])
            rgba[..., i] = np.clip((canal - p2) / (p98 - p2), 0, 1)
        rgba[..., 3] = (raw != nd).all(axis=0)
        return rgba
    (_fig, _ax) = plt.subplots(figsize=(7, 6))
    cx.add_basemap(_ax, crs='EPSG:3857', source=cx.providers.OpenStreetMap.Mapnik, zorder=0)
    _ax.imshow(composite([3, 2, 1]), extent=extent, origin='upper', zorder=1)
    _ax.axis('off')
    plt.show()
    return composite, cx, extent


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La méthode `split_map` crée un **comparateur à volet glissant**, idéal pour opposer deux visualisations de la même scène — ici la vraie couleur (`[3, 2, 1]`) et l'infrarouge fausses couleurs (`[4, 3, 2]`), qui fait ressortir la végétation en rouge :
    """)
    return


@app.cell
def _(leafmap):
    _m = leafmap.Map()
    _m.split_map(left_layer='RGBNIR_of_S2A.tif', right_layer='RGBNIR_of_S2A.tif', left_args={'indexes': [3, 2, 1]}, right_args={'indexes': [4, 3, 2]}, left_label='Vraie couleur', right_label='Infrarouge')
    _m
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pour le livre, la capture statique correspondante réutilise la fonction `composite` définie plus haut, appliquée aux deux composés côte à côte :
    """)
    return


@app.cell
def _(composite, cx, extent, plt):
    (_fig, axes) = plt.subplots(1, 2, figsize=(11, 5))
    for (_ax, _bandes, titre) in zip(axes, ([3, 2, 1], [4, 3, 2]), ('Vraie couleur', 'Infrarouge (PIR, R, V)')):
        cx.add_basemap(_ax, crs='EPSG:3857', source=cx.providers.OpenStreetMap.Mapnik, zorder=0)
        _ax.imshow(composite(_bandes), extent=extent, origin='upper', zorder=1)
        _ax.set_title(titre)
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `leafmap` permet aussi d'ajouter un fond satellite (`m.add_basemap('Esri.WorldImagery')`), de charger des images distantes au format *Cloud Optimized GeoTIFF* (`m.add_cog_layer(url)`), ou d'inspecter les valeurs de pixels au clic (`m.add('inspector')`). C'est un outil précieux pour situer une image ou un résultat de traitement (comme une classification, @sec-chap05) dans son contexte géographique.

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
    return (show_hist,)


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
    [_a.axis('off') for _a in _ax.flatten()]
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
    [_a.axis('off') for _a in _ax.flatten()]
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
    #### Réhaussement gamma (loi de puissance)

    Une autre famille de réhaussements non linéaires très utilisée est la correction gamma (ou loi de puissance), qui applique un exposant $\gamma$ aux valeurs normalisées de l'image [@Jensen2016; @richards2022remote]:

    $$ j = \left(\frac{i}{i_{max}}\right)^{\gamma} \times j_{max} $$ {#eq-rehauss-gamma}

    Un $\gamma < 1$ éclaircit les tons foncés (utile pour une image sous-exposée) alors qu'un $\gamma > 1$ assombrit les tons clairs (utile pour une image surexposée); $\gamma = 1$ correspond à l'identité. Contrairement à l'étirement linéaire, cette transformation n'est pas symétrique entre les ombres et les hautes lumières:
    """)
    return


@app.cell
def _(img_rgb, np, plt):
    gammas = (0.5, 1.0, 2.0)
    img_norm = np.clip(img_rgb.data.transpose(1, 2, 0) / 255.0, 0, 1)
    (_fig, _ax) = plt.subplots(ncols=3, figsize=(9, 3))
    for (_a, g) in zip(_ax, gammas):
        _a.imshow(img_norm ** g)
        _a.set_title(f'$\\gamma$={g}')
        _a.axis('off')
    plt.tight_layout()
    plt.show()
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
    #### Égalisation adaptative (CLAHE)

    L'égalisation globale calcule une seule CDF pour toute l'image, ce qui peut mal fonctionner lorsque le contraste varie localement (zones d'ombre et de forte lumière dans une même scène). L'égalisation adaptative à contraste limité (*Contrast Limited Adaptive Histogram Equalization*, CLAHE) découpe l'image en tuiles et égalise l'histogramme de chacune séparément, avec un plafond (`clip_limit`) qui évite d'amplifier le bruit dans les zones homogènes [@Jensen2016]. La librairie `scikit-image` en fournit une implémentation directe:
    """)
    return


@app.cell
def _(img_rgb, plt):
    from skimage import exposure
    gray = img_rgb.data.transpose(1, 2, 0).mean(axis=2) / 255.0
    img_global = exposure.equalize_hist(gray)
    img_clahe = exposure.equalize_adapthist(gray, clip_limit=0.03)
    (_fig, _ax) = plt.subplots(ncols=3, figsize=(9, 3))
    for (_a, im, title) in zip(_ax, (gray, img_global, img_clahe), ('originale', 'égalisation globale', 'CLAHE')):
        _a.imshow(im, vmin=0, vmax=1)
        _a.set_title(title)
        _a.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La CLAHE fait ressortir davantage de détails locaux (textures, zones d'ombre) sans saturer les zones déjà bien contrastées, contrairement à l'égalisation globale.

    #### Correspondance d'histogrammes

    L'égalisation d'histogramme est en fait un cas particulier d'un problème plus général: faire correspondre la CDF d'une image source à une CDF cible arbitraire, et non uniquement à une distribution uniforme. Cette technique, la correspondance d'histogrammes (*histogram matching*), est notamment utile pour harmoniser la dynamique entre deux acquisitions, par exemple deux scènes adjacentes à mosaïquer [@richards2022remote; @Schowengerdt2007]. La fonction `match_histograms` de `scikit-image` implémente directement $j = CDF_{cible}^{-1}(CDF_{source}(i))$ pour une CDF cible quelconque, ici une distribution gaussienne:
    """)
    return


@app.cell
def _(img_SAR, np, plt):
    from skimage.exposure import match_histograms
    source = np.log10(img_SAR[0].data)
    cible = np.random.normal(loc=source.mean(), scale=source.std(), size=source.shape)
    source_matched = match_histograms(source, cible)
    (_fig, _ax) = plt.subplots(ncols=2, figsize=(7, 3.5))
    _ax[0].imshow(source)
    _ax[0].set_title('originale (dB)')
    _ax[1].imshow(source_matched)
    _ax[1].set_title('après correspondance (cible gaussienne)')
    [_a.axis('off') for _a in _ax]
    plt.tight_layout()
    plt.show()
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
    [_a.axis('off') for _a in _ax.flatten()]
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
    #### Étirement par décorrélation

    Les bandes d'une image multispectrale sont souvent fortement corrélées entre elles, ce qui donne des composés couleurs peu contrastés (dominante grisâtre). L'étirement par décorrélation (*decorrelation stretch*) corrige ce problème en décorrélant les bandes dans l'espace des composantes principales, en égalisant leur variance, puis en revenant dans l'espace original [@Schowengerdt2007; @richards2022remote]:
    """)
    return


@app.cell
def _(img_s2, np, plt):
    def decorrelation_stretch(img):
        X = img.reshape(img.shape[0], -1).astype(float)
        X = X - X.mean(axis=1, keepdims=True)
        (valeurs, vecteurs) = np.linalg.eigh(np.cov(X))
        X_pca = vecteurs.T @ X / np.sqrt(valeurs)[:, None]
        X_stretch = vecteurs @ X_pca
        q = np.quantile(X_stretch, [0.01, 0.02, 0.98, 0.99])
        print(q)
        X_stretch = X_stretch - q[1]
        X_stretch = X_stretch / (q[2] - q[1])
        return X_stretch.clip(0, 1).reshape(img.shape)
    composite_1 = img_s2.sel(band=[4, 3, 2]).data
    composite_stretch = decorrelation_stretch(composite_1)
    (_fig, _ax) = plt.subplots(ncols=2, figsize=(8, 4))
    _ax[0].imshow(np.clip(composite_1.transpose(1, 2, 0) / 4000.0, 0, 1))
    _ax[0].set_title('composé RVB original')
    _ax[1].imshow(composite_stretch.transpose(1, 2, 0))
    _ax[1].set_title('après étirement par décorrélation')
    [_a.axis('off') for _a in _ax]
    plt.tight_layout()
    plt.show()
    return (composite_stretch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le résultat conserve les teintes relatives entre bandes tout en maximisant le contraste de chacune des composantes principales, ce qui fait ressortir davantage de détails que le composé original.

    On peut confirmer cet étalement en traçant l'histogramme des trois bandes du composé étiré avec `show_hist` de `rasterio`, qui accepte directement une matrice `(bandes, lignes, colonnes)`. Après décorrélation, chaque bande occupe désormais toute la plage `[0, 1]` :
    """)
    return


@app.cell
def _(composite_stretch, plt, show_hist):
    (_fig, _ax) = plt.subplots(figsize=(6, 4))
    show_hist(composite_stretch, bins=50, lw=0.0, stacked=False, alpha=0.3, histtype='stepfilled', ax=_ax, title='Histogramme du composé après étirement par décorrélation')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Poids des bandes : le cercle des corrélations

    Au-delà du résultat visuel, l'ACP nous renseigne sur **la façon dont chaque bande contribue à chaque composante principale**. Les vecteurs propres donnent le **poids** de chaque bande dans une composante ; multipliés par la racine carrée de la valeur propre associée, ils fournissent la **corrélation** entre chaque bande et chaque composante. On visualise ces corrélations dans un **cercle des corrélations** : chaque bande devient une flèche partant de l'origine, dont les coordonnées sont ses corrélations avec les deux premières composantes (CP1 et CP2). Une flèche proche du cercle unité est bien représentée dans le plan CP1-CP2 ; deux flèches proches signalent des bandes corrélées, deux flèches opposées des bandes anti-corrélées.
    """)
    return


@app.cell
def _(img_s2, np, plt):
    _bandes = [2, 3, 4, 8, 11, 12]
    noms = ['B', 'V', 'R', 'PIR', 'SWIR1', 'SWIR2']
    X = img_s2.sel(band=_bandes).data.reshape(len(_bandes), -1).astype(float)
    X = X[:, ~np.isnan(X).any(axis=0)]  # on retire les no_data
    X = (X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)  # standardisation
    (valeurs, vecteurs) = np.linalg.eigh(np.corrcoef(X))
    ordre = np.argsort(valeurs)[::-1]  # ACP sur la corrélation
    (valeurs, vecteurs) = (valeurs[ordre], vecteurs[:, ordre])  # variance décroissante
    loadings = vecteurs * np.sqrt(valeurs)
    pct = 100 * valeurs / valeurs.sum()  # corrélation bande <-> composante
    (_fig, _ax) = plt.subplots(figsize=(5.5, 5.5))
    _ax.add_patch(plt.Circle((0, 0), 1, fill=False, color='grey', ls='--'))
    _ax.axhline(0, color='grey', lw=0.5)
    _ax.axvline(0, color='grey', lw=0.5)
    for (i, nom) in enumerate(noms):
        _ax.arrow(0, 0, loadings[i, 0], loadings[i, 1], color='tab:blue', head_width=0.03, length_includes_head=True)
        _ax.text(loadings[i, 0] * 1.15, loadings[i, 1] * 1.15, nom, ha='center', va='center')
    _ax.set_xlim(-1.2, 1.2)
    _ax.set_ylim(-1.2, 1.2)
    _ax.set_aspect('equal')
    _ax.set_xlabel(f'CP1 ({pct[0]:.0f} %)')
    _ax.set_ylabel(f'CP2 ({pct[1]:.0f} %)')
    _ax.set_title('Cercle des corrélations (ACP sur 6 bandes Sentinel-2)')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sur ce composé Sentinel-2, la première composante (CP1, environ 68 % de la variance) est corrélée négativement à presque toutes les bandes : elle traduit la **luminosité globale** de la scène. La seconde (CP2, environ 27 %) oppose le **proche infrarouge et le SWIR1** au reste : c'est un axe de **végétation / humidité**. Les bandes visibles (B, V, R), dont les flèches sont quasi confondues, sont **fortement corrélées** entre elles — c'est précisément cette redondance que l'étirement par décorrélation vient corriger.

    ## Points clés

    ## Exercices

    **À vous de jouer**

    1.  Proposez une autre transformation non linéaire pour l'image SAR (p. ex. la racine carrée ou `np.arcsinh`) et comparez son histogramme à celui obtenu en décibels.

    2.  À l'aide de `skimage.exposure.match_histograms`, faites correspondre l'histogramme de la bande proche infrarouge de `RGBNIR_of_S2A.tif` à celui d'une bande de `sentinel2.tif`. Discutez du résultat.

    3.  À partir de `img_s2`, construisez un nouveau composé coloré (p. ex. `[11, 8, 4]` ou `[8, 4, 3]`) et décrivez les surfaces qu'il met en valeur.

    4.  *(visualisation web)* Dans Colab, installez `leafmap`, chargez `RGBNIR_of_S2A.tif` en composé infrarouge (`indexes=[4, 3, 2]`) sur un fond `Esri.WorldImagery`, puis comparez vraie couleur et infrarouge avec `split_map`.

    5.  Comparez une égalisation d'histogramme globale et une égalisation adaptative (CLAHE) sur une image de votre choix. Dans quels cas la CLAHE fait-elle ressortir des détails invisibles avec l'égalisation globale?

    6.  Appliquez un étirement par décorrélation sur le composé SWIR2, NIR, R de `sentinel2.tif` et comparez-le au composé sans étirement. La corrélation entre bandes est-elle plus ou moins forte que pour le composé RVB naturel?

    7.  *(cercle des corrélations)* Reprenez le **cercle des corrélations** sur les **quatre bandes** de `RGBNIR_of_S2A.tif` (B, V, R, PIR) : standardisez les bandes, calculez l'ACP sur leur matrice de corrélation, puis tracez les flèches des *loadings* dans le plan CP1-CP2. Quelle(s) bande(s) domine(nt) la première composante? La flèche du proche infrarouge est-elle alignée avec celles du visible ou s'en écarte-t-elle nettement? Qu'en concluez-vous sur la corrélation entre le PIR et les bandes visibles?

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
