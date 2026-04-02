-- SQLite schema for shared agent communication
-- Safe from SQL injection via parameterized queries

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT NOT NULL,
    instance TEXT NOT NULL,
    speaker TEXT NOT NULL,
    msg TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast recent message queries
CREATE INDEX IF NOT EXISTS idx_time ON messages(time);
CREATE INDEX IF NOT EXISTS idx_instance ON messages(instance);

-- Insert sample message
INSERT INTO messages (time, instance, speaker, msg) 
VALUES (datetime('now'), 'system', 'system', 'SQLite shared memory initialized');
