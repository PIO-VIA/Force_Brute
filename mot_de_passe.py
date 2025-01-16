import itertools
import pyzipper
import py7zr
import rarfile
import string
import time

def force_brute(file ,ensemble, max_length):
    if file.endswith(".zip"):
        try:
            # Extract the zip file
            with pyzipper.AESZipFile(file) as zf:
                print ("la recherche du mot de passe a commencer")
                for length in range(1, max_length+1):
                    print(f"test des mot de passe de longueur {length}")
                    for password in itertools.product(ensemble, repeat=length):
                        password = ''.join(password)
                        try:
                            # Try the password
                            zf.setpassword(password.encode('utf-8')) 
                            zf.testzip()
                            print(f"mot de passe trouve : {password}")
                            return True
                        except(RuntimeError, pyzipper.zipfile.BadZipFile):
                            
                            pass

            print("Mot de passe non trouve dans les combinaisons generees")
            
        except FileNotFoundError as e:
            print(f"Erreur :{e}")
        except Exception as e :
            print (f"Erreur inattendu : {e}")
    if file.endswith(".rar"):
        try:
            rf = rarfile.RarFile(file)
            print("Recherche du mot de passe pour le fichier .rar commencée.")
        
            for length in range(1, max_length + 1):
                print(f"Test des mots de passe de longueur {length}")
                for password in itertools.product(ensemble, repeat=length):
                    password = ''.join(password)
                    try:
                        rf.extractall(pwd=password)
                        print(f"Mot de passe trouvé : {password}")
                        return True
                    except rarfile.BadRarFile:
                        print("Le fichier .rar est invalide ou corrompu.")
                        return False
                    except rarfile.RarWrongPassword:
                        pass  # Continuer la recherche si le mot de passe est incorrect
            print("Mot de passe non trouvé dans les combinaisons générées.")
        except FileNotFoundError:
            print("Fichier introuvable.")
        except Exception as e:
            print(f"Erreur : {e}")
        return False
    if file.endswith(".7z"):
        try:
            print("Recherche du mot de passe pour le fichier .7z commencée.")
        
            for length in range(1, max_length + 1):
                print(f"Test des mots de passe de longueur {length}")
                for password in itertools.product(ensemble, repeat=length):
                    password = ''.join(password)
                    try:
                        with py7zr.SevenZipFile(file, mode='r', password=password) as zf:
                            zf.extractall()
                            print(f"Mot de passe trouvé : {password}")
                            return True
                    except py7zr.Bad7zFile:
                        print("Le fichier .7z est invalide ou corrompu.")
                        return False
                    except py7zr.PasswordError:
                        pass  # Continuer la recherche si le mot de passe est incorrect
            print("Mot de passe non trouvé dans les combinaisons générées.")
        except FileNotFoundError:
            print("Fichier introuvable.")
        except Exception as e:
            print(f"Erreur : {e}")
        return False




zip_file ="test.zip"
ensemble = string.ascii_letters + string.digits+".,;:'!@%#$*"
max_length = int(input("entrer la longueur maximal d'une combinaison"))
start_time=time.time()
force_brute (zip_file,ensemble,max_length)
end_time=time.time()
print(ensemble)
print(f"le temps de recherche est de :{end_time-start_time}")