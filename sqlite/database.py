import sqlite3

conn = sqlite3.connect("university.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Projects(
    project_id VARCHAR PRIMARY KEY,
    project_directory VARCHAR NOT NULL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Samples(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id VARCHAR NOT NULL,
    preservation VARCHAR,
    isolation_source VARCHAR,
    collection_date DATETIME,
    project_id VARCHAR,
    locality_place INTEGER,
    FOREIGN KEY(project_id) REFERENCES Projects(project_id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Locality_Cities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(2) NOT NULL,
    city TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Locality_Places(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city_id INTEGER,
    FOREIGN KEY(city_id) REFERENCES Locality_Cities(id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Sequencing_Runs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id VARCHAR,
    platform VARCHAR,
    run_date DATETIME,
    run_directory VARCHAR,
    sequencing_approach VARCHAR,
    assembly_method_version VARCHAR,
    genome_coverage INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Barcodes(
    barcode_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER,
    seq_run_id INTEGER,
    replaces_barcode_id INTEGER,
    FOREIGN KEY(sample_id) REFERENCES Samples(id),
    FOREIGN KEY(seq_run_id) REFERENCES Sequencing_Runs(id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Repetition_reasons(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reason TEXT NOT NULL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Repetitions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seq_barcode_id INTEGER,
    reason_id INTEGER,
    FOREIGN KEY(seq_barcode_id) REFERENCES Barcodes(barcode_id),
    FOREIGN KEY(reason_id) REFERENCES Repetition_reasons(id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Resistance_Experiments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER NOT NULL,
    profile_id INTEGER NOT NULL,
    enrichment_media TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Agents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_code TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Agent_info(
    agent_info_id INTEGER PRIMARY KEY AUTOINCREMENT,
    resistance_exp_id INTEGER NOT NULL,
    agent_id INTEGER NOT NULL,
    value INTEGER,
    UNIQUE(resistance_exp_id, agent_id),
    FOREIGN KEY(resistance_exp_id) REFERENCES Resistance_Experiments(id),
    FOREIGN KEY(agent_id) REFERENCES Agents(id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Collectors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Collected_by(
    collector_id INTEGER NOT NULL,
    sample_id INTEGER NOT NULL,
    FOREIGN KEY(sample_id) REFERENCES Samples(id),
    FOREIGN KEY(collector_id) REFERENCES Collectors(id)
)""")

conn.commit()
conn.close()
