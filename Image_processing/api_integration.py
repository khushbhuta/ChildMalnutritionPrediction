import google.generativeai as genai
import json
from pathlib import Path
from typing import Dict, Optional
import os
from PIL import Image

class MalnutritionClassifier:
    """
    A classifier that uses Google Gemini's vision API to detect malnutrition in images.
    Focuses on clinical indicators like visible ribs, muscle wasting, and body proportions.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the classifier with API credentials.
        
        Args:
            api_key: Google API key. If None, reads from GOOGLE_API_KEY env variable
        """
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Set GOOGLE_API_KEY environment variable or pass api_key parameter")
        
        genai.configure(api_key=self.api_key)
        
        # Try different model names that support vision
        model_names = [
            'gemini-1.5-pro-latest',
            'gemini-1.5-pro',
            'gemini-pro-vision',
            'gemini-1.5-flash-latest',
        ]
        
        self.model = None
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"✓ Successfully loaded model: {model_name}")
                break
            except Exception as e:
                print(f"✗ Failed to load {model_name}: {e}")
                continue
        
        if not self.model:
            # List available models for debugging
            print("\nAvailable models:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"  - {m.name}")
            raise ValueError("Could not load any vision model. Check available models above.")
    
    def classify(self, image_path: str, age_group: str = "unknown") -> Dict:
        """
        Classify malnutrition status from an image.
        
        Args:
            image_path: Path to the image file
            age_group: Age group (infant, child, adolescent, adult) for context
            
        Returns:
            Dictionary containing classification results
        """
        # Load the image
        img = Image.open(image_path)
        
        # Create the prompt focused on malnutrition detection
        prompt = f"""You are a medical AI assistant specialized in detecting malnutrition from visual assessment. 
Analyze this image and provide a clinical assessment of nutritional status.

Age Group Context: {age_group}

Focus on these clinical indicators of malnutrition:

SEVERE ACUTE MALNUTRITION (SAM) indicators:
- Visible ribs, spine, and shoulder blades
- Severe muscle wasting (temporal wasting, reduced arm/thigh circumference)
- Thin limbs with loose, wrinkled skin
- Sunken eyes and cheeks
- Distended abdomen (kwashiorkor)
- Hair changes (thin, sparse, discolored)
- Skin changes (dry, peeling, depigmentation)

MODERATE ACUTE MALNUTRITION (MAM) indicators:
- Some visible bones but less severe
- Reduced muscle mass
- Low body fat

WELL-NOURISHED indicators:
- Healthy muscle tone
- Appropriate fat distribution
- Good skin condition
- Proportionate body composition

Provide your response as a JSON object ONLY (no markdown, no code blocks) with this structure:
{{
  "classification": "Severe Acute Malnutrition|Moderate Acute Malnutrition|Well-Nourished|Cannot Determine",
  "confidence": 85,
  "severity_score": 8,
  "clinical_indicators": {{
    "visible_ribs": true,
    "muscle_wasting": "severe",
    "sunken_eyes": true,
    "thin_limbs": true,
    "skin_condition": "dry",
    "distended_abdomen": false,
    "overall_body_composition": "description here"
  }},
  "physical_observations": [
    "specific observation 1",
    "specific observation 2"
  ],
  "risk_level": "Critical",
  "recommended_actions": [
    "immediate action 1",
    "action 2"
  ],
  "limitations": [
    "limitation 1",
    "limitation 2"
  ],
  "medical_disclaimer": "This is a screening tool only. Requires clinical examination for diagnosis."
}}

Be objective and clinical. If the image quality is poor or the person is clothed in a way that prevents assessment, state this clearly.
Return ONLY the JSON object, no other text."""

        try:
            # Call Gemini API with vision
            response = self.model.generate_content([prompt, img])
            
            # Extract and parse JSON response
            response_text = response.text.strip()
            
            # Clean up response if it has markdown code blocks
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(response_text)
            
            # Add token usage info if available
            if hasattr(response, 'usage_metadata'):
                result['api_usage'] = {
                    'prompt_tokens': response.usage_metadata.prompt_token_count,
                    'candidates_tokens': response.usage_metadata.candidates_token_count,
                    'total_tokens': response.usage_metadata.total_token_count,
                }
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "error": f"JSON parsing error: {str(e)}",
                "raw_response": response_text if 'response_text' in locals() else "No response",
                "classification": "Error",
                "message": "Failed to parse AI response"
            }
        except Exception as e:
            return {
                "error": str(e),
                "classification": "Error",
                "message": "Failed to analyze image"
            }
    
    def batch_classify(self, image_paths: list[str], age_group: str = "unknown") -> list[Dict]:
        """
        Classify multiple images.
        
        Args:
            image_paths: List of paths to image files
            age_group: Age group for context
            
        Returns:
            List of classification results
        """
        results = []
        for image_path in image_paths:
            print(f"Analyzing: {image_path}")
            result = self.classify(image_path, age_group)
            result['image_path'] = image_path
            results.append(result)
        return results


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Single image classification
    print("=" * 60)
    print("Malnutrition Classification System (Gemini)")
    print("=" * 60)
    
    try:
        # Initialize classifier with your Google API key
        classifier = MalnutritionClassifier(api_key="YOUR_API_KEY_HERE")
        
        # Example: Classify a single image
        image_path = "IMAGE_PATH_HERE.jpg"  # Replace with your image path
        
        print(f"\nAnalyzing image: {image_path}")
        result = classifier.classify(image_path, age_group="child")
        
        print("\n" + "=" * 60)
        print("CLASSIFICATION RESULTS")
        print("=" * 60)
        print(f"\nClassification: {result.get('classification')}")
        print(f"Confidence: {result.get('confidence')}%")
        print(f"Severity Score: {result.get('severity_score')}/10")
        print(f"Risk Level: {result.get('risk_level')}")
        
        print("\nClinical Indicators:")
        indicators = result.get('clinical_indicators', {})
        for key, value in indicators.items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
        
        print("\nPhysical Observations:")
        for obs in result.get('physical_observations', []):
            print(f"  • {obs}")
        
        print("\nRecommended Actions:")
        for action in result.get('recommended_actions', []):
            print(f"  • {action}")
        
        print("\nAPI Usage:")
        usage = result.get('api_usage', {})
        if usage:
            print(f"  Prompt tokens: {usage.get('prompt_tokens')}")
            print(f"  Response tokens: {usage.get('candidates_tokens')}")
            print(f"  Total tokens: {usage.get('total_tokens')}")
        
        print("\n" + "=" * 60)
        print(result.get('medical_disclaimer'))
        print("=" * 60)
        
        # Save results to JSON
        output_file = "classification_result.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to: {output_file}")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nTo use this classifier:")
        print("1. Install dependencies: pip install google-generativeai pillow")
        print("2. Set your API key: export GOOGLE_API_KEY='your-key-here'")
        print("3. Run the script with an image path")
    
    except FileNotFoundError:
        print(f"\nError: Image file '{image_path}' not found")
        print("Please provide a valid image path")
