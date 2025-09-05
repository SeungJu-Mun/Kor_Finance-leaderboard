import os
import argparse
import pandas as pd
import openai
from vllm import LLM, SamplingParams
from langchain.schema import HumanMessage

parser = argparse.ArgumentParser()
parser.add_argument('--model', help=' : Model to evaluate', default='사용 할 모델명')
parser.add_argument('--model_len', help=' : Maximum Model Length', default=4096, type=int)
args = parser.parse_args()

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "open-api key"))

df_questions = pd.read_json('../dataset/evaluation_data/FinBench.jsonl', lines=True)

single_turn_outputs = []

for question in df_questions['questions']:
    messages = [
    {"role": "system", "content": 'You are an AI assistant. You will be given a task. You must generate a detailed and long answer.'},
    {"role": "user", "content": str(question)}]
    response = client.chat.completions.create(
        model=args.model,
        messages=messages,
        max_tokens=args.model_len,
    )
    single_turn_outputs.append(response.choices[0].message.content)

df_output = pd.DataFrame({
    'id': df_questions['id'],
    'category': df_questions['category'],
    'questions': df_questions['questions'],
    'outputs': list(zip(single_turn_outputs)),
    'references': df_questions['references']
})

df_output.to_json(
    f'{str(args.model).replace("/", "_")}.jsonl',
    orient='records',
    lines=True,
    force_ascii=False
)
