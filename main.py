import random
import readchar
import time
import json
import matplotlib.pyplot as plt

def lista_parole(file, lunghezza):
    parole = []
    """
    Crea una lista di parole di una certa lunghezza da un file.

    :param file: Il percorso del file contenente le parole.
    :param lunghezza: La lunghezza delle parole da estrarre.
    :return: Una lista di parole di lunghezza specificata.
    """
    with open(file, 'r') as f:
        parole_tt = f.readlines()
        parole_tt = [x.strip() for x in parole_tt]
        for i in range(lunghezza):
            parola = random.choice(parole_tt)
            parole.append(parola)

    return parole

def stampa_lista(parole):
    GRIGIO = "\033[90m"
    END = "\033[0m"
    for i in range(len(parole)):
        print(f"{GRIGIO}{parole[i]}{END}", end=" ")
        if i % 10 == 0 and i != 0:
            print("\n")

def get_stringa(lista):
    stringa = ""
    for parola in lista:
        stringa += (parola + " ")
    return stringa[:-1]

def check_tasto(inputk, base):
    if inputk == base:
        return True
    else:
        return False

### gestione salvataggi
def get_user_data(user, file):
    with open(file, 'r') as file:
        users_data = json.load(file)
    if user not in users_data:
        return "X"
    user_data = users_data[user]
    return user_data

def add_user_data(user, file,wpm,acc):
    with open(file, 'r') as f:
        users_data = json.load(f)

    users_data[user]["avg_wpm"].append(wpm)
    users_data[user]["avg_acc"].append(acc)

    with open("salvataggi.json", "w") as f:
        json.dump(users_data, f, indent=4)

def add_new_user(user, file):
    new_user = {
        f"{user}": {
            "avg_wpm": [],
            "avg_acc": []
        }
    }

    with open(file, 'r') as f:
        users_data = json.load(f)

    users_data.update(new_user)
    with open(file, "w") as f:
        json.dump(users_data, f, indent=4)
### gestione grafici

def plot_scatter_chart(x, y, title="Grafico a Dispersione", xlabel="X", ylabel="Y"):
    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, color='red')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def get_plot_data(user,tipo_media):
    user_data = get_user_data(user, "salvataggi.json")
    x = [i for i in range(len(user_data[tipo_media]))]
    y = user_data[tipo_media]
    plot_scatter_chart(x, y,)

def game_loop():

    ROSSO = "\033[31m"
    END = "\033[0m"
    file = "parole_mischiate_eng.txt"
    lunghezza = 5

    lista = lista_parole(file, lunghezza)
    stringa = get_stringa(lista)

    print(f"Inizia il gioco!")
    print("\033[2J")
    print("\033[H")
    stampa_lista(lista)
    print("\033[H")


    start = time.time()
    lettere_corr = 0
    lettere_err = 0
    for lettera in stringa:
        giusto = True
        while True:

            char = readchar.readkey()
            if check_tasto(char, lettera):
                if giusto:
                    print(f"{lettera}", end="", flush=True)
                    lettere_corr += 1
                    break
                else:
                    print(f"{ROSSO}{lettera}{END}", end="", flush=True)
                    lettere_corr += 1
                    break

            else:
                giusto = False
                lettere_err += 1
    end = time.time()
    tempo = end - start
    wpm = ((lettere_corr/5)-(lettere_err/lettere_corr))/(tempo/60)
    accuracy = (lettere_corr/(lettere_corr+lettere_err))*100

    print("\nHai completato il gioco!")
    print(f'il tuo wpm e\' {wpm:.2f}')
    print(f'il tuo accuracy e\' {accuracy:.2f}%')
    return wpm, accuracy

def welcome():
    print("\033[2J")
    print("benvenuto! inserisci il nome del tuo utente")
    user = input("Nome utente: ")
    file = "salvataggi.json"
    user_data = get_user_data(user, file)
    if user_data == "X":
        print("utente non trovato, aggiunto al file di salvataggio")
        add_new_user(user, file)
        user_data = get_user_data(user, file)

    print(f"Benvenuto {user}!")
    return user, file, user_data

def main():
    user, file, user_data = welcome()

    while True:

        wpm, acc = game_loop()
        add_user_data(user, file, wpm, acc)
        print("Vuoi continuare a giocare? \'q\' per uscire \'i\' per informazioni")
        char = readchar.readkey()
        if char == "q":
            print("Uscita dal gioco...")
            break
        elif char == "i":
            print("\033[2J")
            print("Informazioni utente:")
            print(f"Nome utente: {user}")
            print(f"Media WPM: {sum(user_data['avg_wpm'])/len(user_data['avg_wpm'])}")
            print(f"Media Accuracy: {sum(user_data['avg_acc'])/len(user_data['avg_acc'])}")
            print("Vuoi vedere i grafici? (y/n)")
            char = readchar.readkey()
            if char == "y":
                get_plot_data(user, "avg_wpm")
                get_plot_data(user, "avg_acc")

if __name__ == "__main__":
    main()