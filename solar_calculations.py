import ephem
from datetime import datetime, timedelta
import numpy as np

def calculate_analemma(hour, orientation_angle=0, latitude=43.7102, longitude=7.2620):
    """
    Calculate solar positions throughout the year for a specific hour
    Returns projected positions on a sundial with specified orientation
    orientation_angle: degrees from south (positive = towards west, negative = towards east)
    """
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.long = str(longitude)

    sun = ephem.Sun()

    # Calculate positions for each day of the year
    x_positions = []  # Horizontal position on sundial
    y_positions = []  # Vertical position on sundial

    start_date = datetime(2024, 1, 1, hour, 0, 0)

    for day in range(365):
        current_date = start_date + timedelta(days=day)
        observer.date = current_date

        sun.compute(observer)

        # Convert angles to degrees
        alt = float(sun.alt) * 180/np.pi
        az = float(sun.az) * 180/np.pi

        # Project onto vertical plane with specified orientation
        # Only show points when sun is in front of the wall
        az_from_wall = az - (180 + orientation_angle)
        if -90 <= az_from_wall <= 90:
            # Convert to sundial coordinates considering wall orientation
            x = np.tan(np.radians(az_from_wall))
            y = np.tan(np.radians(alt)) / np.cos(np.radians(az_from_wall))

            x_positions.append(x)
            y_positions.append(y)

    return np.array(x_positions), np.array(y_positions)

def get_current_position(orientation_angle=0, latitude=43.7102, longitude=7.2620):
    """Get current sun position projected on sundial with specified orientation"""
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.long = str(longitude)
    observer.date = datetime.utcnow()

    sun = ephem.Sun()
    sun.compute(observer)

    az = float(sun.az) * 180/np.pi
    alt = float(sun.alt) * 180/np.pi

    # Project onto vertical plane with specified orientation
    az_from_wall = az - (180 + orientation_angle)
    if -90 <= az_from_wall <= 90:
        x = np.tan(np.radians(az_from_wall))
        y = np.tan(np.radians(alt)) / np.cos(np.radians(az_from_wall))
        return x, y
    return None, None