
# 🔒 CryptoPy

Un projet de cryptographie implémentant des algorithmes populaires tels que AES, RSA, XOR, ainsi que des fonctionnalités inspirées par PGP (Pretty Good Privacy). Réalisé dans le cadre d'un projet de 3ème année à Epitech Paris.

---

## 🚀 Fonctionnalités

- Chiffrement et déchiffrement AES
- Génération et gestion de clés RSA
- Chiffrement et déchiffrement RSA
- Chiffrement XOR
- Fonctionnalités type PGP : chiffrement, déchiffrement, signature numérique

---

## 🛠️ Installation

Clonez le dépôt :

```bash
git clone https://github.com/votre-username/CryptoPy.git
cd CryptoPy
```

Utilisez le Makefile pour configurer l'environnement :

```bash
make
```

---

## ⚙️ Exemples d'utilisation

Utilisation générale :

```bash
./mypgp [-xor | -aes | -rsa | -pgp] [-c | -d] [-b] KEY
```

Chiffrement XOR :

```bash
./mypgp -xor -c maCle < message.txt > ciphered
```

Déchiffrement XOR :

```bash
./mypgp -xor -d maCle < ciphered > deciphered.txt
```

Génération de clés RSA :

```bash
./mypgp -rsa -g 17 19
```

Chiffrement AES (mode bloc) :

```bash
./mypgp -aes -c -b maCle < message.txt > ciphered
```

Déchiffrement AES (mode bloc) :

```bash
./mypgp -aes -d -b maCle < ciphered > deciphered.txt
```

---

## 📁 Structure du Projet

```
CryptoPy/
├── src/
│   ├── aes.py
│   ├── rsa.py
│   ├── xor.py
│   ├── pgp.py
│   ├── main.py
│   ├── utils.py
│   └── args.py
├── Makefile
└── mypgp (exécutable)
```

---

## 🎓 Auteur

- **Charles Baux** - [GitHub](https://github.com/charlesbx)
- Projet réalisé à **Epitech Paris** en 3ème année.

---
