from veadk.evaluation.adk_evaluator import ADKEvaluator
from veadk.evaluation.deepeval_evaluator import DeepevalEvaluator
from veadk.prompts.prompt_evaluator import eval_principle_prompt
from deepeval.metrics import GEval, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCaseParams
import pytest
from ecommerce_agent.agent import root_agent


class TestAgentEvaluation:
    @pytest.mark.asyncio
    async def test_simple_evalset_with_adkevaluator(self):
        """Agent evaluation tests using ADKEvaluator"""
        evaluator = ADKEvaluator(agent=root_agent)
        await evaluator.evaluate(
            eval_set_file_path="tests/simple.test.json",
            response_match_score_threshold=1,
            tool_score_threshold=0.5,
            num_runs=1,
            print_detailed_results=True,
        )

    @pytest.mark.asyncio
    async def test_complex_evalset_with_adkevaluator(self):
        """Agent evaluation tests using ADKEvaluator"""
        evaluator = ADKEvaluator(agent=root_agent)
        await evaluator.evaluate(
            eval_set_file_path="tests/complex.test.json",
            response_match_score_threshold=1,
            tool_score_threshold=0.5,
            num_runs=1,
            print_detailed_results=True,
        )        

    @pytest.mark.asyncio
    async def test_simple_evalset_with_deepevalevaluator(self):
        """Agent evaluation tests using DeepevalEvaluator"""
        evaluator = DeepevalEvaluator(agent=root_agent)
        metrics = [
            GEval(
                threshold=0.8,
                name="Base Evaluation",
                criteria=eval_principle_prompt,
                evaluation_params=[
                    LLMTestCaseParams.INPUT,
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                    LLMTestCaseParams.EXPECTED_OUTPUT,
                ],
                model=evaluator.judge_model,
            ),
            ToolCorrectnessMetric(threshold=0.5,model=evaluator.judge_model),
        ]
        await evaluator.evaluate(
            eval_set_file_path="tests/simple.test.json", metrics=metrics
        )

    @pytest.mark.asyncio
    async def test_complex_evalset_with_deepevalevaluator(self):
        """Agent evaluation tests using DeepevalEvaluator"""
        evaluator = DeepevalEvaluator(agent=root_agent)
        metrics = [
            GEval(
                threshold=0.8,
                name="Base Evaluation",
                criteria=eval_principle_prompt,
                evaluation_params=[
                    LLMTestCaseParams.INPUT,
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                    LLMTestCaseParams.EXPECTED_OUTPUT,
                ],
                model=evaluator.judge_model,
            ),
            ToolCorrectnessMetric(threshold=0.5,model=evaluator.judge_model),
        ]
        await evaluator.evaluate(
            eval_set_file_path="tests/complex.test.json", metrics=metrics
        )        


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
