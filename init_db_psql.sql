-- CREATE DATABASE "avignon-edt";

-- Suppression des tables si elles existent déjà
DROP TABLE IF EXISTS classroom_events CASCADE;
DROP TABLE IF EXISTS classroom_fetch_links CASCADE;

-- Création de la table classroom_fetch_links
CREATE TABLE classroom_fetch_links (
    classroom_id VARCHAR(100) PRIMARY KEY,  -- Numéro de salle
    link TEXT NOT NULL -- Lien vers la source des créneaux de la salle
);

-- Insertion de données exemple dans classroom_fetch_links
INSERT INTO classroom_fetch_links (classroom_id, link) VALUES
('C042', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200c4de16d114748b20c58caf613e18dca1f526500bd818358a1e3a2053da6f733fb77022e8f3ab459174588d845d705eb25505de77a9f6bbfdd0d75177a5b7021cc83bd04c632ea04ec44eeb776e106416efaaa2480cde39'),
('C040', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200cec6583a4718fba38f3a8ecd62c3a44f6fe29f1d3cbb4255fa0ae092e31e23bd4fba2dd3365f81c72856b2936642180ae3aa5acf372cf3d915072fafd8f762d672d8eaf61ba84d03fe742cb093412f5b2d49021e80a6b6'),
('C038', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def502002b45325dcb9ab8bfd2e8ce79e02dbf9c9448ecb975cd65c31cca4a70399fbef5a71b5b334312c676d39478d204a55c593f3fe74b9ac109c1701d10b04c90aebdf9a99dc90fecb329e547cf4ea5b52a52bd4fff26036624d7064e0f'),
('C036', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def502007e2e10df7ba4600c86b46c5930a529cc67a8d863bf5f21270190ba7231a9ed0ec29f536b61f70aaeb22a1ad4f45b72d6d214ef0e4a420e00af718fdbc5435463937f924707f82c3ff4de0de3920cc9f29b89147c3afc3d'),
('C034', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200eb60da8b852865854c5a5ed8b89e2624978d35131b1060bb6a71bc9ae82aea60f0bf3312f9c3ac03f117502e1839df0cac6ab7909688353871959ab83e0adb06c99b4896327563e8af4d65ce47f9996ec1d4dcf5bb0385'),
('C032', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def502007d6974f6c4c6345c782cf84439a976cc533488c06d53059aa284db7c166c07a9089349ddaa9596e6157eea12404a3769fa5b1b2ade4fff30343c6203a172b3cbed39e7a1c0cfce909bab30781d3fcbce56e125002dd591'),
('C030', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200728278b5d65bfad32b92a97ba5dcb115053e20f548fc9ede07a2513ca4a2dda5904d72c29ebf6cdb1aaa21913e25ff484290ed040a3148152beeb330bc315954136156d508c8b7e4d36f7e3a6d4488a8b20f6204877336'),
('C022', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def502001b63e206c809e6831807a3187426681e75956d4404e6073cead54f3cb2adf131805dc94b37cb1b40ed4334305f8d12d8006a6ee46f88b4d34ffbf04b8b5c9bab6d15627c84bccbf178d6eae33c3d2c0d99368a07497993'),
('C024', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200771a5afc3e62f41a155479f756bd1e0f5b5ff32112288ae32553b8e93d488f482ea3cb8b0337db3d36efc4e40dfcdbd35a4d913f8ce032291fe019df4fb5652a391c6c21af7c34c3cdcc7e1776b82d0c1e430d84384cf8'),
('C137', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200d7f1104d5d137a90d4893151d976c013bf10c30421555a3cbbb544952a14e2a00b55133507029ddc8c9371211923dff119fa1c8fc5d445328f7aeae4f4dbafdd3097e2bbbf28aa78f3dc237b02826764716a6ebdc6c01d346d42'),
('C136', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def502000f715f60308fcee92d47887dcddcb9bc8c9f1bb03d4acdae38e1c91ae98431d84cb168724a7a3822207c8e005ae12aca983c1b01b362752f938de78d14480fac9d2bc8c5792ed15c136634d5c3762c593389c31ef6bea0151c7d'),
('C135', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def502007190001440507ba63ab121c90931a248704b7e0c801fd2a61bd16c8256015fc491045ab4be5816e777a632e695792ad338c2ddeed7c13ff59a3c5f01dbf49f2cde8c63959df3a762d3bcd5bc4c638db781ef347156df4b029141'),
('C131', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200aa20d4c1e451e7415f6f0602426efa4122862271c979f24f12d2926bfedfc343cb5637b692deaa20ecd6637cacb27e77af05f3ba33105d084692a00b6ca8e4e1cb83fb2254f03d7ac09fc7aa43ee5d90f0eac79afb815e820e5c'),
('C130', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200813a481f91ed33166d38304d6e863bc3a079705ebf221695ad96cd069201fe6fe8a3f9ec8dd28d202a53fb90dca11b4184b30dfec359a5c29cc5cbb90d659fa85151baab7651545c4d5f22ec3a4db60cdb3b630eec01c789ef47'),
('C129', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def50200db9038093f97aea5d29f25490e21df4fc7c6bba048140305e9472e16ebe47add1a4276b32aab4b3d6cf71c4b51bf88aa7f3f716b09843b6f666d6d1db43897f0128b88c756471f01990f7199db97c5cde2bad8f5a72b4a651850'),
('C026', 'https://edt-api.univ-avignon.fr/api/exportAgenda/salle/def502002d7583aaa68684ce15b1f8bf681b4769ddba230d70d437be5a4fc83981370375d8dd36d070ef7a9f4b59702391f8e16f8cd1e707cd4a1f86791040637c97b26eb73795712d09c887eabe3868021863548a2d9e64e033431a540a');


-- Création de la table classroom_events (vide pour l'instant)
CREATE TABLE classroom_events (
    event_id VARCHAR(100) PRIMARY KEY, -- Id du créneau
    classroom_id VARCHAR(100) REFERENCES classroom_fetch_links(classroom_id) ON DELETE CASCADE, -- Numéro de salle
    ue_name VARCHAR(100) NOT NULL, -- Nom de l'UE
    teacher TEXT, -- Nom de l'enseignant
    class_group TEXT, -- Promo et groupe d'étudiants
    date_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Date pour lequel ce créneau a été lu dans la source
    date_start TIMESTAMP, -- Date de début du créneau
    date_end TIMESTAMP, -- Date de fin du créneau
    type VARCHAR(50), -- Type de créneau (CM, TD, TP, CM/TD, Evaluation, ...)
    CONSTRAINT valid_date CHECK (date_start < date_end)
);

-- Indexes sur la table classroom_events pour améliorer les performances
CREATE INDEX idx_classroom_id ON classroom_events(classroom_id);
CREATE INDEX idx_ue_name ON classroom_events(ue_name);
CREATE INDEX idx_class_group ON classroom_events(class_group);
CREATE INDEX idx_teacher ON classroom_events(teacher);
CREATE INDEX idx_date_start ON classroom_events(date_start);
CREATE INDEX idx_date_end ON classroom_events(date_end);