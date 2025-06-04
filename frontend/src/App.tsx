import React, { useState, useEffect } from 'react';
import ImageUpload from './components/ImageUpload';
import IngredientsList from './components/IngredientsList';
import RecipesList from './components/RecipesList';
import { AnalysisResult, Recipe } from './types';
import { analyzeImage, generateRecipes, checkHealth } from './services/api';

type AppState = 'upload' | 'ingredients' | 'recipes';

function App() {
  const [currentState, setCurrentState] = useState<AppState>('upload');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  // Check backend health on component mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        await checkHealth();
        setBackendStatus('online');
      } catch (error) {
        setBackendStatus('offline');
      }
    };

    checkBackendHealth();
  }, []);

  const handleImageUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await analyzeImage(file);
      if (result.success) {
        setAnalysisResult(result);
        setCurrentState('ingredients');
      } else {
        setError(result.error || 'Failed to analyze image');
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateRecipes = async (ingredients: string[]) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await generateRecipes(ingredients);
      if (result.success) {
        setRecipes(result.recipes);
        setCurrentState('recipes');
      } else {
        setError('Failed to generate recipes');
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartOver = () => {
    setCurrentState('upload');
    setAnalysisResult(null);
    setRecipes([]);
    setError(null);
  };

  const handleBackToIngredients = () => {
    setCurrentState('ingredients');
    setRecipes([]);
    setError(null);
  };

  const renderBackendStatus = () => {
    if (backendStatus === 'checking') {
      return (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-6">
          <div className="flex items-center">
            <span className="animate-spin mr-2">⏳</span>
            Checking backend connection...
          </div>
        </div>
      );
    }

    if (backendStatus === 'offline') {
      return (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <div className="flex items-center">
            <span className="mr-2">❌</span>
            Backend server is offline. Please start the backend server first.
          </div>
          <div className="text-sm mt-2">
            Run: <code className="bg-red-200 px-2 py-1 rounded">cd backend && source venv/bin/activate && python run.py</code>
          </div>
        </div>
      );
    }

    return (
      <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
        <div className="flex items-center">
          <span className="mr-2">✅</span>
          Backend server is online and ready!
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              🍳 RecipeSnap
            </h1>
            <p className="text-lg text-gray-600">
              AI-Powered Cooking Assistant from Your Fridge
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Backend Status */}
        {renderBackendStatus()}

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <div className="flex items-center">
              <span className="mr-2">⚠️</span>
              {error}
            </div>
          </div>
        )}

        {/* App States */}
        {currentState === 'upload' && (
          <div className="space-y-8">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                Step 1: Upload Your Fridge Photo
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                Take a photo of your fridge contents or ingredients, and our AI will identify what you have available for cooking.
              </p>
            </div>
            <ImageUpload 
              onImageUpload={handleImageUpload} 
              isLoading={isLoading}
            />
          </div>
        )}

        {currentState === 'ingredients' && analysisResult && (
          <div className="space-y-8">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                Step 2: Review & Edit Ingredients
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                Check the detected ingredients and add any missing items before generating recipes.
              </p>
            </div>
            <IngredientsList
              analysisResult={analysisResult}
              onGenerateRecipes={handleGenerateRecipes}
              onStartOver={handleStartOver}
              isLoading={isLoading}
            />
          </div>
        )}

        {currentState === 'recipes' && (
          <div className="space-y-8">
            <RecipesList
              recipes={recipes}
              onStartOver={handleStartOver}
              onBackToIngredients={handleBackToIngredients}
            />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500">
            <p className="mb-2">
              🤖 Powered by AI • Built with React & FastAPI
            </p>
            <p className="text-sm">
              Using free local models: VIT-GPT2 for image analysis & DialoGPT for recipe generation
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
