--PRAGMA foreign_keys=ON; --enforce foreign key constraints tyyliset hommat hoituvat funktiokutsujen tasolla
-- NOT NULL seems like a good thing to put in at this level
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

--three stats for now. Vimma, sisu and kesto roughly translate to ATK, DEF and HP. Integers obviously nothing fancy.
--Battles between invidual monsters are roughly simple and deterministic for now TODO: look into rand with consistent seed values and seed value storage in fights table
--in equivalents terms these could be carpets a person is trying to sell online, stats are prices etc.
CREATE TABLE mons (
    id INTEGER PRIMARY KEY,
    mon_name TEXT NOT NULL,
    vimma INTEGER,
    sisu INTEGER,
    kesto INTEGER,
    user_id INTEGER REFERENCES users
);

--user_id references owners of the mons, not the mons themselves
--optimisation with persistent same combatants indexing?
--past combatants rows are created the moment a fight is executed in the code
--in real world terms, these roughly correspond to a log of a person's actions, or the bidding history in a auction app
CREATE TABLE past_combatants (
    id INTEGER PRIMARY KEY,
    past_mon_name TEXT NOT NULL,
    vimma INTEGER,  
    sisu INTEGER,
    kesto INTEGER,
    user_id INTEGER REFERENCES users
);

--SQL-MONs in past might have different stats
--winner_id should be calculated out runtime, debug tracking
--Possible expansion of using fight_date as a seed value for number generation. Also shows the importance of database anti-tampering measures and integrity checks
--representation of a battle log, IRL equivalent would be something like chatting history 
--regarding a car on sale with or invidual messages on a message board, or a log of a person's actions in an auction app
CREATE TABLE fights (
    id INTEGER PRIMARY KEY,
    mon1_owner_id INTEGER REFERENCES users,
    mon2_owner_id INTEGER REFERENCES users,
    mon1_id INTEGER REFERENCES past_combatants,
    mon2_id INTEGER REFERENCES past_combatants,
    winner_id INTEGER REFERENCES past_combatants,
    fight_date INTEGER DEFAULT CURRENT_TIMESTAMP
);


-- Visit counter fro course material because why not
CREATE TABLE visit_counter (
    id INTEGER PRIMARY KEY,
    visited_at INTEGER DEFAULT CURRENT_TIMESTAMP
);