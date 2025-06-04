import React from 'react';
import { Recipe } from '../types';
import RecipeCard from './RecipeCard';

interface RecipesListProps {
  recipes: Recipe[];
  onStartOver: () => void;
  onBackToIngredients: () => void;
}

const RecipesList: React.FC<RecipesListProps> = ({
  recipes,
  onStartOver,
  onBackToIngredients
}) => {
  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          🍳 Your Recipe Suggestions
        </h2>
        <p className="text-gray-600 text-lg">
          Found {recipes.length} delicious recipe{recipes.length !== 1 ? 's' : ''} for you!
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
        <button
          onClick={onBackToIngredients}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center"
        >
          <span className="mr-2">🔙</span>
          Edit Ingredients
        </button>
        <button
          onClick={onStartOver}
          className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center"
        >
          <span className="mr-2">📸</span>
          Upload New Image
        </button>
      </div>

      {/* Recipes Grid */}
      {recipes.length > 0 ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {recipes.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">😔</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            No recipes found
          </h3>
          <p className="text-gray-500 mb-6">
            We couldn't find any recipes with your ingredients. Try adding more ingredients or upload a new image.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={onBackToIngredients}
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              Edit Ingredients
            </button>
            <button
              onClick={onStartOver}
              className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              Upload New Image
            </button>
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="mt-12 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-yellow-800 mb-3 flex items-center">
          💡 Tips for Better Results
        </h3>
        <ul className="text-yellow-700 space-y-2 text-sm">
          <li>• Take clear, well-lit photos of your ingredients</li>
          <li>• Include common pantry items like salt, pepper, oil, etc.</li>
          <li>• Add ingredients manually if they weren't detected</li>
          <li>• Try different combinations of your available ingredients</li>
        </ul>
      </div>
    </div>
  );
};

export default RecipesList; 