// apiService.ts
import axios from "axios";
import { Environment, Entity } from "~/types/gameModel";

const API_BASE_URL = 'http://127.0.0.1:5500/api';

export interface StatusResponse {
  currentEnvironment?: string;
  perspective?: string;
}

interface StartResponse {
  message: string;
}

type EnvironmentResponse = Record<string, Environment>;

type EntityResponse = Record<string, Entity>;

export class ApiService {
  async getStatus(): Promise<StatusResponse> {
    try {
      const response = await axios.get(`${API_BASE_URL}/status`);
      console.log("Response data:", response.data);

      return response.data as StatusResponse;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Axios error:", error.message);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      } else {
        console.error("An unexpected error occurred:", error);
      }
      throw error;
    }
  }

  async startSimulation(noTurns = 1): Promise<StartResponse> {
    try {
      const response = await axios.get(`${API_BASE_URL}/start`, {
        params: { no_turns: noTurns }, // Always set to 1
      });
      console.log("Response data:", response.data);
      return response.data as StartResponse;
    } catch (error) {
      console.log("startSimulation - error", error);

      if (axios.isAxiosError(error)) {
        console.error("Axios error:", error.message);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      } else {
        console.error("An unexpected error occurred:", error);
      }
      throw error;
    }
  }

  async getEnvironments(): Promise<EnvironmentResponse> {
    try {
      const response = await axios.get(`${API_BASE_URL}/environments`);
      console.log("Response data:", response.data);
      return response.data as EnvironmentResponse;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Axios error:", error.message);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      } else {
        console.error("An unexpected error occurred:", error);
      }
      throw error;
    }
  }

  async getEntities(): Promise<EntityResponse> {
    try {
      const response = await axios.get(`${API_BASE_URL}/entities`);
      console.log("Response data:", response.data);
      return response.data as EntityResponse;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Axios error:", error.message);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      } else {
        console.error("An unexpected error occurred:", error);
      }
      throw error;
    }
  }
  async getNarration(): Promise<string> {
    try {
      const response = await axios.get(`${API_BASE_URL}/narration`);
      console.log("Response data:", response.data);
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
      return response.data.narration;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Axios error:", error.message);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      } else {
        console.error("An unexpected error occurred:", error);
      }
      throw error;
    }
  }

  async getEvent(): Promise<string> {
    try {
      const response = await axios.get(`${API_BASE_URL}/event`);
      console.log("Response data:", response.data);
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
      return response.data.event;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Axios error:", error.message);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      } else {
        console.error("An unexpected error occurred:", error);
      }
      throw error;
    }
  }

  async submitPlayerInput(
    input: string,
  ): Promise<{ feedback?: string; result?: string; approved: boolean }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/user_input`, {
        input,
      });
      console.log("Response data:", response.data);

      // Ensure we're returning an object with the correct structure
      return {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
        feedback: response.data.feedback,
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
        approved: response.data.approved,
      };
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Axios error:", error.message);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      } else {
        console.error("An unexpected error occurred:", error);
      }
      // If there's an error, we return a structured object instead of throwing
      return {
        feedback: "An error occurred while processing your input.",
        approved: false,
      };
    }
  }

  // async getCurrentCharacter() {
  //   try {
  //     const response = await axios.get(`${API_BASE_URL}/current_character`);
  //     console.log("Response data:", response.data);
  //     // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  //     return response.data.current_character;
  //   } catch (error) {
  //     if (axios.isAxiosError(error)) {
  //       console.error("Axios error:", error.message);
  //       if (error.response) {
  //         console.error("Response data:", error.response.data);
  //         console.error("Response status:", error.response.status);
  //       }
  //     } else {
  //       console.error("An unexpected error occurred:", error);
  //     }
  //     throw error;
  //   }
  // }
}

export const apiService = new ApiService();
