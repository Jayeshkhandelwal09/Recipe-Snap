import React, { useState } from 'react';
import { Recipe } from '../types';

interface RecipeCardProps {
  recipe: Recipe;
}

const RecipeCard: React.FC<RecipeCardProps> = ({ recipe }) => {
  const [showInstructions, setShowInstructions] = useState(false);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'hard':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getCuisineEmoji = (cuisine: string) => {
    switch (cuisine.toLowerCase()) {
      case 'italian':
        return '🇮🇹';
      case 'asian':
        return '🥢';
      case 'mediterranean':
        return '🫒';
      case 'american':
        return '🇺🇸';
      case 'healthy':
        return '🥗';
      case 'fusion':
        return '🌍';
      default:
        return '🍽️';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-blue-500 text-white p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-xl font-bold mb-2">{recipe.title}</h3>
            <p className="text-green-100 text-sm">{recipe.description}</p>
          </div>
          <div className="text-2xl ml-4">
            {getCuisineEmoji(recipe.cuisine)}
          </div>
        </div>
        
        {/* Recipe Meta */}
        <div className="flex flex-wrap gap-2 mt-4">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(recipe.difficulty)}`}>
            {recipe.difficulty}
          </span>
          <span className="bg-white bg-opacity-20 text-white px-2 py-1 rounded-full text-xs">
            {recipe.cuisine}
          </span>
          {recipe.source && (
            <span className="bg-white bg-opacity-20 text-white px-2 py-1 rounded-full text-xs">
              {recipe.source}
            </span>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Time and Servings */}
        <div className="grid grid-cols-3 gap-4 mb-6 text-center">
          <div>
            <div className="text-2xl mb-1">⏱️</div>
            <div className="text-sm text-gray-600">Prep</div>
            <div className="font-semibold">{recipe.prep_time}</div>
          </div>
          <div>
            <div className="text-2xl mb-1">🔥</div>
            <div className="text-sm text-gray-600">Cook</div>
            <div className="font-semibold">{recipe.cook_time}</div>
          </div>
          <div>
            <div className="text-2xl mb-1">👥</div>
            <div className="text-sm text-gray-600">Serves</div>
            <div className="font-semibold">{recipe.servings}</div>
          </div>
        </div>

        {/* Ingredients */}
        <div className="mb-6">
          <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
            🛒 Ingredients ({recipe.ingredients.length})
          </h4>
          <div className="grid grid-cols-1 gap-2">
            {recipe.ingredients.map((ingredient, index) => (
              <div key={index} className="flex items-center text-sm">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                {ingredient}
              </div>
            ))}
          </div>
        </div>

        {/* Instructions Toggle */}
        <div className="border-t pt-4">
          <button
            onClick={() => setShowInstructions(!showInstructions)}
            className="w-full bg-blue-50 hover:bg-blue-100 text-blue-700 font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
          >
            <span className="mr-2">📝</span>
            {showInstructions ? 'Hide Instructions' : 'Show Instructions'}
            <span className="ml-2">
              {showInstructions ? '▲' : '▼'}
            </span>
          </button>
        </div>

        {/* Instructions */}
        {showInstructions && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold text-gray-800 mb-3">
              👨‍🍳 Instructions
            </h4>
            <ol className="space-y-3">
              {recipe.instructions.map((instruction, index) => (
                <li key={index} className="flex text-sm">
                  <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold mr-3 mt-0.5 flex-shrink-0">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{instruction}</span>
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* Match Score (if available) */}
        {recipe.match_score && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center justify-between text-sm">
              <span className="text-green-700 font-medium">
                🎯 Ingredient Match
              </span>
              <span className="text-green-800 font-bold">
                {Math.round(recipe.match_score * 100)}%
              </span>
            </div>
            {recipe.matched_ingredients && (
              <div className="text-xs text-green-600 mt-1">
                {recipe.matched_ingredients} of {recipe.ingredients.length} ingredients available
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecipeCard; 