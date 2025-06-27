
# Paye Ton Kawa – API-Client

## Prérequis

- [Docker](https://www.docker.com/products/docker-desktop) et [Docker Compose](https://docs.docker.com/compose/) installés sur votre machine.

## Démarrage rapide

1. **Cloner le dépôt**

   ```sh
   git clone <url-du-depot>
   cd api-clients
   ```

2. **Configurer les variables d’environnement**

   Les identifiants de la base de données sont déjà définis dans le fichier `docker-compose.yml` :
   - Utilisateur : `postgres`
   - Mot de passe : `rkb.0102`
   - Base : `paye_ton_kawa`

   Si besoin, modifiez-les dans le fichier.

3. **Lancer les services (API + PostgreSQL)**

   ```sh
   docker-compose up --build
   ```

   - L’API sera accessible sur [http://localhost:8000](http://localhost:8000)
   - La base PostgreSQL sera accessible sur le port `55433` de votre machine.

4. **Arrêter les services**

   Appuyez sur `Ctrl+C` dans le terminal, puis :

   ```sh
   docker-compose down -v
   ```

## Structure du projet

```
.
├── app/                # Code source FastAPI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Accès à la documentation API

Une fois le projet lancé, ouvrez [http://localhost:8000/docs](http://localhost:8000/docs) pour accéder à la documentation interactive Swagger.

---

**Remarque**  
Si le port `55433` est déjà utilisé, modifiez-le dans le fichier `docker-compose.yml` (section `db:ports`).