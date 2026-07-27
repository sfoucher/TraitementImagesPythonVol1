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
    # Transformations spectrales

    ## Préambule

    Assurez-vous de lire ce préambule avant d'exécuter le reste du notebook.

    ### Objectifs

    Dans ce chapitre, nous abordons l'exploitation de la dimension spectrale des images satellites. Ce chapitre est aussi disponible sous la forme d'un notebook Python:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/03-TransformationSpectrales.ipynb)

    ### Librairies

    Les librairies qui vont être explorées dans ce chapitre sont les suivantes:

    -   [SciPy](https://scipy.org/)

    -   [NumPy](https://numpy.org/)

    -   [spyindex](https://github.com/awesome-spectral-indices/spyndex)

    -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

    -   [Xarray](https://docs.xarray.dev/en/stable/)

    -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

    Dans l'environnement Google Colab, seul `rioxarray` doit être installé.
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # !pip install -qU matplotlib rioxarray xrscipy scikit-image pyarrow spyndex
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifiez les importations:
    """)
    return


@app.cell
def _():
    import numpy as np
    import rioxarray as rxr
    from scipy import signal
    import xarray as xr
    import xrscipy
    import spyndex
    import rasterio as rio

    return np, rxr, spyndex


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
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6O3L_abOfU7h94K22At8qtBuLMGErwo', output= 'sentinel2.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1dM6IVqjba6GHwTLmI7CpX8GP2z5txUq6', output= 'SAR.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1aAq7crc_LoaLC3kG3HkQ6Fv5JfG0mswg', output= 'carte.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1iCZNYTv0qEZRzPhe22nPdpV4Ks7NsY3b', output= 'ASCIIdata_splib07b_rsSentinel2.zip')
    # !unzip -q ASCIIdata_splib07b_rsSentinel2.zip
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
    with rxr.open_rasterio('sentinel2.tif', mask_and_scale= True) as img_s2:
        print(img_s2)
    with rxr.open_rasterio('carte.tif', mask_and_scale= True) as img_carte:
        print(img_carte)
    return img_carte, img_s2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Qu'est ce que l'information spectrale?

    L'information spectrale touche à l'exploitation de la dimension spectrale des images (c.à.d le long des bandes spectrales de l'image). La taille de cette dimension spectrale dépend du type de capteurs considéré. Un capteur à très haute résolution spectrale par exemple aura très peu de bandes (4 ou 5). Un capteur multispectral pourra contenir une quinzaine de bande. À l'autre extrême, on trouvera les capteurs hyperspectraux qui peuvent contenir des centaines de bandes spectrales.

    ![Positions des bandes spectrales pour quelques capteurs ([source](https://landsat.gsfc.nasa.gov/article/sentinel-2a-launches-our-compliments-our-complements/))](images/Landsat.v.Sentinel-2-1.png){fig-align="center" width="6in"}

    Pour une surface donnée, la forme des valeurs le long de l'axe spectrale caractérise le type de matériau observé ainsi que son état. On parle souvent alors de signature spectrale. On peut voir celle-ci comme une généralisation de la couleur d'un matériau au delà des bandes visibles du spectre. L'exploitation de ces signatures spectrales est probablement un des principes les plus importants en télédétection qui le distingue de la vison par ordinateur. L'[USGS](https://www.sciencebase.gov/catalog/item/586e8c88e4b0f5ce109fccae) maintient une base de données spectrales acquises en laboratoire [@Kokaly-2017]. On peut observer sur la figure ci-dessous comment la forme et l'amplitude de trois signatures différentes peut changer en fonction du type de surface.
    """)
    return


app._unparsable_cell(
    r"""
    HOME= !pwd
    with open(f'{HOME[0]}/ASCIIdata_splib07b_rsSentinel2/S07SNTL2_Wavelengths_Sentinel2_(13_bands)_microns.txt','r') as f:
        # Read all lines, skipping the first line
        lines = f.read().split('\n')[1:]  
        # Filter out empty or whitespace-only lines before converting to float
        band_pos = [float(s.replace(' ', ''))*1000 for s in lines if s.strip()]

    with open('ASCIIdata_splib07b_rsSentinel2/ChapterV_Vegetation/S07SNTL2_Rangeland_C03-004_S08%_G27%_ASDFRa_AREF.txt','r') as f:
        lines = f.read().split('\n')[1:]  
        LawnGrass = [float(s.replace(' ', '')) for s in lines if s.strip()]

    with open('ASCIIdata_splib07b_rsSentinel2/ChapterL_Liquids/S07SNTL2_Water+Montmor_SWy-2+0.50g-l_ASDFRa_AREF.txt','r') as f:
        lines = f.read().split('\n')[1:]  
        Water = [float(s.replace(' ', '')) for s in lines if s.strip()]


    with open('ASCIIdata_splib07b_rsSentinel2/ChapterA_ArtificialMaterials/S07SNTL2_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt','r') as f:
        lines = f.read().split('\n')[1:]  
        Concrete = [float(s.replace(' ', '')) for s in lines if s.strip()]
    fig, ax= plt.subplots(figsize = (8,5))
    plt.plot(band_pos,LawnGrass, 'g.-')
    plt.plot(band_pos,Water, 'b.-')
    plt.plot(band_pos,Concrete, 'y.-')
    plt.legend(['Prairie','Eau','Béton'])
    ax.grid('on')
    ax.set_xlabel('Longueur d\'onde (nm)')
    ax.set_ylabel('Réflectance')
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Indices spectraux

    Il existe une vaste littérature sur les indices spectraux, le choix d'un indice plutôt qu'un autre dépend fortement de l'application visée, nous allons simplement couvrir les principes de base ici. Le principe d'un indice spectral consiste à mettre en valeur certaines caractéristiques saillantes du spectre comme des pentes, des gradients, etc.

    La librairie Python [Awesome Spectral Indices](https://awesome-ee-spectral-indices.readthedocs.io/en/latest/) maintient une liste de plus de 200 indices spectraux (radar et optiques). La liste complète est affichable avec la commande suivante:
    """)
    return


@app.cell
def _(spyndex):
    spyndex.indices
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le détail d'un indice particulier, par exemple le \`NDVI\`, est aussi affichable:
    """)
    return


@app.cell
def _(spyndex):
    spyndex.indices["NDVI"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `spyndex` pré-suppose une nomenclature prédéfinie des [bandes](https://awesome-ee-spectral-indices.readthedocs.io/en/latest/#expressions), on peut voir la correspondance sur le tableau ci-dessous:
    """)
    return


@app.cell
def _(spyndex):
    spyndex.bands
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Index | Noms | Spyndex | Noms                      |
    |-------|------|---------|---------------------------|
    | 1     | B01  | A       | Aérosol                   |
    | 2     | B02  | B       | Bleu                      |
    | 3     | B03  | G       | Vert                      |
    | 4     | B04  | R       | Rouge                     |
    | 5     | B05  | RE1     | Red edge 1                |
    | 6     | B06  | RE2     | Red edge 2                |
    | 7     | B07  | RE3     | Red edge 3                |
    | 8     | B08  | N       | Proche-infrarouge 1       |
    | 9     | B08A | N2      | Proche-infrarouge 2       |
    | 10    | B09  | WV      | Vapeur d'eau              |
    | 11    | B11  | S1      | Infra-rouge onde courte 1 |
    | 12    | B12  | S2      | Infra-rouge onde courte 2 |

    : Noms des bandes Sentinel-2

    Deux options sont possibles, on peut soit renommer les noms des bandes avec `xarray` ou "mapper" les noms vers les noms appropriés. Regardons les dimensions de notre jeux de données:
    """)
    return


@app.cell
def _(img_s2):
    img_s2.dims
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut simplement changer les index (`coords`) de la dimension `band`:
    """)
    return


@app.cell
def _(img_s2):
    sentinel2_bands = ['A', 'B', 'G', 'R', 'RE1', 'RE2', 'RE3', 'N', 'N2', 'WV', 'S1', 'S2']
    img_s2_1 = img_s2.sel(band=list(range(1, 13))).assign_coords({'band': sentinel2_bands})
    img_s2_1 = img_s2_1 / 10000  # normalisation en réflectance
    return img_s2_1, sentinel2_bands


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le **NDVI** (*Normalized Difference Vegetation Index*) est l'indice le plus connu. Il se calcule à partir des bandes rouge ($R$) et proche-infrarouge ($N$) :

    $$ NDVI = \frac{N - R}{N + R} $$ {#eq-ndvi}

    La végétation en bonne santé réfléchit fortement le proche-infrarouge et absorbe le rouge : son NDVI est donc élevé (proche de $1$), alors que l'eau, le sol nu ou le bâti donnent des valeurs faibles, voire négatives. Le `SAVI` ajoute un facteur de correction du sol ($L$) pour limiter l'influence du sol visible à travers un couvert végétal clairsemé.

    L'`EVI` (*Enhanced Vegetation Index*) va plus loin en corrigeant également l'effet de l'atmosphère à l'aide de la bande bleue ($B$), ce qui limite la saturation du NDVI sur la végétation dense [@Jensen2016] :

    $$ EVI = G \times \frac{N - R}{N + C_1 \times R - C_2 \times B + L} $$ {#eq-evi}

    avec les constantes usuelles $G=2{,}5$ (gain), $C_1=6$ et $C_2=7{,}5$ (coefficients de correction atmosphérique appliqués respectivement au rouge et au bleu) et $L=1$ (ajustement du sol). On calcule ces trois indices ci-dessous avec `spyndex.computeIndex` :
    """)
    return


@app.cell
def _(img_s2_1, np, plt, spyndex):
    from rasterio import plot
    idx = spyndex.computeIndex(index=['NDVI', 'SAVI'], params={'N': img_s2_1.sel(band='N'), 'R': img_s2_1.sel(band='R'), 'L': 0.5})
    evi = spyndex.computeIndex(index=['EVI'], params={'N': img_s2_1.sel(band='N'), 'R': img_s2_1.sel(band='R'), 'B': img_s2_1.sel(band='B'), 'g': 2.5, 'C1': 6, 'C2': 7.5, 'L': 1})
    (fig, ax) = plt.subplots(2, 2, figsize=(9, 9))
    [a.axis('off') for a in ax.flatten()]
    plot.show(img_s2_1.sel(band=['R', 'G', 'B']).data / 0.3, ax=ax[0, 0], title='RGB')
    plot.show(idx.sel(index='NDVI'), ax=ax[0, 1], title='NDVI')
    plot.show(idx.sel(index='SAVI'), ax=ax[1, 0], title='SAVI')
    (evi_lo, evi_hi) = np.nanpercentile(evi, [2, 98])
    plot.show(evi, vmin=evi_lo, vmax=evi_hi, ax=ax[1, 1], title='EVI')
    # Plot the indices (et l'image RGB pour comparaison)
    plt.tight_layout()  # étirement 2-98 %
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut vérifier l'utilité des indices en vérifiant leur séparabilité pour certaines classes d'intérêts. Nous reprenons ici l'exemple de la section [@sec-05.02.02] pour vérifier l'utilité des indices `NDVI`, `NDWI` et `NDBI`:
    """)
    return


@app.cell
def _(img_carte, np, sentinel2_bands):
    from matplotlib.colors import ListedColormap
    import rasterio
    import geopandas
    from shapely.geometry import Point
    import pandas as pd
    couleurs_classes = {'NoData': 'black', 'Commercial': 'yellow', 'Nuages': 'lightgrey', 'Foret': 'darkgreen', 'Faible_végétation': 'green', 'Sol_nu': 'saddlebrown', 'Roche': 'dimgray', 'Route': 'red', 'Urbain': 'orange', 'Eau': 'blue', 'Tourbe': 'salmon', 'Végétation éparse': 'darkgoldenrod', 'Roche avec végétation': 'darkseagreen'}
    nom_classes = [*couleurs_classes.keys()]
    couleurs_classes = [*couleurs_classes.values()]
    cmap_classes = ListedColormap(couleurs_classes)
    img_carte_1 = img_carte.squeeze()
    class_counts = np.unique(img_carte_1.data, return_counts=True)
    sampled_points = []
    class_labels = []
    for class_label in range(1, 13):
        class_pixels = np.argwhere(img_carte_1.data == class_label)
        n_samples = min(100, len(class_pixels))
    # Liste vide des points échantillonnées
        np.random.seed(0)
        sampled_indices = np.random.choice(len(class_pixels), n_samples, replace=False)  # contient les étiquettes des classes
        sampled_pixels = class_pixels[sampled_indices]  # pour chacune des 12 classes
        sampled_points.extend(sampled_pixels)  # On cherche tous les pixels pour cette étiquette
        class_labels.extend(np.array([class_label] * n_samples)[:, np.newaxis])
    sampled_points = np.array(sampled_points)
    class_labels = np.array(class_labels)  # On se limite à 100 pixels par classe
    transformer = rasterio.transform.AffineTransformer(img_carte_1.rio.transform())
    transform_sampled_points = transformer.xy(sampled_points[:, 0], sampled_points[:, 1])
    points = [Point(xy) for xy in zip(transform_sampled_points[0], transform_sampled_points[1])]  # On les choisit les positions aléatoirement
    gdf = geopandas.GeoDataFrame(range(1, len(points) + 1), geometry=points, crs=img_carte_1.rio.crs)  # ceci permet de répliquer le tirage aléatoire
    coord_list = [(x, y) for (x, y) in zip(gdf['geometry'].x, gdf['geometry'].y)]
    with rasterio.open('sentinel2.tif') as src:
        values = [x[0:13] / 10000.0 for x in src.sample(coord_list)]  # On prends les positions en lignes, colonnes
    for (b, band) in enumerate(sentinel2_bands):
        gdf[band] = [x[b] for x in values]
    # Conversion en NumPy array
    # On peut naviguer les points à l'aide de la géoréférence
    gdf['class'] = class_labels  # On ajoute les points à la liste
    return couleurs_classes, gdf, nom_classes, pd


@app.cell
def _(couleurs_classes, gdf, nom_classes, pd, plt, spyndex):
    import seaborn as sns
    class_selected = [1, 3, 9]
    df = pd.concat([gdf[gdf['class'] == c] for c in class_selected], ignore_index=True)
    # On sélectionne trois classes
    idx_1 = spyndex.computeIndex(index=['NDVI', 'NDWI', 'NDBI'], params={'N': df['N'], 'R': df['R'], 'G': df['G'], 'S1': df['S1']})
    idx_1['Land Cover'] = [nom_classes[l] for l in df['class'].tolist()]
    colors = [couleurs_classes[c] for c in class_selected]
    # Compute the desired spectral indices
    plt.figure(figsize=(15, 15))
    g = sns.PairGrid(idx_1, hue='Land Cover', palette=sns.color_palette(colors))
    g.map_lower(sns.scatterplot)
    g.map_upper(sns.kdeplot, fill=True, alpha=0.5)
    g.map_diag(sns.kdeplot, fill=True)
    g.add_legend()
    # Plot a pairplot to check the indices behaviour
    plt.show()  # Add Land Cover to DataFrame
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Réduction de dimension

    La réduction de dimension vise à ne retenir que l'information principale d'un jeu de données. L'objectif est parfois d'éliminer le bruit d'un capteur ou de faciliter la visualisation en ne retenant que 3 bandes principales. Le degré d'information est souvent mesuré par la variance d'une bande, c'est-à-dire son contraste. L'analyse en composantes principales vise alors à ranger l'information contenue dans une image en ordre de variance décroissante.

    ### Transformations linéaires et produit matriciel

    Une **transformation linéaire de bandes** consiste à produire de nouvelles bandes par sommes pondérées des bandes d'origine. Chaque pixel étant un vecteur de valeurs (une par bande), appliquer les mêmes poids à tous les pixels revient à un simple **produit matriciel** (opérateur `@` dans NumPy). Sur un petit exemple, une matrice `M` transforme 2 bandes en 2 nouvelles combinaisons :
    """)
    return


@app.cell
def _(np):
    pixels = np.array([[10.0, 40.0], [20.0, 10.0], [5.0, 25.0]])
    M = np.array([[0.5, 0.5], [1.0, -1.0]])
    # 3 pixels (en lignes), 2 bandes (en colonnes)
    # Deux combinaisons de bandes définies par une matrice (2 sorties x 2 bandes)
    print(pixels @ M.T)  # moyenne des deux bandes  # différence des deux bandes  # produit matriciel : (3 pixels x 2 sorties)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'analyse en composantes principales pousse cette idée plus loin : au lieu de choisir les poids à la main, elle les **apprend des données** pour maximiser la variance retenue.

    ### Transformation Tasseled Cap (Kauth-Thomas)

    Un exemple historique et toujours largement utilisé de transformation linéaire à coefficients **fixes** (plutôt qu'appris comme en ACP) est la transformation *Tasseled Cap* (ou de Kauth-Thomas), qui combine les bandes réflectives en trois composantes interprétables physiquement : la **brillance** (*brightness*, liée au sol), la **verdure** (*greenness*, liée à la végétation) et l'**humidité** (*wetness*, liée à l'eau du sol et de la végétation) [@Jensen2016; @richards2022remote; @Schowengerdt2007]. Les coefficients ci-dessous, établis par Crist (1985) pour les bandes réflectives de Landsat TM, sont appliqués ici, à titre d'illustration, aux bandes analogues de Sentinel-2 (`B`, `G`, `R`, `N`, `S1`, `S2`) ; chaque capteur possède en pratique ses propres coefficients publiés.
    """)
    return


@app.cell
def _(img_s2_1, np, plt):
    # Coefficients de Crist (1985) pour les bandes réflectives Landsat TM (B, G, R, N, S1, S2),
    # appliqués ici à titre d'illustration aux bandes analogues de Sentinel-2
    tc_coeffs = np.array([[0.3037, 0.2793, 0.4743, 0.5585, 0.5082, 0.1863], [-0.2848, -0.2435, -0.5436, 0.7243, 0.084, -0.18], [0.1509, 0.1973, 0.3279, 0.3406, -0.7112, -0.4572]])
    tc_bands = ['B', 'G', 'R', 'N', 'S1', 'S2']  # Brightness
    X_tc = img_s2_1.sel(band=tc_bands).data.reshape(len(tc_bands), -1)  # Greenness
    (brightness, greenness, wetness) = (tc_coeffs @ X_tc).reshape(3, *img_s2_1.shape[1:])  # Wetness
    (fig_1, ax_1) = plt.subplots(ncols=3, figsize=(10, 4))
    for (a, im, title) in zip(ax_1, (brightness, greenness, wetness), ('Brightness', 'Greenness', 'Wetness')):
        a.imshow(im)
        a.set_title(title)  # (6, pixels)
        a.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Contrairement à l'ACP, ces coefficients ne dépendent pas de l'image : ils permettent donc de comparer directement les composantes entre plusieurs scènes, ce que l'ACP (dont les axes sont recalculés à chaque image) ne permet pas.

    ### Analyse en composantes principales (ACP)

    L'analyse en composantes principales (ACP) est probablement la plus employée. En théorie, l'ACP n'est valide que sur des données gaussiennes, c'est-à-dire que le nuage de points des données a la forme d'une ellipse à $N$ dimensions. Cette ellipse est caractérisée par des directions principales (grand axe versus petit axe). La première composante est celle du grand axe de l'ellipse, pour laquelle la donnée présente le maximum de variation. L'ACP est une décomposition **linéaire** : les composantes principales sont des sommes pondérées des valeurs originales.

    Concrètement, on aplatit le cube en une table `pixels × bandes`, on **centre** les données, puis on diagonalise la **matrice de covariance** (`np.linalg.eigh`, adaptée aux matrices symétriques). Les vecteurs propres donnent les directions principales, et les valeurs propres la variance portée par chacune :
    """)
    return


@app.cell
def _(img_s2_1, np):
    # On aplatit le cube (bandes x pixels) en une table (pixels x bandes)
    cube = img_s2_1.to_numpy()  # (12, lignes, colonnes), réflectance
    (B, H, W) = cube.shape
    X = cube.reshape(B, H * W).T  # (pixels, bandes)
    X_c = X - X.mean(axis=0)  # centrage : moyenne nulle par bande
    cov = np.cov(X_c, rowvar=False)
    # Matrice de covariance (12 x 12), puis vecteurs et valeurs propres
    (valeurs, vecteurs) = np.linalg.eigh(cov)
    ordre = np.argsort(valeurs)[::-1]  # eigh : matrice symétrique
    (valeurs, vecteurs) = (valeurs[ordre], vecteurs[:, ordre])  # variance décroissante
    ratio = valeurs / valeurs.sum()
    print('Variance expliquée (5 premières) :', ratio[:5].round(3))
    print('Cumul des 3 premières composantes :', round(ratio[:3].sum(), 3))
    return B, H, W, X, X_c, ratio, vecteurs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La projection des pixels sur les vecteurs propres est, elle aussi, un **produit matriciel**. On récupère ensuite un cube de composantes rangées par variance décroissante :
    """)
    return


