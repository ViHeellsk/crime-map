
CREATE USER 'pepa'@'%' IDENTIFIED BY 'semtex123.';
GRANT ALL PRIVILEGES ON Interesting_Places.* TO 'pepa'@'%';
FLUSH PRIVILEGES;

CREATE TABLE Interesting_Places (
    place_id INT AUTO_INCREMENT PRIMARY KEY,
    place_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    description TEXT,
    language VARCHAR(10) NOT NULL,
    CONSTRAINT chk_language CHECK (language IN ('EN', 'FR', 'ES', 'DE', 'CZ')), -- Omezí jazyky na konkrétní možnosti
    UNIQUE(place_name, latitude, longitude, language) -- Zajistí unikátnost kombinace názvu místa, souřadnic a jazyka
);

INSERT INTO Interesting_Places (place_name, latitude, longitude, description, language) VALUES
('Větrný mlýn ve vsi Chlumec', 50.554722, 14.146111, 'Historický větrný mlýn s krásným výhledem na okolní krajinu.', 'CZ'),
('Hrad Hněvín', 50.6525, 13.997222, 'Starobylý hrad s bohatou historií a impozantní architekturou.', 'CZ'),
('Přírodní rezervace České středohoří', 50.635, 14.000556, 'Malebná krajina s skalnatými útvary a rozmanitou faunou a flórou.', 'CZ'),
('Krušné hory', 50.65, 13.583333, 'Přírodní rezervace s rozsáhlými lesy a možnostmi turistiky a lyžování.', 'CZ'),
('Zámek Duchcov', 50.612222, 13.7375, 'Barokní zámek s parkem, který slouží jako muzeum a kulturní centrum.', 'CZ'),
('Skalní hrad Rýzmburk', 50.720833, 14.033056, 'Ruiny středověkého skalního hradu s panoramatickým výhledem.', 'CZ'),
('Teplické lázně', 50.640833, 13.8125, 'Lázeňské město se známými minerálními prameny a historickou architekturou.', 'CZ'),
('Vodní nádrž Nechranice', 50.478889, 13.379722, 'Přehrada vhodná pro vodní sporty a rekreační aktivity v krásném přírodním prostředí.', 'CZ'),
('Tisá - skalní město', 50.750833, 14.073056, 'Oblíbený terén pro horolezectví s malebnými skalními útvary.', 'CZ'),
('Město Litoměřice', 50.533333, 14.133333, 'Historické město s dochovanými středověkými památkami a malebným historickým centrem.', 'CZ');

INSERT INTO Interesting_Places (place_name, latitude, longitude, description, language) VALUES
('Windmill in the village of Chlumec', 50.554722, 14.146111, 'Historical windmill with a beautiful view of the surrounding countryside.', 'EN'),
('Hněvín Castle', 50.6525, 13.997222, 'Ancient castle with a rich history and impressive architecture.', 'EN'),
('České středohoří Nature Reserve', 50.635, 14.000556, 'Picturesque landscape with rocky formations and diverse flora and fauna.', 'EN'),
('Krušné hory', 50.65, 13.583333, 'Nature reserve with extensive forests and opportunities for hiking and skiing.', 'EN'),
('Duchcov Castle', 50.612222, 13.7375, 'Baroque castle with a park that serves as a museum and cultural center.', 'EN'),
('Rock castle Rýzmburk', 50.720833, 14.033056, 'Ruins of a medieval rock castle with a panoramic view.', 'EN'),
('Teplice Spa', 50.640833, 13.8125, 'Spa town with famous mineral springs and historical architecture.', 'EN'),
('Nechranice Reservoir', 50.478889, 13.379722, 'Reservoir suitable for water sports and recreational activities in a beautiful natural setting.', 'EN'),
('Tisá - rock city', 50.750833, 14.073056, 'Popular terrain for rock climbing with picturesque rock formations.', 'EN'),
('Town of Litoměřice', 50.533333, 14.133333, 'Historic town with preserved medieval landmarks and a picturesque historic center.', 'EN');

INSERT INTO Interesting_Places (place_name, latitude, longitude, description, language) VALUES
('Windmühle im Dorf Chlumec', 50.554722, 14.146111, 'Historische Windmühle mit herrlichem Blick auf die umliegende Landschaft.', 'DE'),
('Burg Hněvín', 50.6525, 13.997222, 'Alte Burg mit reicher Geschichte und beeindruckender Architektur.', 'DE'),
('Naturreservat České středohoří', 50.635, 14.000556, 'Malerische Landschaft mit felsigen Formationen und vielfältiger Flora und Fauna.', 'DE'),
('Erzgebirge', 50.65, 13.583333, 'Naturreservat mit ausgedehnten Wäldern und Möglichkeiten zum Wandern und Skifahren.', 'DE'),
('Schloss Duchcov', 50.612222, 13.7375, 'Barockschloss mit Park, das als Museum und Kulturzentrum dient.', 'DE'),
('Felsenburg Rýzmburk', 50.720833, 14.033056, 'Ruinen einer mittelalterlichen Felsenburg mit Panoramablick.', 'DE'),
('Teplice Spa', 50.640833, 13.8125, 'Kurort mit berühmten Mineralquellen und historischer Architektur.', 'DE'),
('Nechranice Stausee', 50.478889, 13.379722, 'Stausee für Wassersport und Freizeitaktivitäten in einer wunderschönen Naturlandschaft.', 'DE'),
('Tisá - Felsenstadt', 50.750833, 14.073056, 'Beliebtes Gelände zum Klettern mit malerischen Felsformationen.', 'DE'),
('Stadt Litoměřice', 50.533333, 14.133333, 'Historische Stadt mit erhaltenen mittelalterlichen Sehenswürdigkeiten und malerischem historischen Zentrum.', 'DE');

INSERT INTO Interesting_Places (place_name, latitude, longitude, description, language) VALUES
('Ветряная мельница в деревне Хлумец', 50.554722, 14.146111, 'Историческая ветряная мельница с прекрасным видом на окружающую местность.', 'RU'),
('Замок Хневин', 50.6525, 13.997222, 'Древний замок с богатой историей и впечатляющей архитектурой.', 'RU'),
('Природный заповедник Чешское Средогорье', 50.635, 14.000556, 'Живописный пейзаж с скалистыми образованиями и разнообразной флорой и фауной.', 'RU'),
('Крушные горы', 50.65, 13.583333, 'Природный заповедник с обширными лесами и возможностями для пеших прогулок и катания на лыжах.', 'RU'),
('Замок Духцов', 50.612222, 13.7375, 'Барочный замок с парком, который служит музеем и культурным центром.', 'RU'),
('Скальный замок Рыжмбурк', 50.720833, 14.033056, 'Руины средневекового скального замка с панорамным видом.', 'RU'),
('Теплицкие лечебные источники', 50.640833, 13.8125, 'Курортный город с известными минеральными источниками и исторической архитектурой.', 'RU'),
('Водохранилище Нехранисе', 50.478889, 13.379722, 'Водохранилище подходит для водных видов спорта и отдыха в красивой природной среде.', 'RU'),
('Тиса - скальный город', 50.750833, 14.073056, 'Популярное место для скалолазания с живописными скальными образованиями.', 'RU'),
('Город Литомержице', 50.533333, 14.133333, 'Исторический город с сохраненными средневековыми памятниками и живописным историческим центром.', 'RU');

