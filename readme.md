# Project Description

This project is a recommendation service that provides personalized recommendations based on user preferences. It utilizes machine learning algorithms to analyze user data and generate accurate recommendations.

## How to Run the Application with Docker and Docker Compose

To run the application using Docker and Docker Compose, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone the repository to your local machine.

3. Navigate to the project directory.

4. Build apps both service and db using docker compose:

    ```
    docker-compose -f docker-compose.dev.yml up
    ```

5. The application will now be running on `http://localhost:80`.

6. You can access the application in your browser by navigating to `http://localhost:80`.
