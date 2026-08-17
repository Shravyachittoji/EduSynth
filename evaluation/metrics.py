"""
Evaluation Metrics Module
Calculates engagement, retention, and personalization effectiveness metrics
Provides comprehensive evaluation reports
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import (ENGAGEMENT_WEIGHT_TIME, ENGAGEMENT_WEIGHT_INTERACTIONS, 
                   ENGAGEMENT_WEIGHT_COMPLETION, DATA_DIR)


class EvaluationMetrics:
    """
    Calculates and tracks various evaluation metrics for the learning system
    """
    
    def __init__(self, evaluation_id: str = "default_eval"):
        """
        Initialize evaluation metrics tracker
        
        Args:
            evaluation_id: Unique identifier for this evaluation
        """
        self.evaluation_id = evaluation_id
        self.metrics_path = DATA_DIR / f"metrics_{evaluation_id}.json"
        self.metrics_data = self._load_or_create_metrics()
    
    def _load_or_create_metrics(self) -> Dict:
        """
        Load existing metrics or create new tracking structure
        
        Returns:
            Metrics data dictionary
        """
        if self.metrics_path.exists():
            with open(self.metrics_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "evaluation_id": self.evaluation_id,
                "created_at": datetime.now().isoformat(),
                "sessions": [],
                "aggregate_metrics": {}
            }
    
    def save_metrics(self):
        """
        Persist metrics to disk
        """
        with open(self.metrics_path, 'w') as f:
            json.dump(self.metrics_data, f, indent=2)
    
    def calculate_engagement_score(self, session_data: Dict) -> float:
        """
        Calculate engagement score for a learning session
        
        Args:
            session_data: Dictionary containing session information
                - time_spent: Total time in seconds
                - interactions: Number of interactions
                - completion_rate: Percentage of content completed (0-1)
                
        Returns:
            Engagement score (0-1)
        """
        time_spent = session_data.get("time_spent", 0)
        interactions = session_data.get("interactions", 0)
        completion_rate = session_data.get("completion_rate", 0)
        
        # Normalize time spent (assume 30 minutes is ideal)
        time_score = min(1.0, time_spent / 1800)
        
        # Normalize interactions (assume 20 interactions is ideal)
        interaction_score = min(1.0, interactions / 20)
        
        # Weighted combination
        engagement_score = (
            ENGAGEMENT_WEIGHT_TIME * time_score +
            ENGAGEMENT_WEIGHT_INTERACTIONS * interaction_score +
            ENGAGEMENT_WEIGHT_COMPLETION * completion_rate
        )
        
        return engagement_score
    
    def calculate_learning_gain(self, pre_test_score: float, 
                               post_test_score: float) -> float:
        """
        Calculate normalized learning gain
        
        Args:
            pre_test_score: Pre-test score (0-100)
            post_test_score: Post-test score (0-100)
            
        Returns:
            Normalized learning gain
        """
        if pre_test_score >= 100:
            return 0.0
        
        # Normalized Learning Gain = (post - pre) / (100 - pre)
        gain = (post_test_score - pre_test_score) / (100 - pre_test_score)
        return max(0.0, gain)
    
    def calculate_retention_rate(self, quiz_history: List[Dict], 
                                topic: str, time_window_days: int = 7) -> float:
        """
        Calculate retention rate for a topic over time
        
        Args:
            quiz_history: List of quiz attempts
            topic: Topic to analyze
            time_window_days: Time window for retention analysis
            
        Returns:
            Retention rate (0-1)
        """
        # Filter quizzes for the topic
        topic_quizzes = [q for q in quiz_history if q.get("topic") == topic]
        
        if len(topic_quizzes) < 2:
            return 0.0
        
        # Sort by timestamp
        topic_quizzes.sort(key=lambda x: x.get("timestamp", ""))
        
        # Get first and last quiz in time window
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        
        recent_quizzes = [
            q for q in topic_quizzes 
            if datetime.fromisoformat(q.get("timestamp", "2000-01-01")) > cutoff_date
        ]
        
        if len(recent_quizzes) < 2:
            return 0.0
        
        # Calculate retention as ratio of last to first accuracy
        first_accuracy = recent_quizzes[0].get("accuracy", 0)
        last_accuracy = recent_quizzes[-1].get("accuracy", 0)
        
        if first_accuracy == 0:
            return 0.0
        
        retention = last_accuracy / first_accuracy
        return min(1.0, retention)
    
    def calculate_personalization_effectiveness(self, learner_profile: Dict, 
                                               quiz_history: List[Dict]) -> float:
        """
        Calculate how effective personalization has been
        
        Args:
            learner_profile: Learner profile data
            quiz_history: Quiz history
            
        Returns:
            Personalization effectiveness score (0-1)
        """
        if len(quiz_history) < 3:
            return 0.5  # Neutral score for insufficient data
        
        # Analyze improvement trend
        recent_quizzes = quiz_history[-10:]
        accuracies = [q.get("accuracy", 0) for q in recent_quizzes]
        
        # Calculate trend (positive slope indicates improvement)
        if len(accuracies) > 1:
            x = np.arange(len(accuracies))
            slope = np.polyfit(x, accuracies, 1)[0]
            
            # Normalize slope to 0-1 range
            effectiveness = 0.5 + (slope * 2)  # Assuming slope range of -0.25 to 0.25
            effectiveness = max(0.0, min(1.0, effectiveness))
        else:
            effectiveness = 0.5
        
        return effectiveness
    
    def calculate_dropout_rate(self, sessions: List[Dict]) -> float:
        """
        Calculate session dropout rate
        
        Args:
            sessions: List of session data
            
        Returns:
            Dropout rate (0-1)
        """
        if len(sessions) == 0:
            return 0.0
        
        dropouts = sum(1 for s in sessions if s.get("completion_rate", 1.0) < 0.5)
        dropout_rate = dropouts / len(sessions)
        
        return dropout_rate
    
    def record_session(self, session_data: Dict):
        """
        Record a learning session
        
        Args:
            session_data: Session information
        """
        session_data["timestamp"] = datetime.now().isoformat()
        session_data["engagement_score"] = self.calculate_engagement_score(session_data)
        
        self.metrics_data["sessions"].append(session_data)
        self.save_metrics()
    
    def generate_report(self, learner_profile: Dict, 
                       quiz_history: List[Dict]) -> Dict:
        """
        Generate comprehensive evaluation report
        
        Args:
            learner_profile: Learner profile data
            quiz_history: Quiz history
            
        Returns:
            Evaluation report dictionary
        """
        sessions = self.metrics_data["sessions"]
        
        # Calculate aggregate metrics
        if len(sessions) > 0:
            avg_engagement = np.mean([s.get("engagement_score", 0) for s in sessions])
            total_time = sum(s.get("time_spent", 0) for s in sessions)
            total_interactions = sum(s.get("interactions", 0) for s in sessions)
            avg_completion = np.mean([s.get("completion_rate", 0) for s in sessions])
        else:
            avg_engagement = 0.0
            total_time = 0
            total_interactions = 0
            avg_completion = 0.0
        
        # Calculate learning metrics
        if len(quiz_history) >= 2:
            first_quiz_avg = np.mean([q.get("accuracy", 0) for q in quiz_history[:3]])
            last_quiz_avg = np.mean([q.get("accuracy", 0) for q in quiz_history[-3:]])
            learning_gain = self.calculate_learning_gain(
                first_quiz_avg * 100, 
                last_quiz_avg * 100
            )
        else:
            learning_gain = 0.0
        
        personalization_score = self.calculate_personalization_effectiveness(
            learner_profile, quiz_history
        )
        
        dropout_rate = self.calculate_dropout_rate(sessions)
        
        report = {
            "evaluation_id": self.evaluation_id,
            "generated_at": datetime.now().isoformat(),
            "engagement_metrics": {
                "average_engagement_score": round(avg_engagement, 3),
                "total_time_spent_minutes": round(total_time / 60, 2),
                "total_interactions": total_interactions,
                "average_completion_rate": round(avg_completion, 3),
                "number_of_sessions": len(sessions)
            },
            "learning_metrics": {
                "normalized_learning_gain": round(learning_gain, 3),
                "total_quizzes_attempted": len(quiz_history),
                "average_quiz_accuracy": round(np.mean([q.get("accuracy", 0) for q in quiz_history]), 3) if quiz_history else 0
            },
            "personalization_metrics": {
                "personalization_effectiveness": round(personalization_score, 3),
                "dropout_rate": round(dropout_rate, 3),
                "proficiency_level": learner_profile.get("proficiency_level", "unknown")
            },
            "recommendations": self._generate_recommendations(
                avg_engagement, learning_gain, personalization_score, dropout_rate
            )
        }
        
        return report
    
    def _generate_recommendations(self, engagement: float, learning_gain: float,
                                 personalization: float, dropout: float) -> List[str]:
        """
        Generate recommendations based on metrics
        
        Args:
            engagement: Engagement score
            learning_gain: Learning gain
            personalization: Personalization effectiveness
            dropout: Dropout rate
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if engagement < 0.5:
            recommendations.append("Increase engagement through more interactive content and gamification")
        
        if learning_gain < 0.3:
            recommendations.append("Adjust content difficulty and provide more scaffolding")
        
        if personalization < 0.5:
            recommendations.append("Improve personalization algorithms and gather more learner data")
        
        if dropout > 0.3:
            recommendations.append("Reduce dropout by shortening sessions and increasing motivation")
        
        if not recommendations:
            recommendations.append("System is performing well. Continue monitoring metrics.")
        
        return recommendations


# Example usage and testing
if __name__ == "__main__":
    # Create evaluation metrics tracker
    evaluator = EvaluationMetrics("test_evaluation")
    
    # Record sample sessions
    session1 = {
        "time_spent": 1200,  # 20 minutes
        "interactions": 15,
        "completion_rate": 0.8
    }
    evaluator.record_session(session1)
    
    session2 = {
        "time_spent": 1800,  # 30 minutes
        "interactions": 25,
        "completion_rate": 1.0
    }
    evaluator.record_session(session2)
    
    # Sample quiz history
    quiz_history = [
        {"topic": "Python", "accuracy": 0.5, "timestamp": datetime.now().isoformat()},
        {"topic": "Python", "accuracy": 0.6, "timestamp": datetime.now().isoformat()},
        {"topic": "Python", "accuracy": 0.75, "timestamp": datetime.now().isoformat()},
    ]
    
    # Sample learner profile
    learner_profile = {
        "proficiency_level": "intermediate",
        "learning_style": "visual"
    }
    
    # Generate report
    report = evaluator.generate_report(learner_profile, quiz_history)
    
    print("="*60)
    print("EVALUATION REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))
