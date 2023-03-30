import time
import torch
import argparse
import pandas
import json
import transformers
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering


def clean(question):
    tokens = question.split(" ")
    tokens = ["".join([char.lower() for char in token if char.isalpha()])
              for token in tokens]
    return " ".join(tokens)


def import_squad_data():
    """
    Downloads the SQuAD dev-v2 dataset and organises it into a more
    convenient pandas dataframe.
    See https://rajpurkar.github.io/SQuAD-explorer/
    for more details on SQuAD.
    """
    squad_file = "./dev-v2.0.json"

    with open(squad_file) as squad_file_handle:
        squad_data = json.load(squad_file_handle)["data"]

        title_list = []
        ident_list = []
        context_list = []
        question_list = []
        impossible_list = []
        answer_start_list = []
        answer_text_list = []

        # 'data' contains title and paragraph list
        for it_art in squad_data:
            title = it_art["title"]

            # 'paragraphs' contains context (the copy) and Q&A sets
            for it_par in it_art["paragraphs"]:
                context = it_par["context"]

                # 'qas' contains questions and reference answers
                for it_que in it_par["qas"]:
                    question = it_que["question"]
                    impossible = it_que["is_impossible"]
                    ident = it_que["id"]

                    # 'answers' contains the answer text and location in 'context'
                    for it_ans in it_que["answers"]:
                        answer_start = it_ans["answer_start"]
                        text = it_ans["text"]

                        # set an empty answer for an impossible question
                        if impossible:
                            text = ""

                        # add details of this answer to the list
                        title_list.append(title)
                        ident_list.append(ident)
                        context_list.append(context)
                        question_list.append(question)
                        impossible_list.append(impossible)
                        answer_start_list.append(answer_start)
                        answer_text_list.append(text)

    squad_data_final = pandas.DataFrame(
            {
                "id": ident_list,
                "subject": title_list,
                "context": context_list,
                "question": question_list,
                "clean_question": [clean(question) for question in question_list],
                "impossible": impossible_list,
                "answer_start": answer_start_list,
                "answer": answer_text_list,
            }
        )

    return squad_data_final.drop_duplicates(keep="first")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bf16", action="store_true", required=False, help="fast math mode")
    args = parser.parse_args()

    if args.bf16 is True:
        torch.set_float32_matmul_precision("medium")

    squad_data = import_squad_data()

    token = DistilBertTokenizer.from_pretrained(
        "distilbert-base-uncased", return_token_type_ids=True)
    model = DistilBertForQuestionAnswering.from_pretrained(
        "distilbert-base-uncased-distilled-squad")

    input_ids = []
    attention_masks = []
    for i in range(8):
        item = squad_data.iloc[i]
        encoding = token.encode_plus(
            item["question"],
            item["context"],
            max_length=512, truncation=True
        )

        input_ids.append(encoding["input_ids"])
        attention_masks.append(encoding["attention_mask"])

    model.eval()
    with torch.inference_mode():
        
        # warmup
        start_scores, end_scores = model(
            torch.tensor([input_ids[0] for _ in range(64)]),
            attention_mask=torch.tensor([attention_masks[0] for _ in range(64)]),
            return_dict=False,
        )

        s = time.time()
        for i in range(8):
            start_scores, end_scores = model(
                torch.tensor([input_ids[i] for _ in range(64)]),
                attention_mask=torch.tensor([attention_masks[i] for _ in range(64)]),
                return_dict=False,
            )
        e = time.time()
        print(f"TARGET bert Time {e-s} s")
