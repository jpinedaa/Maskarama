## Installation and Usage

This guide will walk you through setting up the **Maskarama** application, including both the backend and frontend components. The entire project is contained within a single repository and is designed to work seamlessly on Windows.

### Prerequisites

Before you begin, ensure that you have the following software installed on your system:

- **Node.js** (which includes npm): [Node.js](https://nodejs.org/)
- **Docker**: [Docker](https://www.docker.com/products/docker-desktop)
- **Python**: [Python](https://www.python.org/downloads/)

### Installation Steps

1. **Clone the Repository**
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to clone the repository:
     ```bash
     cd path/to/your/directory
     ```
   - Clone the repository:
     ```bash
     git clone https://github.com/jpinedaa/Maskarama.git
     ```
   - Navigate into the cloned repository:
     ```bash
     cd Maskarama
     ```

2. **Set Up the Backend**

   - **Configure the Gemini API Key**
     - Open the `config.json` file located in the root of the repository.
     - Add your Gemini API key to the appropriate field in `config.json`.

   - **Install Python Dependencies**
     - From the root directory of the repository, install the required Python packages:
       ```bash
       pip install -r requirements.txt
       ```

   - **Set Up and Run Docker Containers**
     - Run the setup script to create and configure the necessary Docker containers:
       ```bash
       python setup_containers.py
       ```

   - **Run the Backend Server**
     - After setting up the containers, start the backend server:
       ```bash
       python server.py
       ```

3. **Set Up the Frontend**

   - Navigate into the `frontend` directory:
     ```bash
     cd frontend
     ```
   - Install Node.js dependencies:
     ```bash
     npm install
     ```
   - Run the development server:
     ```bash
     npm run dev
     ```
   - Open your web browser and go to `http://localhost:3000` to access the web application.

### Summary

Once both the backend and frontend servers are running, you can interact with the Maskarama application through your web browser. The backend handles the core logic and simulation, while the frontend provides the user interface for interacting with the game. This setup has been tested and works on Windows.
