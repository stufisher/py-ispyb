INSERT IGNORE INTO SchemaStatus (scriptName, schemaStatus) VALUES ('2019_11_07_AdminVar_bump_version.sql', 'ONGOING');

UPDATE AdminVar SET `value` = '1.7.0' WHERE `name` = 'schemaVersion';

UPDATE SchemaStatus SET schemaStatus = 'DONE' WHERE scriptName = '2019_11_07_AdminVar_bump_version.sql';

