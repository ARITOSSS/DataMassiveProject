from google.cloud import datastore

client = datastore.Client()

kinds = ["User", "Post", "Follow"]

for kind in kinds:
    # Vérifier combien d'entités existent
    query = client.query(kind=kind)
    query.keys_only()
    entities = list(query.fetch())
    print(f"{kind}: {len(entities)} entités")

    # Supprimer toutes les entités si existantes
    if entities:
        for entity in entities:
            client.delete(entity.key)
        print(f"Toutes les entités de kind {kind} ont été supprimées.")
    else:
        print(f"Aucune entité à supprimer pour {kind}.")
