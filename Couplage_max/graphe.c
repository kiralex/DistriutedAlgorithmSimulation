#include "graphe.h"
#include "tasMax.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int ** creerMatrice(char * nomFichier, graphe_t * graphe) {
    FILE * file = NULL;
    file = fopen (nomFichier, "r");
    char string[100];
    int nbSommets = -1;
    int oriente = 1;
    int nbAretes = 0;
    int value = 1;
    int ** matrice;
    int i;
    int j;
    int source, dest, poids;

    /* on va sur le début des arêtes*/
    while(strcmp(string, "debutDefAretes")){
        fscanf(file, "%s", string);
        if(strcmp(string, "nSommets") == 0){
            fscanf(file, "%d", &nbSommets);
        }else if(strcmp(string, "value") == 0){
            fscanf(file, "%d", &value);
        }else if(strcmp(string, "oriente") == 0){
            fscanf(file, "%d", &oriente);
        }
    }

    matrice = (int**) malloc(sizeof(int*) * nbSommets );
    for(i = 0; i<nbSommets; i++){
        matrice[i] = (int*) malloc(sizeof(int) * nbSommets );
        for(j = 0; j<nbSommets; j++){
            int poids = 0;
            matrice[i][j] = poids;
        }
    }

    fscanf(file, "%s", string);
    while(strcmp(string, "finDefAretes")){
        source = atoi(string);
        fscanf(file, "%d", &dest);

        if(value == 1){
            fscanf(file, "%d", &poids);
            matrice[source][dest] = poids;
            if(oriente == 0)
            matrice[dest][source] = poids;
        }else{
            matrice[source][dest] = 1;
            if(oriente == 0)
            matrice[dest][source] = poids;
        }

        fscanf(file, "%s", string);

        nbAretes++;
    }

    graphe->nbAretes = nbAretes;

    fclose(file);
    return matrice;
}

void afficherMatrice(graphe_t * graphe){
    int i;
    int j;
    printf("\n");
    for(i = 0; i<graphe->nbSommets; i++){
        for(j = 0; j<graphe->nbSommets; j++){
            printf("%d \t", graphe->mat[i][j] );
        }
        printf("\n");
    }
}

arete_t * creerTableauAretes(graphe_t * graphe){
    int i;
    int j;
    arete_t * aretes;
    int comptAretes;
    int ** mat;
    int prise[graphe->nbSommets][graphe->nbSommets];

    for(i = 0; i < graphe->nbSommets; i++){
        for(j = 0; j < graphe->nbSommets; j++)
        prise[i][j] = 0;
    }

    aretes = (arete_t *) malloc(sizeof(arete_t ) * graphe->nbAretes);

    mat = graphe->mat;
    comptAretes = 0;

    for(i = 0; i < graphe->nbSommets; i++){
        for(j = 0; j < graphe->nbSommets; j++){
            if(mat[i][j] != 0 && prise[j][i] == 0){
                aretes[comptAretes].source = i;
                aretes[comptAretes].dest = j;
                aretes[comptAretes].poids = mat[i][j];

                prise[i][j] = 1;
                prise[j][i] = 1;
                comptAretes++;
            }
        }
    }

    return aretes;
}

graphe_t * lireGraphe(char * nomFichier){
    int i, source, dest, poids, nbAretes;
    FILE * file = NULL;
    file = fopen (nomFichier, "r");
    char string[100];

    graphe_t * graphe;

    graphe = (graphe_t *) malloc(sizeof(graphe_t));
    nbAretes = 0;

    /* on va sur le début des arêtes */
    while(strcmp(string, "debutDefAretes")){
        fscanf(file, "%s", string);
        if(!strcmp(string, "nSommets")){
            fscanf(file, "%d", &(graphe->nbSommets));
        }else if(!strcmp(string, "oriente")){
            fscanf(file, "%d", &(graphe->oriente));
        }else if(!strcmp(string, "value")){
            fscanf(file, "%d", &(graphe->value));
        }else if(!strcmp(string, "complet")){
            fscanf(file, "%d", &(graphe->complet));
        }
    }

    graphe->mat = creerMatrice(nomFichier, graphe);

    graphe->aretes = creerTableauAretes(graphe);

    fclose(file);

    return graphe;
}

graphe_t * lireGrapheTsp(char * nomFichier){
    int i, source, dest, poids, nbAretes;
    FILE * file = NULL;
    file = fopen (nomFichier, "r");
    char string[100];

    graphe_t * graphe;

    graphe = (graphe_t *) malloc(sizeof(graphe_t));
    nbAretes = 0;

    /* on va sur le début des arêtes */
    while(strcmp(string, "debutDefAretes")){
        fscanf(file, "%s", string);
        if(!strcmp(string, "nSommets")){
            fscanf(file, "%d", &(graphe->nbSommets));
        }else if(!strcmp(string, "oriente")){
            fscanf(file, "%d", &(graphe->oriente));
        }else if(!strcmp(string, "value")){
            fscanf(file, "%d", &(graphe->value));
        }else if(!strcmp(string, "complet")){
            fscanf(file, "%d", &(graphe->complet));
        }
    }

    graphe->mat = creerMatrice(nomFichier, graphe);

    graphe->aretes = creerTableauAretes(graphe);

    fclose(file);

    return graphe;
}

void detruireGraphe(graphe_t * graphe){
	int i;
	if(graphe->mat != NULL){
		for(i = 0; i<graphe->nbSommets; i++){
			if(graphe->mat[i] != NULL)
			free(graphe->mat[i]);
		}
	}

	free(graphe->mat);
    free(graphe->aretes);
    free(graphe);
}

void afficherAretes(arete_t * tab, int taille){
    int i;
    for(i = 0; i < taille; i++){
        printf("%d %d : %d \n", tab[i].source, tab[i].dest, tab[i].poids);
    }
}

void afficherACPM(arete_t * tab, int taille){
    int i;
    int somme;

    somme = 0;

    for(i = 0; i < taille; i++){
        printf("%d %d\n", tab[i].source, tab[i].dest);
        somme += tab[i].poids;
    }
    printf("Longueur de l'arbre : %d\n", somme);
}

arete_t * kruskal(graphe_t * graphe, int taille){
    int composante[graphe->nbSommets];
    int i;
    int cptArbre;
    int cptAretes;
    arete_t temp;
    arete_t * arbre;
    int ind;

    arbre = (arete_t * ) malloc(sizeof(arete_t) * taille);
    cptArbre = 0;
    cptAretes = 0;

    triParTasMax(graphe->aretes, graphe->nbAretes);
    for(i = 0; i < graphe->nbSommets; i++){
        composante[i] = i;
    }

    while(cptArbre < taille){
        temp = graphe->aretes[cptAretes];
        cptAretes ++;
        if(composante[temp.source] != composante[temp.dest]){
            arbre[cptArbre] = temp;
            cptArbre ++;
            ind = composante[temp.dest];
            for(i = 0; i < graphe->nbSommets; i++){
                if(composante[i] == ind){
                    composante[i] = composante[temp.source];
                }
            }

        }
    }

    return arbre;
}
