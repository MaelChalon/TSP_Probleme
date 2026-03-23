# Compte-rendu d'implementation

## Objectif

L'objectif etait de resoudre une instance du probleme du voyageur de commerce (TSP) a l'aide d'un algorithme genetique. L'instance est recuperee via le client HTTP, puis convertie en liste de villes `City`.

## Representation d'une solution

Une solution est representee par une liste d'objets `City`. Chaque individu de la population correspond donc a une permutation complete des villes. Ce choix garantit que chaque ville apparait exactement une fois dans chaque tour.

## Evaluation

La qualite d'un individu est evaluee par la distance totale du circuit. Le calcul est realise avec la formule de Haversine, ce qui permet de tenir compte de la courbure de la Terre et d'obtenir une distance en kilometres. Le circuit est ferme, c'est-a-dire que la distance entre la derniere ville et la premiere est aussi ajoutee.

## Operateurs utilises

### Initialisation

La population initiale est construite aleatoirement. Chaque individu est cree par permutation aleatoire de la liste des villes.

### Selection

La selection retenue est une selection par roulette. Comme il s'agit d'un probleme de minimisation, les poids sont calculés à partir de l'inverse de la distance :

`poids = 1 / distance`

Ainsi, plus un individu est bon, plus il a de chances d'etre selectionne. A chaque generation, on conserve la moitie de la population par cette methode.

### Mutation

Trois operateurs de mutation ont ete implementes :

- `swap` : echange de deux villes aleatoires ;
- `inversion` : inversion de l'ordre des villes sur un segment aleatoire ;
- `insertion` : retrait d'une ville puis reinsertion a une autre position.

### Regeneration de population

La nouvelle population est construite de la maniere suivante :

- les individus selectionnes sont conserves ;
- on choisit ensuite aleatoirement un parent parmi cette selection ;
- on clone ce parent ;
- avec une certaine probabilite, on lui applique une mutation ;
- on repete jusqu'a retrouver la taille de population souhaitee.

Ce choix permet de conserver les meilleurs individus tout en introduisant de la diversification.

## Parametres retenus

Les principaux parametres utilises dans le code actuel sont :

- taille de population : `100` ;
- nombre d'iterations : `100` ;
- taille de la selection a chaque generation : la moitie de la population ;
- taux de mutation par defaut : `0.5` ;
- operateur de mutation par defaut : `swap`.

Ces parametres ont ete choisis pour obtenir un compromis simple entre cout de calcul et qualite des solutions.

## Conclusion

L'algorithme mis en place repose sur une structure genetique classique : initialisation aleatoire, evaluation par distance, selection par roulette, puis regeneration par mutation. L'implementation est simple, lisible et deja suffisante pour produire des solutions valides. Les operateurs supplementaires prepares dans le code permettent d'envisager facilement des essais comparatifs pour ameliorer les performances.
