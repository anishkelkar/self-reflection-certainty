#!/usr/bin/env python3
"""
Demo of the Self-Reflection Certainty library.

This shows the full conversation flow: question → LLM answer → self-reflection → final score.
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
    
    # Create evaluator with debug mode enabled
    evaluator = SelfReflectionCertainty.from_env(debug=True)
    
    # Demo: Single question with full conversation flow
    question = "What is the capital of France?"
    print(f"Question: {question}")
    print()
    
    # Get the full result (debug info will be printed automatically)
    result = evaluator.evaluate_answer(question)
    
    print("🎉 Demo complete!")
    print("\nTo use in your own code:")
    print("  from self_reflection_certainty import SelfReflectionCertainty")
    print("  evaluator = SelfReflectionCertainty.from_env(debug=True)")
    print("  result = evaluator.evaluate_answer('Your question here')")


if __name__ == "__main__":
    main()
