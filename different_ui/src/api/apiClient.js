/**
 * API client for communicating with the backend
 */

// Get API URL from environment variable or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Send a message to the chatbot
 * @param {string} message - The message to send
 * @param {string} userId - The user ID
 * @returns {Promise<Object>} - The response from the chatbot
 */
export const sendMessage = async (message, userId = 'default-user') => {
  try {
    const response = await fetch(`${API_URL}/api/chat/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        user_id: userId,
      }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

/**
 * Get all conversations for a user
 * @param {string} userId - The user ID
 * @returns {Promise<Object>} - The conversations
 */
export const getConversations = async (userId = 'default-user') => {
  try {
    const response = await fetch(`${API_URL}/api/chat/conversations/${userId}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting conversations:', error);
    throw error;
  }
};

/**
 * Get a specific conversation
 * @param {string} conversationId - The conversation ID
 * @returns {Promise<Object>} - The conversation
 */
export const getConversation = async (conversationId) => {
  try {
    const response = await fetch(`${API_URL}/api/chat/conversation/${conversationId}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting conversation:', error);
    throw error;
  }
};

/**
 * Delete a conversation
 * @param {string} conversationId - The conversation ID
 * @returns {Promise<Object>} - The response
 */
export const deleteConversation = async (conversationId) => {
  try {
    const response = await fetch(`${API_URL}/api/chat/conversation/${conversationId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error deleting conversation:', error);
    throw error;
  }
};

/**
 * Search for papers
 * @param {string} query - The search query
 * @param {number} limit - The maximum number of results to return
 * @returns {Promise<Object>} - The search results
 */
export const searchPapers = async (query, limit = 10) => {
  try {
    const response = await fetch(`${API_URL}/api/papers/search?query=${encodeURIComponent(query)}&limit=${limit}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error searching papers:', error);
    throw error;
  }
};

/**
 * Get a specific paper
 * @param {string} paperId - The paper ID
 * @returns {Promise<Object>} - The paper
 */
export const getPaper = async (paperId) => {
  try {
    const response = await fetch(`${API_URL}/api/papers/${paperId}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting paper:', error);
    throw error;
  }
};
