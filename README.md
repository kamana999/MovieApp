## Project Summary

This project is a web application designed to manage the uploading and processing of CSV files containing movie and show data. It includes user authentication, file upload functionality, and comprehensive data management features. The application is built using a modern tech stack that includes Flask, MongoDB, Celery, RabbitMQ for the backend, and React for the frontend.

### Features

- **User Authentication**: Users can log in to access the dashboard where they can manage their data.
- **CSV File Upload**: Logged-in users can upload CSV files containing movie/show data. The application supports a specific CSV format (attached below).
- **Upload Progress Tracking**: Users can monitor the progress of their uploaded CSV files in real-time.
- **Data Management**: Users can view a list of all movies and shows available in the system. The list is paginated.

### Tech Stack

- **Backend**:
  - **Flask**: Serves as the main web framework for handling HTTP requests.
  - **MongoDB**: Used as the database for storing movie/show data and user information.
  - **Celery**: Handles asynchronous tasks, such as processing the uploaded CSV files.
  - **RabbitMQ**: Acts as the message broker for managing task queues in Celery.
  
- **Frontend**:
  - **React**: Provides a dynamic and responsive user interface for interacting with the application.

### Setup Instructions

To set up and run this project locally, follow these steps:

1. **Install Docker**: Ensure you have Docker installed on your machine. You can download Docker from [here](https://www.docker.com/get-started).

2. **Clone the Repository**: Clone this repository to your local machine using the following command:
    ```sh
    git clone <repository-url>
    ```

3. **Navigate to the Project Directory**: Change into the project directory:
    ```sh
    cd <project-directory>
    ```

4. **Run the Project**: Use Docker Compose to build and run the project:
    ```sh
    docker-compose up
    ```

   When you run `docker-compose up`, a script will run and create a default user with the following credentials:
   - **Username**: `admin`
   - **Password**: `admin`

   Please use these credentials to log in to the dashboard.

After running the `docker compose up` command, the application should be accessible at `http://localhost:3000`

This project aims to provide a seamless experience for managing movie/show data, from uploading and processing CSV files to viewing.
