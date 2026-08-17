"""
Learner Profiler Module
Tracks learner behavior, quiz performance, and interaction patterns
Dynamically classifies learners and identifies knowledge gaps
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import PROFICIENCY_LEVELS, BEGINNER_THRESHOLD, INTERMEDIATE_THRESHOLD, DATA_DIR


class LearnerProfiler:
    """
    Manages learner profiles and tracks learning progress
    """
    
    def __init__(self, learner_id: str = "default_learner"):
        """
        Initialize learner profiler
        
        Args:
            learner_id: Unique identifier for the learner
        """
        self.learner_id = learner_id
        self.profile_path = DATA_DIR / f"learner_{learner_id}.json"
        self.profile = self._load_or_create_profile()
    
    def _load_or_create_profile(self) -> Dict:
        """
        Load existing profile or create new one
        
        Returns:
            Dictionary containing learner profile data
        """
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        else:
            # Create new profile with default values
            return {
                "learner_id": self.learner_id,
                "created_at": datetime.now().isoformat(),
                "quiz_history": [],
                "interaction_history": [],
                "topics_studied": {},
                "proficiency_level": "beginner",
                "learning_style": "mixed",
                "total_time_spent": 0,
                "total_interactions": 0,
                "knowledge_gaps": [],
                "preferences": {
                    "prefers_visuals": False,
                    "prefers_examples": True,
                    "prefers_analogies": True
                }
            }
    
    def save_profile(self):
        """
        Persist profile to disk
        """
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)
    
    def record_quiz_attempt(self, topic: str, score: float, total_questions: int, 
                           time_spent: float, difficulty: str):
        """
        Record a quiz attempt
        
        Args:
            topic: Topic of the quiz
            score: Number of correct answers
            total_questions: Total number of questions
            time_spent: Time spent on quiz in seconds
            difficulty: Difficulty level (beginner/intermediate/advanced)
        """
        quiz_data = {
            "topic": topic,
            "score": score,
            "total_questions": total_questions,
            "accuracy": score / total_questions if total_questions > 0 else 0,
            "time_spent": time_spent,
            "difficulty": difficulty,
            "timestamp": datetime.now().isoformat()
        }
        
        self.profile["quiz_history"].append(quiz_data)
        
        # Update topic-specific data
        if topic not in self.profile["topics_studied"]:
            self.profile["topics_studied"][topic] = {
                "attempts": 0,
                "total_score": 0,
                "total_questions": 0,
                "avg_accuracy": 0
            }
        
        topic_data = self.profile["topics_studied"][topic]
        topic_data["attempts"] += 1
        topic_data["total_score"] += score
        topic_data["total_questions"] += total_questions
        topic_data["avg_accuracy"] = topic_data["total_score"] / topic_data["total_questions"]
        
        # Update proficiency level
        self._update_proficiency_level()
        
        # Identify knowledge gaps
        if quiz_data["accuracy"] < BEGINNER_THRESHOLD:
            if topic not in self.profile["knowledge_gaps"]:
                self.profile["knowledge_gaps"].append(topic)
        else:
            # Remove from knowledge gaps if improved
            if topic in self.profile["knowledge_gaps"]:
                self.profile["knowledge_gaps"].remove(topic)
        
        self.save_profile()
    
    def record_interaction(self, interaction_type: str, topic: str, 
                          time_spent: float, engagement_score: float = 0.5):
        """
        Record learner interaction
        
        Args:
            interaction_type: Type of interaction (read, quiz, visual, etc.)
            topic: Topic being studied
            time_spent: Time spent in seconds
            engagement_score: Engagement level (0-1)
        """
        interaction_data = {
            "type": interaction_type,
            "topic": topic,
            "time_spent": time_spent,
            "engagement_score": engagement_score,
            "timestamp": datetime.now().isoformat()
        }
        
        self.profile["interaction_history"].append(interaction_data)
        self.profile["total_time_spent"] += time_spent
        self.profile["total_interactions"] += 1
        
        # Update learning style preferences based on interaction patterns
        self._update_learning_style()
        
        self.save_profile()
    
    def _update_proficiency_level(self):
        """
        Update proficiency level based on recent quiz performance
        """
        if len(self.profile["quiz_history"]) == 0:
            return
        
        # Calculate average accuracy from recent quizzes (last 10)
        recent_quizzes = self.profile["quiz_history"][-10:]
        avg_accuracy = np.mean([q["accuracy"] for q in recent_quizzes])
        
        if avg_accuracy < BEGINNER_THRESHOLD:
            self.profile["proficiency_level"] = "beginner"
        elif avg_accuracy < INTERMEDIATE_THRESHOLD:
            self.profile["proficiency_level"] = "intermediate"
        else:
            self.profile["proficiency_level"] = "advanced"
    
    def _update_learning_style(self):
        """
        Update learning style based on interaction patterns
        """
        if len(self.profile["interaction_history"]) < 5:
            return
        
        # Analyze recent interactions
        recent_interactions = self.profile["interaction_history"][-20:]
        
        visual_count = sum(1 for i in recent_interactions if i["type"] == "visual")
        total_count = len(recent_interactions)
        
        # If more than 40% interactions are visual, prefer visuals
        if visual_count / total_count > 0.4:
            self.profile["preferences"]["prefers_visuals"] = True
            self.profile["learning_style"] = "visual"
        else:
            self.profile["learning_style"] = "textual"
    
    def get_learner_profile(self) -> Dict:
        """
        Get current learner profile
        
        Returns:
            Dictionary containing learner profile
        """
        return {
            "learner_id": self.learner_id,
            "proficiency_level": self.profile["proficiency_level"],
            "learning_style": self.profile["learning_style"],
            "knowledge_gaps": self.profile["knowledge_gaps"],
            "preferences": self.profile["preferences"],
            "total_time_spent": self.profile["total_time_spent"],
            "total_interactions": self.profile["total_interactions"],
            "topics_studied": list(self.profile["topics_studied"].keys())
        }
    
    def get_topic_performance(self, topic: str) -> Optional[Dict]:
        """
        Get performance metrics for a specific topic
        
        Args:
            topic: Topic name
            
        Returns:
            Dictionary with topic performance metrics or None
        """
        return self.profile["topics_studied"].get(topic)
    
    def reset_profile(self):
        """
        Reset learner profile to default state
        """
        self.profile = self._load_or_create_profile()
        self.save_profile()


# Example usage and testing
if __name__ == "__main__":
    # Create a test learner profile
    profiler = LearnerProfiler("test_student_001")
    
    # Simulate quiz attempts
    profiler.record_quiz_attempt(
        topic="Python Basics",
        score=7,
        total_questions=10,
        time_spent=300,
        difficulty="beginner"
    )
    
    profiler.record_quiz_attempt(
        topic="Machine Learning",
        score=4,
        total_questions=10,
        time_spent=450,
        difficulty="intermediate"
    )
    
    # Simulate interactions
    profiler.record_interaction(
        interaction_type="read",
        topic="Python Basics",
        time_spent=600,
        engagement_score=0.8
    )
    
    profiler.record_interaction(
        interaction_type="visual",
        topic="Machine Learning",
        time_spent=200,
        engagement_score=0.9
    )
    
    # Get profile
    profile = profiler.get_learner_profile()
    print("Learner Profile:")
    print(json.dumps(profile, indent=2))
    
    print("\nTopic Performance (Python Basics):")
    print(json.dumps(profiler.get_topic_performance("Python Basics"), indent=2))
