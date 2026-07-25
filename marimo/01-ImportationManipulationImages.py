# /// script
# dependencies = ["rioxarray", "xrscipy"]
# ///

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Importation et manipulation de données spatiales {#sec-chap01}

    ## Préambule

    Assurez-vous de lire ce préambule avant d'exécuter le reste du notebook.

    ### Objectifs

    Dans ce chapitre, nous abordons quelques formats d'images ainsi que leur lecture. Ce chapitre est aussi disponible sous la forme d'un notebook Python:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/01-ImportationManipulationImages.ipynb)

    <div style="border:0.5px solid silver;border-left:.3rem solid #00796d;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2efec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADfUlEQVRYhb2XMXLbMBBFnzVKkSZ0ylRmJkVKMycwfQIrJzB9AVruMsNGLlCHwQVC3UC+AXUC02WKTOQ+hXGAjFNgIYIQZNkZxzvD4UhY7H7s/l0s9+7v73msJFWZAzmQAfvBcidPa5RePdbm3i4ASVWmwBQogOSRdpdAY5RuIvb2gX0H8kEASVXOxHkCGGAhT2uUvgt0M2x0CuBQ/r4BCqN05+m0wMQo3QKMtzjOgEYMGeAsdhpfxEkH1BK1GjhBUuU5H0RxIwKB4pWcYHDax0pSlalRehVxfiFghwACxQujdP0vjgMQ0ZOLfBt7ivvYsCc8EHLRy7GV4OQOy4su0C2wqYg5PzNKNz4HZticz7ewNxWd0xgw0bkFZt7+mHODTesCYCQbM+AcuMWyPjQ8websVHQugWPvOQPmwAE9CQFWEee5cw7CgaQqF1jGHrvy8JwXwHf5+SAvPMd32HI98pZvsOW3SqqyBmqj9Gokm06A24jzFBtGA3zaRUqvA7bifAm8xUYpF+c5NtozsH0gl00x4w09KdcEEyIW9O24M0ovAsbPjdKFB8iBbJOqNMDEAZjI2jov4iRzp/BJuY3ZSVX+AN4Bb5BUiY3CKB3yagGcJlWZjYAUMJELxAFbR0ZSsuYDfXh/Ah+B19ho1d7eczallXc2wpZeF1HKA2WQvAFTo3QtHbIAPgB/gFeB/p0AzxnKSt7pKOJ4IEEbTrHRasRwgy3NG+CLp+MkdrCB7ASwQ3Is03Pgd2R95x2yE4Aw3skKSKQxYZROjdK5RGnq6TgJh5YNGWPDl0XWWmwVTLDlCH0rbmRWWIiTGsulq4DMDmgb2E4d2JF3qjRQcmVZuD/E+Jn8/Ar8Aq7pm85aV4h3iL3SQ8nl3Y08RxNfQxrPEjiS2nf/N3KCC+ydcAl89lLhpA7eIQBjlO7G9GUzjSgX9FNO57qhOHroTmjoU9IGaxPspTUHGElY58BBWK+y5mbC66QqN27KwHiaVKW7NW/wUuKJs1FDfxtm2FzeAllk4HRETESnYdhwUmxY3awQHeW8m3VplM7XAGTRtU3/Ehmcjh0DiYDzB5JwfyeHeL8xlku9t9jcPctIFuxxtgczxUsMpb7zjej+77E8x5Z5OB9sByAbU9noPkymuz5MIvvdhwnApVF6FtN90U+zJwPwTvNsH6dPBhCAyXnmz/O/0JrtInNZu4wAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Objectifs d’apprentissage visés dans ce chapitre</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">

    </div>
    </div>

    ### Bibliothèques

    Les bibliothèques qui vont être explorées dans ce chapitre sont les suivantes:

    -   [SciPy](https://scipy.org/)

    -   [NumPy](https://numpy.org/)

    -   [opencv-python · PyPI](https://pypi.org/project/opencv-python/)

    -   [scikit-image](https://scikit-image.org/)

    -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

    -   [Xarray](https://docs.xarray.dev/en/stable/)

    -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

    Dans l'environnement Google Colab, seul `rioxarray` et `gdal` doivent être installés:
    """)
    return


@app.cell
def _(subprocess):
    #! apt-get update
    subprocess.call(['apt-get', 'update'])
    #! apt-get install gdal-bin libgdal-dev
    subprocess.call(['apt-get', 'install', 'gdal-bin', 'libgdal-dev'])
    # packages added via marimo's package management: rioxarray xrscipy !pip install -q rioxarray xrscipy
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
    import matplotlib.pyplot as plt

    return np, plt, rxr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Données

    Nous utilisons ces images dans ce chapitre:
    """)
    return


@app.cell
def _(subprocess):
    import gdown

    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6Ypg0g1Oy4AJt9XWKWfnR12NW1XhNg_', output= 'RGBNIR_of_S2A.tif')
    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a4PQ68Ru8zBphbQ22j0sgJ4D2quw-Wo6', output= 'landsat7.tif')
    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    #! wget https://raw.githubusercontent.com/sfoucher/TraitementImagesPythonVol1/refs/heads/main/images/modis-aqua.PNG -O modis-aqua.PNG
    subprocess.call(['wget', 'https://raw.githubusercontent.com/sfoucher/TraitementImagesPythonVol1/refs/heads/main/images/modis-aqua.PNG', '-O', 'modis-aqua.PNG'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifiez que vous êtes capable de les lire:
    """)
    return


@app.cell
def _(rxr):
    with rxr.open_rasterio('berkeley.jpg', mask_and_scale=True) as _img_rgb:
        print(_img_rgb)
    with rxr.open_rasterio('RGBNIR_of_S2A.tif', mask_and_scale=True) as img_rgbnir:
        print(img_rgbnir)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Importation d'images

    La première étape avant tout traitement est d'accéder à la donnée image pour qu'elle soit manipulée par le langage Python. L'imagerie satellite présente certains défis notamment en raison de la taille parfois très importante des images. Il existe maintenant certaines bibliothèques, comme [Xarray](https://docs.xarray.dev/en/stable/), qui visent à optimiser la lecture et l'écriture de grandes images. Il est donc conseillé de toujours garder un oeil sur l'espace mémoire occupé par les variables Python représentant les images. La librairie principale en géomatique qui permet d'importer (et d'exporter) de l'imagerie est la librairie [GDAL](https://gdal.org) qui rassemble la plupart des formats sous forme de *driver* (ou pilote en français).

    Dans le domaine de la géomatique, il faut prêter attention à quatre caractéristiques principales des images:

    1\. **La matrice des données** elle-même qui contient les valeurs brutes des pixels. Cette matrice sera souvent un cube à trois dimensions. En Python, ce cube sera le plus souvent un objet de la librairie [NumPy](https://numpy.org/) (voir la section « Manipulation de la matrice de pixels » plus bas).

    2\. **La dynamique des images** c.-à.-d le format de stockage des valeurs individuelles (octet, entier, double, etc.). Ce format décide principalement de la résolution radiométrique et des valeurs minimales et maximales supportées.

    3\. **Le nombre de bandes** spectrales de l'image qui est souvent supérieur à trois et peut atteindre plusieurs centaines de bandes pour certains capteurs (notamment hyperspectraux).

    4\. **La métadonnée** qui va transporter l'information auxiliaire de l'image comme les dimensions et la position de l'image, la date, etc. Cette donnée auxiliaire prendra souvent la forme d'un dictionnaire Python. Elle contiendra aussi l'information de géoréférence.

    Les différents formats se distinguent principalement sur la manière dont ces quatre caractéristiques sont gérées.

    ### Formats des images

    Il existe de nombreux formats numériques pour la donnée de type image parfois appelé donnée matricielle ou donnée *raster*. La librairie GDAL rassemble la plupart des formats matriciels rencontrés en géomatique (voir [Raster drivers — GDAL documentation](https://gdal.org/en/latest/drivers/raster/index.html) pour une liste complète).

    On peut distinguer deux grandes familles de format:

    1\. Les formats de type **RVB** issus de l'imagerie numérique grand public comme [JPEG](https://gdal.org/en/latest/drivers/raster/jpeg.html#raster-jpeg), [png](https://gdal.org/en/latest/drivers/raster/png.html#raster-png), etc. Ces formats ne supportent généralement que trois bandes au maximum (rouge, vert et bleu) et des valeurs de niveaux de gris entre 0 et 255 (format dit 8 bits ou `uint8`).

    2\. **Les géo-formats** issus des domaines scientifiques ou techniques comme GeoTIFF, HDF5, NetCDF, etc. qui peuvent inclure plus que trois bandes et des dynamiques plus élevées (16 bits ou même float).

    Les formats RVB restent très utilisés en Python notamment par les bibliothèques dites de vision par ordinateur (*Computer Vision*) comme OpenCV et scikit-image ainsi que les grandes bibliothèques en apprentissage profond (PyTorch, Tensorflow).

    <div style="border:0.5px solid silver;border-left:.3rem solid #352c76;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2e1f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAABhUlEQVRYhe2Wv3HCMByFP3P0YYMwQHShiGrYgGSCsEFcRSWmVBWYIGYDNoDUashpAdiATOAUyMZnDvsiMKTwa2z9ud/7znqSFSRJQlFSqA1wfzRwnrbG6m6xMygCSKEiYAx8AauKoiP3jCvmDYA+MDFWRycBpFBdYO2aPWP1pqyqFGoFYKweVMw7WbdVmDsF7oBplflf5GpltfNjGYAUagAM2a9VdCnzHEQEbIGh8zoASKE6HNZxdGnznNLasfPMvkDIPvVzY/WqLndXe+68QoCWC8gY+Ek7a1bovMZSqG7w9PAeOYBbaNLONb6B3ZWMO8AjQB4grHP983K7YAnH58DV1a6aIIUa4b81Y2N17A0ghXoGPj3NAfpSqJ2xeuEFAPQAjNWBj7sUKnE1TgL8/wxAltqbAKS/0OUZHuuywVIAY/VCCvWCy4KPeVkAKwFSCEpCdK5uHsIGoAFoABqAPIDvceujzKvN4Wfx4a7odV9MO8Cbe18HSZIghYqB15qNi5oZq8Nf0ER+TJGyROAAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Installation de gdal dans un système Linux</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ul>
    <li>Pour installer GDAL :</li>
    </ul>
    <pre><code>!apt-get update
    !apt-get install gdal-bin libgdal-dev</code></pre>
    </div>
    </div>

    #### Formats de type RVB

    Les premiers formats pour de l'imagerie à une bande (monochrome) et à trois bandes (image couleur rouge-vert-bleu) sont issus du domaine des sciences de l'ordinateur. On trouvera, entre autres, les formats pbm, png et jpeg. Ces formats supportent peu de métadonnées et sont placées dans un entête (*header*) très limité. Cependant, ils restent très populaires dans le domaine de la vision par ordinateur et sont très utilisés en apprentissage profond en particulier. Pour la lecture des images RVB, on peut utiliser les bibliothèques Rasterio, [PIL](https://he-arc.github.io/livre-python/pillow/index.html) ou [OpenCV](https://docs.opencv.org/4.10.0/index.html).

    ##### Lecture avec la librairie PIL

    La librairie PIL retourne un objet de type `PngImageFile`, l'affichage de l'image se fait directement dans la cellule de sortie.
    """)
    return


@app.cell
def _():
    from PIL import Image
    img = Image.open('modis-aqua.PNG')
    img
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Lecture avec la librairie OpenCV

    La librairie [OpenCV](https://docs.opencv.org/4.10.0/index.html) est aussi très populaire en vision par ordinateur. La fonction `imread` donne directement un objet de type NumPy en sortie.
    """)
    return


@app.cell
def _():
    import cv2
    img_1 = cv2.imread('modis-aqua.PNG')
    img_1
    return (cv2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Attention : la fonction `imread` d'OpenCV renvoie les canaux dans l'ordre **BGR** (bleu, vert, rouge) et non RGB. Il faut convertir l'image avant de l'afficher correctement avec `matplotlib` :
    """)
    return


@app.cell
def _(cv2, plt):
    img_bgr = cv2.imread('modis-aqua.PNG')
    _img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    (_fig, _ax) = plt.subplots(1, 2, figsize=(8, 4))
    _ax[0].imshow(img_bgr)
    _ax[0].set_title('Sans conversion (BGR)')
    _ax[0].axis('off')
    _ax[1].imshow(_img_rgb)
    _ax[1].set_title('Après conversion (RGB)')
    _ax[1].axis('off')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Lecture avec la librairie RasterIO

    Rien ne nous empêche de lire une image de format RVB avec [RasterIO](https://rasterio.readthedocs.io/en/stable/) comme décrit dans ci-dessous. Vous noterez cependant les avertissements concernant l'absence de géoréférence pour ce type d'image.
    """)
    return


@app.cell
def _():
    import rasterio
    img_2 = rasterio.open('modis-aqua.PNG')
    img_2
    return (rasterio,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Le format GeoTiff

    Le format GeoTIFF est une extension du format TIFF (Tagged Image File Format) qui permet d'incorporer des métadonnées géospatiales directement dans un fichier image. Développé initialement par Dr. Niles Ritter au Jet Propulsion Laboratory de la [NASA](https://www.earthdata.nasa.gov/esdis/esco/standards-and-practices/geotiff){target="_blank"} dans les années 1990, GeoTIFF est devenu un standard de facto pour le stockage et l'échange d'images géoréférencées dans les domaines de la télédétection et des systèmes d'information géographique (SIG). Ce format supporte plus que trois bandes aussi longtemps que ces bandes sont de même dimension.

    Le format GeoTIFF est très utilisé et est largement supporté par les bibliothèques et logiciels géospatiaux, notamment [GDAL](https://gdal.org) (*Geospatial Data Abstraction Library*), qui offre des capacités de lecture et d'écriture pour ce format. Cette compatibilité étendue a contribué à son adoption généralisée dans la communauté géospatiale.

    ##### Standardisation par l'OGC

    Le standard GeoTIFF proposé par l'Open Geospatial Consortium (OGC) en 2019 formalise et étend les spécifications originales du format GeoTIFF, offrant une norme robuste pour l'échange d'images géoréférencées. Cette standardisation, connue sous le nom d'OGC GeoTIFF 1.1 [-@OGCGeoTIFF], apporte plusieurs améliorations et clarifications importantes.

    #### Le format COG

    Une innovation récente dans l'écosystème GeoTIFF est le format *Cloud Optimized GeoTIFF* ([COG](http://cogeo.org/)), conçu pour faciliter l'utilisation de fichiers GeoTIFF hébergés sur des serveurs web HTTP. Le COG permet aux utilisateurs et aux logiciels d'accéder à des parties spécifiques du fichier sans avoir à le télécharger entièrement, ce qui est particulièrement utile pour les applications basées sur l'infonuagique.

    ### Métadonnées des images

    La manière la plus directe d'accéder à la métadonnée d'une image est d'utiliser les commandes [`rio info`](https://rasterio.readthedocs.io/en/stable/cli.html#info) de la librairie Rasterio ou `gdalinfo` de la librairie `gdal`. Le résultat est imprimé dans la sortie standard ou sous forme d'un dictionnaire Python.
    """)
    return


@app.cell
def _(subprocess):
    #! gdalinfo RGBNIR_of_S2A.tif
    subprocess.call(['gdalinfo', 'RGBNIR_of_S2A.tif'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le plus simple est d'utiliser la fonction `rio info`:
    """)
    return


@app.cell
def _(subprocess):
    #! rio info RGBNIR_of_S2A.tif --indent 2 --verbose
    subprocess.call(['rio', 'info', 'RGBNIR_of_S2A.tif', '--indent', '2', '--verbose'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Depuis Python, `rasterio` donne accès à ces mêmes informations sous forme d'attributs et d'un dictionnaire de métadonnées :
    """)
    return


@app.cell
def _(rasterio):
    with rasterio.open('RGBNIR_of_S2A.tif') as _src:
        print('Nombre de bandes :', _src.count)
        print('Dimensions (lignes, colonnes) :', _src.height, _src.width)
        print('Type des pixels :', _src.dtypes[0])
        print('Système de coordonnées :', _src.crs)
        print('Résolution (m) :', _src.res)
        print('Emprise :', _src.bounds)
        meta = _src.meta
    meta
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Manipulation des images

    ### Manipulation de la matrice de pixels

    La donnée brute de l'image est généralement contenue dans un cube matricielle à trois dimensions (deux dimensions spatiales et une dimension spectrale). Comme exposé précédemment, la librairie dite *"fondationnelle"* pour la manipulation de matrices en Python est [NumPy](https://numpy.org/). Cette librairie contient un nombre très important de fonctionnalités couvrant l'algèbre linéaire, les statistiques, etc.; elle constitue la fondation de nombreuses bibliothèques en traitement numérique (voir (@fig-naturenumpy1))

    ![La librairie NumPy est le fondement de nombreuses bibliothèques scientifiques (d'après [@NumpyNature]).](images/41586_2020_2649_Fig2_HTML.png){#fig-naturenumpy1 width="100%" fig-align="center"}

    ### Information de base

    Les deux informations de base à afficher sur une matrice sont 1) les dimensions de la matrice et 2) le format de stockage (le type). Pour cela, on peut utiliser le code ci-dessous, dont le résultat nous informe que la matrice a trois dimensions et une taille de `(442, 553, 3)` et un type `uint8` qui représente 1 octet (8 bit). Par conséquent, la matrice a `442` lignes, `553` colonnes et `3` canaux ou bandes. Il faut prêter une attention particulière aux valeurs minimales et maximales tolérées par le type de la donnée comme indiqué dans le (@tbl-numpytype) (voir aussi [Data types — NumPy v2.1 Manual](https://numpy.org/doc/stable/user/basics.types.html)).
    """)
    return


@app.cell
def _(cv2):
    img_3 = cv2.imread('modis-aqua.PNG')
    print('Nombre de dimensions: ', img_3.ndim)
    print('Dimensions de la matrice: ', img_3.shape)
    print('Type de la donnée: ', img_3.dtype)
    return


@app.cell
def _():
    from IPython.display import Markdown
    from tabulate import tabulate
    table = [["uint8",   "unsigned char",  8,  0,           255],
             ["int8",    "signed char",    8, -128,         127],
             ["uint16",  "unsigned short", 16, 0,           65535],
             ["int16",   "short",          16, -32768,      32767],
             ["uint32",  "unsigned int",   32, 0,           4294967295],
             ["int32",   "int",            32, -2147483648, 2147483647],
             ["float32", "float",          32, "-3.4e38",   "3.4e38"],
             ["float64", "double",         64, "-1.8e308",  "1.8e308"]]
    Markdown(tabulate(table, headers=["dtype", "Nom", "Taille (bits)", "Min", "Max"], tablefmt="pipe"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Découpage et indexation de la matrice

    L'indexation et le découpage (*slicing*) des matrices dans NumPy sont des techniques essentielles pour manipuler efficacement les données multidimensionnelles en Python, offrant une syntaxe puissante et flexible pour accéder et modifier des sous-ensembles spécifiques d'éléments dans les tableaux (voir @fig-naturenumpy2). Indexer une matrice consiste à accéder à une valeur dans la matrice pour une position particulière, la syntaxe générale est `matrice[ligne, colonne, bande]` et est similaire à la manipulation des [listes](https://docs.python.org/fr/3/tutorial/introduction.html#lists) en Python. Les indices commencent à `0` et se terminent à la `taille-1` de l'axe considéré.

    ![Vue d'ensemble des opérations de base des matrices avec NumPy](images/41586_2020_2649_Fig1_HTML.png){#fig-naturenumpy2 width="100%" fig-align="center"}

    Le découpage (ou *slicing* en anglais) consiste à produire une nouvelle matrice qui est un sous-ensemble de la matrice d'origine. Un découpage se fait avec le symbole ':', la syntaxe générale pour définir un découpage est `[début:fin:pas]`. Si on ne spécifie pas `début` ou `fin` alors les valeurs 0 ou `dimension-1` sont considérées implicitement. Quelques exemples :

    -   choisir un pixel en particulier avec toutes les bandes : `matrice[1, 1, :]`;
    -   choisir la troisième colonne (indice 2) avec toutes les bandes : `matrice[:, 2, :]`.

    La syntaxe de base pour le découpage (*slicing*) des tableaux NumPy repose sur l'utilisation des deux-points (`:`) à l'intérieur des crochets d'indexation. Cette notation permet de sélectionner des plages d'éléments de manière concise et intuitive. La structure générale du découpage est `matrice[start:stop:step]`, où : 1. `start` représente l'index de départ (inclus) 2. `stop` indique l'index de fin (exclu) 3. `step` définit l'intervalle entre chaque élément sélectionné

    Si l'un de ces paramètres est omis, NumPy utilise des valeurs par défaut : 0 pour `start`, la taille du tableau pour `stop`, et 1 pour `step`. Par exemple, pour un tableau unidimensionnel `array`, on peut extraire les éléments du deuxième au quatrième avec `array[1:4]`. Pour sélectionner tous les éléments à partir du troisième, on utiliserait `array[2:]`. Cette syntaxe s'applique également aux tableaux multidimensionnels, où chaque dimension est séparée par une virgule. Ainsi, pour une matrice 2D m, `m[0:2, 1:3]` sélectionnerait une sous-matrice 2x2 composée des deux premières lignes et des deuxième et troisième colonnes. L'indexation négative est également supportée, permettant de compter à partir de la fin du tableau. Par exemple, `a[-3:]` sélectionnerait les trois derniers éléments d'un tableau.
    """)
    return


@app.cell
def _(cv2):
    img_4 = cv2.imread('modis-aqua.PNG')
    img_col = img_4[:, 2, :]
    print('Nombre de dimensions: ', img_col.ndim)  # troisième colonne (indice 2), toutes les bandes
    print('Dimensions de la matrice: ', img_col.shape)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div style="border:0.5px solid silver;border-left:.3rem solid #eb5f23;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fef4ec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADSElEQVRYhbWX0W3bMBCGPwd5jwvwPUY1QNQJokxQL1DVmSDuBHEnqDNBFS7QdIJKE9QdgIDzXAFRJnAfeIzPDC05TXuAIZu64//z7ueRHm02G/63tWU2BvLUu+P/BFbIJwfO+/z/GYG2zApgBnyMXjXAWj7aZsDpqwkI8ILtSu+BCrgz1q0G4l5HoC2zJXAlPxtgYayrDwzPgaaXQFtmE2AKpFayBM7wK55p4LbMpmxFV8ekRCcnQLeXQFtmOVCL4z77LuCdiqvY1cF1W2Y3xrq5GivkuTraA14o8E/AhTxvlNutsW4agRcCfi/kGuARuJIFxQTqZxloy2wGfJWfl8a6SsZXQiqAzxLcw8RrY91U4mq8QHUppwDGul0CCvwRmEa1q/A13wc+ZJ1g5MApPkPbPqBq9wgUegu1ZTYH3gPNAPgdcA2ct2W2xu/9XL0DCFqoAEabzUaD/8KLSoNP2KZuomuesqiEyILmxrpK1L8GOmPdBOA4Um0NTGUb1YrxCV4PSXBJa2esWwtQjRKasW4t3xcy1zLEjn5/eNvRv9UA7gPjBPgCn/bPxrrFvgmE5M94rmNj3Vg5jKO4UPslCYt0c5fyEb8xUnO2GvAEwpdU35Z9/Z7oIJEJl2x1UwxoI3TNW2PdDtFkI1IWSFWhkQh4fSi4FnhqB42GLiRRb8jxqT4DbvHq3ifMsfie9xFNElA3mJWxrlNCC9bbjCRblRAFeLOP6LMSqBT/4HkTAdnXPeBziQ/g9JVoh4AwX0lwA6ykBLW4NET7WMfK/v8iQ5fif78PHFQJouP3KcVtmW3YrvpOre5Wxgp5hhtRg++maznAOmNdcUgGdsClFACf8QKqJJUFXlQfgQfgm4A3wIWxrlCd74wBO1Kr7/Bpmwvzh7bMCulueVtm67bMZopEI0QAbgS4DhNLOx+0Y3hqQhMlwDOZfNXuHi6d+HdAIY3qRxhX4Dom2UV3MqCyoAVY4A+P0AMu4y6WsqhvvBuKiTVwitdAAL9iez+oDgCvFHiRau9JArL6E3wtZ/JOgw9NVEd3ivwQcNjVwCh69w5/t+s7ZAp5VvjsHXIwPSeQskNXIBbueLOXgPcSeKH97UX11QSWJP75vMT+AHO9uY9+8Go9AAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>Une vue versus une copie</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    Avec NumPy, les manipulations peuvent créer des vues ou des copies. Une vue est une simple représentation de la même donnée originale alors qu’une copie est un nouvel espace mémoire.

    Par défaut, un découpage créé une vue.

    On peut vérifier si l’espace mémoire est partagé avec <code>np.shares_memory(arr, slice_arr)</code>.

    On peut toujours forcer une copie avec la méthode <code>copy()</code>

    </div>
    </div>

    ```{=html}

    ```

    ### Indexation avancée

    Au-delà du découpage, NumPy permet de sélectionner des éléments à l'aide de **tableaux d'indices** (*fancy indexing*) : on peut choisir une liste de bandes dans un ordre arbitraire, ou récupérer une valeur différente pour chaque pixel. Contrairement au découpage, l'indexation avancée renvoie toujours une **copie**.
    """)
    return


@app.cell
def _(np):
    petit = np.array([[10, 50, 30], [70, 20, 40], [5, 15, 90]])
    choix = np.array([1, 0, 2])
    # Un indice de bande choisi pour chacun des 3 pixels (3 pixels x 3 bandes)
    print(petit[np.arange(3), choix])  # bande retenue pour chaque pixel  # -> [50, 70, 90]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Appliqué à une image réelle, ce mécanisme permet de réordonner les bandes, ou de construire une carte de la **bande dominante** (la bande la plus brillante en chaque pixel) grâce à `argmax` le long de l'axe spectral :
    """)
    return


@app.cell
def _(np, rxr):
    cube = rxr.open_rasterio('RGBNIR_of_S2A.tif').to_numpy()
    vraie_couleur = cube[[2, 1, 0]]
    print('Bandes réordonnées :', vraie_couleur.shape)  # (4, lignes, colonnes) ; bandes B, V, R, PIR
    bande_dominante = cube.argmax(axis=0)
    # Sélection de bandes par liste d'indices : passage en ordre vrai-couleur (R, V, B)
    print('Carte des bandes dominantes :', bande_dominante.shape)
    # argmax sur l'axe des bandes : indice de la bande la plus brillante par pixel
    print('Bandes présentes :', np.unique(bande_dominante))  # (lignes, colonnes), valeurs 0..3
    return (bande_dominante,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La bande dominante donne un premier aperçu de la nature des surfaces : le proche-infrarouge (indice 3) domine généralement sur la végétation, tandis que le bleu ou le rouge l'emporte sur l'eau et les surfaces artificielles.
    """)
    return


@app.cell
def _(bande_dominante, plt):
    (_fig, _ax) = plt.subplots(figsize=(6, 5))
    im = _ax.imshow(bande_dominante, cmap='viridis')
    _ax.set_title('Bande dominante par pixel (0=B, 1=V, 2=R, 3=PIR)')
    _ax.axis('off')
    _fig.colorbar(im, ax=_ax, ticks=[0, 1, 2, 3], shrink=0.7)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Masquage

    L'utilisation d'un masque est un outil important en traitement d'image car la plupart des images de télédétection contiennent des pixels non valides qu'il faut exclure des traitements (ce que l'on appelle le *no data* en Anglais). Il y a plusieurs raison possibles pour la présence de pixels non valides:

    1.  L'image est projetée dans une grille cartographique et certaines zones, généralement situées en dehors de l'empreinte au sol du capteur, sont à exclure.

    2.  La présence de nuages que l'on veut exclure.

    3.  La présence de pixels erronés dus à des problèmes de capteurs.

    4.  La présence de valeurs non numériques (*not a number* ou `nan`)

    La librairie NumPy fournit des mécanismes pour exclure automatiquement certaines valeurs. Le module `numpy.ma` permet de créer un tableau masqué où les pixels non valides sont ignorés par les calculs statistiques :
    """)
    return


@app.cell
def _(np):
    img_5 = np.array([[12, 0, 15], [8, 20, 0], [0, 21, 23]], dtype=float)
    img_masque = np.ma.masked_equal(img_5, 0)
    # Une petite image dont la valeur 0 représente le "no data"
    print('Moyenne sans masque :', round(img_5.mean(), 2))
    print('Moyenne avec masque :', round(img_masque.mean(), 2))
    img_nan = np.where(img_5 == 0, np.nan, img_5)
    # Masquer les pixels égaux à 0 : ils seront ignorés par les statistiques
    # Approche équivalente avec des NaN et les fonctions « nan » de NumPy
    print('Moyenne (nanmean)   :', round(np.nanmean(img_nan), 2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sur une image réelle, on masque le plus souvent selon un **critère** plutôt qu'une valeur exacte. Ici, on exclut l'eau et les surfaces artificielles (NDVI négatif) pour ne calculer une statistique que sur la végétation. `np.ma.masked_where` masque les pixels remplissant la condition ; `count()` compte les pixels valides et `compressed()` renvoie ces derniers sous forme de tableau 1D :
    """)
    return


@app.cell
def _(np, rxr):
    img_6 = rxr.open_rasterio('RGBNIR_of_S2A.tif').astype('float32')
    (_rouge, _pir) = (img_6.sel(band=3).to_numpy(), img_6.sel(band=4).to_numpy())
    _ndvi = (_pir - _rouge) / (_pir + _rouge)
    ndvi_veg = np.ma.masked_where(_ndvi < 0, _ndvi)
    print('Pixels totaux  :', _ndvi.size)
    print('Pixels valides :', ndvi_veg.count())
    print('NDVI moyen (tous)       :', round(float(_ndvi.mean()), 3))
    print('NDVI moyen (végétation) :', round(float(ndvi_veg.mean()), 3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Calcul d'un rapport de bandes

    Une opération très courante consiste à combiner deux bandes pixel par pixel. Par exemple, un rapport normalisé entre le proche-infrarouge et le rouge met en évidence la végétation (ce type d'indice spectral est approfondi au chapitre @sec-chap03) :
    """)
    return


@app.cell
def _(rxr):
    img_7 = rxr.open_rasterio('RGBNIR_of_S2A.tif').astype('float32')
    _rouge = img_7.sel(band=3)
    _pir = img_7.sel(band=4)
    rapport = (_pir - _rouge) / (_pir + _rouge)
    print('Forme du rapport :', rapport.shape)
    print('Valeurs min/max  :', round(float(rapport.min()), 2), round(float(rapport.max()), 2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exportation d'une image

    Une image chargée avec `rioxarray` peut être réécrite sur le disque au format GeoTIFF avec `rio.to_raster`, en conservant sa géoréférence :
    """)
    return


@app.cell
def _(rxr):
    img_8 = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    img_rvb = img_8.sel(band=[1, 2, 3])
    img_rvb.rio.to_raster('RGBNIR_rvb.tif')
    # On ne conserve que les trois premières bandes visibles (bleu, vert, rouge)
    print('Image exportée :', tuple(img_rvb.sizes.values()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sauvegarde de tableaux NumPy

    L'export GeoTIFF conserve la géoréférence, mais on souhaite parfois simplement **mettre de côté un tableau intermédiaire** (un indice calculé, un masque) pour le recharger plus tard sans tout recalculer. NumPy propose pour cela un format binaire propre : `np.save` écrit un tableau unique (`.npy`), tandis que `np.savez_compressed` regroupe plusieurs tableaux nommés dans une archive compressée (`.npz`).
    """)
    return


@app.cell
def _(np, rxr):
    img_9 = rxr.open_rasterio('RGBNIR_of_S2A.tif').astype('float32')
    (_rouge, _pir) = (img_9.sel(band=3).to_numpy(), img_9.sel(band=4).to_numpy())
    _ndvi = (_pir - _rouge) / (_pir + _rouge)
    np.save('ndvi.npy', _ndvi)
    recharge = np.load('ndvi.npy')
    print('Rechargement identique :', np.allclose(_ndvi, recharge, equal_nan=True))
    np.savez_compressed('bandes.npz', rouge=_rouge, pir=_pir)
    archive = np.load('bandes.npz')
    print("Tableaux dans l'archive :", list(archive.keys()))
    print("Forme de 'pir' :", archive['pir'].shape)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Contrairement au GeoTIFF, ces fichiers ne contiennent **ni géoréférence ni métadonnée** : ils ne servent qu'à un stockage temporaire au sein d'une chaîne de traitement Python.

    ### Créer un raster à partir d'un tableau NumPy

    À l'inverse, on souhaite souvent écrire un **résultat** calculé (un indice, un masque, une classification) dans un GeoTIFF **géoréférencé**. Avec `rasterio`, on part du **profil** de l'image source — qui transporte le système de coordonnées, la transformation affine et les dimensions — que l'on adapte au produit dérivé (ici une seule bande en `float32`) :
    """)
    return


@app.cell
def _(rasterio):
    with rasterio.open('RGBNIR_of_S2A.tif') as _src:
        _rouge = _src.read(3).astype('float32')
        _pir = _src.read(4).astype('float32')
        profil = _src.profile
    _ndvi = (_pir - _rouge) / (_pir + _rouge)
    profil.update(count=1, dtype='float32')
    with rasterio.open('ndvi.tif', 'w', **profil) as _dst:
        _dst.write(_ndvi, 1)
    with rasterio.open('ndvi.tif') as check:
        print('CRS :', check.crs, '| bandes :', check.count, '| type :', check.dtypes[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lorsqu'il n'y a pas d'image source, on construit la géoréférence de toutes pièces. `from_origin` définit la transformation affine à partir du coin supérieur gauche et de la taille des pixels :
    """)
    return


@app.cell
def _(np, rasterio):
    from rasterio.transform import from_origin
    donnee = np.random.default_rng(0).random((100, 100)).astype('float32')
    # Tableau synthétique 100 x 100 et géoréférence construite manuellement
    transform = from_origin(500000, 5000000, 10, 10)
    with rasterio.open('synthetique.tif', 'w', driver='GTiff', height=100, width=100, count=1, dtype='float32', crs='EPSG:32618', transform=transform) as _dst:  # origine (x, y) + pixel de 10 m
        _dst.write(donnee, 1)
    print('Raster synthétique écrit :', donnee.shape, '| pixel 10 m, EPSG:32618')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Changement de projection cartographique

    Une image géoréférencée peut être reprojetée dans un autre système de coordonnées avec `rio.reproject`. `rioxarray` recalcule alors la grille de pixels et met à jour la géoréférence :
    """)
    return


@app.cell
def _(rxr):
    img_10 = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    print("CRS d'origine :", img_10.rio.crs)
    img_wgs84 = img_10.rio.reproject('EPSG:4326')
    print('Après reprojection :', img_wgs84.rio.crs)  # EPSG:32618 (UTM)
    # Reprojection en coordonnées géographiques (latitude/longitude)
    print('Nouvelle forme :', dict(img_wgs84.sizes))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Découpage et rééchantillonnage

    Deux opérations géospatiales complètent la reprojection. Le **découpage** (*clip*) extrait une emprise plus petite : `clip_box` prend une boîte englobante exprimée dans le système de coordonnées de l'image, tandis que `rio.clip` accepte une géométrie quelconque (le polygone d'une zone d'intérêt).
    """)
    return


@app.cell
def _(rxr):
    img_11 = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    (_minx, _miny, _maxx, _maxy) = img_11.rio.bounds()
    (cx, cy) = ((_minx + _maxx) / 2, (_miny + _maxy) / 2)
    (dx, dy) = ((_maxx - _minx) / 4, (_maxy - _miny) / 4)
    sous_image = img_11.rio.clip_box(cx - dx, cy - dy, cx + dx, cy + dy)
    print("Forme d'origine :", tuple(img_11.sizes.values()))
    print('Après découpage :', tuple(sous_image.sizes.values()))
    return (img_11,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le **rééchantillonnage** change la résolution spatiale. `rio.reproject` avec un paramètre `resolution` recalcule la grille de pixels ; on choisit une méthode d'agrégation adaptée — la **moyenne** pour réduire une image continue, le **plus proche voisin** pour une carte de classes :
    """)
    return


@app.cell
def _(img_11):
    from rasterio.enums import Resampling
    img_20m = img_11.rio.reproject(img_11.rio.crs, resolution=20, resampling=Resampling.average)
    # Passage de 10 m à 20 m par moyenne (sous-échantillonnage)
    print("Résolution d'origine     :", img_11.rio.resolution())
    print('Après rééchantillonnage  :', img_20m.rio.resolution(), '| forme :', tuple(img_20m.sizes.values()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```{=html}

    ```

    ## Données en géoscience

    Les données en géoscience contiennent beaucoup de métadonnées et peuvent être composées de différentes variables avec différentes unités, résolution, etc. Ces données sont aussi souvent étiquetées avec des dates sur certains axes, des coordonnées géographiques, des identifiants d'expériences, etc. Par conséquent, utiliser seulement des matrices est souvent incomplet [@xarray-2017].

    Calibration, unités, données manquantes, données éparses.

    ### xarray

    [Xarray](https://docs.xarray.dev/en/latest/getting-started-guide/why-xarray.html) est une puissante bibliothèque Python qui améliore les matrices multidimensionnelles de type numpy en y ajoutant des étiquettes, des dimensions, des coordonnées et des attributs. Elle fournit deux structures de données principales : `DataArray` (un tableau étiqueté à n dimensions) et `Dataset` (une base de données de tableaux multidimensionnels en mémoire).

    Les caractéristiques principales sont les suivantes:

    -   Opérations sur les dimensions nommées au lieu des numéros d'axe

    -   Sélection et opérations basées sur les étiquettes

    -   Diffusion automatique de tableaux basée sur les noms de dimensions

    -   Alignement de type base de données avec des étiquettes de coordonnées

    -   Suivi des métadonnées grâce à des dictionnaires Python

    #### Avantages

    La bibliothèque réduit considérablement la complexité du code et améliore la lisibilité du code pour les applications de calcul scientifique dans divers domaines, notamment la physique, l'astronomie, les géosciences, la bio-informatique, l'ingénierie, la finance et l'apprentissage profond. Elle s'intègre de manière transparente avec NumPy et pandas tout en restant compatible avec l'écosystème Python au sens large.

    #### DataArray

    Un tableau multidimensionnel étiqueté avec des propriétés clées :

    -   `valeurs` : Les données réelles du tableau

    -   `dims` : Dimensions nommées (par exemple, « x », « y », « z »)

    -   `coords` : Dictionnaire de tableaux étiquetant chaque point

    -   `attrs` : Stockage de métadonnées arbitraires

    -   `name` : Identifiant facultatif

    #### Dataset

    Un conteneur de type dictionnaire de `DataArrays` avec des dimensions alignées, contenant :

    -   `dims` : Dictionnaire de correspondance entre les noms des dimensions et les longueurs

    -   `data_vars` : Dictionnaire des variables du DataArray

    -   `coords` : Dictionnaire des variables de coordonnées

    -   `attrs` : Stockage des métadonnées

    Les principales différences sont les suivantes :

    -   `DataArray` contient un seul tableau avec des étiquettes

    -   Le `Dataset` contient plusieurs DataArrays alignés.

    Ces deux structures prennent en charge les opérations de type dictionnaire et les calculs de coordination tout en conservant les métadonnées.

    ![Organisation d'un Dataset dans xarray](images/xarray-dataset-diagram.png){#fig-xarray width="80%" fig-align="center"}

    #### Exemple avec rioxarray

    `rioxarray` ouvre un GeoTIFF directement comme un `DataArray` étiqueté : ses dimensions (`band`, `y`, `x`), ses coordonnées et sa géoréférence sont accessibles via l'accesseur `.rio`. On peut alors sélectionner une bande par son étiquette plutôt que par un numéro d'axe :
    """)
    return


@app.cell
def _(rxr):
    img_12 = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    print('Dimensions :', dict(img_12.sizes))
    print('Système de coordonnées :', img_12.rio.crs)
    print('Résolution (m) :', img_12.rio.resolution())
    _pir = img_12.sel(band=4)
    print('Bande PIR — forme :', _pir.shape, '| valeur maximale :', int(_pir.max()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Sélection et opérations par étiquette

    L'intérêt principal de `xarray` est de travailler par **étiquette** plutôt que par numéro d'axe. On sélectionne une bande par sa position (`isel`) ou par sa valeur (`sel`), et on peut même nommer les bandes pour les désigner explicitement :
    """)
    return


@app.cell
def _(rxr):
    img_13 = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    print('sel == isel :', bool((img_13.sel(band=4) == img_13.isel(band=3)).all()))
    img_n = img_13.assign_coords(band=['B', 'V', 'R', 'PIR'])
    print('Forme de la bande PIR :', img_n.sel(band='PIR').shape)
    (_minx, _miny, _maxx, _maxy) = img_13.rio.bounds()
    centre = img_13.sel(x=(_minx + _maxx) / 2, y=(_miny + _maxy) / 2, method='nearest')
    print('Valeurs au centre :', centre.values.tolist())
    return img_13, img_n


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les opérations respectent les **dimensions nommées** : on calcule la moyenne de chaque bande en réduisant selon `y` et `x`, et un calcul entre bandes (comme le NDVI) renvoie un `DataArray` qui **conserve les coordonnées et la géoréférence** :
    """)
    return


@app.cell
def _(img_13, img_n):
    print('Moyenne par bande :', img_13.mean(dim=['y', 'x']).values.round(1).tolist())
    _ndvi = (img_n.sel(band='PIR') - img_n.sel(band='R')) / (img_n.sel(band='PIR') + img_n.sel(band='R'))
    print('NDVI —', 'type :', type(_ndvi).__name__, '| dimensions :', _ndvi.dims)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```{=html}

    ```

    ```{=html}

    ```

    ## Points clés

    <div style="border:0.5px solid silver;border-left:.3rem solid #357cc0;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#eef5fb;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IB2cksfwAAA/pJREFUWIXNl01sVFUYhp/vzLSlDTbiTCmpoEQT5SemQQNaFw12ftCQrtSmKxLiAmUp0UTsz51prcYFKxM10ZCwarCuiAlMWyQuICkQ7KKlmmBiqDWlc52m1jKkvedz0TuVInTujNH6rr6595z3ec89d+45RwioV/p+rVv0wruNyi4LuwV2Abv922MK4wbGrOi48bzxjLPlVhBfKdagpTf3eEi9bpTDQcP6zic9CaXOd2z6uawATSduVm/8fcN7CO+CVAFLwA8CowqjqjKq4aXvvUWRsIQaRbRRoFGhEXgaCIPeQfl4/qH8h5fe3nY7cICkk92hhgH/EVuB/iXxus531t8IMviWnuknwxpKK7QDBhgTy2sZJzpRNEA8fWuPYIaBTcB1i7wx3BW5FAR8r2Jpt8mgXwI7gZxiY0Ndm689MEDCmWnAyAjwKMg3G+ydtjNOw0I58IJanamavKk6DXoQ+AWr+waduqm/BXj9tIZmr/92HtFmhW9z9ZEDV4/I4j+BF/Tc51qxado9J/ASKt89vPORlq/axMOfHwBmJ9xjiDYDk0u2sq0YPJlyE4l0diSRzo4kU25irbZXj8jikq1sAyYRbZ6dcI8V7hmAZK+7DegGVIXDF5zabNFhiX4K7AX2+vWauuDUZlU4DCjQ7TOXA1hLB1CDSP9QZ3SoKLxMDXVGhxDpB2p8JibWNxcR9BBgrWedwG4qbwGXgct+HUg+wwp6KNY3F5FEauYIIp8B5wa7oi+XObiSlEhnzwIHUH3TIJIEUNWv/wv4KpZIMgy6B4SQmItBDeK97gvi2UYR2a7IdhHNZTqjR4P2D4m5aFFA94RBtgLMbVz4KaiBWJKIHFWoB0WVT4L2LbA2zlcDstUAFYA+aLG4nwa7ImlFPlq5oIyUEsBnKVBhArS/r0TYUahDRksKcLcMsAhI04mb1SX1VN3nV7mzHdEfS+nqswRYNKCTALXzNU8ENWh1pmqAZ/yflxHRUgL8xdJJA3INwFP7YlCD2+ENzy5vOEApbf5Xs+SaQTUDICKvBjUQ6xUeP0ZLn/8VlmrG2IqqASAPJGLOzFNBDFRYCeCFbUkBfEYCyNuKqgEzfLzWVeQUYEzIBFoLROV5lt+iG8Pv10+XEsBnGEVODR+vdQ2AMfQCC6i2x3uy8QA+m1me/4ZE2u1KpmYCBY/3ZOOotgMLPnN5Oc50RG4CKUBEObnfmYuuZaSiZ/xSQOtCar4oBt/vzEVFOen//VI+s8wtmaq0fDD7WLjqTjbzzpY/isHX2pKt+6Z01ad40KmbUmwrkAM9mDeVV2Jpt6lceCztNuVN5RUfnlNs691w/pcHk4LW9Wi2ajTrdTi9V//W8fxPxif/DjJKAKcAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>À retenir</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ul>
    <li><strong>GDAL</strong> est la librairie de référence pour lire/écrire l’imagerie (elle rassemble les formats sous forme de <em>drivers</em>).</li>
    <li>Deux familles de formats : <strong>RVB</strong> (JPEG, PNG — au plus 3 bandes, 8 bits, peu de métadonnées) et <strong>géo-formats</strong> (GeoTIFF, NetCDF, HDF5 — multi-bandes, 16 bits/float, géoréférence). Le <strong>COG</strong> permet l’accès partiel à distance.</li>
    <li>Quatre caractéristiques à surveiller : la <strong>matrice de pixels</strong>, la <strong>dynamique</strong> (<code>dtype</code>), le <strong>nombre de bandes</strong> et les <strong>métadonnées / géoréférence</strong>.</li>
    <li>Consulter les <strong>métadonnées avant de lire</strong> (<code>rio info</code>, <code>gdalinfo</code>, ou les attributs de <code>rasterio</code>).</li>
    <li><code>OpenCV</code> lit les canaux en <strong>BGR</strong> : convertir en RGB (<code>cv2.cvtColor</code>) avant l’affichage.</li>
    <li>Une image est un <strong>tableau NumPy</strong> : indexation/découpage <code>[ligne, colonne, bande]</code> ; attention à la distinction <strong>vue vs copie</strong> (<code>np.shares_memory</code>, <code>.copy()</code>).</li>
    <li>L’<strong>indexation avancée</strong> (tableaux d’indices, <code>argmax(axis=…)</code>) sélectionne des éléments par condition ou construit des cartes dérivées (bande dominante) — elle renvoie une <strong>copie</strong>.</li>
    <li>Les <strong>tableaux masqués</strong> (<code>numpy.ma</code>) excluent les pixels non valides des statistiques : <code>masked_equal</code>/<code>masked_where</code>, puis <code>count()</code> et <code>compressed()</code>.</li>
    <li><code>np.save</code> (<code>.npy</code>) et <code>np.savez_compressed</code> (<code>.npz</code>) stockent des tableaux intermédiaires — <strong>sans</strong> géoréférence, au contraire du GeoTIFF.</li>
    <li><code>rioxarray</code>/<code>xarray</code> ajoutent <strong>dimensions nommées, coordonnées et géoréférence</strong> (accesseur <code>.rio</code>) : sélection par étiquette, reprojection (<code>rio.reproject</code>), export (<code>rio.to_raster</code>).</li>
    <li><code>rioxarray</code> <strong>découpe</strong> (<code>clip_box</code>/<code>clip</code>) et <strong>rééchantillonne</strong> (<code>reproject(resolution=…)</code>, méthode d’agrégation au choix) une image géoréférencée.</li>
    <li><code>xarray</code> sélectionne par <strong>étiquette</strong> (<code>sel</code>) ou position (<code>isel</code>), réduit sur des <strong>dimensions nommées</strong>, et ses calculs <strong>préservent la géoréférence</strong>.</li>
    <li><code>rasterio</code> <strong>écrit</strong> un tableau NumPy dans un GeoTIFF géoréférencé : hériter le <strong>profil</strong> de la source (CRS + transformation) ou le construire (<code>from_origin</code>), puis <code>dst.write</code>.</li>
    </ul>
    </div>
    </div>

    ## Exercices

    <div style="border:0.5px solid silver;border-left:.3rem solid #e34692;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fbe8f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADP0lEQVRYha2XT3LaMBjFf3SyD91rBnqC0BOUbuJl6AkwB9CUnKD0BCXxAeKcIGSpVZ0bwAkKEx8ATkAXemoUgm0I/WY8smVJ7/n78yS3ttstp1iZZF0g1WNhnC3Un6o/N87mVfNbpxAQ+Bw4j7p/qv0R9Y2qSHx4N7q3scBvBLwS8A/dj4ANcCePvLFTPVAAX4yzraivDxCFogcUIvrGE6cSSIE74KdxdlIzrpLEqSGY4V2d1g0yzs6BPnvCcRIB4+waWAKdMsna7yHR2m63aPL4COzCOFuUSZYDQ+DeOJseMjEKB8bZduv58ratjosjCMSltgJ68gZlkg20+KyGRIrPndEZMBD4AuiHhSom9oHfeszxXusAkzLJ1vhc6GjsChjI9bs2UFt8ALp6GDeAt4GpHtfG2SUvMf2O90YHrwk3us/3rJMDV8CTcXZ5VgUYTehroY66NmFh4+w8kuI2r6X4OzthLZNsjM+ZBfJCLQF99Qxfvwu87E5iT+l+ujMvuPgp6kuBX/qAf6Fu8kBP4I/G2UHD2NjGAhpH4He74IcQCNYtk6xdlSNBfoGlcuMLPsbzPeCvkrL1fHk7wSfQ1xC/ncXnvMRyhU/Wmd7tK+ERPjmHwL3aveBwmBL2tdACn4gPSjzwyXchgEf1TXVtmsAPImCcXRtnU+NsT0QCMPgcQQADkTjHV0QgXgkOr3MglUzmu7HWF8dJ2I1keBMBFPgan4lk3vSBsQeG+DJZikgAT4E/ejeMxob7eA/J8aE6Bx7wqlm7x8QErqPJ8aSJ2nuNAV/f18DneG9XuHrAN172i+WhBMJ2CYqtsrwDLLTbBVevjbPTqtgaZ2d1B5QqAkHVFsCFYlxE5OL2qkyyWZlk46ZzwFEEZEHFhvgSW6kvEBwFEvi8KE4h8YaAxKgLfMWLU3dH+3PgIz7OG5FM30tgrxQLsKiapPcz7W53+Lr/fwSaTGU64KValjXDezXvjidQJtkUfwAJ9lj360WDd44iIEUM4Nf4A0ilzB5iZ0BIsJSauMu6am+Ms9O6gZGa1hJsPV/edvFSC14DKs+FeHeG0lzWc/13mPmkM8J+AvovGOC30E7VwHfYEw2/5gB/AcMlhsUeVwFpAAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>À vous de jouer</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ol type="1">
    <li>Ouvrez <code>RGBNIR_of_S2A.tif</code> avec <code>rasterio</code> et affichez son nombre de bandes, son type de pixels, son système de coordonnées et sa résolution.
    </li>
    <li>À l’aide du découpage NumPy, extrayez une fenêtre de 100 × 100 pixels au centre d’une image et affichez-la.
    </li>
    <li>Vérifiez avec <code>np.shares_memory</code> si un découpage crée une <strong>vue</strong> ou une <strong>copie</strong>, puis forcez une copie avec <code>.copy()</code>.
    </li>
    <li>Reprojetez <code>RGBNIR_of_S2A.tif</code> en <code>EPSG:4326</code> avec <code>rioxarray</code>, puis sauvegardez le résultat en GeoTIFF avec <code>rio.to_raster</code>.
    </li>
    <li><em>(indexation avancée)</em> Sur <code>RGBNIR_of_S2A.tif</code>, construisez la carte de la <strong>bande dominante</strong> (<code>argmax</code>), puis affichez le pourcentage de pixels où le proche-infrarouge (indice 3) domine.
    </li>
    <li><em>(masquage)</em> Calculez le NDVI, masquez les pixels d’eau (NDVI < 0) avec <code>np.ma.masked_where</code>, puis comparez le NDVI moyen <strong>avec</strong> et <strong>sans</strong> masque.
    </li>
    <li><em>(sauvegarde)</em> Sauvegardez votre carte de NDVI dans un fichier <code>.npy</code>, rechargez-la, et vérifiez l’égalité avec <code>np.allclose</code> (option <code>equal_nan=True</code>).
    </li>
    <li><em>(découpage)</em> Découpez <code>RGBNIR_of_S2A.tif</code> sur son <strong>quart supérieur gauche</strong> avec <code>clip_box</code> et affichez la sous-image.
    </li>
    <li><em>(rééchantillonnage)</em> Rééchantillonnez l’image à <strong>30 m</strong> par moyenne (<code>reproject</code> avec <code>Resampling.average</code>) et comparez le nombre de pixels à l’original.
    </li>
    <li><em>(xarray)</em> Nommez les bandes (<code>B</code>, <code>V</code>, <code>R</code>, <code>PIR</code>), sélectionnez <code>PIR</code> par étiquette, puis calculez la moyenne de chaque bande sur les dimensions <code>y</code> et <code>x</code>.
    </li>
    <li><em>(écriture)</em> Calculez un masque d’eau (NDVI < 0), écrivez-le comme un GeoTIFF à une bande en réutilisant le profil de <code>RGBNIR_of_S2A.tif</code>, puis relisez-le pour vérifier son CRS.
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
    Chap01Quiz = Quiz("quiz/Chap01.yml", "Chap01")
    render_quizz(Chap01Quiz)
    return


if __name__ == "__main__":
    app.run()
