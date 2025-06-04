from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Dict
import logging
import random

from ..core.config import settings

logger = logging.getLogger(__name__)

class RecipeGenerator:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the recipe generation model"""
        try:
            logger.info("Loading recipe generation model...")
            
            # Set device
            self.device = torch.device("cuda" if torch.cuda.is_available() and settings.use_gpu else "cpu")
            logger.info(f"Using device: {self.device}")
            
            # Load model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.recipe_model_name,
                cache_dir=settings.model_cache_dir
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.recipe_model_name,
                cache_dir=settings.model_cache_dir
            )
            
            # Set pad token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Move model to device
            self.model.to(self.device)
            self.model.eval()
            
            logger.info("Recipe generation model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading recipe generation model: {e}")
            # Continue without model - will use curated recipes only
            self.model = None
            self.tokenizer = None
    
    def generate_recipes(self, ingredients: List[str]) -> List[Dict[str, any]]:
        """Generate recipes based on available ingredients"""
        try:
            if not ingredients:
                return self._get_fallback_recipes()
            
            logger.info(f"Generating recipes for ingredients: {ingredients}")
            
            # Get curated recipes (always available and reliable)
            curated_recipes = self._get_curated_recipes(ingredients)
            
            # Skip AI recipe generation for now as it's producing poor results
            # Focus on curated recipes which are much more reliable
            ai_recipes = []
            
            # Combine results (prioritize curated recipes)
            all_recipes = curated_recipes + ai_recipes
            
            # Return top 3 recipes
            return all_recipes[:3]
            
        except Exception as e:
            logger.error(f"Error generating recipes: {e}")
            return self._get_fallback_recipes()
    
    def _generate_ai_recipe(self, ingredients: List[str]) -> Dict[str, any]:
        """Generate a recipe using the AI model"""
        try:
            # Create prompt
            ingredients_str = ", ".join(ingredients[:5])  # Limit to 5 ingredients
            prompt = f"Recipe with {ingredients_str}:"
            
            # Tokenize
            inputs = self.tokenizer.encode(
                prompt, 
                return_tensors="pt", 
                max_length=100, 
                truncation=True
            )
            inputs = inputs.to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 150,
                    num_return_sequences=1,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            # Decode
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            recipe_text = generated_text[len(prompt):].strip()
            
            # Create structured recipe
            return {
                "id": 999,
                "title": f"AI Recipe with {ingredients[0]}",
                "description": "An AI-generated recipe based on your ingredients",
                "ingredients": ingredients[:5],
                "instructions": [recipe_text] if recipe_text else ["Mix ingredients and cook as desired."],
                "prep_time": "15 minutes",
                "cook_time": "20 minutes",
                "servings": 2,
                "difficulty": "Medium",
                "cuisine": "Fusion",
                "source": "AI Generated"
            }
            
        except Exception as e:
            logger.error(f"Error in AI recipe generation: {e}")
            return None
    
    def _get_curated_recipes(self, ingredients: List[str]) -> List[Dict[str, any]]:
        """Return curated recipes based on available ingredients"""
        recipes_db = [
            {
                "id": 1,
                "title": "Fresh Garden Salad",
                "description": "A healthy and refreshing salad with fresh vegetables",
                "ingredients": ["Lettuce", "Tomato", "Cucumber", "Onion", "Olive Oil", "Lemon"],
                "instructions": [
                    "Wash and chop all vegetables into bite-sized pieces",
                    "Place lettuce in a large salad bowl as the base",
                    "Add tomatoes, cucumber, and onion on top",
                    "Drizzle with olive oil and fresh lemon juice",
                    "Season with salt and pepper to taste",
                    "Toss gently and serve immediately"
                ],
                "prep_time": "15 minutes",
                "cook_time": "0 minutes",
                "servings": 4,
                "difficulty": "Easy",
                "cuisine": "Mediterranean",
                "source": "Curated"
            },
            {
                "id": 2,
                "title": "Vegetable Stir Fry",
                "description": "Quick and healthy stir-fried vegetables",
                "ingredients": ["Broccoli", "Carrot", "Bell Pepper", "Garlic", "Ginger", "Soy Sauce", "Oil"],
                "instructions": [
                    "Heat 2 tablespoons of oil in a large pan or wok over high heat",
                    "Add minced garlic and ginger, stir-fry for 30 seconds until fragrant",
                    "Add harder vegetables first (carrots, broccoli) and cook for 3-4 minutes",
                    "Add softer vegetables (bell peppers) and cook for another 2 minutes",
                    "Add soy sauce and stir everything together",
                    "Cook for 1-2 more minutes until vegetables are tender-crisp",
                    "Serve hot over rice or noodles"
                ],
                "prep_time": "10 minutes",
                "cook_time": "10 minutes",
                "servings": 3,
                "difficulty": "Easy",
                "cuisine": "Asian",
                "source": "Curated"
            },
            {
                "id": 3,
                "title": "Fruit Smoothie Bowl",
                "description": "Nutritious and delicious smoothie bowl",
                "ingredients": ["Banana", "Strawberry", "Blueberry", "Milk", "Honey", "Granola"],
                "instructions": [
                    "Freeze fruits for at least 2 hours before making",
                    "Add frozen banana and berries to a blender",
                    "Pour in a small amount of milk and blend until smooth and thick",
                    "Pour the smoothie into a bowl",
                    "Top with fresh fruits, granola, and a drizzle of honey",
                    "Add nuts or seeds if available",
                    "Serve immediately with a spoon"
                ],
                "prep_time": "5 minutes",
                "cook_time": "0 minutes",
                "servings": 1,
                "difficulty": "Easy",
                "cuisine": "Healthy",
                "source": "Curated"
            },
            {
                "id": 4,
                "title": "Scrambled Eggs with Vegetables",
                "description": "Protein-rich breakfast with fresh vegetables",
                "ingredients": ["Eggs", "Tomato", "Onion", "Pepper", "Cheese", "Butter", "Salt"],
                "instructions": [
                    "Crack 3-4 eggs into a bowl and whisk with salt and pepper",
                    "Dice tomatoes, onions, and peppers into small pieces",
                    "Heat butter in a non-stick pan over medium heat",
                    "Add vegetables and cook for 3-4 minutes until softened",
                    "Pour in the beaten eggs and let sit for 30 seconds",
                    "Gently stir and scramble the eggs with the vegetables",
                    "Add cheese in the last minute and fold in gently",
                    "Serve hot with toast or bread"
                ],
                "prep_time": "8 minutes",
                "cook_time": "7 minutes",
                "servings": 2,
                "difficulty": "Easy",
                "cuisine": "American",
                "source": "Curated"
            },
            {
                "id": 5,
                "title": "Roasted Vegetable Medley",
                "description": "Colorful roasted vegetables with herbs",
                "ingredients": ["Broccoli", "Bell Peppers", "Carrots", "Onions", "Olive Oil", "Herbs", "Salt"],
                "instructions": [
                    "Preheat oven to 425°F (220°C)",
                    "Cut all vegetables into similar-sized pieces",
                    "Toss vegetables with olive oil, salt, and herbs",
                    "Spread on a large baking sheet in a single layer",
                    "Roast for 25-30 minutes, stirring once halfway through",
                    "Vegetables should be tender and lightly caramelized",
                    "Serve as a side dish or over rice"
                ],
                "prep_time": "15 minutes",
                "cook_time": "30 minutes",
                "servings": 4,
                "difficulty": "Easy",
                "cuisine": "Mediterranean",
                "source": "Curated"
            },
            {
                "id": 6,
                "title": "Fresh Vegetable Omelet",
                "description": "Fluffy omelet packed with fresh vegetables",
                "ingredients": ["Eggs", "Milk", "Cheese", "Tomatoes", "Onions", "Bell Peppers", "Herbs"],
                "instructions": [
                    "Beat 3 eggs with 2 tablespoons of milk",
                    "Dice vegetables into small pieces",
                    "Heat a non-stick pan over medium heat with a little oil",
                    "Sauté vegetables for 2-3 minutes until softened",
                    "Pour in the beaten eggs and let set for 1 minute",
                    "Add cheese and herbs to one half of the omelet",
                    "Fold the omelet in half and slide onto a plate",
                    "Serve immediately while hot"
                ],
                "prep_time": "10 minutes",
                "cook_time": "8 minutes",
                "servings": 1,
                "difficulty": "Medium",
                "cuisine": "French",
                "source": "Curated"
            },
            {
                "id": 7,
                "title": "Corn and Vegetable Soup",
                "description": "Hearty soup with fresh corn and vegetables",
                "ingredients": ["Corn", "Carrots", "Onions", "Broccoli", "Vegetable Broth", "Herbs", "Salt"],
                "instructions": [
                    "Heat oil in a large pot over medium heat",
                    "Add diced onions and carrots, cook for 5 minutes",
                    "Add corn kernels and cook for 3 minutes",
                    "Pour in vegetable broth and bring to a boil",
                    "Add broccoli and herbs, simmer for 10 minutes",
                    "Season with salt and pepper to taste",
                    "Serve hot with crusty bread"
                ],
                "prep_time": "15 minutes",
                "cook_time": "20 minutes",
                "servings": 4,
                "difficulty": "Easy",
                "cuisine": "American",
                "source": "Curated"
            },
            {
                "id": 8,
                "title": "Cheese and Herb Frittata",
                "description": "Baked egg dish with cheese and fresh herbs",
                "ingredients": ["Eggs", "Milk", "Cheese", "Herbs", "Onions", "Butter", "Salt"],
                "instructions": [
                    "Preheat oven to 375°F (190°C)",
                    "Beat 6 eggs with milk, salt, and pepper",
                    "Heat butter in an oven-safe skillet over medium heat",
                    "Add diced onions and cook until softened",
                    "Pour in the egg mixture and add cheese and herbs",
                    "Cook for 3-4 minutes until edges start to set",
                    "Transfer to oven and bake for 12-15 minutes",
                    "Cut into wedges and serve warm"
                ],
                "prep_time": "10 minutes",
                "cook_time": "20 minutes",
                "servings": 4,
                "difficulty": "Medium",
                "cuisine": "Italian",
                "source": "Curated"
            }
        ]
        
        # Filter recipes based on available ingredients
        matching_recipes = []
        ingredients_lower = [ing.lower() for ing in ingredients]
        
        for recipe in recipes_db:
            recipe_ingredients_lower = [ing.lower() for ing in recipe["ingredients"]]
            matches = sum(1 for ing in recipe_ingredients_lower 
                         if any(avail in ing or ing in avail for avail in ingredients_lower))
            
            if matches >= 1:  # At least 1 ingredient match
                recipe["match_score"] = matches / len(recipe["ingredients"])
                recipe["matched_ingredients"] = matches
                matching_recipes.append(recipe)
        
        # Sort by match score and return top recipes
        matching_recipes.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        # If we have good matches, return them, otherwise return some default recipes
        if matching_recipes:
            return matching_recipes[:4]
        else:
            return recipes_db[:3]  # Return first 3 as fallback
    
    def _get_fallback_recipes(self) -> List[Dict[str, any]]:
        """Return fallback recipes when no ingredients are detected"""
        return [
            {
                "id": 100,
                "title": "Simple Pasta",
                "description": "A basic pasta dish that's always delicious",
                "ingredients": ["Pasta", "Olive Oil", "Garlic", "Salt", "Pepper"],
                "instructions": [
                    "Boil water in a large pot with salt",
                    "Add pasta and cook according to package instructions",
                    "Heat olive oil in a pan and add minced garlic",
                    "Sauté garlic until fragrant but not brown",
                    "Drain pasta and toss with garlic oil",
                    "Season with salt and pepper to taste",
                    "Serve hot with grated cheese if available"
                ],
                "prep_time": "5 minutes",
                "cook_time": "15 minutes",
                "servings": 2,
                "difficulty": "Easy",
                "cuisine": "Italian",
                "source": "Fallback"
            },
            {
                "id": 101,
                "title": "Basic Fried Rice",
                "description": "Simple fried rice with whatever you have",
                "ingredients": ["Rice", "Eggs", "Oil", "Salt", "Soy Sauce"],
                "instructions": [
                    "Cook rice and let it cool (day-old rice works best)",
                    "Heat oil in a large pan or wok",
                    "Scramble eggs in the pan and set aside",
                    "Add rice to the pan and break up any clumps",
                    "Stir-fry rice for 3-4 minutes",
                    "Add scrambled eggs back to the pan",
                    "Season with soy sauce and salt",
                    "Serve hot"
                ],
                "prep_time": "10 minutes",
                "cook_time": "10 minutes",
                "servings": 2,
                "difficulty": "Easy",
                "cuisine": "Asian",
                "source": "Fallback"
            }
        ] 