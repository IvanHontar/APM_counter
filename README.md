# APM Measurement Script

This script allows you to measure the Actions Per Minute (APM) of a user, record the results in a PostgreSQL database, and display additional messages based on the APM.

## Usage

1. Install the required dependencies:

    ```bash
    pip install psycopg2-binary pynput
    ```

2. Create a file `env.py` and define the following environment variables:

    ```python
    # env.py
    DB_HOST = "your_host"
    DB_NAME = "your_database"
    DB_USER = "your_user"
    DB_PASSWORD = "your_password"
    ```

3. Run the script:

    ```bash
    python your_script.py
    ```

4. Enter your name and press Enter to start APM counting.

5. To stop the counting, press the 'Esc' key.

6. The results will be recorded in the database, and you will see additional messages based on the APM value.

## Dependencies

- psycopg2
- pynput

