"""
Content Generator Module
Uses Large Language Models to generate personalized educational content
Adapts explanations, quizzes, and flashcards based on learner profile
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Dict, List, Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import LLM_MODEL_NAME, LLM_MAX_LENGTH, LLM_TEMPERATURE, DEVICE


class ContentGenerator:
    """
    Generates personalized educational content using LLMs
    """
    
    def __init__(self, model_name: str = LLM_MODEL_NAME):
        """
        Initialize the content generator with an LLM
        
        Args:
            model_name: Hugging Face model identifier
        """
        print(f"Loading LLM model: {model_name} on {DEVICE}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.model.to(DEVICE)
        self.model.eval()
        print("LLM model loaded successfully!")
    
    def _generate_text(self, prompt: str, max_length: int = LLM_MAX_LENGTH, 
                      temperature: float = LLM_TEMPERATURE) -> str:
        """
        Generate text using the LLM
        
        Args:
            prompt: Input prompt
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        inputs = self.tokenizer(prompt, return_tensors="pt", 
                               max_length=512, truncation=True).to(DEVICE)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                num_return_sequences=1
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    
    def generate_explanation(self, topic: str, learner_profile: Dict) -> str:
        """
        Generate personalized explanation for a topic
        
        Args:
            topic: Topic to explain
            learner_profile: Learner's profile data
            
        Returns:
            Personalized explanation text
        """
        proficiency = learner_profile.get("proficiency_level", "beginner")
        prefers_analogies = learner_profile.get("preferences", {}).get("prefers_analogies", True)
        prefers_examples = learner_profile.get("preferences", {}).get("prefers_examples", True)
        
        # Construct personalized prompt
        if proficiency == "beginner":
            level_instruction = "Explain in simple terms suitable for a complete beginner."
        elif proficiency == "intermediate":
            level_instruction = "Explain with moderate technical detail for someone with basic knowledge."
        else:
            level_instruction = "Provide an advanced, in-depth explanation with technical details."
        
        style_instruction = ""
        if prefers_analogies:
            style_instruction += " Use analogies and metaphors."
        if prefers_examples:
            style_instruction += " Include practical examples."
        
        prompt = f"""Task: Explain the concept of '{topic}' for educational purposes.
Level: {level_instruction}
Style: {style_instruction}
Provide a clear, structured explanation:"""
        
        explanation = self._generate_text(prompt, max_length=400)
        return explanation
    
    def generate_quiz(self, topic: str, learner_profile: Dict, 
                     num_questions: int = 5) -> List[Dict]:
        """
        Generate quiz questions for a topic
        
        Args:
            topic: Topic for quiz
            learner_profile: Learner's profile data
            num_questions: Number of questions to generate
            
        Returns:
            List of quiz questions with options and answers
        """
        proficiency = learner_profile.get("proficiency_level", "beginner")
        
        if proficiency == "beginner":
            difficulty = "easy, basic concepts"
        elif proficiency == "intermediate":
            difficulty = "moderate, application-level"
        else:
            difficulty = "challenging, advanced concepts"
        
        quiz_questions = []
        
        for i in range(num_questions):
            prompt = f"""Generate a {difficulty} multiple-choice question about '{topic}'.
Format: Question | Option A | Option B | Option C | Option D | Correct Answer (A/B/C/D)
Question {i+1}:"""
            
            response = self._generate_text(prompt, max_length=200)
            
            # Parse response (simplified parsing)
            # In production, use more robust parsing
            parts = response.split("|")
            if len(parts) >= 6:
                question = {
                    "question": parts[0].strip(),
                    "options": {
                        "A": parts[1].strip(),
                        "B": parts[2].strip(),
                        "C": parts[3].strip(),
                        "D": parts[4].strip()
                    },
                    "correct_answer": parts[5].strip()[0] if parts[5].strip() else "A"
                }
            else:
                # Fallback question if parsing fails
                question = {
                    "question": f"What is an important concept in {topic}?",
                    "options": {
                        "A": "Option A",
                        "B": "Option B",
                        "C": "Option C",
                        "D": "Option D"
                    },
                    "correct_answer": "A"
                }
            
            quiz_questions.append(question)
        
        return quiz_questions
    
    def generate_flashcards(self, topic: str, learner_profile: Dict, 
                           num_cards: int = 5) -> List[Dict]:
        """
        Generate flashcards for a topic
        
        Args:
            topic: Topic for flashcards
            learner_profile: Learner's profile data
            num_cards: Number of flashcards to generate
            
        Returns:
            List of flashcards with front and back content
        """
        proficiency = learner_profile.get("proficiency_level", "beginner")
        
        flashcards = []
        
        for i in range(num_cards):
            prompt = f"""Create a flashcard about '{topic}' for {proficiency} level.
Format: Front (question/term) | Back (answer/definition)
Flashcard {i+1}:"""
            
            response = self._generate_text(prompt, max_length=150)
            
            # Parse response
            parts = response.split("|")
            if len(parts) >= 2:
                flashcard = {
                    "front": parts[0].strip(),
                    "back": parts[1].strip()
                }
            else:
                flashcard = {
                    "front": f"Key concept in {topic}",
                    "back": response.strip()
                }
            
            flashcards.append(flashcard)
        
        return flashcards
    
    def generate_summary(self, topic: str, learner_profile: Dict) -> str:
        """
        Generate a summary of a topic
        
        Args:
            topic: Topic to summarize
            learner_profile: Learner's profile data
            
        Returns:
            Summary text
        """
        proficiency = learner_profile.get("proficiency_level", "beginner")
        
        prompt = f"""Summarize the key points about '{topic}' for a {proficiency} level learner.
Provide a concise summary with main takeaways:"""
        
        summary = self._generate_text(prompt, max_length=300)
        return summary
    
    def adapt_content_difficulty(self, content: str, target_level: str) -> str:
        """
        Adapt existing content to a different difficulty level
        
        Args:
            content: Original content
            target_level: Target proficiency level
            
        Returns:
            Adapted content
        """
        if target_level == "beginner":
            instruction = "Simplify this explanation for a complete beginner"
        elif target_level == "intermediate":
            instruction = "Adapt this explanation for intermediate level"
        else:
            instruction = "Make this explanation more advanced and technical"
        
        prompt = f"""{instruction}:
Original: {content[:200]}
Adapted version:"""
        
        adapted = self._generate_text(prompt, max_length=400)
        return adapted


