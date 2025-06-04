export interface Recipe {
  id: number;
  title: string;
  description: string;
  ingredients: string[];
  instructions: string[];
  prep_time: string;
  cook_time: string;
  servings: number;
  difficulty: string;
  cuisine: string;
  source?: string;
  match_score?: number;
  matched_ingredients?: number;
}

export interface AnalysisResult {
  success: boolean;
  caption: string;
  ingredients: string[];
  confidence: number;
  error?: string;
}

export interface RecipeResponse {
  success: boolean;
  recipes: Recipe[];
  total: number;
}

export interface ApiError {
  detail: string;
} 