from flask import Flask, jsonify, request
import json
from datetime import datetime, time
import logging
import re


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_time(time_string):
    """Convert time string to a datetime object."""
    time_string = time_string.strip()
    if time_string in ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        return None
    time_string = re.sub(r'^(Mon|Tues|Wed|Thu|Fri|Sat|Sun)\s+', '', time_string)

    # Try the two different time formats
    time_formats = [
        '%I:%M %p',  # 11:00 am
        '%I %p',     # 11 am
    ]

    for time_format in time_formats:
        try:
            return datetime.strptime(time_string, time_format)
        except ValueError:
            continue

    raise ValueError(f"Could not parse time: {time_string}")


def parse_hours(hours_string):
    """Parse restaurant's hours string into a structured format."""
    schedules = [schedule.strip() for schedule in hours_string.split('/')]
    parsed_schedule = []

    for schedule in schedules:
        # Split into days and times
        parts = schedule.split(' ', 1)
        days = parts[0]
        times = parts[1] if len(parts) > 1 else ""

        # Parse days
        day_ranges = days.split(',')
        for day_range in day_ranges:
            day_range = day_range.strip()
            if '-' in day_range:
                start_day, end_day = day_range.split('-')
                days_list = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                start_idx = days_list.index(start_day)
                end_idx = days_list.index(end_day)
                if start_idx <= end_idx:
                    days_in_range = days_list[start_idx:end_idx + 1]
                else:
                    days_in_range = days_list[start_idx:] + days_list[:end_idx + 1]
            else:
                days_in_range = [day_range]

            # Parse times
            if times:
                time_parts = times.split('-')
                open_time = time_parts[0].strip()
                close_time = time_parts[1].strip()

                open_datetime = parse_time(open_time)
                close_datetime = parse_time(close_time)

                # Only add to schedule if both times are valid
                if open_datetime is not None and close_datetime is not None:
                    for day in days_in_range:
                        parsed_schedule.append({
                            'day': day,
                            'open': open_datetime.strftime('%H:%M'),
                            'close': close_datetime.strftime('%H:%M')
                        })

    return parsed_schedule


class Restaurant:
    """Represents a restaurant with its operating hours."""
    def __init__(self, name, hours_str):
        self.name = name
        self.hours = parse_hours(hours_str)

    def is_open_at(self, target_datetime):
        """Check if restaurant is open at a given datetime."""
        target_day = target_datetime.strftime('%a')
        if target_day == 'Tue':
            target_day = 'Tues'

        target_time = target_datetime.strftime('%H:%M')

        for hours in self.hours:
            if hours['day'] == target_day:
                return hours['open'] <= target_time <= hours['close']
        return False


# Initialize Flask app
app = Flask(__name__)


def load_restaurants():
    """Load restaurant data and convert to Restaurant objects."""
    with open('restaurants.json', 'r') as f:
        raw_data = json.load(f)
        return [
            Restaurant(r['Restaurant Name'], r['Hours'])
            for r in raw_data
        ]


@app.route('/restaurants/open', methods=['GET'])
def get_open_restaurants():
    """Endpoint which returns restaurants open for a given datetime."""
    try:
        datetime_str = request.args.get('datetime')
        if not datetime_str:
            return jsonify({'error': 'datetime parameter is required'}), 400

        logger.debug(f"Attempting to parse datetime: {datetime_str}")

        # Parse datetime
        try:
            target_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return jsonify({
                'error': 'Invalid format, please use: YYYY-MM-DDTHH:MM:SS'
            }), 400

        logger.debug(f"Successfully parsed datetime: {target_datetime}")

        open_restaurants = [
            restaurant.name
            for restaurant in app.restaurants
            if restaurant.is_open_at(target_datetime)
        ]

        return jsonify({
            'datetime': datetime_str,
            'open_restaurants': open_restaurants
        })

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500


def main():
    app.restaurants = load_restaurants()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
