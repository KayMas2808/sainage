-- Create the Users table
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Create the Preferences table
CREATE TABLE Preferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    accuracy_speed_ratio REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

-- Create the Sign Language Data table (if needed)
CREATE TABLE SignLanguageData (
    data_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    interaction_timestamp DATETIME NOT NULL,
    recognition_result TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);
