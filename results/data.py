import random
import time
import sqlite3
import pandas as pd
import streamlit as st

def generate_synthetic_data(num_records_loc1, num_records_loc2, time_gap_seconds, specific_timestamps=False):
  """Generates synthetic data with specified time gaps and record counts.

  Args:
    num_records_loc1: Number of records for Location-1.
    num_records_loc2: Number of records for Location-2.
    time_gap_seconds: Average time gap between locations in seconds.
    specific_timestamps: Whether to use specific timestamps or random intervals.

  Returns:
    A list of tuples containing (timestamp, location).
  """

  data = []
  locations = ["Location-1", "Location-2"]

  if specific_timestamps:
    # Use specific timestamps
    base_timestamp = int(time.mktime((2024, 7, 18, 20, 50, 0, 0, 0, 0))) * 1000000000
    time_gap = 600 * 1000000000

    location1_timestamps = [base_timestamp + i * 1000000 for i in range(num_records_loc1)]
    location2_timestamps = [base_timestamp + time_gap + i * 1000000 for i in range(num_records_loc2)]

    data = [(timestamp, "Location-1") for timestamp in location1_timestamps] + \
          [(timestamp, "Location-2") for timestamp in location2_timestamps]

  return data

def create_database(data):
  """Creates an SQLite database with the synthetic data.

  Args:
    data: A list of tuples containing (timestamp, location).
  """

  conn = sqlite3.connect('./db/synthetic.db')
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS mqtt_data (
                      timestamp INTEGER,
                      location TEXT
                    )''')
  cursor.executemany('INSERT INTO mqtt_data VALUES (?, ?)', data)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  num_records_loc1 = 5
  num_records_loc2 = 4
  time_gap_seconds = 600
  use_specific_timestamps = True  

  data = generate_synthetic_data(num_records_loc1, num_records_loc2, time_gap_seconds, use_specific_timestamps)
  create_database(data)
