## Table of Contents

1. [Installation and Usage](#installation-and-usage)
   - [Prerequisites](#prerequisites)
   - [Installation Steps](#installation-steps)
   - [Summary](#summary)
   
2. [Development Process](#development-process)
   - [Vision and Concept](#vision-and-concept)
   - [Simulation Details](#simulation-details)
   - [The Role of Gemini API](#the-role-of-gemini-api)
   - [Design Process](#design-process)
   - [Simulation Diagram and Memory Diagram](#simulation-diagram-and-memory-diagram)
   
3. [Roadmap](#roadmap)
   - [Completed Features](#completed-features)
   - [Incomplete Features](#incomplete-features)
   - [Optimization Challenges](#optimization-challenges)
   - [Gratitude](#gratitude)

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

## Development Process

### Vision and Concept

**Maskarama** (formerly known as *Echoes of Creation*) is an intricate god-simulation sandbox game where players step into the role of an omnipotent being, guiding a world filled with characters whose memories, perceptions, and interactions evolve dynamically. The game’s core vision is to create a universe of possibilities where every character is a complex entity driven by a unique knowledge graph, influenced by emotional intensity, novelty, and personal significance.

Players influence the game world by triggering events, shaping perceptions, and weaving intricate stories. The dynamic simulation and narrative engine ensure that every decision impacts the unfolding story, offering endless replayability with each session generating a new tale.

### Simulation Details

**Flow of the Simulation:**
The simulation operates on a turn-based system, with each turn lasting 2 minutes. The flow is divided into six stages:

1. **Stage 1: User Input**
   - **Input:** User Interface Interactions
   - **Output:** 
     - Updated Environment Objects
     - Updated Character Perception
     - Updated Character Memory
     - Updated Entity Inputs
     - Updated Entity State

2. **Stage 2: Entities Update**
   - **Input:** Entity Inputs, Entity State
   - **Output:** Updated Entity State

3. **Stage 3: Characters Perception Update**
   - **Input:** Entity Inputs, Entity State, Character Perception, Character Memory
   - **Output:** 
     - Updated Character’s Perception
     - Updated Memory

4. **Stage 4: Entity Current Output Update**
   - **Input:** Entity Inputs, Entity State, Character Perception
   - **Output:** Updated Entity Current Output

5. **Stage 5: Environments Update**
   - **Input:** Environment Object, Entities’ Current Output, 2 minutes
   - **Output:** 
     - Updated Environment Object
     - Updated Entities’ Inputs

6. **Stage 6: Narrative Generation**
   - **Input:** Environment Object, Character Perception, Last Narrative Unit
   - **Output:** New Narrative Unit
   
  ![v2 Simulation Diagram](https://github.com/user-attachments/assets/99e3bf33-57f7-488a-9bd5-28d80ed87e3d)


**Memory and Perception:**
At the heart of the simulation is the memory system, which is the main feature driving the behavior and interactions of each character. Each character possesses a graph-based memory system implemented using Neo4j and enhanced by the Gemini API. This memory system is a complex knowledge graph that represents long-term memory, storing associations, significant events, and personal experiences.

During the simulation, each character retrieves and updates their memories using Graph Retrieval-Augmented Generation (RAG) techniques powered by the Gemini API. This enables the character to access relevant memories, which then influence their perception and decision-making processes. The Gemini API performs all computational steps, leveraging large language models (LLMs) to process the text-based simulation. The result is a deeply personalized and evolving experience for each character, where memories are continually influenced by their interactions within the game world.

![graph-diagram (1)](https://github.com/user-attachments/assets/f10baeaa-ef05-4f46-a3ae-3061ad313a83)

### The Role of Gemini API

The **Gemini API** is a central component in Maskarama, driving the core AI functionalities that make the game’s simulation and narrative unique and deeply engaging. Its role is multifaceted and includes the following:

- **Memory Management:** The Gemini API powers the complex memory system of each character, utilizing advanced AI techniques to manage the storage, retrieval, and updating of memories. Each character’s memory is a living, evolving entity that directly influences their perceptions and behaviors. The API's Graph RAG capabilities enable the efficient retrieval of relevant memories during each simulation turn, ensuring that the characters’ actions are contextually accurate and richly detailed.

- **Perception and Decision-Making:** The API processes the vast amount of data generated during each turn, helping characters to interpret and react to their environment. By integrating inputs from the environment, other entities, and their own memories, characters can make decisions that reflect their unique experiences and personality traits.

- **Narrative Generation:** The Gemini API is also crucial for the dynamic narrative engine. It synthesizes the current state of the game world, including character perceptions and environmental changes, to generate compelling narrative snippets. These narratives are not pre-scripted; they evolve organically based on the player’s actions and the interactions between entities, providing a personalized story with each playthrough.

- **Simulation Efficiency:** The Gemini API ensures that the complex, turn-based simulation runs smoothly and efficiently. By handling the computational heavy lifting, the API allows Maskarama to offer a rich and immersive experience without compromising performance.

In summary, the Gemini API is the backbone of Maskarama’s advanced AI, enabling the game to deliver a unique blend of strategic depth, narrative richness, and character realism. Its integration allows for a seamless experience where every action, memory, and perception is interconnected, resulting in a living, breathing game world.

### Design Process

**UI/UX Design:**
The design process for Maskarama was guided by the need to create an immersive and intuitive user interface that complements the complexity of the underlying simulation. A moodboard was used to establish the visual tone and atmosphere of the game, emphasizing a blend of mystical, ethereal elements with a user-friendly layout.

![Screenshot 2024-08-12 155542](https://github.com/user-attachments/assets/758d0a19-4077-411b-9c27-eaef66a6cf41)

**Wireframes:**
Early wireframes focused on the flow of information and the ease of interaction. The UI design went through several iterations to ensure that players could easily manage their god-like powers, observe the dynamic world, and influence the narrative without feeling overwhelmed by the game's complexity.

![Mockup_Popup](https://github.com/user-attachments/assets/4ac93d5d-a238-4065-84ad-5a5633c3c04d)

![mockup_gameplay](https://github.com/user-attachments/assets/d968e0e9-85d4-4bba-b837-b2de6ce26834)

**Accessibility Features:**

![accessibility](https://github.com/user-attachments/assets/38ad3930-a030-46fb-b07a-fd633ccc94d1)

### Summary

Once both the backend and frontend servers are running, you can interact with the Maskarama application through your web browser. The backend handles the core logic and simulation, while the frontend provides the user interface for interacting with the game. This setup has been tested and works on Windows.

## Roadmap

As part of our submission to the developer competition, we focused on implementing the core aspects of **Maskarama**. While we successfully completed many of the foundational features, there were some ambitious elements we were unable to finalize before the deadline. Below is a summary of what was achieved and what remains on our development roadmap.

![Screenshot 2024-08-12 151536](https://github.com/user-attachments/assets/ee183141-8a71-4de7-ab23-e41dd1995a1c)

### Completed Features

- **Simulation Framework:** The core turn-based simulation engine was implemented, allowing for the complex interactions between characters, objects, and environments.
- **Memory Storage and Retrieval:** Each character’s memory is managed using a Neo4j-based knowledge graph, with memory retrieval and updates powered by the Gemini API. This ensures that each character’s perceptions and decisions are influenced by their unique past experiences.
- **Main Narration UI:** The main UI panel for narrative generation is operational, displaying the evolving story based on player inputs and the simulation's state.
- **User Input Handling:** The game successfully processes player inputs, allowing users to influence the simulation through various god-like actions.
- **Visual Representation:** Visuals for all characters, objects, and rooms are displayed, providing a clear view of the game world.
- **Stylized Map:** A stylized map was created to give players an overview of the environments and their connections.

### Incomplete Features

- **Detailed Character, Object, and Environment Information:** While the backend handles detailed internal simulation data (such as states, perceptions, and memories), this information is not yet fully integrated into the frontend UI.
- **Character Perspective Selection:** The ability to select a character and change the perspective of the narration is implemented in the backend, but the frontend UI for this feature is still under development.
- **Multiple Turn Simulation:** The backend supports simulating multiple turns in a row, but the frontend interface to trigger this functionality is not yet complete.

### Optimization Challenges

- **Performance:** The current simulation framework, while functional, is not fully optimized. Each turn involves numerous complex steps, leading to longer processing times. This is an area we plan to address in future updates.
- **Prompt Engineering:** Due to time constraints, there was limited opportunity to refine the prompt engineering for the various simulation steps. As a result, the output quality has room for improvement, which we aim to enhance with further development.

### Gratitude

We would like to extend our sincere thanks to Google for the opportunity to participate in the **Gemini API Developer Competition** and for providing the incredible **Gemini API**. The Gemini API has been instrumental in bringing our vision to life, enabling us to execute complex tasks such as managing character memories and generating dynamic narratives. Despite the challenges, the Gemini API has proven to be a powerful tool that allows us to turn imagination into reality, and we look forward to continuing our work with it as we further develop **Maskarama**.
