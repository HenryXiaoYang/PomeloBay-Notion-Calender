# PomeloBay-Notion-Calender

A simple calendar application that syncs with Notion, built with FastAPI and deployed with Docker.

## Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Docker
* Docker Compose

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/PomeloBay-Notion-Calender.git
   cd PomeloBay-Notion-Calender
   ```

2. **Set up your environment variables:**
   Create a `.env` file by copying the example file:
   ```sh
   cp .env.example .env
   ```
   Then, edit the `.env` file to add your Notion API token and proxy URL (if needed).

3. **Build and run with Docker Compose:**
   ```sh
   docker-compose up --build
   ```

The application will be available at `http://localhost:3030`.

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [Docker](https://www.docker.com/) - Containerization platform
* [Notion API](https://developers.notion.com/) - To connect with Notion

---

Happy coding!