import asyncio
from typing import Dict, Any, Tuple
from jinja2 import Environment, StrictUndefined

from alpha_codium.gen.stages.run_baseline import run_baseline
from alpha_codium.gen.stages.run_choose_best_solution import run_choose_best_solution
from alpha_codium.gen.stages.run_evaluate_all_ai_tests import run_evaluate_all_ai_tests
from alpha_codium.gen.stages.run_evaluate_public_tests import run_evaluate_public_tests
from alpha_codium.gen.stages.run_generate_ai_test import run_generate_ai_tests
from alpha_codium.gen.stages.run_generate_possible_solutions import run_generate_possible_solutions
from alpha_codium.gen.stages.run_self_reflect import run_self_reflect
from alpha_codium.gen.stages.run_initial_code_generation import run_initial_code_generation
from alpha_codium.gen.stages.utils import set_configurations
from alpha_codium.llm.ai_handler import AiHandler
from alpha_codium.log import get_logger
from alpha_codium.settings.config_loader import get_settings


class ProblemSolver:
    """
    A class that implements the AlphaCodium approach to solve programming problems.
    This is a simplified version of the CodeContestsCompetitor class that focuses
    on the core functionality.
    """
    
    def __init__(self):
        """Initialize the ProblemSolver."""
        self.prompt = {}
        for set in get_settings():
            if 'code_contests_prompt' in set.lower():
                self.prompt[set.lower()] = get_settings()[set]
        self.ai_handler = AiHandler()
        self.logger = get_logger(__name__)

    def render(self, problem_json: Dict[str, Any], prompt: str) -> Tuple[str, str, float, float]:
        """
        Render the prompt templates with the problem data.
        
        Args:
            problem_json: The problem data
            prompt: The name of the prompt template to use
            
        Returns:
            A tuple containing (system_prompt, user_prompt, temperature, frequency_penalty)
        """
        environment = Environment(undefined=StrictUndefined)
        environment.globals["zip"] = zip
        environment.globals["enumerate"] = enumerate
        
        sys_prompt = environment.from_string(self.prompt[prompt].system).render(problem_json)
        usr_prompt = environment.from_string(self.prompt[prompt].user).render(problem_json)
        
        temperature = getattr(self.prompt[prompt], 'temperature', 0.2)
        frequency_penalty = getattr(self.prompt[prompt], 'frequency_penalty', 0)
        
        return sys_prompt, usr_prompt, temperature, frequency_penalty

    async def _run(self, model: str, problem: Dict[str, Any], prompt: str = "code_contests_prompt_reflect") -> Tuple[str, str]:
        """
        Run a single prompt through the AI model.
        
        Args:
            model: The model to use
            problem: The problem data
            prompt: The name of the prompt template to use
            
        Returns:
            A tuple containing (response, finish_reason)
        """
        system_prompt, user_prompt, temperature, frequency_penalty = self.render(problem, prompt)

        response, finish_reason = await self.ai_handler.chat_completion(
            model=model, system=system_prompt, user=user_prompt,
            temperature=temperature, frequency_penalty=frequency_penalty,
        )
        return response, finish_reason

    async def solve(self, problem: Dict[str, Any], iteration: int = 0) -> str:
        """
        Solve a programming problem using the AlphaCodium approach.
        
        Args:
            problem: The problem data
            iteration: The iteration number (for randomness)
            
        Returns:
            The solution code
        """
        self.logger.info(f"Solving problem using model {get_settings().config['model']}")

        try:
            if get_settings().get("solve.use_baseline", False):
                # Simple baseline approach (single prompt)
                problem['code_recent_solution'] = await run_baseline(self, problem)
            else:
                # Full AlphaCodium approach
                
                # Set configurations based on iteration
                problem = set_configurations(problem, iteration)

                # Step 1: Self-reflection on the problem
                problem = await run_self_reflect(self, problem)

                # Step 2: Generate multiple possible solutions
                problem = await run_generate_possible_solutions(self, problem)

                # Step 3: Choose the best solution
                problem = await run_choose_best_solution(self, problem)

                # Step 4: Generate AI tests
                problem = await run_generate_ai_tests(self, problem)

                # Step 5: Initial code generation
                problem = await run_initial_code_generation(self, problem)

                # Step 6: Evaluate on public tests
                problem = await run_evaluate_public_tests(self, problem)

                # Step 7: Evaluate on AI tests
                problem = await run_evaluate_all_ai_tests(self, problem)

            return problem['code_recent_solution']
        except Exception as e:
            self.logger.error(f"Error solving problem: {e}")
            return ""

    def solve_problem(self, problem: Dict[str, Any], iteration: int = 0) -> str:
        """
        Synchronous wrapper for the solve method.
        
        Args:
            problem: The problem data
            iteration: The iteration number (for randomness)
            
        Returns:
            The solution code
        """
        return asyncio.run(self.solve(problem=problem, iteration=iteration))