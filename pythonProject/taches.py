import argparse
import os
import cmd
from termcolor import colored

FichierTaches = 'Taches.txt'

"""
Récupère la liste de toutes les tâches de chaque personne dans le fichier texte 'Taches.txt'.
"""


def recup_taches():
    listeTaches = {}
    if os.path.exists(FichierTaches):
        with open(FichierTaches, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    personne, tache, statut = line.split(',')
                    if personne not in listeTaches:
                        listeTaches[personne] = []
                    listeTaches[personne].append({'tache': tache, 'statut': statut == 'True'})
    return listeTaches


"""
Mets à jour les infos des tâches dans le fichier texte 'Taches.txt'.
"""


def maj_fichier(taches):
    with open(FichierTaches, 'w') as file:
        for personne, tachesPersonne in taches.items():
            for infosTache in tachesPersonne:
                file.write(f"{personne},{infosTache['tache']},{infosTache['statut']}\n")


"""
Ajoute une tâche (à faire) à une personne choisie dans la liste des tâches et après appel 'maj_fichier()' pour mettre à jour le fichier texte.
"""


def ajout_tache(personne, tache):
    listeTaches = recup_taches()
    if personne not in listeTaches:
        listeTaches[personne] = []
    listeTaches[personne].append({'tache': tache, 'statut': False})
    maj_fichier(listeTaches)
    print(f"Tâche '{tache}' ajoutée pour {personne}.")


"""
Affiche les tâches terminées ou non de la personne demandée.
"""


def voire_taches(personne):
    listeTaches = recup_taches()
    if personne in listeTaches:
        print(f"Tâches de {personne}:")
        idx = 1
        for infosTache in listeTaches[personne]:
            if infosTache['statut']:
                statut = "Terminé"
            else:
                statut = "Non terminé"
            print(f"{idx}. {infosTache['tache']} - {statut}")
            idx += 1
    else:
        print(f"Aucune tâche trouvée pour {personne}.")


"""
Change le statu d'une tâche en terminée.
"""


def terminer_tache(personne, numTache):
    listeTaches = recup_taches()
    if personne in listeTaches and 0 <= (numTache - 1) < len(listeTaches[personne]):
        listeTaches[personne][numTache -1]['statut'] = True
        maj_fichier(listeTaches)
        print(f"Tâche '{listeTaches[personne][numTache - 1]['tache']}' marquée comme terminée pour {personne}.")
    else:
        print("numéro de tâche invalide.")


"""
Change le statut d'une tâche en non terminée (réinitialise la tâche).
"""


def reinitialiser_tache(personne, numTache):
    listeTaches = recup_taches()
    if personne in listeTaches and 0 <= (numTache - 1) < len(listeTaches[personne]):
        listeTaches[personne][numTache -1]['statut'] = False
        maj_fichier(listeTaches)
        print(f"Tâche '{listeTaches[personne][numTache - 1]['tache']}' est réinitialiser {personne}.")
    else:
        print("numéro de tâche invalide.")


"""
Supprime une tâche d'une personne choisie et mets le fichier texte à jour.
"""


def supprimer_tache(personne, numTache):
    listeTaches = recup_taches()

    if personne in listeTaches:
        if numTache >= 1 and numTache <= len(listeTaches[personne]):
            print(f"La tâche '{listeTaches[personne][numTache - 1]['tache']}' à été supprimé de la liste de {personne}.")
            listeTaches[personne].pop(numTache - 1)
            maj_fichier(listeTaches)
        else:
            print('Ce numéros de tâche est introuvable.')
    else:
        print("Cette personne n'est pas dans la liste des tâches.")


class TacheManager(cmd.Cmd):
    intro = colored("Quelle action voulez-vous effectuer? (tapé 'help' pour voir les commandes possibles).", "green")
    prompt = "taches> "

    def do_ajouter(self, arg):
        """Ajouter une tâche."""
        personne = input("A qui voulez vous ajouter une tâche? ").strip()
        tache = input("Quel tâche voulez vous ajouter a cette personne? ").strip()
        valide = input(f"voullez vous ajouter la tache '{tache}' à {personne}? oui/non ").strip().lower()
        if valide == "oui":
            ajout_tache(personne, tache)
        elif valide == "non":
            print(f"La tâche '{tache}' n'a pas été ajouté à {personne}")
        else:
            print("Réponse inconnue")

    def do_voir(self, arg):
        """Voir les tâches d'une personne"""
        personne = input("De qui voulez vous voire les tâches? ").strip()
        voire_taches(personne)

    def do_valider(self, arg):
        """Marquer une tâche comme terminée"""
        personne = input("A qui voulez vous valider une tâche? ").strip()
        num = input("Quel tâche voulez vous valider ? (numéro tâche) ").strip()
        valide = input(f"voullez vous valider la tache ? oui/non ").strip().lower()
        num = int(num)
        if valide == "oui":
            terminer_tache(personne, num)
        elif valide == "non":
            print(f"La tâche n'a pas été valider")
        else:
            print("Réponse inconnue")

    def do_reinitialiser(self, arg):
        """Réinitialiser une tâche"""
        personne = input("A qui voulez vous réinitialiser une tâche? ").strip()
        num = input("Quel tâche voulez vous réinitialiser ? (numéro tâche) ").strip()
        valide = input(f"voullez vous reinitialiser la tache ? oui/non ").strip().lower()
        num = int(num)
        if valide == "oui":
            reinitialiser_tache(personne, num)
        elif valide == "non":
            print(f"La tâche n'a pas été réinitialiser")
        else:
            print("Réponse inconnue")

    def do_supprimer(self, arg):
        """Supprimer une tâche"""
        personne = input("A qui voulez vous supprimer une tâche? ").strip()
        num = input("Quel tâche voulez vous supprimer ? (numéro tâche) ").strip()
        valide = input(f"voullez vous supprimer la tache ? oui/non ").strip().lower()
        num = int(num)
        if valide == "oui":
            supprimer_tache(personne, num)
        elif valide == "non":
            print(f"La tâche n'a pas été supprimer")
        else:
            print("Réponse inconnue")

    def do_help(self, arg):
        """Affiche les commandes possibles"""
        print("Voila la liste des commandes possible.")
        print("-ajouter: Ajouter une tâche.")
        print("-voir: Voir les tâches d'une personne.")
        print("-valider: Marquer une tâche comme terminée.")
        print("-reinitialiser: Marquer une tâche comme non terminée..")
        print("-supprimer: Supprimer une tâche.")
        print("-exit: Quitter le programme.")

    def do_exit(self, args):
        """Quitter le programme"""
        print('Fermeture du programme avec succès.')
        return True

    def postcmd(self, stop, line):
        print(colored("__________________________________________________________________________", "red"))
        return stop


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gestion des tâches ménagères.")
    subparsers = parser.add_subparsers(dest='command')

    parser_ajouter = subparsers.add_parser('ajouter', help="Ajouter une tâche.")
    parser_ajouter.add_argument('personne', type=str, help='Nom de la personne')
    parser_ajouter.add_argument('tache', type=str, help="Description de la tâche. À écrire entre guillemets ('')")

    parser_voir = subparsers.add_parser('voir', help="Voir les tâches d'une personne.")
    parser_voir.add_argument('personne', type=str, help='Nom de la personne')

    parser_valider = subparsers.add_parser('valider', help="Marquer une tâche comme terminée.")
    parser_valider.add_argument('personne', type=str, help='Nom de la personne')
    parser_valider.add_argument('num_tache', type=int, help='Numéro de la tâche')

    parser_reinitialiser = subparsers.add_parser('reinitialiser', help="Marquer une tâche comme non terminée.")
    parser_reinitialiser.add_argument('personne', type=str, help='Nom de la personne')
    parser_reinitialiser.add_argument('num_tache', type=int, help='Numéro de la tâche')

    parser_supprimer = subparsers.add_parser('supprimer', help="Supprimer une tâche.")
    parser_supprimer.add_argument('personne', type=str, help='Nom de la personne')
    parser_supprimer.add_argument('num_tache', type=int, help='Numéro de la tâche')

    parser_shell = subparsers.add_parser('shell', help="Lancer le mode interactif.")

    args = parser.parse_args()

    if args.command == 'ajouter':
        ajout_tache(args.personne, args.tache)
    elif args.command == 'voir':
        voire_taches(args.personne)
    elif args.command == 'valider':
        terminer_tache(args.personne, args.num_tache)
    elif args.command == 'reinitialiser':
        reinitialiser_tache(args.personne, args.num_tache)
    elif args.command == 'supprimer':
        supprimer_tache(args.personne, args.num_tache)
    elif args.command == 'shell':
        TacheManager().cmdloop()
    else:
        parser.print_help()
