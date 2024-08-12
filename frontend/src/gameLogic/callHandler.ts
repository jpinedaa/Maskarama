import axios from "axios";
import { type GameState } from "./gameStateManager"; // Make sure to import your GameState type

export class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async getInitialState(): Promise<GameState> {
    const response = await axios.get(`${this.baseUrl}/initial-state`);
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return
    return response.data;
  }

  async getEnvironmentNarration(environmentId: string): Promise<string> {
    const response = await axios.get(
      `${this.baseUrl}/environment/${environmentId}/narration`,
    );
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
    return response.data.narration;
  }

  async getEventNarration(environmentId: string): Promise<string> {
    const response = await axios.get(
      `${this.baseUrl}/environment/${environmentId}/event`,
    );
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
    return response.data.narration;
  }

  async submitPlayerInput(input: string): Promise<GameState> {
    const response = await axios.post(`${this.baseUrl}/player-input`, {
      input,
    });
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return
    return response.data;
  }

  // Add more methods for other API calls as needed
}
