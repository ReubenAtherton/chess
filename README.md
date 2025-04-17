# Chess Engine ♟️

<img width="300" alt="image" src="https://github.com/user-attachments/assets/74af6679-1ea3-48b0-b8e8-724c339bb714" />
..
<img width="300" alt="image" src="https://github.com/user-attachments/assets/a9e6b14c-7d19-41aa-a049-c3ee5208e757" />

## Overview 📁 :

This is a personal project (work in progress) to follow a Chess engine youtube tutorial, adding my own changes where possible.

Additions to be made:

- Pregame menu with options to customise game UI
- Chess notation menu showing game move history

## Running the Application

### Local Development

To start the game run command:  
`python3 -m src.main.main`

### Docker

To build and run the application using Docker:

1. Build the Docker image:

```bash
docker build -t chess-engine .
```

2. Run the container:

```bash
docker run -p 8080:8080 chess-engine
```

The application will be available at `http://localhost:8080`
