from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent


def run_pipeline(grade, topic):
    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    # Step 1: Generate
    initial_output = generator.generate(grade, topic)

    # Step 2: Review
    review = reviewer.review(initial_output, grade)

    refined_output = None

    # Step 3: Refinement (ONLY ONCE)
    if review["status"] == "fail":
        refined_output = generator.generate(
            grade,
            topic,
            feedback=review["feedback"]
        )

    return {
        "initial": initial_output,
        "review": review,
        "refined": refined_output
    }