@app.cell
def _(B, H, W, X_c, vecteurs):
    # Projection des pixels sur les directions principales
    composantes = (X_c @ vecteurs).T.reshape(B, H, W)   # (composantes, lignes, colonnes)
    print("Cube des composantes :", composantes.shape)
    return (composantes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les trois premières composantes concentrent l'essentiel de l'information (ici plus de 98 % de la variance). On les visualise sous forme d'un composé coloré, à côté des valeurs propres normalisées (*scree plot* en anglais) des variances :
    """)
    return


@app.cell
def _(B, composantes, np, plt, ratio):
    (fig_2, ax_2) = plt.subplots(1, 2, figsize=(10, 4))
    ax_2[0].bar(range(1, B + 1), ratio)
    ax_2[0].set_xlabel('Composante')
    ax_2[0].set_ylabel('Variance expliquée')
    ax_2[0].set_title('Valeurs propres (scree plot)')
    # Composé coloré des 3 premières composantes (étirement min-max par composante)

    def etirer(x):
        return (x - x.min()) / (x.max() - x.min())
    rgb = np.dstack([etirer(composantes[i]) for i in range(3)])
    ax_2[1].imshow(rgb)
    ax_2[1].set_title('Composantes 1-2-3 (RGB)')
    ax_2[1].axis('off')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La première composante ressemble souvent à une image de brillance globale, tandis que les suivantes isolent des contrastes plus fins (végétation, eau). La même décomposition s'obtient de façon numériquement plus stable par **décomposition en valeurs singulières** (`np.linalg.svd`) appliquée aux données centrées. La réduction de dimension prépare aussi la classification (@sec-chap05) en concentrant l'information utile dans quelques bandes.

    ### Reconstruction et erreur de compression

    Conserver seulement les $k$ premières composantes revient à **compresser** l'image : la reconstruction s'obtient en projetant sur les $k$ premiers vecteurs propres, puis en revenant dans l'espace original (l'opération inverse du produit matriciel de projection). On peut alors mesurer l'erreur de reconstruction (RMSE) en fonction de $k$ [@richards2022remote] :
    """)
    return


