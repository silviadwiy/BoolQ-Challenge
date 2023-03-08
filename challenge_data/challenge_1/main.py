import pandas as pd
# from sklearn.metrics import accuracy_score

def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    print("Submission related metadata:")

    # Load the CSV files into pandas dataframes
    df_true = pd.read_csv(test_annotation_file)
    df_pred = pd.read_csv(user_submission_file)

    # Remove missing rows and duplicates
    df_true = df_true.dropna().drop_duplicates()
    df_pred = df_pred.dropna().drop_duplicates()

    # Merge the dataframes on the title column
    df = pd.merge(df_true, df_pred, on='title')

    # Extract the boolean answers from each dataframe
    correct_answers = df_true["true_answer"].values.tolist()
    student_answers = df_pred["answer"].values.tolist()

    # Compare student's answers to correct answers and calculate accuracy
    num_correct = 0
    for i in range(len(correct_answers)):
        if student_answers[i] == correct_answers[i]:
            num_correct += 1

    acc = num_correct / len(correct_answers)
    
    print(kwargs["submission_metadata"])
    output = {}
    if phase_codename == "train":
        print("Evaluating for Train Phase")
        output["result"] = [
            {
                "train_split": {
                    "Score": acc,
                }
            }
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]["train_split"]
        print("Completed evaluation for Train Phase")
    elif phase_codename == "dev":
        print("Evaluating for Dev Phase")
        output["result"] = [
            {
                "dev_split": {
                    "Score": acc,
                }
            }
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]
        print("Completed evaluation for Dev Phase")
    return output
