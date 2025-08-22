#!/usr/bin/env python3
"""
Demo of the Self-Reflection Certainty library.

This shows how to use the library to evaluate answer trustworthiness.
"""

import os
import sys

# Add the src directory to the path so we can import our library
sys.path.insert(0, 'src')

from self_reflection_certainty import SelfReflectionCertainty


def main():
    """Run the demo."""
    print("🚀 Self-Reflection Certainty Demo")
    print("=" * 50)
    
    # Check if API key is set
    if not os.getenv('LLM_API_KEY'):
        print("⚠️  No API key found!")
        print("   Set your API key first:")
        print("   export LLM_API_KEY='your-api-key'")
        print("   export LLM_MODEL='gpt-4'  # or any other model")
        print()
        print("   Then run: python demo.py")
        return
    
    print("✅ API key found, running demo...")
    print()
    
    # Create evaluator
    evaluator = SelfReflectionCertainty.from_env()
    
    # Demo 1: Evaluate a simple question
    print("📝 Demo 1: Evaluating a simple question")
    print("Question: What is the capital of France?")
    
    result = evaluator.evaluate_answer("What is the capital of France?")
    print(f"Answer: {result['answer']}")
    print(f"Certainty: {result['certainty_score']:.2f}")
    print()
    
    # Demo 2: Evaluate an existing answer
    print("📝 Demo 2: Evaluating an existing answer")
    print("Question: What is 2 + 2?")
    print("Answer: 2 + 2 equals 4")
    
    result = evaluator.evaluate_answer(
        question="What is 2 + 2?",
        answer="2 + 2 equals 4"
    )
    print(f"Certainty: {result['certainty_score']:.2f}")
    print(f"Trustworthy: {'Yes' if result['certainty_score'] >= 0.7 else 'No'}")
    print()
    
    # Demo 3: Trustworthiness check
    print("📝 Demo 3: Trustworthiness check")
    print("Question: What is the population of Tokyo?")
    print("Answer: Tokyo has a population of approximately 37 million people.")
    
    is_trustworthy, result = evaluator.is_trustworthy(
        question="What is the population of Tokyo?",
        answer="Tokyo has a population of approximately 37 million people.",
        threshold=0.8
    )
    
    print(f"Certainty: {result['certainty_score']:.2f}")
    print(f"Trustworthy (threshold 0.8): {'Yes' if is_trustworthy else 'No'}")
    print()
    
    print("🎉 Demo complete!")
    print("\nTo use in your own code:")
    print("  from self_reflection_certainty import SelfReflectionCertainty")
    print("  evaluator = SelfReflectionCertainty.from_env()")
    print("  result = evaluator.evaluate_answer('Your question here')")


if __name__ == "__main__":
    main()
