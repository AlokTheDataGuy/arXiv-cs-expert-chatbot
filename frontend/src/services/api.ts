import axios from 'axios';
import type { ChatResponse } from '../types';

const API_URL = 'http://localhost:8000';

export const api = {
  /**
   * Send a chat message to the backend
   * @param query The user's query
   * @returns The response from the chatbot
   */
  sendMessage: async (query: string): Promise<ChatResponse> => {
    try {
      const response = await axios.post(`${API_URL}/chat`, { query });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  /**
   * Get the full URL for an image
   * @param filename The image filename
   * @returns The full URL for the image
   */
  getImageUrl: (filename: string): string => {
    return `${API_URL}/images/${filename}`;
  }
};
