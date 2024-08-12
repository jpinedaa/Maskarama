/* eslint-disable @typescript-eslint/no-unsafe-assignment */
// pages/api/game.ts
import type { NextApiRequest, NextApiResponse } from "next";
import axios from "axios";

const API_BASE_URL = process.env.API_BASE_URL;

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const { method, query, body } = req;

  try {
    let response;

    switch (method) {
      case "GET":
        switch (query.action) {
          case "status":
            response = await axios.get(`${API_BASE_URL}/status`);
            break;
          case "start":
            response = await axios.get(`${API_BASE_URL}/start`, {
              params: { no_turns: query.no_turns },
            });
            break;
          case "environments":
            response = await axios.get(`${API_BASE_URL}/environments`);
            break;
          case "entities":
            response = await axios.get(`${API_BASE_URL}/entities`);
            break;
          case "narration":
            response = await axios.get(`${API_BASE_URL}/narration`);
            break;
          case "event":
            response = await axios.get(`${API_BASE_URL}/event`);
            break;
          default:
            return res.status(400).json({ error: "Invalid action" });
        }
        break;

      case "POST":
        if (query.action === "user_input") {
          response = await axios.post(`${API_BASE_URL}/user_input`, body);
        } else {
          return res.status(400).json({ error: "Invalid action" });
        }
        break;

      default:
        return res.status(405).json({ error: "Method not allowed" });
    }

    return res.status(response.status).json(response.data);
  } catch (error) {
    console.error("API error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
