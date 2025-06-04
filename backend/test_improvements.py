#!/usr/bin/env python3
"""
Test script to verify RecipeSnap AI improvements
"""
import requests
import json

def test_recipe_generation():
    """Test recipe generation with generic ingredients"""
    print("🧪 Testing Recipe Generation...")
    
    url = "http://localhost:8000/api/v1/generate-recipes"
    data = {"ingredients": ["Vegetables", "Fruits", "Fresh"]}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Recipe generation successful!")
            print(f"📊 Generated {result['total']} recipes")
            
            for i, recipe in enumerate(result['recipes'][:2], 1):
                print(f"\n🍽️  Recipe {i}: {recipe['title']}")
                print(f"   Description: {recipe['description']}")
                print(f"   Ingredients: {', '.join(recipe['ingredients'][:5])}...")
                print(f"   Time: {recipe['prep_time']} prep + {recipe['cook_time']} cook")
                print(f"   Difficulty: {recipe['difficulty']}")
        else:
            print(f"❌ Recipe generation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing recipes: {e}")

def test_health_check():
    """Test API health"""
    print("\n🏥 Testing API Health...")
    
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API is healthy: {result['message']}")
        else:
            print(f"❌ API health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking health: {e}")

if __name__ == "__main__":
    print("🍳 RecipeSnap AI Improvements Test")
    print("=" * 40)
    
    test_health_check()
    test_recipe_generation()
    
    print("\n" + "=" * 40)
    print("✨ Test completed!")
    print("\n💡 Key Improvements Made:")
    print("   • Fixed ingredient detection to use specific items")
    print("   • Disabled problematic AI recipe generation")
    print("   • Enhanced curated recipe database")
    print("   • Better matching algorithm for ingredients")
    print("   • More realistic and practical recipes") 