import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Group:
  group_id:   int
  created_at: str

  def __getitem__(self, item):
    return getattr(self, item)

@dataclass
class GroupSettings:
  settings_id: int
  group_id:    int
  accept_only_messages: bool
  accept_only_commands: bool
  default_quality: str

  def __getitem__(self, item):
    return getattr(self, item)

class Database():
  def __init__(self, name: str = "cobalt"):
    self.name = name if name.endswith(".db") else f"{name}.db"

  def initialize(self):
    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()

    with open("init.sql", "r") as f:
      cursor.executescript(f.read())

    connection.commit()
    connection.close()

  def get_group(self, group_id: int):
    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))

    group = cursor.fetchone()
    connection.close()

    if group == None:
      return None

    return Group(*group)

  def get_group_settings(self, group_id: int):
    self.create_group(group_id)

    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM group_settings WHERE group_id = ?", (group_id,))

    group_settings = cursor.fetchone()
    connection.close()

    return GroupSettings(*group_settings)

  def update_group_settings(self, group_id: str, key: str, value: str):
    self.create_group(group_id)

    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()
    cursor.execute(f"UPDATE group_settings SET {key} = ? WHERE group_id = ?", (value, group_id,))
    connection.commit()
    connection.close()

  def create_group(self, group_id: int):
    group = self.get_group(group_id)
    if group != None:
      return

    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO groups (group_id) VALUES (?)", (group_id,))
    cursor.execute("INSERT INTO group_settings (group_id) VALUES (?)", (group_id,))
    connection.commit()
    connection.close()

  def log_activity(self, group_id: int):
    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO group_activity (group_id) VALUES (?)", (group_id,))
    connection.commit()
    connection.close()

  def get_daily_statistics(self):
    today = datetime.today()

    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(DISTINCT group_id) FROM group_activity WHERE DATE(timestamp) = ?", (today.isoformat(),))
    unique_members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM group_activity WHERE DATE(timestamp) = ?", (today.isoformat(),))
    total_members = cursor.fetchone()[0]

    connection.close()

    return unique_members, total_members

  def get_weekly_statistics(self):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())

    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(DISTINCT group_id) FROM group_activity WHERE DATE(timestamp) >= ? AND DATE(timestamp) <= ?", (start_of_week.isoformat(), today.isoformat(),))
    unique_members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM group_activity WHERE DATE(timestamp) >= ? AND DATE(timestamp) <= ?", (start_of_week.isoformat(), today.isoformat(),))
    total_members = cursor.fetchone()[0]

    connection.close()

    return unique_members, total_members

  def get_monthly_statistics(self):
    today = datetime.today()
    start_of_month = today.replace(day=1)

    connection = sqlite3.connect(self.name)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(DISTINCT group_id) FROM group_activity WHERE DATE(timestamp) >= ? AND DATE(timestamp) <= ?", (start_of_month.isoformat(), today.isoformat(),))
    unique_members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM group_activity WHERE DATE(timestamp) >= ? AND DATE(timestamp) <= ?", (start_of_month.isoformat(), today.isoformat(),))
    total_members = cursor.fetchone()[0]

    connection.close()

    return unique_members, total_members