# Example usage and testing
if __name__ == "__main__":
    # Create content generator
    generator = ContentGenerator()
    
    # Sample learner profile
    learner_profile = {
        "proficiency_level": "beginner",
        "learning_style": "visual",
        "preferences": {
            "prefers_visuals": True,
            "prefers_examples": True,
            "prefers_analogies": True
        }
    }
    
    topic = "Machine Learning"
    
    print("\n" + "="*60)
    print("GENERATING EXPLANATION")
    print("="*60)
    explanation = generator.generate_explanation(topic, learner_profile)
    print(explanation)
    
    print("\n" + "="*60)
    print("GENERATING QUIZ")
    print("="*60)
    quiz = generator.generate_quiz(topic, learner_profile, num_questions=3)
    for i, q in enumerate(quiz, 1):
        print(f"\nQ{i}: {q['question']}")
        for key, value in q['options'].items():
            print(f"  {key}. {value}")
        print(f"  Correct: {q['correct_answer']}")
    
    print("\n" + "="*60)
    print("GENERATING FLASHCARDS")
    print("="*60)
    flashcards = generator.generate_flashcards(topic, learner_profile, num_cards=3)
    for i, card in enumerate(flashcards, 1):
        print(f"\nCard {i}:")
        print(f"  Front: {card['front']}")
        print(f"  Back: {card['back']}")
    
    print("\n" + "="*60)
    print("GENERATING SUMMARY")
    print("="*60)
    summary = generator.generate_summary(topic, learner_profile)
    print(summary)
