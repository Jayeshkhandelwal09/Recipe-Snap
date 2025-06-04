import React, { useState } from 'react';
import { AnalysisResult } from '../types';

interface IngredientsListProps {
  analysisResult: AnalysisResult;
  onGenerateRecipes: (ingredients: string[]) => void;
  onStartOver: () => void;
  isLoading?: boolean;
}

const IngredientsList: React.FC<IngredientsListProps> = ({
  analysisResult,
  onGenerateRecipes,
  onStartOver,
  isLoading = false
}) => {
  const [ingredients, setIngredients] = useState<string[]>(analysisResult.ingredients);
  const [newIngredient, setNewIngredient] = useState('');

  const addIngredient = () => {
    if (newIngredient.trim() && !ingredients.includes(newIngredient.trim())) {
      setIngredients([...ingredients, newIngredient.trim()]);
      setNewIngredient('');
    }
  };

  const removeIngredient = (index: number) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addIngredient();
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          🔍 Detected Ingredients
        </h2>
        
        {/* Analysis Info */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-blue-800 mb-2">
            <strong>Image Analysis:</strong> {analysisResult.caption}
          </p>
          <p className="text-sm text-blue-600">
            <strong>Confidence:</strong> {Math.round(analysisResult.confidence * 100)}%
          </p>
        </div>

        {/* Ingredients Grid */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Your Ingredients ({ingredients.length})
          </h3>
          
          {ingredients.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mb-4">
              {ingredients.map((ingredient, index) => (
                <div
                  key={index}
                  className="bg-green-100 border border-green-300 rounded-lg px-3 py-2 flex items-center justify-between"
                >
                  <span className="text-green-800 font-medium">{ingredient}</span>
                  <button
                    onClick={() => removeIngredient(index)}
                    className="text-red-500 hover:text-red-700 ml-2"
                    title="Remove ingredient"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg mb-2">🤔 No ingredients detected</p>
              <p>Try adding some manually below</p>
            </div>
          )}
        </div>

        {/* Add Ingredient */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">
            Add More Ingredients
          </h3>
          <div className="flex gap-2">
            <input
              type="text"
              value={newIngredient}
              onChange={(e) => setNewIngredient(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="e.g., tomatoes, cheese, bread..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              onClick={addIngredient}
              disabled={!newIngredient.trim() || isLoading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Add
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => onGenerateRecipes(ingredients)}
            disabled={ingredients.length === 0 || isLoading}
            className="bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white px-8 py-3 rounded-lg font-semibold text-lg transition-colors flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <span className="animate-spin mr-2">⏳</span>
                Generating Recipes...
              </>
            ) : (
              <>
                🍳 Generate Recipes ({ingredients.length} ingredients)
              </>
            )}
          </button>
          
          <button
            onClick={onStartOver}
            disabled={isLoading}
            className="bg-gray-500 hover:bg-gray-600 disabled:bg-gray-300 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            📸 Upload New Image
          </button>
        </div>
      </div>
    </div>
  );
};

export default IngredientsList; 