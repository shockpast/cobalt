CREATE TABLE IF NOT EXISTS groups (
  group_id    INTEGER PRIMARY KEY,
  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS group_settings (
  settings_id           INTEGER PRIMARY KEY,
  group_id              INTEGER NOT NULL,

  accept_only_messages  BOOLEAN DEFAULT(0),
  accept_only_commands  BOOLEAN DEFAULT(0),
  default_quality       TEXT DEFAULT('720'),

  FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS group_activity (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  group_id  INTEGER NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- settings
  -- accept_only_messages: false/true
  -- accept_only_commands: false/true
  -- default_quality: 480/720/1080