@app.cell
def _(B, X, composantes, np, plt, vecteurs):
    def erreur_reconstruction(k):
        proj_k = composantes[:k].reshape(k, -1).T  # (pixels, k)
        X_approx = proj_k @ vecteurs[:, :k].T + X.mean(axis=0)  # (pixels, bandes)
        return np.sqrt(np.mean((X - X_approx) ** 2))  # RMSE
    erreurs = [erreur_reconstruction(k) for k in range(1, B + 1)]
    (fig_3, ax_3) = plt.subplots(figsize=(5, 4))
    ax_3.plot(range(1, B + 1), erreurs, 'o-')
    ax_3.set_xlabel('Nombre de composantes conservées (k)')
    ax_3.set_ylabel('Erreur de reconstruction (RMSE)')
    ax_3.grid(True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'erreur diminue rapidement avec le nombre de composantes conservées, ce qui confirme que l'essentiel de l'information est capté par les toutes premières composantes — ici, une poignée de composantes suffit à approcher fidèlement les 12 bandes d'origine.

    L'ACP suppose une distribution gaussienne des données et ne retient que des combinaisons linéaires classées par variance décroissante, ce qui n'est pas toujours le critère le plus pertinent. La transformation en **fraction de bruit minimum/maximum** (*Minimum/Maximum Noise Fraction*, MNF) classe plutôt les composantes par rapport signal-sur-bruit décroissant, ce qui la rend préférable pour les images hyperspectrales bruitées [@richards2022remote]. L'**analyse en composantes indépendantes** (ICA) relâche quant à elle l'hypothèse gaussienne en recherchant des composantes statistiquement indépendantes plutôt que simplement décorrélées.

    ## Points clés

    ## Exercices

    **À vous de jouer**

    1.  Calculez le **NDWI** (eau) et le **NDBI** (bâti) avec `spyndex` sur `img_s2`, puis affichez-les côte à côte avec le NDVI.

    2.  Comparez les **signatures spectrales** de deux surfaces supplémentaires de la base USGS (p. ex. neige, végétation sèche) sur les bandes Sentinel-2.

    3.  Parcourez `spyndex.indices`, choisissez un indice adapté à l'eau ou aux sols, identifiez les bandes qu'il requiert, et calculez-le sur `img_s2`.

    4.  Renommez les bandes de `img_s2` avec la nomenclature `spyndex` et vérifiez le résultat avec `img_s2.coords['band']`.

    5.  *(produit matriciel)* Construisez une matrice `2 × 4` transformant les 4 bandes de `RGBNIR_of_S2A.tif` en deux nouvelles bandes (brillance moyenne et différence PIR - Rouge) à l'aide de l'opérateur `@`, puis affichez-les.

    6.  *(ACP)* Réalisez l'ACP de `img_s2`, affichez la **variance expliquée** par chaque composante (éboulis), et vérifiez combien de composantes sont nécessaires pour atteindre 95 % de variance cumulée.

    7.  *(Tasseled Cap)* Appliquez la transformation Tasseled Cap à une autre combinaison de bandes (p. ex. en remplaçant `S1` par `RE1`) et comparez visuellement les composantes obtenues à celles de la section.

    8.  *(reconstruction)* À partir de l'ACP de `img_s2`, déterminez le nombre minimal de composantes nécessaires pour obtenir une erreur de reconstruction (RMSE) inférieure à 0.01.

    ## Quiz

    ::: {.content-visible when-profile="production"}
    Utilisez la version html.
    :::
    """)
    return


@app.cell
def _():
    from code_complementaire.quizz_functions import Quiz, render_quizz
    Chap03Quiz = Quiz("quiz/Chap03.yml", "Chap03")
    render_quizz(Chap03Quiz)
    #import os
    #output_format = os.environ.get("QUARTO_PROFILE")
    #print(output_format)
    return


if __name__ == "__main__":
    app.run()
