"""
Practice Agent for EduPath (ACT phase).

Generates contextual practice sessions (MCQ & Short Answer) and evaluates learner submissions deterministically.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from ai.agents.base_agent import BaseAgent
from app.schemas.practice import (
    LearnerAnswerItem,
    PracticeQuestion,
    PracticeQuestionPublic,
    PracticeResultRecord,
    PracticeSession,
    QuestionEvaluationResult,
)
from app.utils.logger import logger
from app.utils.skill_normalizer import normalize_skill_name

# Curated foundational practice question dataset
DETERMINISTIC_PRACTICE_BANK: Dict[str, List[PracticeQuestion]] = {
    "Python": [
        PracticeQuestion(
            question_id="q_py_101",
            question="Which built-in Python data structure is immutable?",
            question_type="mcq",
            options=["List", "Tuple", "Dictionary", "Set"],
            correct_answer="Tuple",
            explanation="Tuples are immutable sequence types in Python whose elements cannot be modified after creation.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_102",
            question="Which block construct in Python is used to handle runtime exceptions?",
            question_type="mcq",
            options=["try / except", "catch / throw", "do / handle", "try / catch"],
            correct_answer="try / except",
            explanation="Python uses 'try' to execute risky code and 'except' to handle exceptions.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_103",
            question="Which built-in function returns the number of items in a list or container?",
            question_type="mcq",
            options=["len()", "count()", "size()", "length()"],
            correct_answer="len()",
            explanation="len() returns the total number of elements in a sequence or collection.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_104",
            question="Which keyword is used to declare a function definition in Python?",
            question_type="mcq",
            options=["def", "function", "fn", "define"],
            correct_answer="def",
            explanation="Function definitions start with the 'def' keyword followed by function name and parameters.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_105",
            question="What boolean value does bool([]) evaluate to in Python?",
            question_type="mcq",
            options=["False", "True", "None", "Error"],
            correct_answer="False",
            explanation="Empty sequences (lists, tuples, strings) evaluate to False in a boolean context.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_106",
            question="Which standard module provides basic mathematical functions such as sqrt and log?",
            question_type="mcq",
            options=["math", "cmath", "calc", "numbers"],
            correct_answer="math",
            explanation="The standard 'math' module contains functions for floating-point math operations.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_107",
            question="Which literal syntax creates an empty key-value dictionary in Python?",
            question_type="mcq",
            options=["{}", "[]", "()", "<>"],
            correct_answer="{}",
            explanation="Curly braces {} define dictionary literals in Python.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_108",
            question="Which operator performs floor (integer) division in Python?",
            question_type="mcq",
            options=["//", "/", "%", "**"],
            correct_answer="//",
            explanation="The '//' operator divides operands and rounds down to the nearest integer.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_109",
            question="Which keyword initiates an iterative loop over an iterable object in Python?",
            question_type="mcq",
            options=["for", "loop", "repeat", "foreach"],
            correct_answer="for",
            explanation="Python's 'for' statement iterates over items of any sequence or iterable.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_py_110",
            question="What is the correct syntax to import the standard json module in Python?",
            question_type="mcq",
            options=["import json", "include json", "require json", "using json"],
            correct_answer="import json",
            explanation="The 'import' statement is used to load external or standard modules.",
            difficulty="beginner",
        ),
    ],
    "Statistics": [
        PracticeQuestion(
            question_id="q_stat_101",
            question="What measure of central tendency represents the arithmetic average of a dataset?",
            question_type="mcq",
            options=["Median", "Mean", "Mode", "Standard Deviation"],
            correct_answer="Mean",
            explanation="The mean is computed by summing all values and dividing by the total count.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_stat_102",
            question="Which statistical metric measures the spread or dispersion of data around the mean?",
            question_type="mcq",
            options=["Standard Deviation", "Correlation", "Skewness", "Percentile"],
            correct_answer="Standard Deviation",
            explanation="Standard deviation measures how spread out numbers are from the mean.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_stat_103",
            question="In hypothesis testing, what does a p-value less than 0.05 typically indicate?",
            question_type="mcq",
            options=["Reject Null Hypothesis", "Accept Null Hypothesis", "Inconclusive Data", "Zero Variance"],
            correct_answer="Reject Null Hypothesis",
            explanation="A p-value < 0.05 indicates strong evidence against the null hypothesis, suggesting statistical significance.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_stat_104",
            question="What type of distribution is symmetric and bell-shaped?",
            question_type="mcq",
            options=["Uniform Distribution", "Normal Distribution", "Binomial Distribution", "Poisson Distribution"],
            correct_answer="Normal Distribution",
            explanation="The Normal (Gaussian) distribution is symmetric and bell-shaped with equal mean, median, and mode.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_stat_105",
            question="What theorem states that the sample mean distribution approaches normal as sample size increases?",
            question_type="mcq",
            options=["Central Limit Theorem", "Bayes Theorem", "Law of Large Numbers", "Chebyshev Inequality"],
            correct_answer="Central Limit Theorem",
            explanation="The Central Limit Theorem establishes that sample means approximate a normal distribution for large samples.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_stat_106",
            question="Which term describes the probability of committing a Type I error?",
            question_type="mcq",
            options=["Alpha (α)", "Beta (β)", "Power", "Variance"],
            correct_answer="Alpha (α)",
            explanation="Alpha represents the significance level or probability of rejecting a true null hypothesis (Type I error).",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_stat_107",
            question="What metric measures the strength and direction of a linear relationship between two continuous variables?",
            question_type="mcq",
            options=["Pearson Correlation Coefficient", "Chi-Square", "ANOVA F-Statistic", "Interquartile Range"],
            correct_answer="Pearson Correlation Coefficient",
            explanation="Pearson's r ranges from -1 to +1 measuring linear correlation strength.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_stat_108",
            question="Which measure of dispersion represents the difference between the 75th and 25th percentiles?",
            question_type="mcq",
            options=["Interquartile Range (IQR)", "Standard Deviation", "Variance", "Range"],
            correct_answer="Interquartile Range (IQR)",
            explanation="IQR = Q3 - Q1, capturing the middle 50% of ordered data.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_stat_109",
            question="What statistical test compares the means of more than two independent groups?",
            question_type="mcq",
            options=["One-Way ANOVA", "Student's t-test", "Chi-Square Test", "Mann-Whitney U Test"],
            correct_answer="One-Way ANOVA",
            explanation="ANOVA (Analysis of Variance) tests for significant mean differences across 3+ groups.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_stat_110",
            question="In linear regression, what statistic represents the proportion of target variance explained by the model?",
            question_type="mcq",
            options=["R-squared (R²)", "Root Mean Squared Error (RMSE)", "P-value", "Adjusted Alpha"],
            correct_answer="R-squared (R²)",
            explanation="R² indicates the fraction of variance in the dependent variable explained by independent variables.",
            difficulty="intermediate",
        ),
    ],
    "Probability": [
        PracticeQuestion(
            question_id="q_prob_101",
            question="What is the probability of rolling an even number on a fair 6-sided die?",
            question_type="mcq",
            options=["1/6", "1/2", "1/3", "2/3"],
            correct_answer="1/2",
            explanation="There are 3 even numbers (2, 4, 6) out of 6 possible outcomes, so 3/6 = 1/2.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_prob_102",
            question="What theorem calculates conditional probability P(A|B) using P(B|A), P(A), and P(B)?",
            question_type="mcq",
            options=["Bayes Theorem", "Central Limit Theorem", "Law of Large Numbers", "Markov Inequality"],
            correct_answer="Bayes Theorem",
            explanation="Bayes' Theorem provides a mathematical formula for determining conditional probability.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_prob_103",
            question="If two events A and B are independent, what is P(A and B)?",
            question_type="mcq",
            options=["P(A) * P(B)", "P(A) + P(B)", "P(A) / P(B)", "P(A|B)"],
            correct_answer="P(A) * P(B)",
            explanation="For independent events, the joint probability is the product of their individual probabilities.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_prob_104",
            question="What is the sum of all probabilities in a complete sample space?",
            question_type="mcq",
            options=["1.0", "0.5", "100", "0.0"],
            correct_answer="1.0",
            explanation="The total probability of all mutually exclusive events in a sample space equals 1.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_prob_105",
            question="Which probability distribution models the number of successes in n independent Bernoulli trials?",
            question_type="mcq",
            options=["Binomial Distribution", "Exponential Distribution", "Poisson Distribution", "Gaussian Distribution"],
            correct_answer="Binomial Distribution",
            explanation="The Binomial distribution specifies probabilities for n independent trials with constant success probability p.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_prob_106",
            question="What distribution models the number of rare events occurring in a fixed interval of time or space?",
            question_type="mcq",
            options=["Poisson Distribution", "Uniform Distribution", "Bernoulli Distribution", "Normal Distribution"],
            correct_answer="Poisson Distribution",
            explanation="The Poisson distribution describes the rate of independent rare events per interval.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_prob_107",
            question="What is the expected value of a fair 6-sided die roll?",
            question_type="mcq",
            options=["3.5", "3.0", "4.0", "3.6"],
            correct_answer="3.5",
            explanation="Expected value = (1+2+3+4+5+6)/6 = 21/6 = 3.5.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_prob_108",
            question="If P(A) = 0.4, what is the probability of the complement event P(A')?",
            question_type="mcq",
            options=["0.6", "0.4", "1.0", "0.0"],
            correct_answer="0.6",
            explanation="P(A') = 1 - P(A) = 1 - 0.4 = 0.6.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_prob_109",
            question="Which rule states that P(A or B) = P(A) + P(B) - P(A and B)?",
            question_type="mcq",
            options=["Addition Rule", "Multiplication Rule", "Chain Rule", "Bayes Rule"],
            correct_answer="Addition Rule",
            explanation="The General Addition Rule computes the probability of the union of two events.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_prob_110",
            question="What term describes events that cannot occur simultaneously?",
            question_type="mcq",
            options=["Mutually Exclusive", "Independent", "Correlated", "Continuous"],
            correct_answer="Mutually Exclusive",
            explanation="Mutually exclusive events have no overlapping outcomes (P(A and B) = 0).",
            difficulty="beginner",
        ),
    ],
    "Machine Learning": [
        PracticeQuestion(
            question_id="q_ml_101",
            question="What is supervised learning in machine learning?",
            question_type="mcq",
            options=["Training a model on labeled input-output pairs", "Clustering unlabelled data automatically", "Reinforcement through reward signals", "Generating random target outputs"],
            correct_answer="Training a model on labeled input-output pairs",
            explanation="Supervised learning algorithms learn a mapping from input features to target labels using labeled datasets.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_ml_102",
            question="What occurs when a machine learning model exhibits overfitting?",
            question_type="mcq",
            options=["Model performs well on training data but poorly on unseen test data", "Model performs poorly on both training and test datasets", "Model generalizes perfectly to any validation dataset", "Model training fails to converge due to high bias"],
            correct_answer="Model performs well on training data but poorly on unseen test data",
            explanation="Overfitting happens when a model learns noise and training details rather than general patterns.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_ml_103",
            question="What is the primary purpose of a validation dataset in ML training?",
            question_type="mcq",
            options=["Tuning hyperparameters and evaluating intermediate model performance", "Final deployment testing in production", "Training neural network weights directly", "Generating synthetic features for training"],
            correct_answer="Tuning hyperparameters and evaluating intermediate model performance",
            explanation="Validation sets provide an unbiased evaluation of a model fit during hyperparameter tuning.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_ml_104",
            question="What is K-fold cross-validation?",
            question_type="mcq",
            options=["Resampling dataset into K subsets to iteratively train and validate", "Splitting dataset into 80% train and 20% test once", "Training K separate models on K different servers", "Evaluating model inference speed K times"],
            correct_answer="Resampling dataset into K subsets to iteratively train and validate",
            explanation="K-fold cross-validation evaluates generalization performance across K distinct validation folds.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_ml_105",
            question="Which algorithm uses a sigmoid logistic function for binary classification?",
            question_type="mcq",
            options=["Logistic Regression", "Linear Regression", "K-Means Clustering", "Principal Component Analysis"],
            correct_answer="Logistic Regression",
            explanation="Logistic regression maps linear combinations of features to probabilities using the logistic sigmoid function.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_ml_106",
            question="What is gradient descent in machine learning optimization?",
            question_type="mcq",
            options=["Iterative algorithm updating weights in direction of steepest loss decrease", "Random parameter search across feature space", "Technique for removing noisy outliers from datasets", "Method for encoding categorical strings"],
            correct_answer="Iterative algorithm updating weights in direction of steepest loss decrease",
            explanation="Gradient descent iteratively moves model parameters toward lower loss values.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_ml_107",
            question="What defines unsupervised machine learning?",
            question_type="mcq",
            options=["Discovering hidden structures or clusters in unlabeled data", "Predicting continuous values from target labels", "Manual rule-based decision tree construction", "Training using real-time user click feedback"],
            correct_answer="Discovering hidden structures or clusters in unlabeled data",
            explanation="Unsupervised algorithms find intrinsic patterns (e.g. clusters) without target labels.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_ml_108",
            question="What role does L1 / L2 regularization play in machine learning models?",
            question_type="mcq",
            options=["Penalizes large weight coefficients to prevent overfitting", "Increases training set size automatically", "Speeds up data loading throughput", "Converts multi-class problems to binary problems"],
            correct_answer="Penalizes large weight coefficients to prevent overfitting",
            explanation="Regularization adds a penalty term to the loss function to constrain parameter complexity.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_ml_109",
            question="What metric measures the fraction of true positives among all positive predictions?",
            question_type="mcq",
            options=["Precision", "Recall", "Accuracy", "Mean Absolute Error"],
            correct_answer="Precision",
            explanation="Precision = True Positives / (True Positives + False Positives).",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_ml_110",
            question="Which ensemble algorithm constructs multiple decision trees using random feature subsets?",
            question_type="mcq",
            options=["Random Forest", "Support Vector Machine", "Naive Bayes", "K-Nearest Neighbors"],
            correct_answer="Random Forest",
            explanation="Random Forest averages predictions from an ensemble of randomized decision trees.",
            difficulty="intermediate",
        ),
    ],
    "Deep Learning": [
        PracticeQuestion(
            question_id="q_dl_101",
            question="What is the primary role of an activation function in a neural network?",
            question_type="mcq",
            options=["Introducing non-linearity to learn complex non-linear patterns", "Normalizing input batch values to zero mean", "Saving weight parameters to disk", "Calculating the learning rate dynamically"],
            correct_answer="Introducing non-linearity to learn complex non-linear patterns",
            explanation="Without non-linear activation functions, a deep neural network behaves like a single linear model.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_dl_102",
            question="What is backpropagation in deep learning?",
            question_type="mcq",
            options=["Computing gradients of loss with respect to weights using chain rule", "Forwarding input data through hidden layers to produce output", "Shuffling training dataset batches randomly", "Pruning unused neurons from deep networks"],
            correct_answer="Computing gradients of loss with respect to weights using chain rule",
            explanation="Backpropagation applies the calculus chain rule backward from loss to update all trainable weights.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_dl_103",
            question="Which neural network architecture is tailored for grid-structured spatial data like images?",
            question_type="mcq",
            options=["Convolutional Neural Network (CNN)", "Recurrent Neural Network (RNN)", "Multilayer Perceptron (MLP)", "Autoencoder"],
            correct_answer="Convolutional Neural Network (CNN)",
            explanation="CNNs utilize spatial convolution kernels to effectively extract local feature hierarchies in visual data.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_dl_104",
            question="Which architecture relies on self-attention mechanisms to process sequential text data efficiently?",
            question_type="mcq",
            options=["Transformer", "Convolutional Network", "Decision Tree", "Support Vector Machine"],
            correct_answer="Transformer",
            explanation="Transformers process sequence tokens in parallel via self-attention mechanisms.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_dl_105",
            question="What is dropout in neural network regularization?",
            question_type="mcq",
            options=["Randomly zeroing out a fraction of neuron outputs during training", "Dropping corrupt dataset rows during data loading", "Reducing model precision from FP32 to INT8", "Stopping training early when validation loss rises"],
            correct_answer="Randomly zeroing out a fraction of neuron outputs during training",
            explanation="Dropout prevents co-adaptation of features by deactivating random units during forward passes.",
            difficulty="beginner",
        ),
    ],
    "Data Processing": [
        PracticeQuestion(
            question_id="q_dp_101",
            question="What is feature standardization (Z-score normalization)?",
            question_type="mcq",
            options=["Rescaling features to have mean=0 and standard deviation=1", "Bounding numerical values strictly between 0 and 1", "Replacing missing values with zero", "Converting string categories into numbers"],
            correct_answer="Rescaling features to have mean=0 and standard deviation=1",
            explanation="Standardization computes (x - mean) / std to produce zero-centered unit variance features.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_dp_102",
            question="What encoding method creates binary indicator columns for categorical variables?",
            question_type="mcq",
            options=["One-Hot Encoding", "Label Encoding", "Target Encoding", "Ordinal Encoding"],
            correct_answer="One-Hot Encoding",
            explanation="One-Hot Encoding converts each distinct category into a binary column flag.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_dp_103",
            question="What is data leakage in machine learning preprocessing?",
            question_type="mcq",
            options=["Using test dataset information during model training or preprocessing", "Exporting unencrypted datasets to public S3 buckets", "Loss of feature columns during dataframe joins", "Dropping rows containing missing null values"],
            correct_answer="Using test dataset information during model training or preprocessing",
            explanation="Data leakage occurs when test target information leaks into training feature engineering.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_dp_104",
            question="Which dimensionality reduction algorithm projects data onto orthogonal axes of maximum variance?",
            question_type="mcq",
            options=["Principal Component Analysis (PCA)", "K-Means", "Linear Regression", "Random Forest"],
            correct_answer="Principal Component Analysis (PCA)",
            explanation="PCA identifies orthogonal principal components that capture maximum variance in high-dimensional data.",
            difficulty="intermediate",
        ),
        PracticeQuestion(
            question_id="q_dp_105",
            question="What method handles severe target class imbalance in classification datasets?",
            question_type="mcq",
            options=["SMOTE or Class-weighted loss functions", "Dropping minority class rows", "Ignoring minority class accuracy", "Disabling model validation"],
            correct_answer="SMOTE or Class-weighted loss functions",
            explanation="Synthetic Minority Over-sampling (SMOTE) and class weighting balance model sensitivity.",
            difficulty="beginner",
        ),
    ],
    "MLOps": [
        PracticeQuestion(
            question_id="q_mlops_101",
            question="What is the main objective of MLOps practice?",
            question_type="mcq",
            options=["Standardizing ML deployment, tracking, and continuous monitoring", "Replacing data engineers with automated scripts", "Eliminating model evaluation in production", "Writing ML code in C++ only"],
            correct_answer="Standardizing ML deployment, tracking, and continuous monitoring",
            explanation="MLOps integrates ML development with DevOps workflows for reliable operational deployment.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_mlops_102",
            question="What phenomenon describes performance degradation when real-world data distribution shifts over time?",
            question_type="mcq",
            options=["Model / Data Drift", "Overfitting", "Gradient Explosion", "Dead Neurons"],
            correct_answer="Model / Data Drift",
            explanation="Drift occurs when production input statistical distributions change relative to training data.",
            difficulty="beginner",
        ),
        PracticeQuestion(
            question_id="q_mlops_103",
            question="What infrastructure component acts as a central repository for serving standardized features to ML models?",
            question_type="mcq",
            options=["Feature Store", "Model Registry", "API Gateway", "Message Queue"],
            correct_answer="Feature Store",
            explanation="Feature Stores maintain consistent features across training and real-time online inference.",
            difficulty="intermediate",
        ),
    ],
}


class PracticeAgent(BaseAgent):
    """
    Generates structured practice sessions and evaluates learner answer submissions.
    """

    def __init__(self, provider=None):
        super().__init__(
            name="PracticeAgent",
            description="Synthesizes targeted practice tasks, MCQs, and evaluates learner submissions with detailed feedback.",
            provider=provider,
        )

    def _generate_synthetic_questions(self, skill_name: str, needed_count: int, start_idx: int) -> List[PracticeQuestion]:
        """Synthesizes targeted practice questions for any skill topic to fulfill exact required count."""
        questions = []
        topics_pool = [
            f"Core Concepts of {skill_name}",
            f"Practical Application of {skill_name}",
            f"Best Practices in {skill_name}",
            f"Advanced Techniques in {skill_name}",
            f"Troubleshooting & Debugging {skill_name}",
            f"Architecture & Design for {skill_name}",
            f"Performance Optimization in {skill_name}",
            f"Security & Reliability in {skill_name}",
            f"Integration Patterns with {skill_name}",
            f"Evaluation Metrics for {skill_name}",
        ]
        
        for i in range(needed_count):
            idx = start_idx + i + 1
            topic_str = topics_pool[i % len(topics_pool)]
            q_id = f"q_{skill_name.lower().replace(' ', '_')}_{idx}"
            
            q = PracticeQuestion(
                question_id=q_id,
                question=f"Which key principle is essential for {topic_str}?",
                question_type="mcq",
                options=[
                    f"Applying standard benchmark methodology for {skill_name}",
                    f"Disregarding requirements and using arbitrary defaults",
                    f"Executing unverified manual modifications",
                    f"Bypassing evaluation and validation steps",
                ],
                correct_answer=f"Applying standard benchmark methodology for {skill_name}",
                explanation=f"Applying standard benchmark methodology for {skill_name} ensures correctness and reliability.",
                difficulty="beginner" if idx % 2 == 1 else "intermediate",
            )
            questions.append(q)
        return questions

    def generate_practice_session(
        self,
        user_id: str,
        task_id: str,
        skill_name: str,
        difficulty: str = "beginner",
        practice_mode: str = "general",
        module_id: Optional[str] = None,
        skills: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generates/selects practice questions for a learning task.
        Enforces EXACT question counts: 10 questions for general mode, 5 questions for module mode.
        General mode mixes questions across learner's improvement skills without module constraint.
        """
        target_count = 10 if practice_mode == "general" else 5

        if practice_mode == "general":
            module_id = None
            target_skills = [s.strip() for s in skills if s and s.strip()] if skills else [skill_name]
            if not target_skills or target_skills == ["General"]:
                target_skills = ["Machine Learning", "Statistics", "Probability", "Model Evaluation", "MLOps"]

            # Distribute 10 questions across target improvement skills
            selected_questions: List[PracticeQuestion] = []
            per_skill = max(1, target_count // len(target_skills))

            for s_name in target_skills:
                norm_s = normalize_skill_name(s_name)
                bank: List[PracticeQuestion] = []
                for key, q_list in DETERMINISTIC_PRACTICE_BANK.items():
                    if key.lower() == norm_s.lower() or key.lower() in norm_s.lower() or norm_s.lower() in key.lower():
                        bank = list(q_list)
                        break

                s_qs = list(bank[:per_skill])
                if len(s_qs) < per_skill:
                    synth = self._generate_synthetic_questions(s_name, per_skill - len(s_qs), len(s_qs))
                    s_qs.extend(synth)

                for q in s_qs:
                    q.skill_name = s_name
                    if not q.topic:
                        q.topic = f"{s_name} Core Concepts"

                selected_questions.extend(s_qs[:per_skill])

            # If still fewer than target_count (due to integer rounding), fill with top skill
            if len(selected_questions) < target_count:
                fill_skill = target_skills[0]
                needed = target_count - len(selected_questions)
                synth = self._generate_synthetic_questions(fill_skill, needed, len(selected_questions))
                for q in synth:
                    q.skill_name = fill_skill
                    q.topic = f"{fill_skill} Core Concepts"
                selected_questions.extend(synth)

            selected_questions = selected_questions[:target_count]
            topic = f"General Practice ({', '.join(target_skills[:3])} - 10 Questions)"
        else:
            # Module Mode: 5 questions strictly for selected module skill
            norm_skill = normalize_skill_name(skill_name)
            bank: List[PracticeQuestion] = []
            for key, q_list in DETERMINISTIC_PRACTICE_BANK.items():
                if key.lower() == norm_skill.lower() or key.lower() in norm_skill.lower() or norm_skill.lower() in key.lower():
                    bank = list(q_list)
                    break

            selected_questions = list(bank[:target_count])
            if len(selected_questions) < target_count:
                needed = target_count - len(selected_questions)
                synth_qs = self._generate_synthetic_questions(skill_name, needed, len(selected_questions))
                selected_questions.extend(synth_qs)

            selected_questions = selected_questions[:target_count]
            for q in selected_questions:
                q.skill_name = skill_name
                if not q.topic:
                    q.topic = f"{skill_name} Core Concepts"

            topic = f"{skill_name} (Module Practice - 5 Questions)"

        practice_id = f"prac_{uuid.uuid4().hex[:10]}"

        # Create public version of questions omitting correct answers but including skill_name and topic
        public_questions = [
            PracticeQuestionPublic(
                question_id=q.question_id,
                question=q.question,
                question_type=q.question_type,
                options=q.options,
                difficulty=q.difficulty,
                skill_name=q.skill_name or skill_name,
                topic=q.topic or f"{skill_name} Core Concepts",
            )
            for q in selected_questions
        ]

        session = PracticeSession(
            practice_id=practice_id,
            user_id=user_id,
            task_id=task_id,
            module_id=module_id,
            skill_name=skill_name,
            topic=topic,
            difficulty=difficulty,
            practice_mode=practice_mode,
            questions=public_questions,
            created_at=datetime.utcnow().isoformat(),
        )

        return {
            "session_data": session.model_dump(),
            "full_questions": [q.model_dump() for q in selected_questions],
        }

    def evaluate_submission(
        self,
        session_data: Dict[str, Any],
        full_questions: List[Dict[str, Any]],
        submitted_answers: List[Dict[str, Any]],
    ) -> PracticeResultRecord:
        """
        Evaluates learner's submitted answers against authoritative question correct_answer values.
        Computes score, total, percentage, and per-question explanation.
        """
        answers_map = {a["question_id"]: a.get("learner_answer", "").strip() for a in submitted_answers}
        question_results: List[QuestionEvaluationResult] = []
        score = 0

        for q in full_questions:
            q_id = q["question_id"]
            correct_ans = q["correct_answer"].strip()
            learner_ans = answers_map.get(q_id, "").strip()

            # Case-insensitive substring or exact match comparison
            is_correct = False
            if q.get("question_type") == "mcq":
                is_correct = learner_ans.lower() == correct_ans.lower()
            else:
                # Short answer flexible keyword check
                is_correct = (learner_ans.lower() == correct_ans.lower()) or (
                    len(learner_ans) > 2 and learner_ans.lower() in correct_ans.lower()
                ) or (len(correct_ans) > 2 and correct_ans.lower() in learner_ans.lower())

            if is_correct:
                score += 1

            question_results.append(
                QuestionEvaluationResult(
                    question_id=q_id,
                    question=q["question"],
                    correct=is_correct,
                    learner_answer=learner_ans if learner_ans else "No answer provided",
                    correct_answer=correct_ans,
                    explanation=q["explanation"],
                )
            )

        total_questions = len(full_questions)
        percentage = round((score / total_questions) * 100.0, 1) if total_questions > 0 else 0.0
        result_id = f"res_{uuid.uuid4().hex[:10]}"

        record = PracticeResultRecord(
            result_id=result_id,
            user_id=session_data["user_id"],
            practice_id=session_data["practice_id"],
            task_id=session_data["task_id"],
            skill_name=session_data["skill_name"],
            topic=session_data["topic"],
            difficulty=session_data["difficulty"],
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            question_results=question_results,
            completed_at=datetime.utcnow().isoformat(),
        )

        return record

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Base agent execute entry point."""
        mode = inputs.get("mode")
        if mode == "generate":
            res = self.generate_practice_session(
                user_id=inputs.get("user_id", "demo_user_1"),
                task_id=inputs.get("task_id", "task_01"),
                skill_name=inputs.get("skill_name", "Python"),
                difficulty=inputs.get("difficulty", "beginner"),
            )
            return res["session_data"]
        elif mode == "evaluate":
            record = self.evaluate_submission(
                session_data=inputs.get("session_data", {}),
                full_questions=inputs.get("full_questions", []),
                submitted_answers=inputs.get("submitted_answers", []),
            )
            return record.model_dump()
        else:
            raise ValueError("PracticeAgent execution mode must be 'generate' or 'evaluate'.")
