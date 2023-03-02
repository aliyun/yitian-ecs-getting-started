import transformers
import torch
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import time
import argparse
import json
import pandas
import random


def parse_arguments():
    """
    Takes arguments from the command line and checks whether
    they have been parsed correctly
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-id",
        "--squadid",
        type=str,
        help="ID of SQuAD record to use. A record will be picked at random if unset",
        required=False,
    )
    parser.add_argument(
        "-s",
        "--subject",
        type=str,
        help="Pick a SQuAD question on the given subject at random",
        required=False,
    )
    parser.add_argument(
        "-t",
        "--text",
        type=str,
        help="Filename of a user-specified text file to answer questions on. Note: SQuAD id is ignored if set.",
        required=False,
    )
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        help="Question to ask about the user-provided text. Note: SQuAD id is ignored if set.",
        required=False,
    )
    parser.add_argument("--bf16", action="store_true", required=False, help="fast math mode")

    args = vars(parser.parse_args())

    return args


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
    args = parse_arguments()

    if args["bf16"] is True:
        torch.set_float32_matmul_precision("medium")

    source = ""
    subject = ""
    context = ""
    question = ""
    answer = ""
    squadid = ""

    if args:
        if "text" in args:
            if args["text"]:
                source = args["text"]
        if "subject" in args:
            if args["subject"]:
                subject = args["subject"]
        if "context" in args:
            if args["context"]:
                context = args["context"]
        if "question" in args:
            if args["question"]:
                question = args["question"]
                clean_question = clean(question)
        if "answer" in args:
            if args["answer"]:
                answer = args["answer"]
        if "squadid" in args:
            if args["squadid"]:
                squadid = args["squadid"]
    else:
        exit("Parser didn't return args correctly")

    if question:
        if source:
            with open(source, "r") as text_file_handle:
                context = text_file_handle.read()
        else:
            print("No text provided, searching SQuAD dev-2.0 dataset")
            squad_data = import_squad_data()
            squad_records = squad_data.loc[
                squad_data["clean_question"] == clean_question
            ]
            if squad_records.empty:
                exit(
                    "Question not found in SQuAD data, please provide context using `--text`."
                )
            subject = squad_records["subject"].iloc[0]
            context = squad_records["context"].iloc[0]
            question = squad_records["question"].iloc[0]
            answer = squad_records["answer"]
    else:
        squad_data = import_squad_data()

        if squadid:
            source = args["squadid"]
            squad_records = squad_data.loc[squad_data["id"] == source]
            i_record = 0
        else:
            if subject:
                print(
                    "Picking a question at random on the subject: ",
                    subject,
                )
                squad_records = squad_data.loc[
                    squad_data["subject"] == subject
                ]
            else:
                print(
                    "No SQuAD ID or question provided, picking one at random!"
                )
                squad_records = squad_data

            n_records = len(squad_records.index)
            i_record = random.randint(0, max(0, n_records - 1))

        if squad_records.empty:
            exit(
                "No questions found in SQuAD data, please provide valid ID or subject."
            )

        n_records = len(squad_records.index)
        # i_record = random.randint(0, n_records - 1)
        i_record = 1
        source = squad_records["id"].iloc[i_record]
        subject = squad_records["subject"].iloc[i_record]
        context = squad_records["context"].iloc[i_record]
        question = squad_records["question"].iloc[i_record]
        answer = squad_records["answer"].iloc[i_record]

    # DistilBERT question answering using pre-trained model.
    token = DistilBertTokenizer.from_pretrained(
        "distilbert-base-uncased", return_token_type_ids=True)

    model = DistilBertForQuestionAnswering.from_pretrained(
        "distilbert-base-uncased-distilled-squad")

    encoding = token.encode_plus(
        question,
        context,
        max_length=512, truncation=True
    )

    input_ids, attention_mask = (
        encoding["input_ids"],
        encoding["attention_mask"],
    )

    start_scores, end_scores = model(
        torch.tensor([input_ids]),
        attention_mask=torch.tensor([attention_mask]),
        return_dict=False,
    )

    answer_ids = input_ids[
        torch.argmax(start_scores) : torch.argmax(end_scores) + 1
    ]
    answer_tokens = token.convert_ids_to_tokens(
        answer_ids, skip_special_tokens=True
    )
    answer_tokens_to_string = token.convert_tokens_to_string(answer_tokens)

    # Display results
    print("\nDistilBERT question answering example.")
    print("======================================")
    print("Reading from: ", subject, source)
    print("\nContext: ", context)
    print("--")
    print("Question: ", question)
    print("Answer: ", answer_tokens_to_string)
    print("Reference Answers: ", answer)

    from torch.profiler import profile, ProfilerActivity
    model.eval()
    with torch.inference_mode():
        with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
            model(
                torch.tensor([input_ids for _ in range(32)]),
                attention_mask=torch.tensor([attention_mask for _ in range(32)]),
                return_dict=False,
            )
        print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=15, top_level_events_only=False))

