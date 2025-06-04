import axios from 'axios';
import { AnalysisResult, RecipeResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for model loading
});

export const analyzeImage = async (file: File): Promise<AnalysisResult> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/analyze-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to analyze image');
    }
    throw new Error('Network error occurred');
  }
};

export const generateRecipes = async (ingredients: string[]): Promise<RecipeResponse> => {
  try {
    const response = await api.post('/generate-recipes', {
      ingredients,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to generate recipes');
    }
    throw new Error('Network error occurred');
  }
};

export const checkHealth = async (): Promise<any> => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend server is not responding');
  }
};

export const loadModels = async (): Promise<any> => {
  try {
    const response = await api.post('/models/load');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to load models');
    }
    throw new Error('Network error occurred');
  }
}; 